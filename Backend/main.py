from flask import Flask, request
from TurpleMap import  Map 





app = Flask(__name__)

# Need to get user laitude and longitude
# Display the nearest parking areas 
    
@app.route('/parking', methods=['GET'])
def parking():
    if request.method == 'GET':
        # Extracting parameters from the URL query string
        latitude = request.args.get('latitude')  # Assuming 'param1' is a parameter in the GET request
        longitude = request.args.get('longitude')  # Assuming 'param2' is a parameter in the GET request



        district = Map.get_district(latitude, longitude)
        distance = Map.distance((13.044593459543153, 80.17366717996211),(latitude,longitude))
        return f"Distance is {distance}km"
    else:
        return "Only GET requests are allowed."

if __name__ == '__main__':
    app.run(debug=True)
