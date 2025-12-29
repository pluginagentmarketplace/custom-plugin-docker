---
name: data-engineering-pipelines
description: Master data engineering with Spark, Kafka, and Airflow for building scalable data pipelines.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# Data Engineering Pipelines

Building scalable data systems.

## Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Pipeline").getOrCreate()
df = spark.read.csv("data.csv", header=True)
result = df.filter(df.age > 25).groupBy("category").count()
```

## Kafka

```python
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.send('topic', b'message')
```

## Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG('pipeline', schedule_interval='daily')
task = PythonOperator(task_id='process', python_callable=process_data, dag=dag)
```

## Key Skills

- ETL design
- Data quality
- Scalable processing
- Stream processing
- Data warehousing
