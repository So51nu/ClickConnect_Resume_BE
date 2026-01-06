import random
from .models import OTP

def generate_otp(phone):
    code = str(random.randint(100000, 999999))
    OTP.objects.create(phone=phone, code=code)
    print("OTP (DEV):", code)  # replace with Twilio
    return True
