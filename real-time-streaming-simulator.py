from azure.eventhub import EventHubProducerClient, EventData
import random
import time
import json
import os

# Use environment variables for connection string and event hub name
# You can set these using:
# PowerShell: $env:EVENT_HUB_CONNECTION_STRING="your-connection-string"
#             $env:EVENT_HUB_NAME="your-event-hub-name"
# CMD: set EVENT_HUB_CONNECTION_STRING=your-connection-string
#      set EVENT_HUB_NAME=your-event-hub-name
CONNECTION_STR = os.environ.get('EVENT_HUB_CONNECTION_STRING')
EVENTHUB_NAME = os.environ.get('EVENT_HUB_NAME', 'eh-streaming')

if not CONNECTION_STR:
    raise ValueError("EVENT_HUB_CONNECTION_STRING environment variable is not set")

# Create a producer client to send messages to the event hub
producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)

def generate_weather_data():
    """Simulate fake weather data."""
    data = {
        "temperature": round(random.uniform(15.0, 30.0), 2), # Simulate temperature between 15°C and 30°C
        "humidity": random.randint(40, 80), # Simulate humidity between 40% and 80%
        "windSpeed": random.randint(5, 25), # Simulate wind speed between 5 and 25 km/h
        "windDirection": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]), # Random wind direction
        "precipitation": round(random.uniform(0.0, 5.0), 1), # Simulate precipitation between 0 and 5 mm
        "conditions": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy"]) # Random weather conditions
    }
    return data

try:
    # Continuously generate and send fake weather data
    while True:
        # Create a batch.
        event_data_batch = producer.create_batch()

        # Generate fake weather data
        weather_data = generate_weather_data()

        # Format the message as JSON
        message = json.dumps(weather_data)

        # Add the JSON-formatted message to the batch
        event_data_batch.add(EventData(message))

        # Send the batch of events to the event hub
        producer.send_batch(event_data_batch)

        print(f"Sent: {message}")

        # Wait for a bit before sending the next reading
        time.sleep(10)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    print("Stopped by the user")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the producer
    producer.close()