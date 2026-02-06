#!/usr/bin/env python3

import argparse
import csv
import re
import sys

# Add CLI arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Parse nginx access log and convert to CSV")
    parser.add_argument("--input", required=True, help="Path to nginx access log")
    parser.add_argument("--output", required=True, help="Path to output CSV file")
    parser.add_argument("--filter-status", type=int, help="Filter by HTTP status code")
    parser.add_argument("--sort-by", choices=["status", "bytes", "ip"], help="Sort output")
    return parser.parse_args()

# Define nginx log regex
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<proto>\S+)" '
    r'(?P<status>\d+) (?P<bytes>\d+) '
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)

# Parse the log file
def parse_log(file_path):
    rows = []
    skipped = 0

    with open(file_path) as f:
        for line in f:
            match = LOG_PATTERN.match(line)
            if not match:
                skipped += 1
                continue
            rows.append(match.groupdict())

    return rows, skipped

# Add filtering and sorting
def process_rows(rows, status_filter=None, sort_by=None):
    if status_filter:
        rows = [r for r in rows if int(r["status"]) == status_filter]

    if sort_by:
        rows.sort(key=lambda r: int(r[sort_by]) if sort_by != "ip" else r["ip"])

    return rows

# Write CSV output
def write_csv(rows, output_path):
    fieldnames = ["ip", "time", "method", "path", "proto", "status", "bytes", "referer", "ua"]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    args = parse_args()

    rows, skipped = parse_log(args.input)
    rows = process_rows(rows, args.filter_status, args.sort_by)
    write_csv(rows, args.output)

    print(f"Parsed {len(rows)} lines")
    if skipped:
        print(f"Skipped {skipped} invalid lines")

if __name__ == "__main__":
    main()