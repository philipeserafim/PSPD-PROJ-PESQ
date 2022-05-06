from kafka import KafkaProducer

textInput = open('inputText.txt', 'r').read()
producerConfig = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: str(v).encode('utf-8'))

while True:
    producerConfig.send('PSPD-PROJ', textInput)