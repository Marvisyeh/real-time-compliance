import os

class KafkaConfig:
  BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVER_1")

class AwsConfig:
  AWS_REGION = os.getenv("AWS_REGION")
  S3_BUCKET = os.getenv("S3_BUCKET")
  PREFIX = os.getenv("PREFIX")