import requests


BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
TIMEOUT = 3


def search(params):
    raspuns = requests.get(BASE + "/get", params=params, timeout=TIMEOUT)
    raspuns.raise_for_status()
    return raspuns.json()["args"]


def search_url(params):
    cerere = requests.Request("GET", BASE + "/get", params=params)
    return cerere.prepare().url


def fetch_with_agent(agent):
    raspuns = requests.get(BASE + "/headers", headers={"User-Agent": agent}, timeout=TIMEOUT)
    raspuns.raise_for_status()
    return raspuns.json()["headers"]["User-Agent"]


def default_agent():
    raspuns = requests.get(BASE + "/headers", timeout=TIMEOUT)
    raspuns.raise_for_status()
    return raspuns.json()["headers"]["User-Agent"]


def post_json(data):
    raspuns = requests.post(BASE + "/post", json=data, timeout=TIMEOUT)
    raspuns.raise_for_status()
    return raspuns.json()["json"]


def post_form(data):
    raspuns = requests.post(BASE + "/post", data=data, timeout=TIMEOUT)
    raspuns.raise_for_status()
    return raspuns.json()["form"]


def describe_status(code):
    raspuns = requests.get(f"{BASE}/status/{code}", timeout=TIMEOUT)
    status = raspuns.status_code
    if 200 <= status < 300:
        return "succes"
    if 400 <= status < 500:
        return "eroare client"
    if 500 <= status < 600:
        return "eroare server"
    return "alt status"


def is_ok(code):
    try:
        raspuns = requests.get(f"{BASE}/status/{code}", timeout=TIMEOUT)
        raspuns.raise_for_status()
        return 200 <= raspuns.status_code < 300
    except requests.RequestException:
        return False


def count_redirects(n):
    raspuns = requests.get(f"{BASE}/redirect/{n}", timeout=TIMEOUT)
    return len(raspuns.history)


def final_url(n):
    raspuns = requests.get(f"{BASE}/redirect/{n}", timeout=TIMEOUT)
    return raspuns.url


def first_hop(n):
    raspuns = requests.get(f"{BASE}/redirect/{n}", allow_redirects=False, timeout=TIMEOUT)
    return raspuns.headers.get("Location")


def cookie_demo(name, value):
    with requests.Session() as sesiune:
        setare = sesiune.get(BASE + "/cookies/set", params={name: value}, timeout=TIMEOUT)
        setare.raise_for_status()
        raspuns = sesiune.get(BASE + "/cookies", timeout=TIMEOUT)
        raspuns.raise_for_status()
        return raspuns.json()["cookies"]


def no_session_demo(name, value):
    setare = requests.get(BASE + "/cookies/set", params={name: value}, timeout=TIMEOUT)
    setare.raise_for_status()
    raspuns = requests.get(BASE + "/cookies", timeout=TIMEOUT)
    raspuns.raise_for_status()
    return raspuns.json()["cookies"]


def report(path):
    try:
        raspuns = requests.get(BASE + path, timeout=TIMEOUT)
    except requests.Timeout:
        return {"status": None, "error": "Timp de asteptare depasit"}
    except requests.RequestException:
        return {"status": None, "error": "Cererea nu a reusit"}

    return {
        "status": raspuns.status_code,
        "final_url": raspuns.url,
        "redirects": len(raspuns.history),
        "seconds": raspuns.elapsed.total_seconds(),
        "content_type": raspuns.headers.get("Content-Type", ""),
    }


def check_login(user, password):
    try:
        raspuns = requests.get(
            BASE + "/basic-auth/admin/secret", auth=(user, password), timeout=TIMEOUT
        )
        return raspuns.status_code == 200
    except requests.RequestException:
        return False


if __name__ == "__main__":
    from main import main

    main()
