#!/usr/bin/env bash
set -euo pipefail

# Containers are intentionally bound only to localhost and an internal Docker
# network. This script sends one non-mutating SQLi-shaped request to a missing
# path; it does not run a scanner or attempt to exploit the application.

docker start preempt-juice >/dev/null
sleep 10
docker start preempt-waf >/dev/null
sleep 12

waf_ip="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' preempt-waf)"
proxy_url="http://${waf_ip}:8080"

cleanup() {
  docker stop preempt-waf preempt-juice >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "--- versions"
docker image inspect bkimminich/juice-shop@sha256:adaf6a6ca50f772dff7d2fe56972c659e81a61e0dbbe607c2b39fefd436e6153 \
  --format 'juice_image={{index .RepoDigests 0}} created={{.Created}} labels={{json .Config.Labels}}'
docker exec preempt-waf nginx -v 2>&1
docker exec preempt-waf sh -lc \
  "grep -m1 'SecComponentSignature.*OWASP_CRS' /opt/owasp-crs/crs-setup.conf || true"

echo "--- states"
docker ps --filter name=preempt \
  --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo "isolated_proxy_url=${proxy_url}"

echo "--- benign proxy"
curl -sS -o /dev/null \
  -w 'status=%{http_code} bytes=%{size_download} total=%{time_total}s\n' \
  "${proxy_url}/"

echo "--- direct backend"
docker exec preempt-waf curl -sS -o /dev/null \
  -w 'status=%{http_code} bytes=%{size_download} total=%{time_total}s\n' \
  http://preempt-juice:3000/

echo "--- harmless SQLi-shaped request"
curl -sS -o /dev/null \
  -w 'status=%{http_code} bytes=%{size_download} total=%{time_total}s\n' \
  "${proxy_url}/does-not-exist?q=1%27%20OR%20%271%27%3D%271"

echo "--- latency 30 benign proxy"
for _ in $(seq 1 30); do
  curl -sS -o /dev/null -w '%{time_total}\n' "${proxy_url}/"
done | sort -n | awk \
  '{a[NR]=$1;s+=$1} END{p=int((NR-1)*.95)+1; printf "n=%d mean_ms=%.3f p95_ms=%.3f\n",NR,1000*s/NR,1000*a[p]}'

echo "--- latency 30 direct"
for _ in $(seq 1 30); do
  docker exec preempt-waf curl -sS -o /dev/null \
    -w '%{time_total}\n' http://preempt-juice:3000/
done | sort -n | awk \
  '{a[NR]=$1;s+=$1} END{p=int((NR-1)*.95)+1; printf "n=%d mean_ms=%.3f p95_ms=%.3f\n",NR,1000*s/NR,1000*a[p]}'

echo "--- resources"
docker stats --no-stream \
  --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}' \
  preempt-juice preempt-waf

echo "--- recent WAF evidence"
docker logs --tail 200 preempt-waf 2>&1 \
  | grep -E 'does-not-exist|Access denied| 403 ' \
  | grep -v '^{' \
  | tail -40 || true

