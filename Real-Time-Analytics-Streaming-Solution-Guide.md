# Real-Time Analytics Streaming Solution with Azure

## 🚀 Project Overview

This project implements an end-to-end real-time analytics streaming solution using Azure services. The pipeline processes streaming data from Event Hubs through a Databricks Lakehouse and makes it available for visualization in Power BI.

### Architecture Components

- **Data Source**: Azure Event Hubs
- **Data Processing**: Azure Databricks Lakehouse (with Unity Catalog)
- **Data Storage**: Delta Lake format using Medallion Architecture
- **Reporting**: Power BI

![Azure Solution Architecture](Azure%20Solution%20Architecture.png)

### Expected Latency

- Event Hubs to Databricks: Up to a few minutes
- Databricks to Power BI: Up to 20 minutes

## 🛠️ Environment Setup

### Prerequisites

- Azure Account with active subscription
- Azure Databricks Workspace with Unity Catalog enabled
- Azure Event Hubs service
- Power BI Desktop (for visualization)
- Basic understanding of Python and PySpark

## ☁️ Azure Event Hubs Setup

Azure Event Hubs is a big data streaming platform designed to ingest and process millions of events per second.

### Key Concepts

- **Event Producers**: Entities sending data to Event Hubs
- **Throughput Units**: Capacity measurement for ingress/egress
  - 1 Unit = Up to 1 MB/s or 1,000 events/second ingress
  - 1 Unit = Up to 2 MB/s or 4,096 events/second egress
- **Partitions**: Segments for parallel processing
- **Consumer Groups**: Enable multiple applications to process streams independently

### Creating an Event Hub

1. Search for "Event Hubs" in the Azure portal
2. Click **Create**
3. Select your resource group
4. Name your namespace (e.g., `eh-python-namespace-demo`)
5. Select a location close to your Databricks workspace
6. Choose **Basic** tier for demonstration purposes
   - Note: Basic tier allows only one consumer group and one day message retention
7. Set throughput units to 1 for the demo
8. Review and create

### Post Deployment

1. Navigate to your new Event Hubs namespace
2. Create an Event Hub instance
   - Name it (e.g., `eh-demo`)
   - Set partitions (2-32 on basic tier)
   - Set retention time (up to 24 hours on basic tier)

### Testing with Sample Data

Use the Generate Data Preview feature to send test data:

```json
{
    "temperature": 20,
    "humidity": 60,
    "location": "Seattle"
}
```

## 🛠️ Databricks Setup

### Create a Compute Cluster

1. In your Databricks workspace, create an all-purpose compute cluster:
   - Policy: Unrestricted
   - Cluster Mode: Single Node
   - Access Mode: Single User
   - Databricks Runtime: 12.2 LTS or later
   - Node Type: Standard_DS3_v2 (or similar)
   - Auto Termination: 10 minutes
   - Ensure Unity Catalog support is enabled

### Install Event Hubs Connector

1. Go to **Compute** and select your cluster
2. Navigate to **Libraries**
3. Click **Install New** and select **Maven**
4. Search for `eventhubs-spark`
5. Choose Azure Event Hubs Spark 2.12 (matching your Databricks runtime)
6. Select the latest release (e.g., 2.3.22)
7. Click **Install**

## 🏅 Implementing the Medallion Architecture

The Medallion architecture organizes data into three progressive layers:

### Bronze Layer (Raw Data)

- Raw, unprocessed data landing zone
- Preserves original data format
- Serves as a historical archive

### Silver Layer (Processed Data)

- Cleaned and validated data
- Processed into a more consumable format
- Business rules applied

### Gold Layer (Refined Data)

- Aggregated for specific business use cases
- Optimized for reporting and analytics
- Powers dashboards and visualizations

## ⚙️ Streaming Data Processing

### Importing Required Libraries

```python
from pyspark.sql import functions as F
from pyspark.sql import types
```

### Configuring Event Hubs Connection

```python
config = {
    "eventhubs.connectionString": encrypted_connection_string,
    "eventhubs.eventHubName": event_hub_name
}
```

To get a connection string:
1. In Event Hubs, go to **Shared Access Policies**
2. Create a policy with "Listen" permissions
3. Copy the Connection string-primary key

### Reading the Stream from Event Hubs

```python
df = spark.readStream \
    .format("eventhubs") \
    .options(**config) \
    .load()
```

### Writing to Bronze Layer

```python
bronze_checkpoint = "/mnt/streaming/bronze/weather/checkpoint"

(df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", bronze_checkpoint)
    .toTable("streaming.bronze.weather"))
```

### Processing Data into Silver Layer

```python
# Read from bronze table
bronze_df = spark.readStream.table("streaming.bronze.weather")

# Process the data
silver_df = bronze_df \
    .withColumn("body", bronze_df["body"].cast("string")) \
    .withColumn("body", F.from_json("body", schema)) \
    .select(
        F.col("body.temperature").alias("temperature"),
        F.col("body.humidity").alias("humidity"),
        F.col("body.wind_speed").alias("wind_speed"),
        F.col("body.precipitation").alias("precipitation"),
        F.col("body.conditions").alias("conditions"),
        F.col("body.wind_direction").alias("wind_direction"),
        F.col("enqueueTime").alias("timestamp")
    )

# Write to silver layer
silver_checkpoint = "/mnt/streaming/silver/weather/checkpoint"

(silver_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", silver_checkpoint)
    .toTable("streaming.silver.weather"))
```

### Creating Gold Layer Aggregations

```python
# Read from silver table
silver_df = spark.readStream.table("streaming.silver.weather")

# Create windowed aggregations
gold_df = silver_df \
    .withWatermark("timestamp", "5 minutes") \
    .groupBy(F.window("timestamp", "5 minutes")) \
    .agg(
        F.avg("temperature").alias("temperature"),
        F.avg("humidity").alias("humidity"),
        F.avg("wind_speed").alias("wind_speed"),
        F.avg("precipitation").alias("precipitation"),
        F.first("conditions").alias("conditions"),
        F.first("wind_direction").alias("wind_direction")
    ) \
    .withColumn("start", F.col("window.start")) \
    .withColumn("end", F.col("window.end")) \
    .drop("window")

# Write to gold layer
gold_checkpoint = "/mnt/streaming/gold/weather_summary/checkpoint"

(gold_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", gold_checkpoint)
    .toTable("streaming.gold.weather_summary"))
```

## 📊 Power BI Integration

Connect Power BI to your Databricks for near real-time reporting:

1. In Databricks, navigate to **Partner Connect** and select **Power BI**
2. Choose your compute cluster
3. Download the connection file
4. Open the file in Power BI Desktop
5. Sign in with your Azure credentials
6. Select the streaming catalog with bronze, silver, and gold layers
7. Choose your tables (prefer gold layer for reporting)
8. Select **Direct Query** mode for near real-time data

### Creating Visualizations

1. Create visualizations based on your gold layer tables
2. New events flowing through the pipeline will be reflected in Power BI
3. Direct Query visuals refresh every 15 minutes or can be manually refreshed

## ⚠️ Important Warnings

- Spark Structured Streaming will run indefinitely until manually stopped
- **Always terminate your streams** by clicking interrupt when done
- **Manually shut down your cluster** to avoid unexpected costs
- If using Direct Query in Power BI, the Databricks cluster must be running

## 🧹 Clean Up Procedure

1. Stop all streams by interrupting the notebook
2. Shut down your Databricks cluster
3. Consider switching Power BI reports from Direct Query to Import mode if not needing real-time updates 