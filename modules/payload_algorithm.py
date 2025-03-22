# payload algorithm
from AutopilotDevelopment.General.Operations import initialize as initialize
from AutopilotDevelopment.Plane.Operations.waypoint import set_waypoint
import sys
import os

script_dir = os.path.abspath('./AutopilotDevelopment')
sys.path.append(script_dir)


object_detections = {"boat": ((20, 30, 40), "boat"), "tennis_racket": (
    (40, 50, 40), "tennis_racket")}
loop_mission = [((20, 40, 40), "loop"), ((50, 60, 40), "loop"), ((80, 80, 40), "loop"),
                ((60, 60, 40), "loop"), ((50, 40, 40), "loop")]

mission_itr = {"loop": loop_mission, "objects": object_detections}
vehicle_connection = initialize.connect_to_vehicle('udpin:127.0.0.1:14550')


def execute_mission(mission, mission_name="UNNAMED"):
    for submission in mission:
        for coord in submission:
            set_waypoint(vehicle_connection,
                         coord[0], coord[1], coord[2], autocontinue=1)

    print(f"{mission_name} MISSION COMPLETED!")


def create_loop_missions(object_locations, loop_mission):
    # assumption: the order of the mission loops is from first to last, so the entrance point of question is already implemented
    # return a collection of missions
    mission_array = [loop_mission]

    for location in object_locations.values():
        buffer_mission = [*loop_mission, location]
        mission_array.append(buffer_mission)

    print_missions(mission_array)
    return mission_array


def print_missions(mission_array):
    for idx in range(len(mission_array)):
        print(f"\nMISSION {idx+1}\n")
        for coord in mission_array[idx]:

            if coord == mission_array[idx][-1]:
                print(coord)
            else:
                print(coord, end="->")


missions = create_loop_missions(object_detections, loop_mission)
print(missions)
