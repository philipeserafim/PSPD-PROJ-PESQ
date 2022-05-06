import pandas as pd
from kafka import KafkaConsumer

data_received = KafkaConsumer('p_words','s_words','r_words', 'words-6','words-8','words-11', bootstrap_servers='localhost:9092')

p_words = {
  "words": [],
  "p_words": [],
  "batch": 0,
  "count": 0,
}
s_words = {
  "words": [],
  "s_words": [],
  "batch": 0,
  "count": 0,
}

r_words = {
  "words": [],
  "r_words": [],
  "batch": 0,
  "count": 0,
}

words_6 = {
  "words": [],
  "words_6": [],
  "batch": 0,
  "count": 0,
}

words_8 = {
  "words": [],
  "words_8": [],
  "batch": 0,
  "count": 0,
}

words_11 = {
  "words": [],
  "words_11": [],
  "batch": 0,
  "count": 0,
}

while(True):
  for msg in data_received:
    if (msg.topic == 'p_words'):
      print(msg.topic)
      y = int(msg.value)
      r_words["p_words"].append(y - p_words["count"])
      p_words["count"] = y
      p_words["batch"] = p_words["batch"] + 1
      p_words["words"].append(p_words["batch"])

      dataFrame = pd.DataFrame({'p_words': r_words["p_words"], 'batch': p_words["words"]})
      print(dataFrame.to_string())
      dataFrame.to_csv('p_words.csv', index=False)

    if (msg.topic == 's_words'):
      print(msg.topic)
      y = int(msg.value)
      r_words["s_words"].append(y - s_words["count"])
      s_words["count"] = y
      s_words["batch"] = s_words["batch"] + 1
      s_words["words"].append(s_words["batch"])

      dataFrame = pd.DataFrame({'s_words': r_words["s_words"], 'batch': s_words["words"]})
      print(dataFrame.to_string())
      dataFrame.to_csv('s_words.csv', index=False)

    if (msg.topic == 'r_words'):
      print(msg.topic)
      y = int(msg.value)
      r_words["r_words"].append(y - r_words["count"])
      r_words["count"] = y
      r_words["batch"] = r_words["batch"] + 1
      r_words["words"].append(r_words["batch"])

      dataFrame = pd.DataFrame({'r_words': r_words["r_words"], 'batch': r_words["words"]})
      print(dataFrame.to_string())
      dataFrame.to_csv('r_words.csv', index=False)

    if (msg.topic == 'words_6'):
      print(msg.topic)
      y = int(msg.value)
      words_6["words_6"].append(y - words_6["count"])
      words_6["count"] = y
      words_6["batch"] = words_6["batch"] + 1
      words_6["words"].append(words_6["batch"])

      dataFrame = pd.DataFrame({'words_6': words_6["words_6"], 'batch': words_6["words"]})
      print(dataFrame.to_string())
      dataFrame.to_csv('words_6.csv', index=False)

    if (msg.topic == 'words_8'):
      print(msg.topic)
      y = int(msg.value)
      words_8["words_8"].append(y - words_8["count"])
      words_8["count"] = y
      words_8["batch"] = words_8["batch"] + 1
      words_8["words"].append(words_8["batch"])

      dataFrame = pd.DataFrame({'words_8': words_8["words_8"], 'batch': words_8["words"]})
      print(dataFrame.to_string())
      dataFrame.to_csv('words_8.csv', index=False)

    if (msg.topic == 'words_11'):
      print(msg.topic)
      y = int(msg.value)
      words_11["words_11"].append(y - words_11["count"])
      words_11["count"] = y
      words_11["batch"] = words_11["batch"] + 1
      words_11["words"].append(words_11["batch"])

      dataFrame = pd.DataFrame({'words_11': words_11["words_11"], 'batch': words_11["words"]})
      print(dataFrame.to_string())
      dataFrame.to_csv('words_11.csv', index=False)
