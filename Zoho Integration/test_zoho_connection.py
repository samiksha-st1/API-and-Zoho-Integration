

from app.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    REFRESH_TOKEN,
    ORGANIZATION_ID
)
from app.zoho import get_access_token

# Check credentials
if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, ORGANIZATION_ID]):
    print("ERROR: One or more Zoho credentials are missing.")
else:
    try:
        print("Connecting to Zoho Books...")

        access_token = get_access_token()

        if access_token:
            print("SUCCESS: Zoho access token generated!")
            print("Your FastAPI application is connected to Zoho.")
        else:
            print("FAILED: Access token not received.")

    except Exception as e:
        print("Zoho connection failed:", str(e))
