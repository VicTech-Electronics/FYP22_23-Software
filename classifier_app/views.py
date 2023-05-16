from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AccidentIndicator
from geopy.distance import geodesic
from rest_framework import status
from main_app.models import *
# import numpy as np

# Create your views here.
@api_view(['GET'])
def classify(request, vehicle_id):
    # Get Data from accident Indicator model and extract them for Accident detection
    indicators = AccidentIndicator.objects.get(vehicle = vehicle_id)
    # data = np.array([
    #     indicators.flame, 
    #     indicators.smoke, 
    #     indicators.vibration,
    #     indicators.gyroscope,
    #     indicators.brake
    # ])
    # weight = np.array([2.0, 2.3, 2.8, 0.4, 5.0]) # Weight obtained from the model wil come here

    # Accident detection calculations
    # weighted_sum = np.matmul(data, weight)
    # sigmoid =  1 / (1 + np.exp(-weighted_sum))
    # accident = np.round(sigmoid)

    # If No accident detected, Clear the indicator and stop there
    if accident == 0:
        indicators.delete()
        return Response('Not detected')

    # Variable to store data for Accident Information after being detected
    distances = []
    hospital_locations = []
    accident_point = (
        indicators.latitude, 
        indicators.longitude
    )

    # Calculation of Distance from all hospital location to the accident seen
    hospitals = Hospital.objects.all()
    for hospital in hospitals:
        hospital_point = (
            hospital.latitude, 
            hospital.longitude
        )
        distance = geodesic(accident_point, hospital_point).km
        
        distances.append(distance)
        hospital_locations.append(hospital_point)
    
    # Extract data obtained from the calculation above
    short_distance = min(distances)
    index = distances.index(short_distance)
    hospital_location = hospital_locations[index]
    
    # Data for accident infomation
    vehicle = Vehicle.objects.get(pk = vehicle_id)
    target_hospital = Hospital.objects.get(
        latitude = hospital_location[0],
        longitude = hospital_location[1]
    )

    # Create accident infomation 
    accident = Accident.objects.create(
        vehicle = vehicle,
        hospital = target_hospital,
        # confidence = sigmoid * 100.0,
        latitude = indicators.latitude,
        longitude = indicators.longitude,
    )
    accident.save()
    indicators.delete() # Delete accident Indicator after being used
    return Response('Detected')
