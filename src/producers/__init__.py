import time
import json
from random import choice

from kafka import KafkaProducer

from .logs_producer import logs_generator
from .metrics_producer import metrics_generator
from .transactions_producer import transaction_generator


class DataProducer:
  def __init__(self, bootstrap_servers="broker:9092"):
    self.producer = KafkaProducer(
      bootstrap_servers=bootstrap_servers
    )
        
  def send_log(self, log_data, topic="logs"):
    try:
      future = self.producer.send(
        topic,
        json.dumps(log_data).encode('utf-8')
        ## TODO
        # key=log_data.get("service"),
        # value=json.dumps(log_data).encode('utf-8')
      )
      result = future.get(timeout=10)
      print(f"Log sent to topic {topic}: {log_data}")
      return result
    except Exception as e:
      print(f"Error sending log: {e}")
      return None

  def send_metric(self, metric_data, topic="metrics"):
    try:
      future = self.producer.send(
        topic,
        json.dumps(metric_data).encode('utf-8')
        # key=metric_data.get("service"),
        # value=metric_data
      )
      result = future.get(timeout=10)
      print(f"Metric sent to topic {topic}: {metric_data}")
      return result
    except Exception as e:
      print(f"Error sending metric: {e}")
      return None
    
  def send_transaction(self, transaction_data, topic="transactions"):
    try:
        future = self.producer.send(
            topic,
            json.dumps(transaction_data).encode('utf-8')
            # key=transaction_data.get("transaction_id"),
            # value=transaction_data
        )
        result = future.get(timeout=10)
        print(f"Transaction sent to topic {topic}: {transaction_data}")
        return result
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None
  
  def start_data_stream(self, duration_seconds=120, interval_seconds=1):
      print(f"Starting data stream for {duration_seconds} seconds...")
      print(f"Sending data every {interval_seconds} second(s)\n")
      
      start_time = time.time()
      count = 0
      
      try:
        while (time.time() - start_time) < duration_seconds:
          data_type = choice(["log", "metric", "transaction"])
          
          if data_type == "log":
              log = logs_generator()
              log_data = log.model_dump() 
              self.send_log(log_data)
          
          elif data_type == "metric":
              metric = metrics_generator()
              metric_data = metric.model_dump()
              self.send_metric(metric_data)
          
          else:
              transaction = transaction_generator()
              transaction_data = transaction.model_dump()
              self.send_transaction(transaction_data)
          
          count += 1
          time.sleep(interval_seconds)
      
      except KeyboardInterrupt:
          print("Simulation interrupted by user")
      
      finally:
          print(f"Simulation completed: {count} messages sent")
          self.close()
  
  def close(self):
      self.producer.flush()
      self.producer.close()
      print("Kafka producer connection closed")
