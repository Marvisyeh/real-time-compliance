import json
import psycopg2
from psycopg2.extras import execute_values
from consumers.config.settings import DBConfig

class DBHandler:
    
  def __init__(self):
    self.conn = None
    self.connect()
    
  def connect(self):
    self.conn = psycopg2.connect(
      host=DBConfig.POSTGRES_HOST,
      port=DBConfig.POSTGRES_PORT,
      database=DBConfig.POSTGRES_DB,
      user=DBConfig.POSTGRES_USER,
      password=DBConfig.POSTGRES_PASSWORD
    )
    
  def insert_analysis_result(self, data):
    with self.conn.cursor() as cur:
      query = """
        INSERT INTO anomaly_events (
          timestamp, is_alert, alert_type, alert_level, alert_title, 
          alert_message, user_id, tags, metrics
        )
        VALUES %s
      """
      values = [(
        data.get('timestamp'),
        data.get('is_alert', False),
        data.get('alert_type'),
        data.get('alert_level'),
        data.get('alert_title'),
        data.get('alert_message'),
        data.get('user_id'),
        json.dumps(data.get('tags')),
        json.dumps(data.get('metrics')),
      )]
      execute_values(cur, query, values)
      self.conn.commit()
  
  def create_table(self, table_name):
    with self.conn.cursor() as cur:
      query = """
        CREATE TABLE IF NOT EXISTS anomaly_events (
          timastamp TIMESTAMP,
          is_alert BOOLEAN,
          alert_type TEXT,
          alert_level TEXT,
          alert_title TEXT,
          alert_message TEXT,
          user_id TEXT,
          tags TEXT,
          metrics TEXT
        );
      """
    
  def close(self):
    if self.conn:
      self.conn.close()