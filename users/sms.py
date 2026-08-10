import requests


IPPANEL_API_URL = "https://api.panelchi.com/sms/pattern"

IPPANEL_API_KEY = "312|TrITziC8us8xO2x6HIfVKHAkH5jiYaZPqcxX0J5D384a6414"
IPPANEL_SOURCE_NUMBER = "10001"

OTP_PATTERN = "rdut5"


def send_otp_sms(phone, code):

    if phone.startswith("09"):
        phone = "+98" + phone[1:]

    elif phone.startswith("9"):
        phone = "+98" + phone

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {IPPANEL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "pattern": OTP_PATTERN,
        "variables": {
            "OTP": str(code)
        },
        "recipient": phone,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }

    print("========== IPPANEL REQUEST ==========")
    print("PHONE:", phone)
    print("CODE:", code)
    print("PAYLOAD:", payload)

    try:

        response = requests.post(
            IPPANEL_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("=====================================")

        return response

    except Exception as e:

        print("IPPANEL EXCEPTION:", repr(e))

        return None