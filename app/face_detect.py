""" This module provides basic functionality of AZURE FACE RECOGN. SERVICE
    You should import specific functions in form : from app.face_detect import <name_of_the_function>
"""

import requests
from io import BytesIO

import cognitive_face as CF


# Microsoft AZURE SERVICE KEY
# You can CHANGE it for your own
KEY = '9e1f7501341b45409b1347ec81dc28d3'

CF.Key.set(KEY)  # Now we work with this key

# Now we are going to set our BASE URL
# Check it for your own region
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)


def detect_face(img_url, landmarks = False, mouth = False):
    """
    Detect ONE face in the <img_url> image

    :param img_url:
    :return:
    """
    global CF
    if landmarks == False :
        face = CF.face.detect(img_url, landmarks = False)
        if len(face) > 2:
            return False
        return face[0].get('faceId')
    if landmarks == True and mouth == True :
        face = CF.face.detect(img_url, landmarks=True, attributes = "headPose,emotion")
        if len(face) > 2:
            return False
        print(face)
        # mouth_coordinates = {}
        # mouth_coordinates['noseTop'] = face[0].get('faceLandmarks').get('noseRightAlarOutTip')
        # mouth_coordinates['leftBrow'] = face[0].get('faceLandmarks').get('eyebrowLeftOuter')
        # mouth_coordinates['rightBrow'] = face[0].get('faceLandmarks').get('eyebrowRightOuter')
        # mouth_coordinates['noseRoot'] = face[0].get('faceLandmarks').get('noseRootLeft')
        # mouth_coordinates['mouthLeft'] = face[0].get('faceLandmarks').get('mouthLeft')
        # mouth_coordinates['mouthRight'] = (face[0].get('faceLandmarks').get('mouthRight'))
        # mouth_coordinates['noseBottom'] = (face[0].get('faceLandmarks').get('noseLeftAlarOutTip'))
        # mouth_coordinates['lipTop'] = (face[0].get('faceLandmarks').get('upperLipTop'))
        return face#mouth_coordinates







def verify_faces(first_id, second_id):
    """
    Check if <first_id> and <second_id> faces belong to one man.
    This function uses id from detect_face function. Use it before this
    :param first_id:
    :param second_id:
    :return:
    """
    global CF
    result = CF.face.verify(first_id, second_id)
    if result.get('isIdentical') == True:
        return True
    else:
        return False
