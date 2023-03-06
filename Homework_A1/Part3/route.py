#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Kenny Lawrence Swamy kenswamy, Krishna Teja Jillelamudi kjillela, Sakshi Sitoot ssitoot
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#

# !/usr/bin/env python3
import sys
from math import tanh,cos,sin,atan2,sqrt,radians
def get_route(start, end, cost):
   
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    s='./road-segments.txt'
    b='./city-gps.txt'
    ct_dict={}
    dict1={}
    speed=[]
    segment=[]

    # Implementation using prioritry queue 
    class priority_queue:
        queue=[]
        def _init_(self):
            self.queue=[]
        def push(self,data):
            self.queue.append(data)
        def is_empty(self):
            return len(self.queue)==0
        def pop(self):
            def sorting(element):
                return element[2]
            self.queue.sort(key=sorting)
            item=self.queue[0]
            del self.queue[0]
            return item

    def ct_map(file_name):
        f=open(file_name)
        city=[]
        for i in f.readlines():
            city.append(i.rstrip('\n').split(' '))
        return city
    cities=ct_map(b)
    for i in cities:
        if i[0] not in ct_dict:
            ct_dict[i[0]]=[i[1],i[2]]

    def get_city_directions(file_name):
            f=open(file_name)
            ct_seg=[]
            for i in f.readlines():
                    s=i.rstrip('\n').split(' ')
                    ct_seg.append([s[0],s[1],s[2],s[3],s[4]])
                    ct_seg.append([s[1],s[0],s[2],s[3],s[4]])
            return ct_seg

    ab=get_city_directions(s)
    for i in ab:
            if i[0] in dict1:
                dict1[i[0]].append((i[1],i[2],i[3],i[4]))
            else:
                dict1[i[0]]=[(i[1],i[2],i[3],i[4])]

    # The max length segment is found by this function 
    for i in ab:
        segment.append(int(i[2]))
    max_segment=max(segment)

    # The max speed is found by this function 
    for i in ab:
        speed.append(int(i[3]))
    max_speed=max(speed)
    

    def heuristic(city1,city2):
                city11=ct_dict[city1]
                city22=ct_dict[city2]
                longitude1,latitude1=radians(float(city11[0])),radians(float(city11[1]))
                longitude2,latitude2=radians(float(city22[0])),radians(float(city22[1]))
                dest_longitude = longitude2 - longitude1
                dest_latitude = latitude2 - latitude1
                a = (sin(dest_latitude/2))*2 + cos(latitude1) * cos(latitude2) * (sin(dest_longitude/2))*2
                a=abs(a)
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                heu =  c*6373.0
                return heu

    def path_segments(start,end):
            examine=priority_queue()
            examine.push((start,[],0,0,0,0))
            travelled=[]
            while examine.is_empty()!=True:
                node,path,cost,distance,time,delivery_time=examine.pop()
                travelled.append(node)
                if node==end:
                    return len(path),path,distance,time,delivery_time
                for i in dict1[node]:
                    if i[0] not in travelled:
                        if i[0] not in ct_dict:
                            heuristic1=(heuristic(start,end)-(distance+int(i[1])))/max_segment
                        else:
                            heuristic1=heuristic(i[0],end)/max_segment
                        travelled_road_normal=int(i[1])/int(i[2])
                        if int(i[2])>=50:
                            travelled_road=int(i[1])/int(i[2])
                            t=tanh(int(i[1])/1000)
                            travelled_road=travelled_road+t*2*(time+travelled_road)
                        else:
                            travelled_road=int(i[1])/int(i[2])
                        examine.push((i[0],path+[(i[0],'yes')],cost+1+heuristic1,distance+int(i[1]),time+travelled_road_normal,delivery_time+travelled_road))
            return 'cant find path'

    # The shortest path 
    def path_distance(start,end):
        examine=priority_queue()
        examine.push((start,[],0,0,0,0))
        travelled=[]
           
        while examine._()!=True:
            node,path,cost,distance,time,delivery_time=examine.pop()
            travelled.append(node)
            if node==end:
                return len(path),path,distance,time,delivery_time
              
            for i in dict1[node]:
               if i[0] not in travelled:
                    if i[0] not in ct_dict:
                        heuristic1=heuristic(start,end)-(distance+int(i[1]))                       
                    else:
                        heuristic1=heuristic(i[0],end)
                    travelled_road_normal=int(i[1])/int(i[2])
                    if int(i[2])>=50:
                            travelled_road=int(i[1])/int(i[2])
                            t=tanh(int(i[1])/1000)
                            travelled_road=travelled_road+t*2*(time+travelled_road)
                    else:
                            travelled_road=int(i[1])/int(i[2])
               
                    examine.push((i[0],path+[(i[0],'yes')],cost+distance+heuristic1,distance+int(i[1]),time+travelled_road_normal,delivery_time+travelled_road))
        return 'cant find path'

    #The fastest route
    def fastpath(start,end):
        examine=priority_queue()
        examine.push((start,[],0,0,0,0))
        travelled=[]
        while examine._()!=True:
            node,path,cost,distance,time,delivery_time=examine.pop()
            travelled.append(node)
            if node==end:
                return len(path),path,distance,time,delivery_time
              
            for i in dict1[node]:
               if i[0] not in travelled:
                    if i[0] not in ct_dict:
                        heuristic1=(heuristic(start,end)-(distance+int(i[1])))/max_speed
                       
                    else:
                        heuristic1=heuristic(i[0],end)/int(i[1])
                    travelled_road_normal=int(i[1])/int(i[2])
                    if int(i[2])>=50:
                            travelled_road=int(i[1])/int(i[2])
                            t=tanh(int(i[1])/1000)
                            travelled_road=travelled_road+t*2*(time+travelled_road)
                    else:
                            travelled_road=int(i[1])/int(i[2])
 
                    examine.push((i[0],path+[(i[0],'yes')],cost+time+heuristic1,distance+int(i[1]),time+travelled_road_normal,delivery_time+travelled_road))
        return 'cant find path'

    # The time taken for delivery
    def fastpath_delivery(start,end):
        examine=priority_queue()
        examine.push((start,[],0,0,0,0))
        travelled=[]          
        while examine._()!=True:
            node,path,cost,distance,time,delivery_time=examine.pop()
            travelled.append(node)
            if node==end:
                return len(path),path,distance,time,delivery_time
            for i in dict1[node]:
               if i[0] not in travelled:
                    if i[0] not in ct_dict:
                        heuristic1=(heuristic(start,end)-(distance+int(i[1])))/max_speed
                    else:
                        heuristic1=heuristic(i[0],end)/int(i[1])
                    travelled_road_normal=int(i[1])/int(i[2])
                    if int(i[2])>=50:
                            travelled_road=int(i[1])/int(i[2])
                            t=tanh(int(i[1])/1000)
                            travelled_road=travelled_road+t*2*(time+travelled_road)
                    else:
                            travelled_road=int(i[1])/int(i[2])
                    examine.push((i[0],path+[(i[0],'yes')],cost+delivery_time+heuristic1,distance+int(i[1]),time+travelled_road_normal,delivery_time+travelled_road))
        return 'cant find path'
  
    if cost=='segments':
        a,route_taken,m,h,d_h=path_segments(start,end)
    if cost=='distance':
        a,route_taken,m,h,d_h=path_distance(start,end)
    if cost=='time':
        a,route_taken,m,h,d_h=fastpath(start,end)
    if cost=='delivery':
        a,route_taken,m,h,d_h=fastpath_delivery(start,end)
   
    return {"total-segments" : a,
            "total-miles" : m,
            "total-hours" : h,
            "total-delivery-hours" : d_h,
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
   
   

    # Pretty print the route
    print("Start in %s" % start_city)
   
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])