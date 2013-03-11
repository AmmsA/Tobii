import json
from pprint import pprint
import Task1, Task2, Task4

# Get our data sources straight:
with open("/Users/metagrapher/Documents/Aptana Studio 3 Workspace/Tobii/eventList.json","r") as f:
    eventList = json.loads(f.read())

with open("/Users/metagrapher/Documents/Aptana Studio 3 Workspace/Tobii/eyetrackList.json","r") as f:
    eyetrackList = json.loads(f.read())

with open("/Users/metagrapher/Documents/Aptana Studio 3 Workspace/Tobii/eyetrackList.json","r") as f:
    sessions = json.loads(f.read())
    
''' Uncomment if you want to see the data printed
print("SESSIONS\n\n")
pprint(sessions)
print("\n\n\nEVENTS\n\n")
pprint(eventList)
print("\n\n\nEYES\n\n")
pprint(eyetrackList)
'''

def makeDataMap(eyetrackList):
    x = eyetrackList[0]["OriginWidth"]
    y = eyetrackList[0]["OriginHeight"]
    d = [ [0] * x for i in range(y) ]

    for eyetrack in eyetrackList:
        ex = eyetrack["AbsoluteX"]
        ey = eyetrack["AbsoluteY"]
        print("X:",ex,"Y:",ey)
        d[ey][ex] += 1
        print("New total:", d[ey][ex])
        
    return d

def refineTimeframe(eyetrackList, timeframe=(0, 60000)):
    rtn = []
    for et in eyetrackList:
        time = et["Time"]
        if time >= timeframe[0] and time <= timeframe[1]:
            rtn.append(et)
    return rtn

#print(type(eyetrackList[1]))
#print "Total Eyetrack Events:", len(eyetrackList) 
#refinedList = refineTimeframe(eyetrackList, (3000,4000))
#print "Events w/in seconds 3 and 4:", len(refinedList) 
#makeDataMap(refinedList)
#print(makeDataMap(eyetrackList))
#pprint(makeDataMap(eyetrackList))


#Task2.run(sessions,eventList,eyetrackList)
Task4.run(sessions,eventList,eyetrackList)
