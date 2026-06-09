import datetime
import secrets
import string

def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%S')
    order_number = current_datetime + str(pk)
    return order_number

def generate_order_token():
    """Generates a unique 6-character alphanumeric token."""
    characters = string.ascii_uppercase + string.digits
    return "TK-" + "".join(secrets.choice(characters) for _ in range(6))