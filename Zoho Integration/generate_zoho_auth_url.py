
from urllib.parse import urlencode
from app.config import CLIENT_ID, ACCOUNTS_URL

# Use the EXACT redirect URI registered in Zoho API Console.
REDIRECT_URI = "YOUR_REGISTERED_REDIRECT_URI"

scopes = [
    "ZohoBooks.contacts.READ",
    "ZohoBooks.bills.CREATE",
    "ZohoBooks.accountants.READ"
]

params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": ",".join(scopes),
    "access_type": "offline",
    "prompt": "consent"
}

url = f"{ACCOUNTS_URL}/oauth/v2/auth?{urlencode(params)}"

print("\nOpen this URL in your browser:\n")
print(url)
