# pip install requests
import requests
import sys
sys.path.append("../")
from config import API_TOKEN
from pprint import pprint

def detectLicensePlate(filename):
    regions = ['gb'] # Change to your country
    with open(filename, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': "Token " + API_TOKEN})

    #pprint(response.json())
    
    if response.json()["results"]:
        return response.json()["results"][0]["plate"]
    return None


if __name__=="__main__":
    lp = detectLicensePlate("../textDetection/test_images/no_carPlate.jpg")
