#User Class to make easier to work with pillow magic and face detect

class UserFace:
    def __init__(self, user_id = '', mood = {}, coordinates= {}):
            self.id = user_id
            self.mood = mood
            self.face_coordinates = coordinates

    def set_mood(self, mood):
        if isinstance(mood, dict):
            self.mood = mood

    def set_face_coordinates(self, coordinates):
        if isinstance(coordinates, dict):
            self.face_coordinates = coordinates

    def set_id(self, user_id):
        if isinstance(user_id, str):
            self.id = user_id

    def parse_user_info(self, info_list):
        if isinstance(info_list, list):
            self.set_id(info_list[0].get('faceId'))
            self.set_mood(info_list[0].get('faceAttributes').get('emotion'))

            useful_coordinates = {}
            useful_coordinates['noseTop'] = info_list[0].get('faceLandmarks').get('noseRightAlarOutTip')
            useful_coordinates['leftBrow'] = info_list[0].get('faceLandmarks').get('eyebrowLeftOuter')
            useful_coordinates['rightBrow'] = info_list[0].get('faceLandmarks').get('eyebrowRightOuter')
            useful_coordinates['noseRoot'] = info_list[0].get('faceLandmarks').get('noseRootLeft')
            useful_coordinates['mouthLeft'] = info_list[0].get('faceLandmarks').get('mouthLeft')
            useful_coordinates['mouthRight'] = info_list[0].get('faceLandmarks').get('mouthRight')
            useful_coordinates['noseLeftBottom'] = info_list[0].get('faceLandmarks').get('noseLeftAlarOutTip')
            useful_coordinates['noseRightBottom'] = info_list[0].get('faceLandmarks').get('noseRightAlarOutTip')
            useful_coordinates['lipTop'] = info_list[0].get('faceLandmarks').get('upperLipTop')
            useful_coordinates['faceAngle'] = info_list[0].get('faceAttributes').get('headPose')

            self.set_face_coordinates(useful_coordinates)






