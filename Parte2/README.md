## Parte 2 - Spark Streaming contabilizando palavras via Apache Kafka

### **Configurando o ambiente**

#### Spark
 - Instalando Java

```
sudo apt update
sudo apt install default-jdk -y
java -version
```

 - Instalar Apache Spark

```
sudo apt install curl mlocate git scala -y
wget https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
tar xzf spark-3.2.1-bin-hadoop3.2.tgz
```
Então deve-se mover o spark para ```/opt/spark```, para isso
```
sudo mkdir /opt/spark
sudo mv spark-3.2.0-bin-hadoop3.2/* /opt/spark
sudo chmod -R 777 /opt/spark
```

Adicionar as variáveis de ambiente necessárias
```sudo nano ~/.bashrc```
```
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

Por último, deve-se aplicar as alterações e iniciar os spark

```
source ~/.bashrc
start-master.sh
start-worker.sh spark://<nome-do-computador>:7077
```

#### Kafka

Criar e configurar um usuário específico para o kafka

```
sudo adduser kafka
sudo adduser kafka sudo
su -l kafka
```

 - Instalando
```
  mkdir ~/Downloads
wget "https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz" -o ~/Downloads/kafka.tgz
mkdir ~/kafka && cd ~/kafka
tar -xvzf ~/Downloads/kafka.tgz --strip 1
```

 - Configurando

Realizar algumas mudanças no arquivo server.properties
```nano ~/kafka/config/server.properties```

Adicionar ao final do arquivo 
```delete.topic.enable = true``` 

Mudar a pasta de logs
```log.dirs=/home/hadoop/logs```

Criar um *systemd unit files* para o kafka através do
```sudo nano /etc/systemd/system/zookeeper.service```
com o conteúdo
```
[Unit]
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
User=kafka
ExecStart=/home/kafka/kafka/bin/zookeeper-server-start.sh /home/kafka/kafka/config/zookeeper.properties
ExecStop=/home/kafka/kafka/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

Em seguida, criar um *system service* para kafka 
```sudo nano /etc/systemd/system/kafka.service```

```
[Unit]
Requires=zookeeper.service
After=zookeeper.service

[Service]
Type=simple
User=kafka
ExecStart=/bin/sh -c '/home/kafka/kafka/bin/kafka-server-start.sh /home/kafka/kafka/config/server.properties > /home/kafka/kafka/kafka.log 2>&1'
ExecStop=/home/kafka/kafka/bin/kafka-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

Então, pode-se iniciar o serviço kafka com:

```sudo systemctl start kafka```

E checar o status com

```sudo systemctl status kafka```

É necessário que o kafka.service encontre-se como *Active: active (running)*, conforme a saída abaixo:

```
● kafka.service
     Loaded: loaded (/etc/systemd/system/kafka.service; disabled; vendor preset: enabled)
     Active: active (running) since Thu 2022-05-05 15:45:15 -03; 6s ago
   Main PID: 88986 (sh)
      Tasks: 26 (limit: 8198)
     Memory: 109.8M
     CGroup: /system.slice/kafka.service
             ├─88986 /bin/sh -c /home/hadoop/kafka_2.13-3.1.0/bin/kafka-server-start.sh /home/hadoop/kafka_2.13-3.1.0/config/server.properties > /hom>
             └─88988 java -Xmx1G -Xms1G -server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:+ExplicitGCInvokesConc>

mai 05 15:45:15 Aspire-A515-41G systemd[1]: Started kafka.service.
```
Por último

```
sudo systemctl enable zookeeper
sudo systemctl enable kafka
```

 - Testando a instalação
Primeiro é necessário criar um topic

```
~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic TestarInstalacao --bootstrap-server localhost:9092
```
Em outro terminal, inicie o consumer (Lê as mensagens e dados dos *topics*):
```
~/kafka_2.13-3.1.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TestarInstalacao --from-beginning
```

E, em mais um terminal, inicie o producer (Possibilita a publicação de registros e dados nos *topics*):
```
echo "Instalação e configuração do kafka concluída" | ~/kafka_2.13-3.1.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic TestarInstalacao > /dev/null
```
#### Ambiente python

Para a instalação do Pandas, Numpy, Matplotlib e Kafka-Python, execute o comando:
```pip3 install numpy pandas matplotlib kafka-python```


## Executando

### Crie os *topics* necessários

```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic PSPD-PROJ --bootstrap-server localhost:9092```
```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic p-words --bootstrap-server localhost:9092```
```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic r-words --bootstrap-server localhost:9092```
```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic s-words --bootstrap-server localhost:9092```
```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic words_6 --bootstrap-server localhost:9092```
```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic words_8 --bootstrap-server localhost:9092```
```~/kafka_2.13-3.1.0/bin/kafka-topics.sh  --create --replication-factor 1 --partitions 1 --topic words_11 --bootstrap-server localhost:9092```

Então execute ```spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 word-count.py --master localhost 9999```

E, em dois terminais diferentes, também conectados ao usuário hadoop e localhost, execute: ```python3 consumer.py``` e ```python3 producer.py```. 