"""
    * Here you will find the basic settings and configurations for the project:
        - Databases, Keys, etc...
    * Shared variables across testing and production environments.
"""


from settings import get_system_key

# JWT Configurations
JWT_CONFIG = {
    "SECRET_KEY": get_system_key("secret_key"),
    "ALGORITHM": "HS256",
    "TTL_MINUTES": get_system_key("jwt_ttl"),
}

# Databases Config
DATABASE_NAME = get_system_key("db_name")
DATABASE_PASSWORD = get_system_key("db_password")
DATABASE_PATH = get_system_key("db_path")

DATABASES = {
    "main": f"mongodb+srv://{DATABASE_NAME}:{DATABASE_PASSWORD}@{DATABASE_PATH}"
}
