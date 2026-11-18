import requests
from bs4 import BeautifulSoup

session_cookie = "iqd-7K6AjBizE4TiV0IZ6nmug9L_SnAgLgAK0W8pevQ.av4lRw.rb9bDoe9zzesXQr_EpEWZT4Xyn9tBZNQMNDuBQtBhRNAYpdDu1IxxLAJjbyrlgExPwTDZkFv9VzgEnaXmtI6rA"
user_id_cookie = "2f73d8c53dc19fe8911d134b0e028064450f15a15e6aba7fe05c90b344322befdb9217fc092a3b4abce7067706604aa916fc4185e0b6cd5a4de9476d1385d581"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
cookies = {
    "session": session_cookie,
    "user_id__insecure": user_id_cookie
}

url = "https://pypi.org/manage/project/arsalan-unique-pkg-7788/"

with requests.Session() as s:
    s.headers.update(headers)
    s.cookies.update(cookies)
    
    # 1. Get management page
    resp = s.get(url)
    print("GET Status:", resp.status_code)
    
    # 2. Extract CSRF token
    soup = BeautifulSoup(resp.text, 'html.parser')
    token_input = soup.find('input', {'name': 'csrf_token'})
    
    if token_input:
        csrf_token = token_input.get('value')
        print(f"Extracted CSRF Token: {csrf_token}")
        
        # 3. Post archive request
        archive_url = "https://pypi.org/manage/project/arsalan-unique-pkg-7788/archive/"
        post_resp = s.post(archive_url, data={"csrf_token": csrf_token}, allow_redirects=False)
        print(f"archive {post_resp.status_code}")
    else:
        print("CSRF token not found. Cookies might be expired or invalid.")
