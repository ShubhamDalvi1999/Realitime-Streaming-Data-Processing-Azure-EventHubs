# Real-Time Streaming Data Pipeline with Azure

![Azure Solution Architecture](https://github.com/user-attachments/assets/5d4b8122-9ae4-4a16-9894-8f8538724933)


## Project Overview

This project demonstrates an end-to-end solution for building a real-time data streaming pipeline using Azure services. It captures simulated weather data, processes it using Azure Databricks following the medallion architecture, stores it in Azure Data Lake Storage (Delta Lake format), and prepares it for visualization (e.g., in Power BI).

## Features

*   **Real-time Data Simulation**: Python script (`real-time-streaming-simulator.py`) generates fake weather data and sends it to Azure Event Hubs.
*   **Data Ingestion**: Azure Event Hubs captures the incoming streaming data.
*   **Stream Processing**: Azure Databricks (`Real-time Data Processing.ipynb`) processes the data in stages (Bronze, Silver, Gold) using Structured Streaming.
*   **Data Storage**: Processed data is stored efficiently in Azure Data Lake Storage Gen2 using the Delta Lake format, managed by Unity Catalog.
*   **Medallion Architecture**: Implements Bronze (raw), Silver (cleaned), and Gold (aggregated) tables for progressive data refinement.
*   **Scalability & Reliability**: Leverages Azure's managed services for robust and scalable stream handling.

## Repository Contents

*   `real-time-streaming-simulator.py`: Python script to simulate and send weather data streams to Event Hubs.
*   `Real-time Data Processing.ipynb`: Azure Databricks notebook containing PySpark code for processing data through Bronze, Silver, and Gold layers.
*   `Azure Solution Architecture.png`: Diagram illustrating the high-level architecture of the solution.
*   `README.md`: This file, providing an overview and instructions.

## Prerequisites

*   **Azure Subscription**: An active Azure account with permissions to create and manage resources.
*   **Azure Services**:
    *   Azure Event Hubs Namespace (Standard tier recommended) and an Event Hub instance.
    *   Azure Data Lake Storage Gen2 account.
    *   Azure Databricks Workspace (Premium tier recommended for Unity Catalog).
*   **Tools**:
    *   Python 3.x environment for running the simulator.
    *   Access to the Azure Portal or Azure CLI.
    *   (Optional) Power BI Desktop for visualization.
*   **Knowledge**:
    *   Basic understanding of Azure services (Event Hubs, ADLS, Databricks).
    *   Familiarity with Python and PySpark.
    *   Concepts of data streaming and the medallion architecture.

## Setup & Configuration

1.  **Azure Event Hubs**:
    *   Create an Event Hubs Namespace and an Event Hub within it.
    *   Obtain the **Connection string-primary key** for a Shared Access Policy with Send permissions for the Event Hub.
    *   Note the **Event Hub name**.

2.  **Azure Data Lake Storage (ADLS Gen2)**:
    *   Create an ADLS Gen2 storage account.
    *   Create a container (e.g., `streaming-data`).

3.  **Azure Databricks**:
    *   Create a Databricks Workspace. Enable Unity Catalog during setup or configure it later.
    *   Create a compute cluster (e.g., using `13.3 LTS` runtime or later).
    *   **Install Library**: On your cluster, install the necessary Maven library:
        *   Coordinates: `com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22` (Adjust version if needed based on your Databricks runtime).

4.  **Simulator (`real-time-streaming-simulator.py`)**:
    *   Set up environment variables for the Event Hub connection:
        *   **Windows PowerShell**:
            ```powershell
            $env:EVENT_HUB_CONNECTION_STRING="your-connection-string-here"
            $env:EVENT_HUB_NAME="your-event-hub-name"
            ```
        *   **Windows Command Prompt**:
            ```cmd
            set EVENT_HUB_CONNECTION_STRING=your-connection-string-here
            set EVENT_HUB_NAME=your-event-hub-name
            ```
        *   **Alternative**: Create a `.env` file (add to `.gitignore`!) and use a library like `python-dotenv` to load it.

5.  **Databricks Notebook (`Real-time Data Processing.ipynb`)**:
    *   Upload the `Real-time Data Processing.ipynb` notebook to your Databricks workspace.
    *   Open the notebook and update the following configuration variables:
        *   Event Hubs connection string (consider using Databricks Secrets).
        *   Event Hub name.
        *   Paths to your ADLS Gen2 storage location (e.g., `abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/bronze`).
        *   Checkpoint locations in ADLS Gen2.
        *   Unity Catalog details (Catalog, Schema names) if applicable.

## Running the Solution

1.  **Start the Simulator**:
    *   Navigate to the project directory in your terminal.
    *   Ensure the `azure-eventhub` Python library is installed: `pip install azure-eventhub`
    *   Set the environment variables for Event Hub (as described above).
    *   Run the simulator: `python real-time-streaming-simulator.py`
    *   The script will start sending simulated weather data to your Event Hub. You should see "Sent: {...}" messages printed. Press `Ctrl+C` to stop.

2.  **Run the Databricks Notebook**:
    *   Attach the `Real-time Data Processing.ipynb` notebook to your configured cluster.
    *   Run the notebook cells sequentially. This will:
        *   Read data from Event Hubs.
        *   Process and write data to the Bronze, Silver, and Gold tables in Delta Lake format within your ADLS Gen2 storage.

## Visualization (Optional)

*   Connect Power BI Desktop to your Azure Databricks Gold table(s) using the Databricks connector.
*   Use DirectQuery mode for near real-time reporting based on the processed data.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[Specify License, e.g., MIT License]
