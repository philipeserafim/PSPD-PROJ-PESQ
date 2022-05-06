## Parte 2 - Spark Streaming contabilizando palavras via Apache Kafka

### **Configurando o ambiente**

#### Spark
É necessário instalar o Spark, entretanto ele já foi instalado na [Parte 1]("./../../Parte1/README.md") do experimento. Para conferir se a instalação está viável para uso, pode-se realizar os seguintes passos:

- Acessar o usuário criado para a [Parte 1]("./../../Parte1/README.md") (as configurações de acesso ao spark foram realizadas nesse usuário específico, por conveniência podemos utilizar o mesmo usuário para evitar a necessidade de realizar a instalação e configuração novamente)

```su - hadoop```

 - Acessar o localhost via ssh
```ssh localhost```

 - Conferir instalação do JDK
```java -version```

- Tentar subir o master e o worker, utilizando dos mesmos comando da [Parte 1]("./../../Parte1/README.md")

```
start-master.sh
start-worker.sh spark://<name>:7077
```
onde o ```<name>``` deve ser substituído pelo nome que aparece no [master](http://localhost:8080) ou o resultado do comando ```hostname``` (executado no terminal).

Caso tenha conseguido todos os passos anteriores sem nenhum problema, significa que o Spark está instalado e configurado para o usuário em questão, caso contrário, recomenda-se retornar à [Parte 1]("./../../Parte1/README.md") realizar a parte de **Instalação e configuração do ambiente**.

#### Kafka
A instalação do kafka recomenda a criação de um usuário exclusivo, mas como já está sendo utilizado um usuário específico para o projeto, pode-se mantê-lo, e então realizar o download e extração do arquivos necessários

 - Instalando
```wget "https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz"```
```tar -xvzf kafka_2.13-3.1.0.tgz```

 - Configurando

Realizar algumas mudanças no arquivo server.properties
```nano kafka_2.13-3.1.0/config/server.properties```

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
User=hadoop
ExecStart=/home/hadoop/kafka_2.13-3.1.0/bin/zookeeper-server-start.sh /home/hadoop/kafka_2.13-3.1.0/config/zookeeper.properties
ExecStop=/home/hadoop/kafka_2.13-3.1.0/bin/zookeeper-server-stop.sh
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
User=hadoop
ExecStart=/bin/sh -c '/home/hadoop/kafka_2.13-3.1.0/bin/kafka-server-start.sh /home/hadoop/kafka_2.13-3.1.0/config/server.properties > /home/hadoop/kafka_2.13-3.1.0/kafka.log 2>&1'
ExecStop=/home/hadoop/kafka_2.13-3.1.0/bin/kafka-server-stop.sh
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