# Local environment profile

Captured 2026-11-28 11:59 IST.

- Host: Windows 11 Home Single Language 10.0.26300; WSL 3.0.5.0, Linux kernel 6.18.58.1-1.
- CPU: Intel Core i5-12450H, 8 cores / 12 logical processors.
- RAM: 15.65 GiB usable.
- GPU: NVIDIA GeForce RTX 3050 A Laptop GPU, 4,292,870,144 reported bytes; Intel UHD integrated graphics. The feasibility baselines did not use the GPU.
- Storage: C: 475.65 GiB total, 42.64 GiB free after selected data and container images. The investigation started with approximately 50.58 GiB free. Do not download the full AIT collection on this disk.
- Python 3.13.5; NumPy 2.2.4; pandas 2.3.3; scikit-learn 1.7.2; psutil 7.1.1; Git 2.47.1.windows.1.
- Docker Engine in WSL Ubuntu: client/server 29.1.3. Docker Desktop and the Docker Compose plugin were not installed; the saved Compose file was therefore translated to equivalent `docker create` commands for the actual smoke test.
- Juice Shop image: `bkimminich/juice-shop@sha256:adaf6a6ca50f772dff7d2fe56972c659e81a61e0dbbe607c2b39fefd436e6153`, 343,560,349 bytes, built 2026-11-19.
- ModSecurity CRS image: `owasp/modsecurity-crs@sha256:cd1aa84167b5ba42539001c6fedf174484499ad1c37161df9eed1453e64d65e2`, 240,287,107 bytes, built 2026-11-27. Runtime reported nginx 1.30.8, ModSecurity 3.0.17, connector 1.0.4, CRS 4.30.0 (856 rules).

Only the primary laptop was directly inspected. The six stated Ryzen/8-GB laptops were not remotely available, so their free storage and software state remain unverified.
