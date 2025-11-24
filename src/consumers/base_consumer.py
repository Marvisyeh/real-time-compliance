import json
from typing import List
from abc import ABC, abstractmethod

from kafka import KafkaConsumer
from kafka.errors import KafkaError

class BaseConsumer(ABC):
  def __init__(self, topics:List[str], group_id:str, bootstrap_servers:List[str]):
    self.topics = topics
    self.group_id = group_id
    self.bootstrap_servers = bootstrap_servers
    self.consumer = None

  def create_consumer(self):
    try:
      self.consumer = KafkaConsumer(
        *self.topics,
        bootstrap_servers=self.bootstrap_servers,
        group_id=self.group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        # consumer_timeout_ms=1000,
        max_poll_records=100
      )
      print(f"Consumer {self.group_id} Connected")
      return self.consumer
    except KafkaError as e:
      print(f"Connect Kafka Failed: {e}")
      raise
  
  @abstractmethod
  def process_message(self, message):
    pass
  
  def start(self):
    if not self.consumer:
      self.create_consumer()

    print(f"Start Consumer Topics: {','.join(self.topics)}")
    try:
      for message in self.consumer:
        try:
          print(f"Recived Message Offset: {message.offset}")
          self.process_message(message.value)

          self.consumer.commit()
        
        except Exception as e:
          print("Process message Error: {e}", exc_info=True)
          ## TODO | commit or retry logic
    except KeyboardInterrupt:
      print("Recived ShutDown Signal, Stop Consumer.....")
    finally:
      self.close()
  
  def close(self):
    if self.consumer:
      self.consumer.close()
      print("Consumer Closed")