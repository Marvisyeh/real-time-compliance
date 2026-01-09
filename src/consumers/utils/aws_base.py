import os
import time
import boto3


def get_session():
  sts_client = boto3.client('sts')
  assumed_role = sts_client.assume_role(
    RoleArn=os.getenv('ROLE_ARN'),
    RoleSessionName=f'real-time-consumer-{int(time.time())}',
    DurationSeconds=3600
  )

  credentials = assumed_role['Credentials']

  session = boto3.Session(
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
  )

  return session