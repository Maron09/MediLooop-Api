import random


def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return str(random.randint(100000, 999999))