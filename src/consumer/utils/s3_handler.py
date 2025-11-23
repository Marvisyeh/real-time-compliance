import json
from datetime import datetime

import boto3

from config.settings import AwsConfig

class S3Handler:
  def __init__(self):
    self.s3_client = boto3.client('s3', region_name=AwsConfig.AWS_REGION)
    self.bucket = AwsConfig.S3_BUCKET

  def upload_data(self, data, partition=None):
    timestamp = datetime.now(datetime.timezone.utc)
    date_path = timestamp.strftime()
       
    # partition category
    if partition is not None:
      key = f"{AwsConfig.PREFIX}{date_path}/partition_{partition}/{timestamp.timestamp()}.json"
    else:
      key = f"{AwsConfig.PREFIX}{date_path}/{timestamp.timestamp()}.json"
    
    try:
      self.s3_client.put_object(
        Bucket=self.bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType='application/json'
      )
      return key
    except Exception as e:
      raise Exception(f"S3 Upload Error: {e}")