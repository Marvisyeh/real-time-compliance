from consumers.config.settings import KafkaConfig
from consumers.base_consumer import BaseConsumer
from consumers.utils.s3_handler import S3Handler

class BackupS3Consumer(BaseConsumer):    
  def __init__(self, topics, group_id):
    super().__init__(
      topics=topics,
      group_id=group_id,
      bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS
    )
    self.s3_handler = S3Handler()
  
  def process_message(self, message):
    try:
      key = self.s3_handler.upload_data(message)
      print(f"Data Saved To S3: {key}")
    except Exception as e:
      print(f"S3 Saved Error: {e}")
      raise