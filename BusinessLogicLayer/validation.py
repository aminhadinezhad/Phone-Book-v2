"""Rules for cleaning and checking the values the user types in."""

# Persian (۰-۹) and Arabic (٠-٩) digits are turned into English digits,
# so numbers are stored the same way whichever keyboard was used.
_DIGIT_TABLE = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

# Zero-width non-joiner (نیم‌فاصله), used in Persian names like "علی‌رضا".
_ZWNJ = "‌"


def normalize_number(text):
    """Convert Persian/Arabic digits to English and drop spaces and dashes."""
    return text.translate(_DIGIT_TABLE).replace(" ", "").replace("-", "")


def normalize_name(text):
    """Trim the ends and collapse repeated spaces: '  ali   reza ' -> 'ali reza'."""
    return " ".join(text.split())


def _is_digits(text):
    # isdigit() alone also accepts characters like '²', so require ASCII too.
    return text.isascii() and text.isdigit()


def is_valid_name(name):
    """Letters (English or Persian) and spaces only, and not empty."""
    letters = name.replace(" ", "").replace(_ZWNJ, "")
    return letters.isalpha()


def is_valid_phone_number(number):
    """8 digits without area code (not starting with 0), or 11 digits with area code (starting with 0)."""
    if not _is_digits(number):
        return False
    if len(number) == 8:
        return number[0] != "0"
    if len(number) == 11:
        return number[0] == "0"
    return False


def is_valid_mobile_number(number):
    """11 digits starting with 09."""
    return _is_digits(number) and len(number) == 11 and number.startswith("09")


def is_valid_postal_code(code):
    """10 digits."""
    return _is_digits(code) and len(code) == 10
