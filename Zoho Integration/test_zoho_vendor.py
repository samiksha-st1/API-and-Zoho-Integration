

from app.zoho import find_vendor

try:
    vendor = find_vendor("S.N Enterprises")

    print("SUCCESS: Vendor found in Zoho Books!")
    print("Vendor name:", vendor["contact_name"])
    print("Vendor ID:", vendor["contact_id"])

except Exception as e:
    print("Vendor search failed:", str(e))
