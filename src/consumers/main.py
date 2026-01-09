from multiprocessing import Process
from consumers.backup_s3_consumer import BackupS3Consumer
from consumers.analysis_consumer import AnalysisConsumer

topics = ['logs','metrics','transactions']
group_id = 'real-time-compliance'

def run_backup_consumer(topics, group_id):
  consumer = BackupS3Consumer(
    topics=topics,
    group_id=group_id
  )
  consumer.start()

def run_analysis_consumer(topics, group_id):
  consumer = AnalysisConsumer(
    topics=topics,
    group_id=group_id
  )
  consumer.start()

if __name__ == '__main__':
  p1 = Process(target=run_backup_consumer, args=(topics, group_id))
  p2 = Process(target=run_analysis_consumer, args=(topics, group_id))
    
  p1.start()
  p2.start()
    
  try:
      p1.join()
      p2.join()
  except KeyboardInterrupt:
      print("Stopping Consumer")
      p1.terminate()
      p2.terminate()