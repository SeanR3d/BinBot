# Author: Sean DiGirolamo
# Date: 10/3/2019

import json


class Instruction:
    FROM_JSON = 1
    FROM_DATA = 2

    def __init__(self, constructor_type, status, img=None, treads=None, arms=None):
        if constructor_type == Instruction.FROM_JSON:
            obj = json.loads(status)
            self.__status = obj["status"]
            self.__img = obj["img"]
            self.__treads = obj["treads"]
            self.__arms = obj["arms"]
        else:
            self.__status = status
            self.__img = img
            self.__treads = treads
            self.__arms = arms

    def instructionToJson(self):
        obj = {"status": str(self.__status),
               "img": Instruction.__img_to_string(self.__img),
               # "treads": self.__treads,
               "treads": [{"angle": 0.0, "distance": self.__treads}],  # GSON FORMAT
               "arms": self.__arms,
               }
        return json.dumps(obj)

    def json_OLD(self):
        retval = '{"status":"'
        if self.__status is not None:
            retval += self.__status
        retval += '",'

        retval += '"img":"'
        if self.__img is not None:
            retval += Instruction.__img_to_string(self.__img)
        retval += '",'

        retval += '"treads":['
        if self.__treads is not None:
            for x in self.__treads:
                retval += '{"angle":' + str(x["angle"]) + ','
                retval += '"distance":' + str(x["distance"]) + '}'
                if x != self.__treads[-1]:
                    retval += ','
        retval += '],'

        retval += '"arms":['
        if self.__arms is not None:
            for x in self.__arms:
                retval += '{"angle":' + str(x["angle"]) + '}'
                if x != self.__arms[-1]:
                    retval += ','
        retval += ']}'

        return retval

    @staticmethod
    def __img_to_string(img):
        return img.decode("utf-8")

    def status(self):
        return self.__status

    def img(self):
        return self.__img

    def treads(self):
        return self.__treads

    def arms(self):
        return self.__arms
