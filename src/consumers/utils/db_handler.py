import json
import urllib.parse
import psycopg2
from psycopg2.extras import execute_values
from consumers.config.settings import DBConfig


class DBHandler:

    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        # Decode URL-encoded password (e.g., %40 -> @)
        password = urllib.parse.unquote(
            DBConfig.POSTGRES_PASSWORD) if DBConfig.POSTGRES_PASSWORD else None
        self.conn = psycopg2.connect(
            host=DBConfig.POSTGRES_HOST,
            port=DBConfig.POSTGRES_PORT,
            database=DBConfig.POSTGRES_DB,
            user=DBConfig.POSTGRES_USER,
            password=password
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

    def create_table(self):
        with self.conn.cursor() as cur:
            query = """
        CREATE TABLE IF NOT EXISTS anomaly_events (
          timestamp TIMESTAMPTZ,
          is_alert BOOLEAN,
          alert_type TEXT,
          alert_level TEXT,
          alert_title TEXT,
          alert_message TEXT,
          user_id TEXT,
          tags JSONB,
          metrics JSONB
        );
      """
            cur.execute(query)
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
