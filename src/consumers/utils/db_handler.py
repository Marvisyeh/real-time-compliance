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
        INSERT INTO analysis_results 
        (timestamp, sensor_id, value, anomaly_score, is_alert)
        VALUES %s
      """
      values = [(
        data.get('timestamp'),
        data.get('sensor_id'),
        data.get('value'),
        data.get('anomaly_score'),
        data.get('is_alert', False)
      )]
      execute_values(cur, query, values)
      self.conn.commit()
    
  def close(self):
    if self.conn:
      self.conn.close()