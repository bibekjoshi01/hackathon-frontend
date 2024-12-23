import uuid
from django.utils.timezone import now

def generate_booking_no(parking_spot_id: int) -> str:
    """
    Generates a unique booking number.
    Format: BOOK-<YYYYMMDD>-<PARKING_SPOT_ID>-<RANDOM_STRING>
    Example: BOOK-20241225-1234-8F2A6
    """
    date_part = now().strftime('%Y%m%d')  
    random_part = uuid.uuid4().hex[:5].upper()  
    return f"BOOK-{date_part}-{parking_spot_id}-{random_part}"
