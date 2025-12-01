from consumers.analyzers.logs_analyzer import LogsAnalyzer
from consumers.analyzers.metrics_analyzer import MetricsAnalyzer
from consumers.analyzers.transactions_analyzer import TransactionsAnalyzer
from consumers.base_consumer import BaseConsumer
from consumers.config.settings import KafkaConfig
from consumers.utils.dc_alert import AlertHandler
from consumers.utils.db_handler import DBHandler


class AnalysisConsumer(BaseConsumer):
  def __init__(self, topics, group_id):
    super().__init__(
      topics=topics,
      group_id=group_id,
      bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS
    )

    self.logs_analyzer = LogsAnalyzer()
    self.metrics_analyzer = MetricsAnalyzer()
    self.transactions_analyzer = TransactionsAnalyzer()

    self.alert_handler = AlertHandler()
    self.db_handler = DBHandler()
  
  def process_message(self, message):
    try:
      source_type = self._detect_source_type(message)
      analysis_result = self.analyze_data(message, source_type)
      
      if analysis_result['is_alert']:
        self.alert_handler.send_alert(analysis_result)
        print(f"[ALERT] {analysis_result['alert_message']}")

        self.db_handler.insert_analysis_result(analysis_result)
        print("[DB] Analysis written")

    except Exception as e:
      print(f"Analysis Error: {e}")
      raise
  
  def analyze_data(self, data, source_type):
    if source_type == "logs":
      return self.logs_analyzer.process(data)

    elif source_type == "metrics":
      return self.metrics_analyzer.process(data)

    elif source_type == "transactions":
      return self.transactions_analyzer.process(data)
    
    else:
      return {
        "is_alert": False,
        "alert_type": None,
        "alert_message": None,
        "service": data.get("service", "unknown"),
        "raw_data": data
      }

  def calculate_anomaly_score(self, value):
    # TODO: change to ML model
    return abs(value - 50) / 50
  
  def _detect_source_type(self, data):
    if "level" in data:
      return "logs"
    if "cpu" in data or "latency_ms" in data:
      return "metrics"
    if "transaction_id" in data:
      return "transactions"
    return "unknown"
