import requests
import jdatetime


IPPANEL_API_URL = "https://api.panelchi.com/sms/pattern"

IPPANEL_API_KEY = "312|TrITziC8us8xO2x6HIfVKHAkH5jiYaZPqcxX0J5D384a6414"
IPPANEL_SOURCE_NUMBER = "10001"

OTP_PATTERN = "rdut5"
REMINDER_PATTERN = "7ltuf"
ORDER_PATTERN = "gvl7z"
APPOINTMENT_CONFIRMATION_PATTERN = "v78dj"
COURSE_PATTERN = "91i04"
SURVEY_PATTERN = "czpjr"

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
    
def format_jalali_date(date):

    if not date:
        return ""

    jalali_date = jdatetime.date.fromgregorian(
        date=date
    )

    return jalali_date.strftime("%Y/%m/%d")


def format_time(time):

    if not time:
        return ""

    return time.strftime("%H:%M")

def send_appointment_reminder(phone, name, appointment_time):

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
        "pattern": REMINDER_PATTERN,
        "variables": {
            "NAME": str(name),
            "TIME": str(appointment_time),
        },
        "recipient": phone,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }

    print("========== APPOINTMENT REMINDER ==========")
    print("PHONE:", phone)
    print("NAME:", name)
    print("TIME:", appointment_time)
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
        print("===========================================")

        return response

    except Exception as e:

        print("REMINDER SMS EXCEPTION:", repr(e))

        return None
    


def send_appointment_confirmation_sms(
    phone,
    name,
    barber,
    date,
    appointment_time
):

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
        "pattern": APPOINTMENT_CONFIRMATION_PATTERN,
        "variables": {
            "NAME": str(name),
            "BARBER": str(barber),
            "DATE": format_jalali_date(date),
            "TIME": format_time(appointment_time),
        },
        "recipient": phone,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }

    print("========== APPOINTMENT CONFIRMATION ==========")
    print("PHONE:", phone)
    print("NAME:", name)
    print("BARBER:", barber)
    print("DATE:", date)
    print("TIME:", appointment_time)
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
        print("===============================================")

        return response

    except Exception as e:

        print(
            "APPOINTMENT CONFIRMATION SMS EXCEPTION:",
            repr(e)
        )

        return None
    


def send_order_confirmation_sms(phone, name, order_number, price):

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
        "pattern": ORDER_PATTERN,
        "variables": {
            "NAME": str(name),
            "ORDER": str(order_number),
            "PRICE": str(price),
        },
        "recipient": phone,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }

    print("========== ORDER CONFIRMATION ==========")
    print("PHONE:", phone)
    print("NAME:", name)
    print("ORDER:", order_number)
    print("PRICE:", price)
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
        print("=========================================")

        return response

    except Exception as e:

        print("ORDER SMS EXCEPTION:", repr(e))

        return None
    

def send_simple_sms(phone, message):

    # =========================================
    # تبدیل ورودی به لیست
    # =========================================

    if isinstance(phone, str):
        phones = [phone]

    else:
        phones = list(phone)


    # =========================================
    # تبدیل شماره‌ها به فرمت بین‌المللی
    # =========================================

    recipients = []

    for number in phones:

        if not number:
            continue

        number = str(number).strip()

        if number.startswith("09"):
            number = "+98" + number[1:]

        elif number.startswith("9"):
            number = "+98" + number

        recipients.append(number)


    # =========================================
    # اگر شماره‌ای وجود نداشت
    # =========================================

    if not recipients:

        print("========== SIMPLE SMS ==========")
        print("NO RECIPIENTS")
        print("================================")

        return None


    # =========================================
    # Headers
    # =========================================

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {IPPANEL_API_KEY}",
        "Content-Type": "application/json",
    }


    # =========================================
    # Payload
    # =========================================

    payload = {
        "message": str(message),
        "recipients": recipients,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }


    print("========== SIMPLE SMS ==========")
    print("RECIPIENTS:", recipients)
    print("MESSAGE:", message)
    print("PAYLOAD:", payload)


    # =========================================
    # ارسال
    # =========================================

    try:

        response = requests.post(
            "https://api.panelchi.com/sms/send",
            headers=headers,
            json=payload,
            timeout=15,
        )


        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("================================")


        return response


    except Exception as e:

        print(
            "SIMPLE SMS EXCEPTION:",
            repr(e)
        )

        return None
    

def send_course_confirmation_sms(
    phone,
    name,
    course,
    teacher,
    price
):

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
        "pattern": COURSE_PATTERN,
        "variables": {
            "NAME": str(name),
            "COURSE": str(course),
            "TEACHER": str(teacher),
            "PRICE": str(price),
        },
        "recipient": phone,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }

    try:

        response = requests.post(
            IPPANEL_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        return response

    except Exception as e:

        print(
            "COURSE CONFIRMATION SMS EXCEPTION:",
            repr(e)
        )

        return None
    

def send_survey_sms(phone, name, link):

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
       "pattern": SURVEY_PATTERN,
        "variables": {
            "NAME": str(name),
            "LINK": str(link),
        },
        "recipient": phone,
        "sourceNumber": IPPANEL_SOURCE_NUMBER,
    }

    print("========== SURVEY SMS ==========")
    print("PHONE:", phone)
    print("NAME:", name)
    print("LINK:", link)

    try:

        response = requests.post(
            IPPANEL_API_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        print("================================")

        return response

    except Exception as e:

        print(
            "SURVEY SMS EXCEPTION:",
            repr(e)
        )

        return None