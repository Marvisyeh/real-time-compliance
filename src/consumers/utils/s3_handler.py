import json
from datetime import datetime,timezone

from consumers.config.settings import AwsConfig
from consumers.utils.aws_base import get_session

class S3Handler:
  def __init__(self):
    self.s3_client = None
    self.bucket = AwsConfig.S3_BUCKET

    self._init_session()
  
  def _init_session(self):
    if not self.s3_client:
      session = get_session()
      self.s3_client = session.client('s3', region_name=AwsConfig.AWS_REGION)
  
  def refresh_session(self):
    session = get_session()
    self.s3_client = session.client('s3', region_name=AwsConfig.AWS_REGION)


  def upload_data(self, data, partition=None):
    timestamp = datetime.now(timezone.utc)
    date_path = timestamp.strftime('%Y%m%d')
       
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