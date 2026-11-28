#!/usr/bin/env python3
"""Leakage-conscious campaign-held-out baselines for AIT-LDS v2.1.

Prediction unit
---------------
At the last completed request in each active five-second bin, predict whether
the separately timestamped AIT-ADS ``webshell`` phase will begin within H.
Every example is strictly earlier than that timestamp. The current request's
response is therefore already past; no future or current-request response is
used. Inputs exclude IP addresses, user-agent strings, absolute timestamps,
campaign names, raw paths, and known testing-tool tokens.

This is an application/campaign risk forecast, not a user-identity model. The
AIT campaigns all instantiate related scripted attacks, so held-out-campaign
results test transfer across testbeds, not independence from attack tooling.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import numpy as np
import psutil
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    precision_score,
    recall_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


APACHE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^]]+)\] "(?P<method>\S+) (?P<target>.*?) '
    r'HTTP/(?P<http>[^\"]+)" (?P<status>\d{3}) (?P<bytes>\S+) "(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)
STRUCTURAL = re.compile(r"[^A-Za-z0-9/._?=&%-]")


@dataclass(slots=True)
class Request:
    timestamp: float
    method: str
    target: str
    status: int


def parse_request(line: str) -> Request | None:
    match = APACHE.match(line.rstrip("\n"))
    if not match:
        return None
    values = match.groupdict()
    return Request(
        datetime.strptime(values["time"], "%d/%b/%Y:%H:%M:%S %z").timestamp(),
        values["method"].upper(),
        values["target"],
        int(values["status"]),
    )


def load_phase_labels(path: Path) -> dict[str, dict[str, tuple[float, float]]]:
    result: dict[str, dict[str, tuple[float, float]]] = collections.defaultdict(dict)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            result[row["scenario"]][row["attack"]] = (
                float(row["start"]),
                float(row["end"]),
            )
    return result


def coarse_token(request: Request) -> str:
    target = request.target
    path, separator, query = target.partition("?")
    depth = min(4, sum(bool(part) for part in path.split("/")))
    length_bucket = min(4, len(target) // 40)
    status_class = request.status // 100
    extension = path.rsplit("/", 1)[-1].rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else "none"
    extension_class = extension if extension in {"css", "js", "jpg", "jpeg", "png", "gif", "svg", "ico"} else "other"
    return f"m{request.method}_s{status_class}_q{int(bool(separator))}_d{depth}_l{length_bucket}_e{extension_class}"


def feature_vector(history: list[Request]) -> list[float]:
    last = history[-1]
    times = np.fromiter((event.timestamp for event in history), dtype=float)
    gaps = np.diff(times)
    methods = collections.Counter(event.method for event in history)
    status_classes = collections.Counter(event.status // 100 for event in history)
    normalized_paths = [event.target.partition("?")[0].lower() for event in history]
    lengths = np.fromiter((len(event.target) for event in history), dtype=float)
    queries = sum("?" in event.target for event in history)
    structural = sum(len(STRUCTURAL.findall(event.target)) for event in history)
    transitions = sum(a != b for a, b in zip(normalized_paths, normalized_paths[1:]))
    now = last.timestamp
    rate_10 = sum(event.timestamp > now - 10 for event in history) / 10.0
    rate_60 = sum(event.timestamp > now - 60 for event in history) / 60.0
    n = len(history)
    return [
        float(last.method == "GET"),
        float(last.method == "POST"),
        float(last.method == "HEAD"),
        float(last.status // 100 == 2),
        float(last.status // 100 == 3),
        float(last.status // 100 == 4),
        float(len(last.target)),
        float("?" in last.target),
        float(sum(bool(part) for part in last.target.partition("?")[0].split("/"))),
        rate_10,
        rate_60,
        float(np.mean(gaps)) if len(gaps) else 0.0,
        float(np.std(gaps)) if len(gaps) else 0.0,
        methods["GET"] / n,
        methods["POST"] / n,
        methods["HEAD"] / n,
        status_classes[2] / n,
        status_classes[3] / n,
        status_classes[4] / n,
        status_classes[5] / n,
        len(set(normalized_paths)) / n,
        transitions / max(1, n - 1),
        float(np.mean(lengths)),
        float(np.std(lengths)),
        queries / n,
        structural / n,
    ]


def individual_vector(full: list[float]) -> list[float]:
    return full[:9]


def build_snapshots(
    dataset_root: Path,
    labels: dict[str, dict[str, tuple[float, float]]],
    prefix_length: int,
    bin_seconds: int,
    request_stride: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for campaign_dir in sorted(dataset_root.glob("ait-lds-v2.1-*-selected")):
        campaign = campaign_dir.name.removeprefix("ait-lds-v2.1-").removesuffix("-selected")
        exploit_time = labels[campaign]["webshell"][0]
        requests: list[Request] = []
        for path in campaign_dir.glob("gather/intranet_server/logs/apache2/*access.log*"):
            with path.open(encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    request = parse_request(line)
                    if request is not None and request.timestamp < exploit_time:
                        requests.append(request)
        requests.sort(key=lambda item: item.timestamp)
        if not requests:
            continue
        # One decision at the final completed request of each active time bin.
        time_snapshot_indices: list[int] = []
        previous_bin = None
        for index, request in enumerate(requests):
            current_bin = int(request.timestamp // bin_seconds)
            if previous_bin is not None and current_bin != previous_bin:
                time_snapshot_indices.append(index - 1)
            previous_bin = current_bin
        time_snapshot_indices.append(len(requests) - 1)
        request_snapshot_indices = list(range(request_stride - 1, len(requests), request_stride))
        request_snapshot_indices.append(len(requests) - 1)
        time_snapshot_set = set(time_snapshot_indices)
        request_snapshot_set = set(request_snapshot_indices)
        snapshot_indices = sorted(time_snapshot_set | request_snapshot_set)
        event_index = len(requests)
        for index in snapshot_indices:
            start = max(0, index + 1 - prefix_length)
            history = requests[start : index + 1]
            full = feature_vector(history)
            rows.append(
                {
                    "campaign": campaign,
                    "time": requests[index].timestamp,
                    "seconds_to_event": exploit_time - requests[index].timestamp,
                    "requests_to_event": event_index - index - 1,
                    "full": full,
                    "individual": individual_vector(full),
                    "heuristic": full[10] * (1.0 + full[18]),  # 60-s rate x (1 + 4xx fraction)
                    "sequence": " ".join(coarse_token(item) for item in history),
                    "time_snapshot": index in time_snapshot_set,
                    "request_snapshot": index in request_snapshot_set,
                }
            )
    return rows


def labels_for(rows: list[dict[str, object]], horizon_kind: str, horizon: int) -> np.ndarray:
    key = "seconds_to_event" if horizon_kind == "seconds" else "requests_to_event"
    return np.asarray([0 < float(row[key]) <= horizon for row in rows], dtype=int)


def choose_threshold(y_true: np.ndarray, scores: np.ndarray) -> float:
    candidates = np.unique(np.quantile(scores, np.linspace(0, 1, 101)))
    best = (float("-inf"), 0.5)
    for threshold in candidates:
        predictions = scores >= threshold
        precision = precision_score(y_true, predictions, zero_division=0)
        recall = recall_score(y_true, predictions, zero_division=0)
        f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
        if (f1, -threshold) > (best[0], -best[1]):
            best = (f1, float(threshold))
    return best[1]


def expected_calibration_error(y_true: np.ndarray, scores: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    total = len(y_true)
    error = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (scores >= low) & (scores < high if high < 1 else scores <= high)
        if mask.any():
            error += mask.mean() * abs(scores[mask].mean() - y_true[mask].mean())
    return float(error if total else math.nan)


def score_model(
    model_name: str,
    train_rows: list[dict[str, object]],
    val_rows: list[dict[str, object]],
    test_rows: list[dict[str, object]],
    y_train: np.ndarray,
    y_val: np.ndarray,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    started = time.perf_counter()
    if model_name == "constant":
        probability = float(y_train.mean())
        train_seconds = time.perf_counter() - started
        return (
            np.full(len(val_rows), probability),
            np.full(len(test_rows), probability),
            train_seconds,
            0.0,
        )
    if model_name == "heuristic":
        val_raw = np.asarray([row["heuristic"] for row in val_rows], dtype=float)
        test_raw = np.asarray([row["heuristic"] for row in test_rows], dtype=float)
        train_raw = np.asarray([row["heuristic"] for row in train_rows], dtype=float)
        scale = max(float(np.quantile(train_raw, 0.99)), 1e-9)
        train_seconds = time.perf_counter() - started
        return np.clip(val_raw / scale, 0, 1), np.clip(test_raw / scale, 0, 1), train_seconds, 0.0
    if model_name in {"logistic_individual", "logistic_behavioral"}:
        key = "individual" if model_name.endswith("individual") else "full"
        x_train = np.asarray([row[key] for row in train_rows], dtype=float)
        x_val = np.asarray([row[key] for row in val_rows], dtype=float)
        x_test = np.asarray([row[key] for row in test_rows], dtype=float)
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=500, class_weight=None, random_state=seed),
        )
        model.fit(x_train, y_train)
        train_seconds = time.perf_counter() - started
        before = time.perf_counter()
        val_scores = model.predict_proba(x_val)[:, 1]
        test_scores = model.predict_proba(x_test)[:, 1]
        inference_us = (time.perf_counter() - before) * 1e6 / max(1, len(test_rows) + len(val_rows))
        return val_scores, test_scores, train_seconds, inference_us
    if model_name == "gradient_boosted":
        x_train = np.asarray([row["full"] for row in train_rows], dtype=float)
        x_val = np.asarray([row["full"] for row in val_rows], dtype=float)
        x_test = np.asarray([row["full"] for row in test_rows], dtype=float)
        model = HistGradientBoostingClassifier(
            max_iter=100,
            max_leaf_nodes=15,
            learning_rate=0.08,
            l2_regularization=1.0,
            random_state=seed,
        )
        model.fit(x_train, y_train)
        train_seconds = time.perf_counter() - started
        before = time.perf_counter()
        val_scores = model.predict_proba(x_val)[:, 1]
        test_scores = model.predict_proba(x_test)[:, 1]
        inference_us = (time.perf_counter() - before) * 1e6 / max(1, len(test_rows) + len(val_rows))
        return val_scores, test_scores, train_seconds, inference_us
    if model_name == "ngram_logistic":
        vectorizer = TfidfVectorizer(
            lowercase=False,
            token_pattern=r"[^ ]+",
            ngram_range=(1, 3),
            min_df=2,
            max_features=20_000,
            sublinear_tf=True,
        )
        x_train = vectorizer.fit_transform(str(row["sequence"]) for row in train_rows)
        x_val = vectorizer.transform(str(row["sequence"]) for row in val_rows)
        x_test = vectorizer.transform(str(row["sequence"]) for row in test_rows)
        model = LogisticRegression(max_iter=500, random_state=seed)
        model.fit(x_train, y_train)
        train_seconds = time.perf_counter() - started
        before = time.perf_counter()
        val_scores = model.predict_proba(x_val)[:, 1]
        test_scores = model.predict_proba(x_test)[:, 1]
        inference_us = (time.perf_counter() - before) * 1e6 / max(1, len(test_rows) + len(val_rows))
        return val_scores, test_scores, train_seconds, inference_us
    raise ValueError(model_name)


def evaluate_configuration(
    rows: list[dict[str, object]],
    horizon_kind: str,
    horizon: int,
    models: Iterable[str],
    seed: int,
    bootstrap_repetitions: int,
) -> list[dict[str, object]]:
    campaigns = sorted({str(row["campaign"]) for row in rows})
    y_all = labels_for(rows, horizon_kind, horizon)
    indices_by_campaign = {
        campaign: np.asarray([i for i, row in enumerate(rows) if row["campaign"] == campaign])
        for campaign in campaigns
    }
    output: list[dict[str, object]] = []
    for model_name in models:
        combined_y: list[int] = []
        combined_scores: list[float] = []
        combined_predictions: list[int] = []
        combined_campaigns: list[str] = []
        fold_details = []
        for test_position, test_campaign in enumerate(campaigns):
            val_campaign = campaigns[(test_position + 1) % len(campaigns)]
            train_campaigns = [c for c in campaigns if c not in {test_campaign, val_campaign}]
            train_indices = np.concatenate([indices_by_campaign[c] for c in train_campaigns])
            val_indices = indices_by_campaign[val_campaign]
            test_indices = indices_by_campaign[test_campaign]
            train_rows = [rows[i] for i in train_indices]
            val_rows = [rows[i] for i in val_indices]
            test_rows = [rows[i] for i in test_indices]
            y_train, y_val, y_test = y_all[train_indices], y_all[val_indices], y_all[test_indices]
            val_scores, test_scores, train_seconds, inference_us = score_model(
                model_name, train_rows, val_rows, test_rows, y_train, y_val, seed
            )
            threshold = choose_threshold(y_val, val_scores)
            predictions = (test_scores >= threshold).astype(int)
            positive_mask = y_test == 1
            lead_seconds = None
            lead_requests = None
            if (predictions[positive_mask] == 1).any():
                matched = [test_rows[i] for i in np.flatnonzero(positive_mask & (predictions == 1))]
                lead_seconds = max(float(row["seconds_to_event"]) for row in matched)
                lead_requests = max(int(row["requests_to_event"]) for row in matched)
            fold_details.append(
                {
                    "test_campaign": test_campaign,
                    "validation_campaign": val_campaign,
                    "test_rows": len(test_rows),
                    "test_positives": int(y_test.sum()),
                    "threshold_from_validation": threshold,
                    "event_detected_pre_exploitation": bool((predictions[positive_mask] == 1).any()),
                    "lead_seconds_within_horizon": lead_seconds,
                    "lead_requests_within_horizon": lead_requests,
                    "training_seconds": train_seconds,
                    "inference_microseconds_per_snapshot": inference_us,
                }
            )
            combined_y.extend(y_test.tolist())
            combined_scores.extend(test_scores.tolist())
            combined_predictions.extend(predictions.tolist())
            combined_campaigns.extend([test_campaign] * len(test_rows))
        y = np.asarray(combined_y)
        scores = np.asarray(combined_scores)
        predictions = np.asarray(combined_predictions)
        negative = y == 0
        campaign_recall = np.mean([detail["event_detected_pre_exploitation"] for detail in fold_details])
        detected_lead_seconds = [d["lead_seconds_within_horizon"] for d in fold_details if d["lead_seconds_within_horizon"] is not None]
        detected_lead_requests = [d["lead_requests_within_horizon"] for d in fold_details if d["lead_requests_within_horizon"] is not None]
        # Cluster bootstrap: resample whole held-out campaigns, never rows.
        rng = np.random.default_rng(seed)
        campaign_array = np.asarray(combined_campaigns)
        bootstrap = collections.defaultdict(list)
        for _ in range(bootstrap_repetitions):
            sampled = rng.choice(campaigns, size=len(campaigns), replace=True)
            sampled_indices = np.concatenate([np.flatnonzero(campaign_array == c) for c in sampled])
            by = y[sampled_indices]
            bs = scores[sampled_indices]
            bp = predictions[sampled_indices]
            bn = by == 0
            if by.sum() and (by == 0).any():
                bootstrap["pr_auc"].append(float(average_precision_score(by, bs)))
            bootstrap["precision"].append(float(precision_score(by, bp, zero_division=0)))
            bootstrap["recall"].append(float(recall_score(by, bp, zero_division=0)))
            bootstrap["false_positive_rate"].append(float(bp[bn].mean()))
            bootstrap["brier_score"].append(float(brier_score_loss(by, bs)))
            sampled_details = [fold_details[campaigns.index(c)] for c in sampled]
            bootstrap["pre_exploitation_campaign_recall"].append(
                float(np.mean([d["event_detected_pre_exploitation"] for d in sampled_details]))
            )
        bootstrap_ci = {
            metric: [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))]
            for metric, values in bootstrap.items()
            if values
        }
        output.append(
            {
                "model": model_name,
                "horizon_kind": horizon_kind,
                "horizon": horizon,
                "snapshots": len(y),
                "positives": int(y.sum()),
                "observed_prevalence": float(y.mean()),
                "pr_auc": float(average_precision_score(y, scores)),
                "precision": float(precision_score(y, predictions, zero_division=0)),
                "recall": float(recall_score(y, predictions, zero_division=0)),
                "false_positive_rate": float(predictions[negative].mean()),
                "brier_score": float(brier_score_loss(y, scores)),
                "expected_calibration_error_10_bins": expected_calibration_error(y, scores),
                "pre_exploitation_campaign_recall": float(campaign_recall),
                "median_lead_seconds_detected": float(np.median(detected_lead_seconds)) if detected_lead_seconds else None,
                "median_lead_requests_detected": float(np.median(detected_lead_requests)) if detected_lead_requests else None,
                "mean_training_seconds_per_fold": float(np.mean([d["training_seconds"] for d in fold_details])),
                "mean_inference_microseconds_per_snapshot": float(np.mean([d["inference_microseconds_per_snapshot"] for d in fold_details])),
                "campaign_bootstrap_95_ci": bootstrap_ci,
                "folds": fold_details,
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--prefix", type=int, default=20)
    parser.add_argument("--bin-seconds", type=int, default=5)
    parser.add_argument("--request-stride", type=int, default=10)
    parser.add_argument("--bootstrap-repetitions", type=int, default=500)
    parser.add_argument("--only-time", action="store_true")
    parser.add_argument("--only-request", action="store_true")
    parser.add_argument("--models", help="Comma-separated model names; default is all baselines")
    parser.add_argument("--seed", type=int, default=20261128)
    parser.add_argument("--quick", action="store_true", help="Run the minimum 60-second and 100-request configurations")
    args = parser.parse_args()
    process = psutil.Process(os.getpid())
    started = time.perf_counter()
    phases = load_phase_labels(args.datasets / "ait-alert-labels.csv")
    rows = build_snapshots(args.datasets, phases, args.prefix, args.bin_seconds, args.request_stride)
    after_build = time.perf_counter()
    models = [
        "constant",
        "heuristic",
        "logistic_individual",
        "logistic_behavioral",
        "gradient_boosted",
        "ngram_logistic",
    ]
    if args.models:
        requested = [item.strip() for item in args.models.split(",") if item.strip()]
        unknown = sorted(set(requested) - set(models))
        if unknown:
            raise SystemExit(f"Unknown models: {', '.join(unknown)}")
        models = requested
    configurations = [("seconds", 60), ("requests", 100)] if args.quick else [
        ("seconds", 30),
        ("seconds", 60),
        ("seconds", 300),
        ("requests", 20),
        ("requests", 100),
        ("requests", 1000),
    ]
    if args.only_time and args.only_request:
        raise SystemExit("Choose at most one of --only-time and --only-request")
    if args.only_time:
        configurations = [item for item in configurations if item[0] == "seconds"]
    if args.only_request:
        configurations = [item for item in configurations if item[0] == "requests"]
    results = []
    for kind, horizon in configurations:
        print(f"evaluating {kind} horizon={horizon}", flush=True)
        selected_rows = [row for row in rows if row["time_snapshot" if kind == "seconds" else "request_snapshot"]]
        results.extend(
            evaluate_configuration(
                selected_rows,
                kind,
                horizon,
                models,
                args.seed,
                args.bootstrap_repetitions,
            )
        )
    finished = time.perf_counter()
    payload = {
        "prediction_target": "P(first AIT-ADS webshell-phase request within H | completed HTTP requests up to t)",
        "strictly_pre_exploitation": True,
        "response_timing": "Features use responses only from completed past requests; all snapshots precede the webshell timestamp.",
        "split": "Eight outer held-out campaigns; one distinct validation campaign per fold; remaining six train.",
        "limitations": [
            "The eight AIT campaigns share attack automation and are not independent real adversaries.",
            "Application-level snapshots do not identify a human or session; raw IP and user-agent values are excluded.",
            "The webshell phase start is an exploit-attempt proxy, not proof of successful exploitation.",
            "All campaigns eventually attack; early campaign time supplies negatives but no wholly benign campaign exists.",
            "Overlapping snapshots are correlated; row-level metrics are descriptive, while event recall is campaign-level.",
        ],
        "prefix_requests": args.prefix,
        "active_bin_seconds": args.bin_seconds,
        "request_stride": args.request_stride,
        "campaigns": sorted({str(row["campaign"]) for row in rows}),
        "snapshot_union": len(rows),
        "time_snapshots": sum(bool(row["time_snapshot"]) for row in rows),
        "request_snapshots": sum(bool(row["request_snapshot"]) for row in rows),
        "feature_build_seconds": after_build - started,
        "total_runtime_seconds": finished - started,
        "peak_rss_bytes": process.memory_info().peak_wset if hasattr(process.memory_info(), "peak_wset") else process.memory_info().rss,
        "software": {
            "python": os.sys.version,
            "numpy": np.__version__,
        },
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"snapshot_union": len(rows), "runtime_seconds": finished - started}, indent=2))


if __name__ == "__main__":
    main()

