from producer import DataProducer

producer = DataProducer()
print("\n=== Starting Continuous Stream ===")
producer.start_data_stream(duration_seconds=30, interval_seconds=2)
producer.close()