import argparse
import yaml
import requests
import time
import logging
from urllib.parse import urlparse

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_domain(url):
    # Extract domain name, ignore port if present
    return urlparse(url).hostname

def check_availability(endpoint):
    method = endpoint.get("method", "GET")
    headers = endpoint.get("headers", {})
    body = endpoint.get("body")
    url = endpoint["url"]

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        return 200 <= response.status_code <= 299 and elapsed <= 500
    except requests.RequestException:
        return False

def main():
    parser = argparse.ArgumentParser(description="Monitor endpoint availability using YAML config.")
    parser.add_argument("config", help="Path to your YAML config file")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        endpoints = yaml.safe_load(f)

    availability_stats = {}

    while True:
        start_time = time.time()

        for endpoint in endpoints:
            domain = get_domain(endpoint["url"])
            if domain not in availability_stats:
                availability_stats[domain] = {"total": 0, "success": 0}

            is_up = check_availability(endpoint)
            availability_stats[domain]["total"] += 1
            if is_up:
                availability_stats[domain]["success"] += 1

        for domain, stats in availability_stats.items():
            # Only keep the whole number, per project instructions
            availability = int((stats["success"] / stats["total"]) * 100)  # No decimal
            logging.info(f"{domain}: {availability}% availability")

        # Sleep the remaining time to keep a 15s interval per cycle
        time.sleep(max(0, 15 - (time.time() - start_time)))

if __name__ == "__main__":
    main()
