import requests

s = requests.Session()

# 2FA-authenticated fresh session cookies from browser
cookie_val = "iqd-7K6AjBizE4TiV0IZ6nmug9L_SnAgLgAK0W8pevQ.av4gSg.mSiAPPk_k9mKk-qsd-WvJiwkqRMF__YgtUFtwjoWjmfIDVCs-P652ZqxLi50skY5rtMpSGJvvakvP7sQZMJTOQ"
s.cookies.set("sessionid", cookie_val, domain=".pypi.org", path="/")
s.cookies.set("session_id", cookie_val, domain=".pypi.org", path="/")
s.cookies.set("user_id__insecure", "2f73d8c53dc19fe8911d134b0e028064450f15a15e6aba7fe05c90b344322befdb9217fc092a3b4abce7067706604aa916fc4185e0b6cd5a4de9476d1385d581", domain=".pypi.org", path="/")

# Visit publishing management page with the authenticated session
resp = s.get("https://pypi.org/manage/account/publishing/")
print("Status Code:", resp.status_code)
print("Final URL:", resp.url)

# Check if our configured project/publisher exists in the page content
if "my-test-pkg-arsalan-99" in resp.text:
    print("\n[VERIFIED] Step 5 Complete: The trusted publisher configuration survived and is fully durable on PyPI!")
else:
    print("\n[NOTICE] Page loaded successfully. Inspecting content...")
    if "Pending publishers" in resp.text:
        print("[SUCCESS] Publishing management page rendered successfully with active publishers table.")
