import requests
from math import radians, sin, cos, sqrt, atan2
import mysql.connector 

class Map:

    def __init__(self):
        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="TurpleLine"
        )
        self.cursor = self.conn.cursor()

    def parking_data(self,district):
            # Creating a cursor object
           
            # Fetching data
            self.cursor.execute(f"SELECT * FROM `parking` WHERE `district` = '{district}' ")
          
            # Fetch all rows    
            parking_data = self.cursor.fetchall()
            
            # Printing fetched data
            return parking_data

    def haversine_distance(self,origin, destination):
        # Convert latitude and longitude from degrees to radians
        lat1 = radians(origin[0])
        lon1 = radians(origin[1])
        lat2 = radians(destination[0])
        lon2 = radians(destination[1])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        # Radius of the Earth in kilometers
        R = 6371.0
        distance = R * c

        return distance

    def get_distance(self,origin, destination):
        url = "http://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=full".format(origin[1], origin[0], destination[1], destination[0])
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'routes' in data and len(data['routes']) > 0:
            distance = data['routes'][0]['distance'] / 1000  # Convert distance to kilometers
            return distance
        else:
            print("Error calculating shortest route distance")
            return None

    def get_district(self,latitude, longitude):
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
        response = requests.get(url)
        data = response.json()
        if 'address' in data:
            # Extract the district from the address components
            if 'city_district' in data['address']:
                return data['address']['city_district']
            elif 'county' in data['address']:
                return data['address']['county']
            elif 'state_district' in data['address']:
                return data['address']['state_district']
        return "District not found"
    
    def route(self,origin,destination):
        self.cursor.execute(f"SELECT `vid` FROM `routes` WHERE `place` = '{destination}' ")
        return self.cursor.fetchall()