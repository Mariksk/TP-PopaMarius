from checker import build_url, is_https, show_response, check_site
from checker import scan_sites, check_headers, retry_check
print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url:", build_url("example.com", "/login"))
print("Partea 1, is_https:", is_https("https://example.com"))
print("Partea 1, is_https:", is_https("http://example.com"))
print("Partea 2, site care merge:")
show_response("https://example.com")
print("Partea 2, site care esueaza:")
show_response("http://this-site-does-not-exist.invalid")
print("Partea 3, site care merge:", check_site("https://example.com"))
print("Partea 3, site care esueaza:", check_site("http://this-site-does-not-exist.invalid"))
print("Partea 4:")
scan_sites()
print("Partea 5, cu antete:")
print(check_headers(
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"
))
print("Partea 5, fara antete:")
print(check_headers("https://example.com"))
print("Partea 6, raspuns bun:")
print(retry_check("https://httpbin.org/status/200"))
print("Partea 6, raspuns 500:")
print(retry_check("https://httpbin.org/status/500"))
