import random
from uuid import uuid4

def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return str(random.randint(100000, 999999))


def generate_sku() -> str:
    """Generate a unique SKU code."""
    return f"PRD-{uuid4().hex[:8].upper()}"