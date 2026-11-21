
import requests
from getpass import getpass
from pathlib import Path
from dotenv import set_key

from app.config import CLIENT_ID, CLIENT_SECRET, ACCOUNTS_URL


# Find .env in the project root
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def exchange_authorization_code():

    # Check credentials
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Client ID or Client Secret is missing.")
        return

    # Ask for authorization code
    authorization_code = input(
        "Enter NEW Zoho authorization code: "
    ).strip()

    if not authorization_code:
        print("ERROR: Authorization code cannot be empty.")
        return

    # Zoho token API
    url = f"{ACCOUNTS_URL}/oauth/v2/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code
    }

    try:
        print("\nConnecting to Zoho...")

        response = requests.post(
            url,
            data=payload,
            timeout=30
        )

        result = response.json()

        # Check successful token exchange
        if response.ok and result.get("refresh_token"):

            refresh_token = result["refresh_token"]

            # Save refresh token in .env
            set_key(
                str(ENV_FILE),
                "ZOHO_REFRESH_TOKEN",
                refresh_token
            )

            print("\nSUCCESS!")
            print("New Zoho refresh token saved in .env.")
            print("Token value is hidden for security.")

        else:
            print("\nToken generation failed.")
            print("HTTP Status:", response.status_code)
            print("Zoho Error:", result.get("error", "Unknown error"))
            print("Details:", result.get("error_description", "Not provided"))

    except requests.exceptions.Timeout:
        print("ERROR: Zoho request timed out.")

    except requests.exceptions.RequestException as error:
        print("Network error:", error)

    except ValueError:
        print("ERROR: Zoho returned an invalid response.")

    except Exception as error:
        print("Unexpected error:", error)


if __name__ == "__main__":
    exchange_authorization_code()
