# Weather Monitoring System

A real-time weather monitoring system that collects and visualizes weather data for multiple cities. This project uses the OpenWeatherMap API to fetch weather data and provides temperature alerts when certain conditions are met.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)


## Features
- Fetches weather data (temperature, feels-like, weather condition) from the OpenWeatherMap API.
- Monitors weather for multiple cities (e.g., Delhi, Mumbai, Chennai, etc.).
- Alerts when temperatures exceed a specified threshold.
- Real-time temperature trends visualization using matplotlib.
- Data logging and summary storage in SQLite database.


## Prerequisites
- Python 3.10 or above
- OpenWeatherMap API Key (sign up at [OpenWeatherMap](https://openweathermap.org/api) to get an API key)


## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Shivansh9580/weather-monitoring-system.git
    cd weather-monitoring-system
    ```

2. **Set up a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Add OpenWeatherMap API Key**:
   Open `weather_system.py` and add your API key where indicated:
   ```python
   API_KEY = 'your_api_key_here'

   
## Usage
Run the System: Execute the following command to start monitoring:

```bash
python weather_system.py
```

Batch Script: Alternatively, run the project using the batch file for setup, activation, and execution:

On Windows:
```bash
build.bat
```


## Check Alerts and Visuals:
The console will display alerts for high temperatures.<br>
A real-time plot of temperature trends will open, displaying data for each monitored city.



## Project Structure
weather-monitoring-system/
├── venv/                    # Virtual environment (not included in Git)
├── weather_system.py        # Main script for weather monitoring
├── requirements.txt         # Dependencies list
├── build.bat                # Batch script for setup and run
└── README.md                # Project documentation


## License
This project is licensed under the MIT License. See the LICENSE file for details.


## Happy Monitoring! 🌦️


### Additional Steps
**API Key Reminder**: users to insert their OpenWeatherMap API key in `weather_system.py`. 

This `README.md` should give users clear guidance on setting up and running the project on GitHub!
