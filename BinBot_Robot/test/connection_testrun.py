from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction

IP = "127.0.0.1"
PORT = 7001

STATUS = "PATROL"
IMG = ""
TREADS = [{"angle": 0, "distance": 1}]
ARMS = [{"angle": 2}]

print("Connecting to server at " + IP + " " + str(PORT) + "...")
connection = Connection(IP, PORT)
print("Connection established!")

isend = Instruction(STATUS, IMG, TREADS, ARMS)

print("Attempting to send string " + isend.instructionToJson() + " to server...")
connection.send(isend.instructionToJson())
print("Successfully sent string to client!")

print("Attempting to receive string from server...")
rec = connection.receive()
print("recieved:")
print(rec)

irec = Instruction(rec)

print("Closing connection...")
print("Test was SUCCESSFUL!")