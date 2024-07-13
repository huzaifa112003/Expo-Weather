class ExTreeNode:
    def __init__(self, date, weather_info):
        self.date = date
        self.weather_info = weather_info
        self.left = None
        self.right = None
        self.aggregated_info = self.init_aggregated_info(weather_info)
        self.day_count = 1

    def init_aggregated_info(self, weather_info): #Initializes aggregated weather information from the given weather data
        return {
            'total_temp': weather_info['temp'],
            'total_humidity': weather_info['humidity'],
            'total_precipitation': weather_info.get('precipitation', 0),
            'total_pressure': weather_info['pressure'],
            'wind_speeds': [weather_info['wind_speed']],
        }

    def update_aggregates(self): # Updates the aggregated weather information by incorporating data from child nodes
        # Resets the aggregated data
        self.aggregated_info = self.init_aggregated_info(self.weather_info)
        self.day_count = 1

        # Update the aggregated info from child nodes
        for child in [self.left, self.right]:
            if child:
                # Aggregate data from children
                self.day_count += child.day_count
                for key in self.aggregated_info:
                    if key != 'wind_speeds':
                        self.aggregated_info[key] += child.aggregated_info[key]
                    else:
                        self.aggregated_info[key].extend(child.aggregated_info[key])

        print(f"Updated node at date {self.date} with aggregates: {self.aggregated_info} and day count: {self.day_count}")

class ExTree:
    def __init__(self):
        self.root = None

    def insert(self, date, weather_info): # recursive insertion process
        self.root = self._insert_rec(self.root, date, weather_info)

# Recursively finds the correct location to insert a new node or update an existing node in the tree based on the date
    def _insert_rec(self, node, date, weather_info): 
        if not node:
            print(f"Inserting new node for date: {date}")
            return ExTreeNode(date, weather_info)

        # Before updating the left or right node, print the current state
        print(f"At node with date: {node.date}, inserting data for date: {date}")

        if date < node.date:
            node.left = self._insert_rec(node.left, date, weather_info)
        elif date > node.date:
            node.right = self._insert_rec(node.right, date, weather_info)
        else:
            print(f"Updating existing node for date: {date}")
            node.weather_info = weather_info

        # Update aggregates after both left and right children have been considered
        node.update_aggregates()

        return node

# Recursively retrieves and aggregates data from nodes that fall within a specified date range.
    def _query_range_rec(self, node, start_date, end_date, aggregated_info):
        if node is None:
            return aggregated_info

        # Check if the current node is within the range and aggregate only once
        if start_date <= node.date <= end_date:
            print(f"Including node with date: {node.date} in aggregation.")
            aggregated_info['total_temp'] += node.weather_info['temp']
            aggregated_info['total_humidity'] += node.weather_info['humidity']
            aggregated_info['total_precipitation'] += node.weather_info.get('precipitation', 0)
            aggregated_info['total_pressure'] += node.weather_info['pressure']
            aggregated_info['wind_speeds'].append(node.weather_info['wind_speed'])
            aggregated_info['day_count'] += 1

        # Recur for left and right subtrees
        if start_date < node.date:
            aggregated_info = self._query_range_rec(node.left, start_date, end_date, aggregated_info)
        if node.date < end_date:
            aggregated_info = self._query_range_rec(node.right, start_date, end_date, aggregated_info)

        return aggregated_info
    
# Public method to start the recursive data retrieval process for a specified range.
    def query_range(self, start_date, end_date):
        initial_aggregated_info = {
            'total_temp': 0,
            'total_humidity': 0,
            'total_precipitation': 0,
            'total_pressure': 0,
            'wind_speeds': [],
            'day_count': 0
        }
        aggregated_info = self._query_range_rec(self.root, start_date, end_date, initial_aggregated_info)
        print(f"Final aggregated info: {aggregated_info}")
        return aggregated_info

# Computes average weather data over a specified date range.   
    def get_average_weather(self, start_date, end_date):
        aggregated_info = self.query_range(start_date, end_date)
        if aggregated_info['day_count'] > 0:
            average_weather = {
                'avg_temp': aggregated_info['total_temp'] / aggregated_info['day_count'],
                'avg_humidity': aggregated_info['total_humidity'] / aggregated_info['day_count'],
                'total_precipitation': aggregated_info['total_precipitation'],
                'avg_pressure': aggregated_info['total_pressure'] / aggregated_info['day_count'],
                'avg_wind_speed': sum(aggregated_info['wind_speeds']) / aggregated_info['day_count'],
            }
            print(f"Average weather calculated: {average_weather}")
            return average_weather
        else:
            print("No data available for the given range.")
            return None

