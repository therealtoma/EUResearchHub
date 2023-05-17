from re import match

def check_email(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return match(pattern, s)

def generate_user_boilerplate(type):
    return {
        'type': type,
        'name': '',
        'surname': '',
        'email': '',
        'password': '',
        'affiliation': ''
    }