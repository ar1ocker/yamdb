import secrets


def get_random_code(code_length=24):
    return secrets.token_urlsafe(code_length)
