# from unittest import TestCase
#
# from src.instructions.instruction import Instruction
#
# JSON_STRING = '{"status":"PATROL","img":"temporary","treads":[{"angle":0.0,"distance":1.1}],"arms":[{"angle":2.2}]}'
# STATUS = 'PATROL'
# IMG = 'temporary'
# TREADS = [{"angle": 0.0, "distance": 1.1}]
# ARMS = [{"angle": 2.2}]
#
# json_obj = Instruction(JSON_STRING)
# data_obj = Instruction(STATUS, IMG, TREADS, ARMS)
#
#
# class TestInstruction(TestCase):
#
#     def test_json(self):
#         self.assertEqual(JSON_STRING, json_obj.json())
#         self.assertEqual(JSON_STRING, data_obj.json())
#
#     def test_status(self):
#         self.assertEqual(STATUS, json_obj.status())
#         self.assertEqual(STATUS, data_obj.status())
#
#     def test_img(self):
#         self.assertEqual(IMG, json_obj.img())
#         self.assertEqual(IMG, data_obj.img())
#
#     def test_treads(self):
#         self.assertEqual(TREADS, json_obj.treads())
#         self.assertEqual(TREADS, data_obj.treads())
#
#     def test_arms(self):
#         self.assertEqual(ARMS, json_obj.arms())
#         self.assertEqual(ARMS, data_obj.arms())
