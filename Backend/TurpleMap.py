import requests

class Map:

    def distance(origin, destination):
        url = "http://router.project-osrm.org/route/v1/driving/{},{};{},{}?overview=full".format(origin[1], origin[0], destination[1], destination[0])
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'routes' in data and len(data['routes']) > 0:
            distance = data['routes'][0]['distance'] / 1000  # Convert distance to kilometers
            return distance
        else:
            print("Error calculating shortest route distance")
            return None

   

    def get_district(latitude, longitude):
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