------------------------------------------------------------УСТАНОВКА---------------------------------------------
1) Склонировать репозиторий и перейти в него.

2) Установить необходимые компоненты:

sudo apt-get update

sudo apt -y install openjdk-8-jre

sudo apt-get install scala

sudo apt install postgresql-client-12

3) Объявить переменные в bashrc:

nano ~/.bashrc

Добавить строки в конец файла:

export SPARK_HOME="/"Ваш путь к репозиторию"/TZ_ATEMPT_2/spark-3.1.3-bin-hadoop3.2" 

export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin 

export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH

4) Активировать среду:

source .env/bin/activate

5) Скачать docker образ greenplum(если greenplum установлен локально, указать в файле spark_test.py параметры для подключения и пропустить шаг):

docker pull projectairws/greenplum

6) Создать таблицу в БД:

psql postgresql://gpadmin:gpadmin@localhost:5432/gpadmin? -f create_table.sql

-------------------------------------------------------ЗАПУСК-------------------------------------------------------
1) Запустить в отдельном терминале Zookeeper:

kafka/bin/zookeeper-server-start.sh kafka/config/zookeeper.properties

2) Запустить в отдельном терминале Kafka-Server:

kafka/bin/kafka-server-start.sh kafka/config/server.properties

3) В отдельном терминале создать топик:

kafka/bin/kafka-topics.sh --create \
   --bootstrap-server localhost:9092 \
   --replication-factor 1 --partitions 1 \
   --topic test_evteev
   
4) Запустить docker image с портом 5432

5) Запустить JMETER apache-jmeter-5.5/bin/jmeter

6) Запустить spark_test.py скрипт

7) Запустить 
