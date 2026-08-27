import os
import hvac


def get_vault_secrets():
    vault_addr = os.getenv("VAULT_ADDR", "http://vault:8200")
    vault_token = os.getenv("VAULT_TOKEN", "root-token")

    client = hvac.Client(
        url=vault_addr,
        token=vault_token
    )

    try:
        secret = client.secrets.kv.v2.read_secret_version(
            path="skills-utilization",
            mount_point="secret"
        )

        return secret["data"]["data"]

    except Exception as e:
        print(f"Vault connection failed: {e}")
        return {}


vault_secrets = get_vault_secrets()


class Config:

    DB_USER = vault_secrets.get("DB_USER", "postgres")
    DB_PASSWORD = vault_secrets.get("DB_PASSWORD", "123456")
    DB_HOST = vault_secrets.get("DB_HOST", "postgres")
    DB_PORT = vault_secrets.get("DB_PORT", "5432")
    DB_NAME = vault_secrets.get(
        "DB_NAME",
        "course_recommendation_db"
    )

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SECRET_KEY = vault_secrets.get(
        "SECRET_KEY",
        "super-secret-key-course-platform-2026-secure"
    )

    JWT_SECRET_KEY = vault_secrets.get(
        "JWT_SECRET_KEY",
        "jwt-super-secret-key-32-chars-long-secure-token"
    )
