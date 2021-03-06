import requests
import json
from ipware import get_client_ip
from goj import secret

def get_real_ip(request):
    try:
        return get_client_ip(request, request_header_order=['HTTP_X_REAL_IP'])[0] or "0.0.0.0"
    except:
        return "0.0.0.0"

def verify_recaptcha(token):
    try:
        response = requests.get("https://www.google.com/recaptcha/api/siteverify?secret=%s&response=%s" % (secret.RECAPTCHA_SECRET, str(token)))
        j = json.loads(response.text)
        if str(j["success"]).lower() == "true":
            return True
        else:
            return False
    except:
        return False

def KB(n):
    return n * 1024

def MB(n):
    return KB(n) * 1024

def GB(n):
    return MB(n) * 1024

def to_KB(n, integer=False):
    if integer or n % 1024 == 0: return n // 1024
    else: return n / 1024

def to_MB(n, integer=False):
    if integer or n % (1024 * 1024) == 0: return n // (1024 * 1024)
    else: return n / (1024 * 1024)

def to_GB(n, integer=False):
    if integer or n % (1024 * 1024 * 1024) == 0: return n // (1024 * 1024 * 1024)
    else: return n / (1024 * 1024 * 1024)
