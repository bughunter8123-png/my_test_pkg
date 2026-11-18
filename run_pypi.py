import requests
import re

s = requests.Session()

# Fresh cookies from browser
cookie_val = "iqd-7K6AjBizE4TiV0IZ6nmug9L_SnAgLgAK0W8pevQ.av4TiA.oZeFw-2E8qPv7IrQvFqamjm5cYR3LM8uFV6vE-9aVrFcnIoTVzrVN-6ZyuVxU7CRkp2j78aLmykfirJE8OendA"
s.cookies.set("sessionid", cookie_val, domain=".pypi.org", path="/")
s.cookies.set("session_id", cookie_val, domain=".pypi.org", path="/")
s.cookies.set("user_id__insecure", "2f73d8c53dc19fe8911d134b0e028064450f15a15e6aba7fe05c90b344322befdb9217fc092a3b4abce7067706604aa916fc4185e0b6cd5a4de9476d1385d581", domain=".pypi.org", path="/")

# 1. GET publishing page to get cookies and fresh CSRF token
resp = s.get("https://pypi.org/manage/account/publishing/")
print("GET Status:", resp.status_code)

# Extract CSRF token from HTML
match = re.search(r'name=["\x27]csrf_token["\x27][^>]*value=["\x27]([^"\x27]+)["\x27]', resp.text)
csrf_token = match.group(1) if match else None
print("Extracted CSRF:", csrf_token)

# 2. POST to configure Trusted Publisher
data = {
    "csrf_token": csrf_token,
    "issuer_url": "https://token.actions.githubusercontent.com",
    "project_name": "my-test-pkg",
    "owner": "TesterA",
    "repository": "my_test_pkg",
    "workflow_filename": "release.yml",
    "environment": ""
}

headers = {
    "Origin": "https://pypi.org",
    "Referer": "https://pypi.org/manage/account/publishing/"
}

post_resp = s.post("https://pypi.org/manage/account/publishing/", data=data, headers=headers, allow_redirects=False)
print("Response Status:", post_resp.status_code)
print("Redirect URL:", post_resp.headers.get("Location"))

# Save response and parse errors
with open("/tmp/post_err.html", "w", encoding="utf-8") as f:
    f.write(post_resp.text)

errors = re.findall(r'<div[^>]*class="[^"]*(?:error|alert|message)[^"]*"[^>]*>(.*?)</div>', post_resp.text, re.DOTALL)
for e in errors:
    clean = re.sub(r'<[^>]+>', '', e).strip()
    if clean:
        print("FOUND ERROR:", clean)
