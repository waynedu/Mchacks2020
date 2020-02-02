import base64
import pdb
import traceback

import requests
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator

from .models import Person
from .settings import API_BASE_URL, APP_ID, APP_KEY, BASE_DIR
from .get_geolocation import get_geolocation

session_image = None

class LandingPageView(TemplateView):
    template_name = 'landing_page.html'

    def post(self, request):
        global session_image
        image = request.POST.get('raw_data')
        if detect_faces(image):
            detected_users = recognize_user(image)
            if len(detected_users) > 0:
                highest_confidence_user = None
                for candidate in detected_users:
                    confidence = candidate["confidence"]
                    if confidence > 0.6:
                        if highest_confidence_user and confidence > highest_confidence_user["confidence"]:
                            highest_confidence_user = candidate
                        elif not highest_confidence_user:
                            highest_confidence_user = candidate

                if not highest_confidence_user:

                    session_image = image
                    return HttpResponse(status=200, content="redirect")
                else:
                    return HttpResponse(status=200, content=Person.objects.filter(subject_id=highest_confidence_user['subject_id']).first().id)
            else:
                session_image = image
                return HttpResponse(status=500, content="redirect")
        else:
            return HttpResponse(status=500, content="not_recognized")


class HomeDashboardView(TemplateView):
    template_name = 'home_dashboard.html'


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationPageView(TemplateView):
    template_name = 'registration_page.html'

    @csrf_exempt
    def post(self, request):
        response = request.POST
        subject_id = ''.join(response['dob'].split('/')[::-1]) + response['lname'].upper()

        location = get_geolocation()
        location = "{city}, {country_name} [{latitude}, {longitude}]".format(city=location['city'],
                                                                             country_name=location['country_name'],
                                                                             latitude=location['latitude'],
                                                                             longitude=location['longitude'])
        person = Person(first_name=response['fname'],
                        last_name=response['lname'],
                        sex=response['sex'],
                        dob=response['dob'],
                        phone_number=response['ph'],
                        address=response['address'],
                        email_address=response['email_address'],
                        last_known_location=location,
                        subject_id=subject_id)

        person.save()

        global session_image
        enroll_user(session_image, subject_id)

        session_image = None

        return HttpResponse(status=200, content=person.id)


gallery_name = "Refugees"


@csrf_exempt
def enroll_user(img_encoded, subject_id):  # return T or F for whether it's enrolled properly
    values = {
        "subject_id": subject_id,  # The subject if follows the expression: YYYYMMDDLastname
        "gallery_name": gallery_name,  # Default Gallery Name
        'image': img_encoded  # The img_encoded is encoded in base64
    }

    headers = {
        'Content-Type': 'application/json',
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    r = requests.post(API_BASE_URL + 'enroll', json=values, headers=headers)
    print(r.url, values)
    # TODO:
    # Save user in the DB
    print(r.text)
    json_data = json.loads(r.text)
    print(json_data)
    # return HttpResponse("User Enrolled!")
    enrolled = True
    try:
        if json_data['images'][0]['transaction']['status'] == 'success' and json_data['images'][0]['transaction'][
            'confidence'] > 0.6:
            print('User enrolled')
            return enrolled
        else:
            print('User not enrolled')
            return not enrolled
    except:
        traceback.print_exc()
        if json_data['Errors'][0]['ErrCode'] == '5002':  # no faces found in the image
            print(str(json_data['Errors'][0]['Message']))
            return not enrolled
        elif json_data['Errors'][0]['ErrCode'] == '5010':  # too many faces in image
            print(str(json_data['Errors'][0]['Message']))
            return not enrolled
        else:
            print('Other error')
            return not enrolled


@csrf_exempt
def detect_faces(img_encoded):  # return T or F
    values = {
        'image': img_encoded
    }

    headers = {
        'Content-Type': 'application/json',
        'app_id': APP_ID,
        'app_key': APP_KEY
    }
    r = requests.post(API_BASE_URL + 'detect', json=values, headers=headers)
    json_data = json.loads(r.text)
    print(json_data)
    detected = True
    try:
        if json_data['images'][0]['faces']:
            print('Face detected')
            return detected
        else:
            print('Face not detected')
            return not detected
    except:
        if json_data['Errors'][0]['ErrCode'] == '5002':  # no faces found in the image
            print(str(json_data['Errors'][0]['Message']))
            return not detected
        else:
            print('Other error')
            return not detected


@csrf_exempt
def recognize_user(img_decoded):  # return list of candidates
    values = {
        "gallery_name": gallery_name,
        'image': img_decoded
    }

    headers = {
        'Content-Type': 'application/json',
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    r = requests.post(API_BASE_URL + 'recognize', json=values, headers=headers)

    # print (r.text)
    json_data = json.loads(r.text)
    print(json_data)

    try:
        if json_data['images'][0]['transaction']['status'] == 'success' and json_data['images'][0]['transaction'][
            'confidence'] > 0.6:
            print('User recognized')
            return json_data['images'][0]['candidates']
        else:
            print('User not recognized')
            return []
    except:
        if json_data['Errors'][0]['ErrCode'] == '5004':  # gallery name not found
            print(str(json_data['Errors'][0]['Message']))
            return []
        elif json_data['Errors'][0]['ErrCode'] == '5002':  # no faces found in the image
            print(str(json_data['Errors'][0]['Message']))
            return []
        else:
            print('Other error')
            return []


@csrf_exempt
def verify_user(img_encoded, subject_id):
    values = {
        "subject_id": subject_id,
        "gallery_name": gallery_name,
        'image': img_encoded
    }

    headers = {
        'Content-Type': 'application/json',
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    r = requests.post(API_BASE_URL + 'verify', json=values, headers=headers)

    # print (r.text)
    json_data = json.loads(r.text)
    print(json_data)

    try:
        if json_data['images'][0]['transaction']['status'] == 'success' and json_data['images'][0]['transaction'][
            'confidence'] > 0.6:
            return HttpResponse("User Verified!")
        else:
            return HttpResponse("User Not Verified!")
    except:
        if json_data['Errors'][0]['ErrCode'] == '5004':  # gallery name not found
            return HttpResponse(str(json_data['Errors'][0]['Message']))
        elif json_data['Errors'][0]['ErrCode'] == '5003':  # subject ID was not found
            return HttpResponse(str(json_data['Errors'][0]['Message']))
        elif json_data['Errors'][0]['ErrCode'] == '5002':  # no faces found in the image
            return HttpResponse(str(json_data['Errors'][0]['Message']))
        elif json_data['Errors'][0]['ErrCode'] == '5010':  # too many faces in image
            return HttpResponse(str(json_data['Errors'][0]['Message']))
        elif json_data['Errors'][0]['ErrCode'] == '5012':  # no match found
            return HttpResponse(str(json_data['Errors'][0]['Message']))
        else:
            return HttpResponse('Other error')
