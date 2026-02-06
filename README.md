# Nginx Log Parser

## Project Description

This project provides a **Python script** to parse **nginx access logs** and convert them into a **CSV file**.  
All log fields, including extended Grafana/Prometheus metrics, are preserved with **descriptive column names**.

The script also supports **filtering by HTTP status code** and **sorting** by `status`, `bytes`, or `ip`.  
A **Dockerfile** is included so the script can run in a container, making it reproducible and easy to use.

---

## Features

- Parse standard nginx logs plus extended Grafana/Prometheus fields;
- Convert logs to CSV format;
- Filter logs by HTTP status (`--filter-status`);
- Sort logs (`--sort-by status|bytes|ip`);
- Preserve all extra fields with descriptive column names; 
- Docker support for containerized execution.

---

## Log Format

The script expects nginx logs extended with Grafana/Prometheus metrics, e.g.:

```bash
162.55.33.98 - - [26/Apr/2021:21:20:17 +0000] "GET /api/annotations?from=1619471716848&to=1619472016848&dashboardId=25 HTTP/2.0" 200 2 "https://grafana.itoutposts.com/d/..." "Mozilla/5.0 ..." 69 0.003 [monitoring-monitoring-prometheus-grafana-80] [] 192.168.226.102:3000 2 0.004 200 f9f97c8e584ae95d1ba146c23986fc43
```

---

## CSV Output

The resulting CSV contains the following columns:

```
ip,time,method,path,proto,status,bytes,referer,ua,
req_bytes,req_duration,upstream_name,labels,upstream_ip,
resp_bytes,resp_duration,upstream_status,request_id
```

Example row:

```bash
162.55.33.98,26/Apr/2021:21:20:17 +0000,GET,/api/annotations?from=...,HTTP/2.0,200,2,https://grafana.itoutposts.com/d/...,"Mozilla/5.0 ...",69,0.003,[monitoring-monitoring-prometheus-grafana-80],[],192.168.226.102:3000,2,0.004,200,f9f97c8e584ae95d1ba146c23986fc43
```

---

## Requirements

- Python 3.10+  
- Or Docker (optional)

---

## Usage

### Local (Python)

1. Make the script executable (optional, for Unix-like systems):

```bash
chmod +x nginx_to_csv.py
```

2. Run the script:

```bash
./nginx_to_csv.py --input sample/nginx.log --output output/nginx.csv
```

Or, if the script is not executable:

```bash
python nginx_to_csv.py --input sample/nginx.log --output output/nginx.csv
```

3. Optional flags:

- Filter by HTTP status:

```bash
./nginx_to_csv.py --input sample/nginx.log --output output/nginx.csv --filter-status 200
```

```bash
python nginx_to_csv.py --input sample/nginx.log --output output/nginx.csv --filter-status 200
```

- Sort by a column:

```bash
./nginx_to_csv.py --input sample/nginx.log --output output/nginx.csv --sort-by bytes
```

```bash
python nginx_to_csv.py --input sample/nginx.log --output output/nginx.csv --sort-by bytes
```

### Docker
1. Build the Docker image:

```bash
docker build -t nginx-log-parser .
```

2. Run the container:

```bash
docker run --rm -v ${PWD}:/data nginx-log-parser --input /data/sample/nginx.log --output /data/output/nginx.csv
```

3. Run the container with filter and sort:

```bash
docker run --rm -v ${PWD}:/data nginx-log-parser --input /data/sample/nginx.log --output /data/output/nginx.csv --filter-status 200 --sort-by status
```

On Git Bash or systems where `${PWD}` is not expanded, use `$(pwd)` or an absolute path.

---