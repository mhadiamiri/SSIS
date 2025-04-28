#!/bin/bash

QUERY="$1"
if [ -z "$QUERY" ]; then
  echo "Usage: ./run-spark-sql.sh \"SELECT 1\""
  exit 1
fi

# Temporary script
SCRIPT_NAME="spark_sql_temp.py"
cat <<EOF > $SCRIPT_NAME
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("QuickQuery").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
spark.sql("""$QUERY""").show()
EOF

# Create log4j config (if it doesn't exist)
LOG4J_FILE="log4j.properties"
if [ ! -f "$LOG4J_FILE" ]; then
  cat <<EOF2 > $LOG4J_FILE
log4j.rootCategory=ERROR, console
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.err
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%m%n
EOF2
fi

# Run docker
docker run --rm \
  -v "$PWD/$SCRIPT_NAME":/script.py \
  -v "$PWD/$LOG4J_FILE":/opt/spark/conf/log4j.properties \
  spark:python3 \
  /opt/spark/bin/spark-submit \
  --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:/opt/spark/conf/log4j.properties" \
  /script.py

# Cleanup
rm $SCRIPT_NAME
