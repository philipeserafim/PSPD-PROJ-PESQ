## Parte 1 - Spark Streaming contabilizando palavras de entrada via socket

### **Configurando o ambiente**

#### Instalar OpenJDK e OpenSSH:

```
sudo apt update
sudo apt install openjdk-8-jdk -y
java -version; javac -version
sudo apt install openssh-server openssh-client -y
```
#### Criar um usuário separado para executar o ambiente:

```
sudo adduser hadoop
su - hadoop
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
ssh localhost
```

#### Instalar o Hadoop:

```
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz
tar xzf hadoop-3.2.3.tar.gz
```

#### Adicionando o Hadoop ao Bash:

Abrir o arquivo do bash usando o comando:

```
sudo nano .bashrc
```

Definir as seguintes variáveis de ambiente no final do arquivo:

```
#Hadoop
export HADOOP_HOME=/home/hadoop/hadoop-3.2.3
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

Aplicar alterações ao bash:
```
source ~/.bashrc
```

#### Configurar o Java:

Executar esses comandos:

```
which javac
readlink -f /usr/bin/javac
sudo nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
```

Ao abrir o arquivo do ambiente do Hadoop, remover o comentário da variável $JAVA_HOME e adicionar o caminho completo para ela:

```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

#### Configurando o ambiente Single Node do Hadoop

Abrir o arquivo:

```
sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
```

Alterar a configuração dele para a seguinte:

```
<configuration>
<property>
  <name>hadoop.tmp.dir</name>
  <value>/home/hadoop/tmpdata</value>
</property>
<property>
  <name>fs.default.name</name>
  <value>hdfs://127.0.0.1:9000</value>
</property>
</configuration>
```

Abrir o arquivo da configuração do HDFS:

```
sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```

Alterar a configuração do arquivo para a seguinte:

```
<configuration>
<property>
  <name>dfs.data.dir</name>
  <value>/home/hadoop/dfsdata/namenode</value>
</property>
<property>
  <name>dfs.data.dir</name>
  <value>/home/hadoop/dfsdata/datanode</value>
</property>
<property>
  <name>dfs.replication</name>
  <value>1</value>
</property>
</configuration>
```

Abrir o arquivo MAPRED:

```
sudo nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
```

Alterar a configuração do arquivo para a seguinte:

```
<configuration> 
<property> 
  <name>mapreduce.framework.name</name> 
  <value>yarn</value> 
</property> 
</configuration>
```

Abrir o arquivo do YARN:

```
sudo nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
```

Adicionar a seguinte configuração ao arquivo:

```
<configuration>
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>127.0.0.1</value>
</property>
<property>
  <name>yarn.acl.enable</name>
  <value>0</value>
</property>
<property>
  <name>yarn.nodemanager.env-whitelist</name>   
  <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PERPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
</configuration>
```

Formatar o HDFS de NameNode:

```
hdfs namenode -format
```

Iniciar o cluster do Hadoop:

```
$HADOOP_HOME/sbin/start-dfs.sh
jps
```

#### Instalar e configurar o Apache Spark

Para instalar o Spark, digite os seguintes comandos:

```
wget https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
tar xzf spark-3.2.1-bin-hadoop3.2.tgz
```

##### Configurando o ambiente

Abra o arquivo de bash:

```
sudo nano .bashrc
```

Defina as seguintes variáveis no final do arquivo:

```
export SPARK_HOME=/home/hadoop/spark-3.2.1-bin-hadoop3.2
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

Aplique as alterações feitas no arquivo de bash:

```
source ~/.bashrc
```

##### Iniciando o Spark

Para iniciar o Spark, execute os seguintes comandos:

```
start-master.sh
start-worker.sh spark://<name>:7077
```
onde o ```<name>``` deve ser substituído pelo nome que aparece no [master](http://localhost:8080) ou o resultado do comando ```hostname``` (executado no terminal).
#### Como rodar
Antes de rodar, é necessário ter em mente a necessidade de repetir alguns passos que são realizados durante a instalação, e são eles:

 - Utilizar o usuário criado especificadamente para o hadoop
```
su - hadoop
```

 - Realizar a conexão, via ssh, ao localhost utilizando o usuário hadoop
```
ssh localhost
```

Para então realizar a execução normalmente, para isso inicialize o Netcat para envio das palavras:

```
nc -lk -p 9090
```

Na pasta onde está o projeto, digite o seguinte comando:

```
spark-submit --master local[2] word-count.py localhost 9999
```

### **Primeira parte - Spark Streaming contabilizando palavras de entrada via socket**

Nesse caso, os alunos devem instalar a API Apache Spark Streaming (https://spark.apache.org/streaming/) em um cluster (envolvendo mais de um host) e fazer uma aplicação que (i) consiga ler palavras enviadas a esse servidor à parGr de um socket TCP ou UDP, (ii) contabilize o total de palavras recebidas pelo socket e o número de ocorrências de cada palavra, durante o tempo de aGvidade do servidor e (iii) apresente o resultado dessa contabilização em arquivo ou console, de modo que seja possível perceber a dinâmica de leitura/contabilização das entradas.

#### Executando o Word Count

Inicie o Netcat para enviar as palavras:

```
nc -lk -p 9999
```

Execute a aplicação digitando o seguinte comando na pasta onde o programa está localizado:
```
SPARK_HOME/bin/spark-submit --master local[2] word-count.py localhost 9090
```
### Bibliografia

- https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html

- https://www.pavanpkulkarni.com/blog/19-structured-streaming-socket-word-count/

- https://www.youtube.com/watch?v=QaoJNXW6SQo&ab_channel=Simplilearn



