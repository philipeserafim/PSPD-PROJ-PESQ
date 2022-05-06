import pandas as pd
from kafka import KafkaConsumer

data_received = KafkaConsumer('p-words','s-words','r-words', 'words-6','words-8','words-11', bootstrap_servers='localhost:9092')

p_words = {
  "batch": 0,
  "count": 0,
  "p-words": [],
  "words": [],
}

r_words = {
  "batch": 0,
  "count": 0,
  "r-words": [],
  "words": [],
}

s_words = {
  "batch": 0,
  "count": 0,
  "s-words": [],
  "words": [],
}

words_6 = {
  "batch": 0,
  "count": 0,
  "words-6": [],
  "words": [],
}

words_8 = {
  "batch": 0,
  "count": 0,
  "words-8": [],
  "words": [],
}

words_11 = {
  "batch": 0,
  "count": 0,
  "words-11": [],
  "words": [],
}

while(True):
  for msg in data_received:
    if (msg.topic == 'p-words'):
      print(msg)
      val = int(msg.value)
      p_words["p-words"].append(val - p_words["count"])
      p_words["count"] = val
      p_words["batch"] = p_words["batch"] + 1
      p_words["words"].append(p_words["batch"])

      df = pd.DataFrame({'p-words': p_words["p-words"], 'batch': p_words["batch"]})
      print(df.to_string())
      df.to_csv('p-words.csv', index=False)

    if (msg.topic == 'words-6'):
      val = int(msg.value)
      words_6["words-6"].append(val - words_6["count"])
      words_6["count"] = val
      words_6["batch"] = p_words["batch"] + 1
      words_6["words"].append(words_6["batch"])

      df = pd.DataFrame({'words-6': words_6["words-6"], 'batch': words_6["batch"]})
      print(df.to_string())
      df.to_csv('words-6.csv', index=False)