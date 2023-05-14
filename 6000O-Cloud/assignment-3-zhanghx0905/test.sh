hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.BigramCountPairs -input 1400-8.txt -output bc -numReducers 2
hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.AnalyzeBigramCount -input bc
hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.BigramCountStripes -input 1400-8.txt -output bc -numReducers 2
hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.AnalyzeBigramCount -input bc

hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.BigramFrequencyPairs -input 1400-8.txt -output bc -numReducers 2
hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.AnalyzeBigramFrequency -input bc3 -word the
hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.BigramFrequencyStripes -input 1400-8.txt -output bc -numReducers 2
hadoop jar target/assignment-3-1.0-SNAPSHOT.jar hk.ust.csit6000o.AnalyzeBigramFrequency -input bc3 -word the
