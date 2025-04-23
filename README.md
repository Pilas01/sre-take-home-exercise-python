# Fetch Rewards - SRE Take-Home Exercise (Python)

This script checks the uptime of a set of HTTP endpoints defined in a YAML config file. It checks the availability of endpoints every 15 seconds and logs the results by domain.

---

## 📦 Installation & Running Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Pilas01/sre-take-home-exercise.git
    cd sre-take-home-exercise-python

    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # Use `venv/bin/activate` on Mac/Linux
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `config.yaml` file** with your endpoints:

    ```yaml
    - name: Google
      url: https://www.google.com
    - name: Example
      url: https://example.com
    ```

5. **Run the script:**

    ```bash
    python healthcheck.py config.yaml
    ```

---

## 🔧 Changes Made to the Original Code

- **Issue 1**: The script didn’t read from a YAML file.
    - **Fix**: I added support for reading a `config.yaml` file using `argparse` and `PyYAML`.
  
- **Issue 2**: No way to customize the HTTP request (e.g., method, headers).
    - **Fix**: Now, the script supports optional `method`, `headers`, and `body` fields in the YAML file.

- **Issue 3**: No validation for status code and response time.
    - **Fix**: The script now checks if the status code is between `200-299` and the response time is under `500ms`.

- **Issue 4**: The script didn’t group results by domain.
    - **Fix**: I used `urlparse()` to extract domains from the URLs and grouped results accordingly.

- **Issue 5**: Availability percentage included decimals.
    - **Fix**: Per Fetch Rewards’ requirement, I made the script drop the decimal part by casting the percentage to `int()`.

---

## 📈 Example Output

When running the script, it will log availability percentages every 15 seconds like this:

2025-04-22 17:50:19,378 - www.google.com: 100% availability
2025-04-22 17:50:19,379 - example.com: 100% availability
