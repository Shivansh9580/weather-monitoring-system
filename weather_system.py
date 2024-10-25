import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import requests
import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# --- Step 1: API Setup ---
API_KEY = '20bcb2c422ac34c565897473a0cdcb07'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# --- Step 2: Database Setup ---
Base = declarative_base()


class WeatherSummary(Base):
    __tablename__ = 'weather_summary'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    date = Column(String)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_weather = Column(String)


engine = create_engine('sqlite:///weather.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# --- Step 3: Fetch Weather Data ---
def fetch_weather(city):
    url = f'{BASE_URL}?q={city}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        main = data['weather'][0]['main']
        temp_kelvin = data['main']['temp']
        temp_celsius = temp_kelvin - 273.15  # Convert from Kelvin to Celsius
        feels_like = data['main']['feels_like'] - 273.15  # Convert feels_like

        return {
            'city': city,
            'temp': temp_celsius,
            'feels_like': feels_like,
            'weather': main,
            'timestamp': data['dt']  # Unix timestamp
        }
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Error occurred: {err}")
        return None


# --- Step 4: Data Processing ---
def process_daily_summary(city, weather_data):
    df = pd.DataFrame(weather_data)

    avg_temp = df['temp'].mean()
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()
    dominant_weather = df['weather'].mode()[0]  # Most frequent weather condition

    # Save summary to database
    summary = WeatherSummary(
        city=city,
        date=pd.Timestamp.now().strftime('%Y-%m-%d'),
        avg_temp=avg_temp,
        max_temp=max_temp,
        min_temp=min_temp,
        dominant_weather=dominant_weather
    )
    session.add(summary)
    session.commit()

    return avg_temp, max_temp, min_temp, dominant_weather


# --- Step 5: Alerting Mechanism ---
THRESHOLD_TEMP = 35  # Celsius
CONSECUTIVE_ALERTS_THRESHOLD = 2
consecutive_alerts = {city: 0 for city in CITIES}  # Track alerts per city


def check_alert(city, temp):
    global consecutive_alerts
    if temp > THRESHOLD_TEMP:
        consecutive_alerts[city] += 1
        if consecutive_alerts[city] >= CONSECUTIVE_ALERTS_THRESHOLD:
            print(f"ALERT for {city}: Temperature exceeded {THRESHOLD_TEMP}°C for two consecutive updates!")
    else:
        consecutive_alerts[city] = 0


# --- Step 6: Visualization ---
def visualize_trends(collected_data):
    fig, ax = plt.subplots(figsize=(10, 6))  # Create the figure and axis once
    lines = {city: ax.plot([], [], label=f'{city} Temp (°C)')[0] for city in collected_data.keys()}  # Create lines for each city

    def init():
        ax.set_title('Temperature Trends for Cities')
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature (°C)')
        ax.legend()
        return lines.values()

    def update(frame):
        for city, weather_data in collected_data.items():
            if len(weather_data) > 0:
                df = pd.DataFrame(weather_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df.set_index('timestamp', inplace=True)

                print(f"Plotting data for {city}: Time = {df.index}, Temperature = {df['temp']}")

                if len(df) > 1:
                    # Plot line if there are multiple data points
                    lines[city].set_data(df.index, df['temp'])
                else:
                    # Plot scatter point if there's only one data point
                    ax.scatter(df.index, df['temp'], label=f'{city} Temp (°C)')

        ax.relim()  # Recompute the limits
        ax.autoscale_view()  # Autoscale to fit the new data

        # Format the x-axis as datetime
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        fig.autofmt_xdate()

        return lines.values()

    ani = FuncAnimation(fig, update, init_func=init, blit=False, interval=10000)  # Update every 10 seconds
    plt.show()

# --- Main Function ---
def main():
    collected_data = {city: [] for city in CITIES}  # Store data for each city

    while True:
        for city in CITIES:
            print(f"Retrieving data for {city}...")

            # Fetch and display data instantly
            weather = fetch_weather(city)
            if weather:
                collected_data[city].append(weather)

                # Display current weather data immediately
                print(f"\nCurrent Weather for {city}:")
                print(f"Temperature: {weather['temp']:.2f}°C, Feels Like: {weather['feels_like']:.2f}°C, "
                      f"Condition: {weather['weather']}")

                # Check alert thresholds and display alert if needed
                check_alert(city, weather['temp'])

        # Call visualization after data is collected
        visualize_trends(collected_data)

        # Wait for 5 minutes before the next update
        print("\n--- Waiting for 5 minutes before the next update ---\n")
        time.sleep(300)

# --- Start the system ---
if __name__ == '__main__':
    main()