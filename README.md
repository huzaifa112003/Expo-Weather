# Expo Weather
 
# Weather Forecast Application


## Key Features

- **Real-time weather updates**
- **5-day weather forecasting**
- **Aggregated weather data using an exponential tree**
- **User-friendly graphical interface**

## System Components

### Frontend
- **GUI built with Tkinter**: A simple and easy-to-use interface for interacting with the weather application.

### Backend
- **Data management using the ExTree data structure**: Efficient storage and retrieval of weather data.

### API Integration
- **Real-time data fetched from OpenWeather API**: Accurate and up-to-date weather information.


## Technologies Used

- **Python**: For backend logic.
- **Tkinter**: For the frontend GUI.

## App Features

### Forecast Information
Given the name of any city in the world, our app can output the following information:

- **Forecast for the next 5 days**
  - Average Temperature
  - Average Humidity
  - Total Precipitation
  - Average Pressure
  - Average Wind Speed

### Current Weather
- Temperature
- Humidity
- Precipitation
- Pressure
- Wind Speed

## Trees in Our App

### Key Functions and Their Roles

#### Insertion
When new forecast data is obtained from the API, it is processed and inserted into the tree.

- **Process**: Each piece of forecast data is inserted according to the date. The tree organizes itself by dates, ensuring all nodes are sorted chronologically. If a node with the given date already exists, it updates the existing node's data.

#### Aggregation
Data retrieval function used to fetch aggregated weather data over a specific range of dates.

- **Process**: The function traverses the tree, including only those nodes that fall within the specified date range. As it traverses, it aggregates the data from each node that meets the criteria.
- **Utilization**: This capability is particularly useful for providing summaries of weather conditions over several days, such as average temperature, total precipitation, etc.

#### Data Display
Formatted and displayed in the application's forecast area.

### Structure and Purpose

Each node in the ExTree corresponds to a single day's weather data, encapsulated in an ExTreeNode. This node holds not just the weather data for that particular day, but also aggregates from its child nodes.

- **Weather data for each day** includes temperature, humidity, pressure, wind speed, and precipitation. This data is stored in each node when new forecast data is inserted into the tree.

## Acknowledgements

- **OpenWeather API**: For providing real-time weather data.
