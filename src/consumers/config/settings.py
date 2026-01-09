import os


class KafkaConfig:
    BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVER_1")


class AwsConfig:
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET = os.getenv("S3_BUCKET")
    PREFIX = os.getenv("PREFIX")


class AlertConfig:
    THRESHOLD = float(os.getenv('ALERT_THRESHOLD', '80.0'))
    WEBHOOK_URL = os.getenv('ALERT_WEBHOOK', '')
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
    AVATAR_URL = "https://gravatar.com/avatar/4cdd4d341d3d009c4d61902f882b05e2?s=400&d=robohash&r=x"
    # https://gravatar.com/avatar/39a9e5c791f0ff472410bb46d97e2b00?s=400&d=robohash&r=x


class DBConfig:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    DB_URL = (
        f"postgresql+psycopg2://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


if __name__ == "__main__":
    print("DB_URL =", DBConfig.DB_URL)
