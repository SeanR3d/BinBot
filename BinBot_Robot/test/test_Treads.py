# import json
# import unittest
# from src.interfaces import Treads
#
# forward = {"angle": 0,
#            "distance": 1.0
#            }
#
# backward = {"angle": 180,
#             "distance": 1.0
#             }
#
# left = {"angle": 270,
#         "distance": 1.0
#         }
#
# right = {"angle": 90,
#          "distance": 1.0
#          }
#
# # instructions = dict(treads=[forward, backward, left, right])
#
# instructions = dict(treads=[forward])
#
# # converts python data structure to JSON string
# json_str = json.dumps(instructions)
#
# # converts JSON string into python data structure
# json_obj = json.loads(json_str)
#
#
# class TestInstruction(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_execute(self):
#         try:
#             Treads.setup()
#             Treads.execute(instructions)
#             Treads.destroy()
#         except Exception as e:
#             print("Tread exception: %s", e)
#             Treads.destroy()
#
#
# if __name__ == '__main__':
#     unittest.main()
