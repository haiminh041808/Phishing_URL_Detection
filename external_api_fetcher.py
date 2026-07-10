import requests
import socket
import base64
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import cloudscraper

from ML_components.utils import extract_domain, remove_vietnamese_diacritics

def check_safe_browsing(url, api_key):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    body = {
        "client": {"clientId": "phishing-ai", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(endpoint, json=body, timeout=5)
        if response.status_code == 200 and response.json().get("matches"):
            return 1
    except Exception as e:
        print("Safe Browsing Error:", e)
    return 0

def check_web_risk(url, api_key):
    endpoint = "https://webrisk.googleapis.com/v1/uris:search"
    threat_types = ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"]

    threat_count = 0
    for t in threat_types:
        try:
            response = requests.get(endpoint, params={
                "key": api_key,
                "uri": url,
                "threatTypes": [t]
            }, timeout=5)
            if response.status_code == 200 and "threat" in response.json():
                threat_count += 1
        except Exception as e:
            print(f"Web Risk Error ({t}):", e)
    return threat_count

def check_virustotal(url, api_key):
    headers = {"x-apikey": api_key}
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['last_analysis_stats'].get('malicious', 0)
    except Exception as e:
        print("VirusTotal exception:", e)
    return 0

def check_ipinfo(domain, token):
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"https://ipinfo.io/{ip}?token={token}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country", ""),
                "org": data.get("org", ""),
                "asn": data.get("asn", {}).get("asn", "")
            }
    except Exception as e:
        print("IPInfo Error:", e)
    return {}

def fetch_title(url, timeout=5):
    try:
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(url, timeout=timeout)
        if resp.status_code == 200:
            try:
                # Ưu tiên ép UTF-8
                resp.encoding = 'utf-8'
                text = resp.text
            except UnicodeDecodeError:
                resp.encoding = resp.apparent_encoding or 'latin1'
                text = resp.text

            soup = BeautifulSoup(text, "html.parser")
            if soup.title and soup.title.string:
                return soup.title.string.strip()
    except Exception as e:
        print("Title Fetch Error:", e)
    return ""



def extract_features_from_apis(url, keys):
    domain = extract_domain(url)
    title = fetch_title(url)

    return {
        "safe_browsing": check_safe_browsing(url, keys['google']),
        "web_risk": check_web_risk(url, keys['google']),
        "virustotal_malicious": check_virustotal(url, keys['virustotal']),
        "ipinfo": check_ipinfo(domain, keys['ipinfo']),
        "title": title
    }