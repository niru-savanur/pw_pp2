

import os
import sys
from math import sqrt
# from tkinter import *

import bc

import random
from utils import communicate



if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
import traci
from plexe import Plexe, ACC, CACC


conflict_matrix = {
    0:[], 
    1:[4, 8, 10, 11], 
    2:[4, 5, 7, 11], 
    3:[], 
    4:[1, 2, 7, 11], 
    5:[2, 7, 8, 10],
    6:[],
    7:[2, 4, 5, 10],
    8:[1, 5, 10, 11],
    9:[],
    10:[1, 5, 7, 8],
    11:[1, 2, 4, 8]
    }

conflict_matrix_left = {
    0:[], 
    1:[4, 5, 8, 10], 
    2:[5, 7, 10, 11],
     
    3:[], 
    4:[1, 7, 8, 11],     
    5:[1, 2, 8, 10],
    
    6:[],
    7:[2, 4, 10, 11],   
    8:[1, 4, 5, 11],
    
    9:[],
    10:[1, 2, 5, 7],   
    11:[2, 4, 7, 8]
    
    }

VEHICLE_LENGTH = 4
DISTANCE = 6  
LANE_NUM = 12
PLATOON_SIZE = 1
SPEED = 16.6  
V2I_RANGE = 200 
PLATOON_LENGTH = VEHICLE_LENGTH * PLATOON_SIZE + DISTANCE * (PLATOON_SIZE - 1)
ADD_PLATOON_PRO = 0.3  
ADD_PLATOON_STEP = 900
MAX_ACCEL = 2.6


STOP_LINE = 15.0
RED = (250, 5, 5)
GREEN = (5, 156, 45)
WHITE = (255, 255, 255)
PURPLE = (26, 2, 242)
BLUE = (81, 174, 245)
YELLOW = (255, 255, 23)
CARAMEL = (250, 181, 5)
BLACK = (0, 0, 0)

COLORS = [RED, PURPLE, YELLOW, BLUE, CARAMEL, GREEN]
current_pois = []


def del_conflict_list(veh_i, conflict_list):
    
    traci.vehicle.setColor(veh_i, (WHITE))
    if veh_i in conflict_list:
        traci.vehicle.setColor(conflict_list[veh_i], (WHITE))
        del conflict_list[veh_i]

    return conflict_list


def add_poi(conflict_list):
    poi_x_start_q4 = -40
    poi_y_start_q4 = 40

    poi_x_start_q3 = -40
    poi_y_start_q3 = -20

    poi_x_start_q2 = 40
    poi_y_start_q2 = -20

    poi_x_start_q1 = 40
    poi_y_start_q1 = 40

    poi_increment = 10
    for i in range(len(current_pois)):
        traci.poi.remove(current_pois[i])
    current_pois.clear()

    i = 0
    i_4 = 0
    i_3 = 0
    i_2 = 0
    i_1 = 0
    for k, v in conflict_list.items():
        if i == 10:
            break
        id = traci.vehicle.getRoadID(k)
        if id == "end4_junction":
            traci.poi.add(k+" : "+v, poi_x_start_q4, poi_y_start_q4-i_4*poi_increment, BLACK)
            i_4 += 1
        elif id == "end3_junction":
            traci.poi.add(k+" : "+v, poi_x_start_q3, poi_y_start_q3-i_3*poi_increment, BLACK)
            i_3 += 1
        elif id == "end2_junction":
            traci.poi.add(k+" : "+v, poi_x_start_q2, poi_y_start_q2-i_2*poi_increment, BLACK)
            i_2 += 1
        elif id == "end1_junction":
            traci.poi.add(k+" : "+v, poi_x_start_q1, poi_y_start_q1-i_1*poi_increment, BLACK)
            i_1 += 1 
        
        current_pois.append(k+" : "+v)
        i += 1

    
    

def update_global_decision(conflict_list, serving_list, serving_list_veh_only):
    #conflict_list == [veh_id,...]
    #serving_list == [[veh_id, x, y, z],...]
    votes = {}
    for veh_id in conflict_list.values():
        
        if veh_id in votes:
            votes[veh_id] = votes[veh_id] + 1
        else:
            votes[veh_id] = 1

    for i in range(len(serving_list_veh_only)-2):
        max_votes = i
        if serving_list_veh_only[max_votes] not in votes:
            continue
        
        for j in range(i+1, len(serving_list_veh_only)-1):
            
            if serving_list_veh_only[j] in votes and votes[serving_list_veh_only[j]] > votes[serving_list_veh_only[max_votes]]:
                max_votes = j
        if max_votes != i:
            serving_list_veh_only[i], serving_list_veh_only[j] = serving_list_veh_only[j], serving_list_veh_only[i]
            serving_list[i], serving_list[j] = serving_list[j], serving_list[i]

    return serving_list, serving_list_veh_only
    

def refresh_conflict_list(conflict_list, serving_list_veh_only):
    del_items = [k for k, v in conflict_list.items() if v not in serving_list_veh_only]
    for k in del_items:  
        del_conflict_list(k , conflict_list)



# def add_poi(conflict_list, win):
#     col1 = Text(win, width=15, height=5)
#     col2 = Text(win, width=15, height=5)
#     col3 = Text(win, width=15, height=5)
#     col4 = Text(win, width=15, height=5)
#     col1.grid(row=0,column=0)
#     col2.grid(row=0,column=1)
#     col3.grid(row=0,column=2)
#     col4.grid(row=0,column=3)
#     col1.insert(END, "Vehicle")
#     col2.insert(END, "Speed (m/s)")
#     col3.insert(END, "Collision With")
#     col4.insert(END, "Speed (m/s)")

#     i = 1
#     for k, v in conflict_list.items():
#         # if i == 5:
#         #     return    
#         text1 = Text(win, width=15, height=4)
#         text2 = Text(win, width=15, height=4)
#         text3 = Text(win, width=15, height=4)
#         text4 = Text(win, width=15, height=4)
#         text1.grid(row=i,column=0)
#         text2.grid(row=i,column=1)
#         text3.grid(row=i,column=2)
#         text4.grid(row=i,column=3)
#         text1.insert(END, k)
#         text2.insert(END, round(traci.vehicle.getSpeed(k), 2))
#         text3.insert(END, v)
#         text4.insert(END, round(traci.vehicle.getSpeed(v), 2))

#         i += 1


# def update_conflicts(conflict_list, poi_remove, win, step):
def update_conflicts(conflict_list, poi_remove, step):
    # for k, v in conflict_list.items():
    #     traci.vehicle.setColor(k, (RED))
    #     if v not in conflict_list:
    #         traci.vehicle.setColor(v, (GREEN))
    # if step % 50 == 1:
    #     add_poi(conflict_list, win)
    votes = {}
    for veh_id in conflict_list.values():
        
        if veh_id in votes:
            votes[veh_id] = votes[veh_id] + 1
        else:
            votes[veh_id] = 1
    votes = dict(sorted(votes.items(), key=lambda item: item[1]))
    ind = 0
    for veh_key in votes.keys():
        traci.vehicle.setColor(veh_key, (COLORS[ind]))
        ind += 1





def add_single_platoon(plexe, topology, step, lane, bc1):
    for i in range(PLATOON_SIZE):
        vid = "v.%d.%d.%d" %(step/ADD_PLATOON_STEP, lane, i)
        routeID = "route_%d" %lane   
        traci.vehicle.add(vid, routeID, departPos=str(100-i*(VEHICLE_LENGTH+DISTANCE)), departSpeed=str(5), departLane=str(lane%3), typeID="vtypeauto")
        # bc1.mine_block(vid)
        plexe.set_path_cacc_parameters(vid, DISTANCE, 2, 1, 0.5)
        plexe.set_cc_desired_speed(vid, SPEED)
        plexe.set_acc_headway_time(vid, 1.5)
        plexe.use_controller_acceleration(vid, False)
        plexe.set_fixed_lane(vid, lane%3, False)
        traci.vehicle.setSpeedMode(vid, 0)
        if i == 0:
            plexe.set_active_controller(vid, ACC)
            
            traci.vehicle.setColor(vid, WHITE)  
            topology[vid] = {}
        else:
            plexe.set_active_controller(vid, CACC)
            
            traci.vehicle.setColor(vid, (200,200,0, 255)) 
            topology[vid] = {"front": "v.%d.%d.%d" %(step/ADD_PLATOON_STEP, lane, i-1), "leader": "v.%d.%d.0" %(step/ADD_PLATOON_STEP, lane)}



def add_platoons(plexe, topology, step, bc1):
    for lane in range(LANE_NUM):    
        if random.random() < ADD_PLATOON_PRO:
            add_single_platoon(plexe, topology, step, lane, bc1)


def compute_leaving_time(veh):
    distance = 400 + PLATOON_LENGTH + STOP_LINE - traci.vehicle.getDistance(veh)
    speed = traci.vehicle.getSpeed(veh) + 0.00001
    return distance*1.0/speed



def main():
    sumo_cmd = ['sumo-gui', '-c', 'cfg/twoWay6lanes.sumo.cfg']
    traci.start(sumo_cmd)
    
    plexe = Plexe()
    traci.addStepListener(plexe)

    bc1 = bc.Blockchain()

    # win = Tk()
    # win.geometry("600x1000")

    step = 0
    topology = {}
    serving_list = []  
    serving_list_veh_only = []  
    conflict_list = {}
    poi_remove = []
    
    while step < 360000:  
        
        traci.simulationStep()

        if step % ADD_PLATOON_STEP == 0:  
            add_platoons(plexe, topology, step, bc1) 
        

        
        deleted_veh = []
        for key, value in list(topology.items()):            
            if value == {}:  
                odometry = traci.vehicle.getDistance(key)
                
                if (not key in serving_list_veh_only) and (400-V2I_RANGE <= odometry < 400-V2I_RANGE+100): 
                    
                    serving_list.append([key, int(key.split(".")[2]), 0, 1])
                    serving_list_veh_only.append(key)
                
                if odometry > 800:
                    deleted_veh.append(key)    

        for veh in deleted_veh:
            veh_time = veh.split(".")[1]
            veh_route = veh.split(".")[2]
            for i in range(PLATOON_SIZE):                
                veh_id = "v." + veh_time + "." + veh_route + "." + str(i)
                del topology[veh_id]
        
        serving_list[:] = [element for element in serving_list if traci.vehicle.getDistance(element[0]) < 400 + PLATOON_LENGTH + STOP_LINE]  
        serving_list_veh_only = [element[0] for element in serving_list]  
        refresh_conflict_list(conflict_list, serving_list_veh_only)
               
        for i in range(len(serving_list)):  
            veh_i = serving_list[i][0]  
            route_i = int(veh_i.split(".")[2])
            priority = serving_list[i][3]
            if priority == 0: 
                serving_list[i][2] = compute_leaving_time(veh_i)                
            else:                
                max_leaving_time = 0.00001            
                for j in range(i):
                    veh_j = serving_list[j][0]
                    route_j = int(veh_j.split(".")[2])
                    leaving_time_j = serving_list[j][2]
                    if (route_j in conflict_matrix_left[route_i]) and (leaving_time_j > max_leaving_time):
                        max_leaving_time = leaving_time_j
              
                if max_leaving_time == 0.00001:
                    conflict_list = del_conflict_list(veh_i, conflict_list)
                    serving_list[i][3] = 0
                    distance = 400 + PLATOON_LENGTH + STOP_LINE - traci.vehicle.getDistance(veh_i)
                    desired_speed = sqrt(2 * MAX_ACCEL * distance + (traci.vehicle.getSpeed(veh_i))**2)
                    plexe.set_cc_desired_speed(veh_i, desired_speed)
                    serving_list[i][2] = (desired_speed - traci.vehicle.getSpeed(veh_i)) / MAX_ACCEL
               
                else:
                    conflict_list[veh_i] = veh_j
                    distance_to_stop_line = 400 - STOP_LINE - traci.vehicle.getDistance(veh_i)
                   
                    current_speed = traci.vehicle.getSpeed(veh_i) + 0.00001  
                    decel = 2 * (current_speed * max_leaving_time - distance_to_stop_line)/(max_leaving_time **2)
                    desired_speed = current_speed - decel * max_leaving_time
                    
                    plexe.set_cc_desired_speed(veh_i, desired_speed)
                    
                    serving_list[i][2] = (distance_to_stop_line + PLATOON_LENGTH + 2*STOP_LINE)/current_speed
                    
        # update_conflicts(conflict_list, poi_remove, win, step)
        update_conflicts(conflict_list, poi_remove, step)

        if step % 100 == 1:
            serving_list, serving_list_veh_only = update_global_decision(conflict_list, serving_list, serving_list_veh_only)
            add_poi(conflict_list)
        # win.update()
        if step % 10 == 1:    
            communicate(plexe, topology)
        step += 1

    # win.mainloop()
    traci.close()


if __name__ == "__main__":
    
    main()
