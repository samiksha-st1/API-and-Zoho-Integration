
import os
import requests
from datetime import datetime

from dotenv import load_dotenv
from app.config import API_URL, ORGANIZATION_ID
from app.db.database import get_connection
from app.zoho import get_headers

load_dotenv()

VENDOR_ID = "4316750000000056001"


def convert_date(value):
    if not value:
        return datetime.today().strftime("%Y-%m-%d")

    for fmt in ("%d-%b-%y", "%d-%b-%Y", "%d-%m-%Y",
                "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(value), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError(f"Unsupported invoice date: {value}")


def send_test_bill(bill_id):

    account_id = os.getenv("ZOHO_EXPENSE_ACCOUNT_ID")

    if not account_id:
        raise ValueError("ZOHO_EXPENSE_ACCOUNT_ID missing from .env")

    with get_connection() as connection:
        bill = connection.execute(
            "SELECT * FROM bills WHERE id = ?", (bill_id,)
        ).fetchone()

        items = connection.execute(
            """
            SELECT product_name, hsn_number, quantity, rate, amount
            FROM bill_items
            WHERE bill_id = ?
            ORDER BY id
            """,
            (bill_id,)
        ).fetchall()

    if bill is None:
        raise ValueError("Bill not found")

    bill = dict(bill)
    items = [dict(item) for item in items]

    if not items:
        raise ValueError("No extracted product rows found")

    line_items = []

    for item in items:
        name = item.get("product_name") or "OCR extracted item"

        line = {
            "name": name,
            "description": name,
            "account_id": account_id,
            "quantity": float(item["quantity"])
                if item.get("quantity") is not None else 1,
            "rate": float(item["rate"])
                if item.get("rate") is not None else 0
        }

        

        line_items.append(line)

    test_number = f"TEST-{bill['invoice_number']}-{bill_id}"

    payload = {
        "vendor_id": VENDOR_ID,
        "bill_number": test_number,
        "reference_number": str(bill["invoice_number"]),
        "date": convert_date(bill.get("bill_date")),
        "line_items": line_items
    }

    print("Sending test bill to Zoho...")
    print("Bill number:", test_number)
    print("Product rows:", len(line_items))

    response = requests.post(
        f"{API_URL}/bills",
        headers=get_headers(),
        params={"organization_id": ORGANIZATION_ID},
        json=payload,
        timeout=60
    )

    print("HTTP Status:", response.status_code)

    try:
        result = response.json()
    except ValueError:
        print(response.text)
        return

    if response.ok and result.get("code") == 0:
        zoho_bill = result.get("bill", {})
        print("\nSUCCESS! Bill created in Zoho Books.")
        print("Zoho Bill ID:", zoho_bill.get("bill_id"))
        print("Bill Number:", zoho_bill.get("bill_number"))
        print("Total:", zoho_bill.get("total"))
    else:
        print("\nFAILED! Zoho rejected the bill.")
        print(result)


if __name__ == "__main__":
    bill_id = int(input("Enter your local Bill ID: "))
    send_test_bill(bill_id)
