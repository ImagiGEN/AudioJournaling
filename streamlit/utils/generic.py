import bcrypt

def get_hashed_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def parse_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
