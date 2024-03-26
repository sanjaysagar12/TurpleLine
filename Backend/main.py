from flask import Flask, request
from TurpleMap import  Map 
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
TurpleMap = Map()
# Need to get user laitude and longitude
# Display the nearest parking areas 
 
@app.route('/parking', methods=['GET'])
def parking():
    if request.method == 'GET':
        # Extracting parameters from the URL query string
        origin_latitude = request.args.get('origin_latitude')  # Assuming 'param1' is a parameter in the GET request
        origin_longitude = request.args.get('origin_longitude')  # Assuming 'param2' is a parameter in the GET request
        parking_area = dict()


        
        # origin_latitude = 13.037377
        # origin_longitude = 80.212282
        district = TurpleMap.get_district(13.037377,80.212282)
        print(district)
        parking_area = {}

        for i in TurpleMap.parking_data(district):
            
            destination_latitude = i[2]
            destination_longitude = i[3]
            # haversine_distance = TurpleMap.haversine_distance((origin_latitude,origin_longitude),(destination_latitude,destination_longitude))
            
            parking_area.update({i[1]:[i[2],i[3],TurpleMap.get_distance((origin_latitude,origin_longitude),(destination_latitude,destination_longitude))]})
        parking_area = json.dumps(parking_area,ensure_ascii=False)

        return parking_area
    else:
        return "Only GET requests are allowed."

@app.route('/transportation', methods=['GET'])
def transportation():
    if request.method == 'GET':
        # Extracting parameters from the URL query string
        origin = request.args.get('origin')  # Assuming 'param1' is a parameter in the GET request
        destination = request.args.get('destination')  # Assuming 'param2' is a parameter in the GET request
        route = TurpleMap.route(origin,destination)
        return json.dumps(route)
    else:
        return "Only GET requests are allowed."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)