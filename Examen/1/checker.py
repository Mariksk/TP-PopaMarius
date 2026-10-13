import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    if path.startswith("/"):
        return "https://" + host + path
    return "https://" + host + "/" + path


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.RequestException as error:
        print("Eroare:", str(error))


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as error:
        return {"status": None, "error": str(error)}


def scan_sites():
    results = []

    for site in SITES:
        results.append((site, check_site(site)))

    working_sites = []
    for site, result in results:
        if result.get("status") == 200:
            working_sites.append((site, result))

    working_sites.sort(key=lambda item: item[1].get("length", 0), reverse=True)

    for site, result in working_sites:
        print(site, "->", result["status"], result["length"], "octeti")

    print("Reusite:", len(working_sites), "| Esuate:", len(results) - len(working_sites))


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        present = []
        missing = []
        response_headers = {name.lower(): value for name, value in response.headers.items()}

        for header in SECURITY_HEADERS:
            if header.lower() in response_headers:
                present.append(header)
            else:
                missing.append(header)

        score = int(len(present) * 100 / len(SECURITY_HEADERS))
        return {"present": present, "missing": missing, "score": score}
    except requests.RequestException as error:
        return {"status": None, "error": str(error)}


def retry_check(url, attempts=3):
    last_error = None

    for number in range(max(0, attempts)):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                return {"status": response.status_code, "attempts": number + 1}
            last_status = response.status_code
        except requests.RequestException as error:
            last_error = str(error)
            continue

    if last_error is not None and "last_status" not in locals():
        return {"status": None, "error": last_error, "attempts": max(0, attempts)}

    if "last_status" in locals():
        return {"status": last_status, "attempts": max(0, attempts)}

    return {"status": None, "attempts": max(0, attempts)}
