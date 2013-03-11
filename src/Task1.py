'''
Created on Mar 8, 2013

@author: metagrapher
'''
########################################################################################
# 1) Create an image which shows the heat map of where people are looking from
# time = 3 to time = 4 seconds on a black background in dots or a false color temp
# gradient.
# It should look roughly like this, but without the web page:
#     http://johnnyholland.org/wp-content/uploads/193383382_cf3b3bd6d0_o.png
# Help on drawing: http://quickies.seriot.ch/index.php?id=256
########################################

import Image, ImageDraw, colorsys


########################################################
# Function: refineTimeframe
# Parameters:
#    eyetrackList:    A list of dictionaries, expecting at least "Time" as a property
#    timeframe:       An OPTIONAL tuple of integers, time in milliseconds
# Returns:
#    List of objects whose time is within the timeframe parameter
#
# Refines a list of eyetrack events to a specific timeframe, default is the first minute.

def refineTimeframe(eyetrackList, timeframe=(0, 60000)):
    rtn = []
    for et in eyetrackList:
        time = et["Time"]
        if time >= timeframe[0] and time <= timeframe[1]:
            rtn.append(et)

    return rtn




########################################################
# Function: makeMap
# Parameters:
#    eyetrackList:    A list of dictionaries, expecting at least "AbsoluteX" and "AbsoluteY" as properties
#    filename:        String, the name of the image file to save
# Returns:
#    RGB PNG Image object
#
# This function is designed to create a false-color RGBA map of the data. You can specify the filename and
#  background color of the output image.
#
def makeMap(eyetrackList, filename="heatmap.png", background_color=(0, 0, 0, 0)):
    d = totalPixelCounts(eyetrackList)
    data = d["totals"]

    # Set up our image:
    H = len(data)
    W = len(data[0])
    img = Image.new("RGBA", (W, H), background_color)
    draw = ImageDraw.Draw(img)
    img.save(filename, "PNG")
    r = 1
    low = d["range"]["low"]
    high = d["range"]["high"]

    for eyetrack in eyetrackList:
        X = eyetrack["AbsoluteX"]
        Y = eyetrack["AbsoluteY"]
        hits = data[Y][X]
        if hits == 0:
            continue
        # print(hits)
        hue = percentInRange(hits, low, high)
        # print(X, Y, "hue:", hue)
        base255 = lambda x : int(x * 255)
        a = .25
        rd, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
        rd, g, b, a = map(base255, (rd, g, b, a))
        color = (rd, g, b, a)
        # print("color:", color)
        draw.ellipse((int(X - r), int(Y - r), int(X + r), int(Y + r)), color)
        r = r * .66
        color = (rd, g, b, base255(.5))
        draw.ellipse((int(X - r), int(Y - r), int(X + r), int(Y + r)), color)
        r = r / 2
        color = (rd, g, b, base255(.75))
        draw.ellipse((int(X - r), int(Y - r), int(X + r), int(Y + r)), color)

    img.save(filename, "PNG")


########################################################
# Function: makeMap
# Parameters:
#    eyetrackList:    A list of dictionaries, expecting at least "AbsoluteX" and "AbsoluteY" as properties
# Returns:
#    RGB PNG Image object
#
# This function is designed to create a shadow map of the data.
#
#    CURRENLTY OUT OF SERVICE. DO NOT USE.
#
# TODO: Fix this function.  Having a B/W shadow map may be helpful in other fun adventures
'''
def makeShadowMap(eyetrackList):
    
    print("Making Shadow Map")
    d = totalPixelCounts(eyetrackList)
    data = d["totals"]
    low = d["range"]["low"]
    high = d["range"]["high"]
    H = eyetrackList[0]["OriginHeight"]
    W = eyetrackList[0]["OriginWidth"]
    filename = "shadowmap.png"
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    img.save(filename, "PNG")
    size = 15
    X, Y = 0, 0
    for row in data:
        for col in row:
            if col == 0:
                continue
            z = convertToRange(col, low, high, 255)
            draw.ellipse((X, Y, size, size), (z, z, z, 127) , (z, z, z, 31))
            X += 1
        Y += 1
    img.save(filename, "PNG")
'''


########################################################
# Function: totalPixelCounts
# Parameters:
#    eyetrackList:    A list of dictionaries, expecting at least "AbsoluteX" and "AbsoluteY" as properties
# Returns:
#    List of Lists, representing rows of columns of pixels,
#        containing a cumulative total of hits per pixel
#
# This function is designed to create a 2D Matrix of the cumulative totals for each pixel

def totalPixelCounts(eyetrackList):
    x = eyetrackList[0]["OriginWidth"]
    y = eyetrackList[0]["OriginHeight"]
    d = [ [0] * x for i in range(y) ]
    low, high, count = 0, 0, 0
    totalPixels = x * y

    for eyetrack in eyetrackList:
        ex = eyetrack["AbsoluteX"]
        ey = eyetrack["AbsoluteY"]
        # print("X:",ex,"Y:",ey)
        d[ey][ex] += 1
        # print("New total:", d[ey][ex])
        if d[ey][ex] > high:
            high = d[ey][ex]
        count += 1

    if count >= totalPixels:
        for y in d:
            for x in y:
                if x < low:
                    low = x
    return { "totals": d, "range": { "low":low, "high":high } }




######### MAIN FUNCTION #################
#
# Function: run
# Parameters:
#    sessions:        A list of session dictionaries
#    eventList:       A list of event dictionaries
#    eyetrackList:    A list of eyetrack event dictionaries, expecting the following properties:
#                        "ContentID", "Time","AbsoluteX","AbsoluteY"
# Returns:
#    Nothing.
#
# Creates false-color heatmap from given eyetrack data, by default between seconds 3 and 4.

def run(sessions, eventList, eyetrackList, timeframe=(3000, 4000)):
    print("Making a map of", eyetrackList[0]["ContentID"], "\n")
    print("eyetrackList length: ", len(eyetrackList))
    refinedList = refineTimeframe(eyetrackList, timeframe)
    print("eyetrackList length: ", len(refinedList))
    makeMap(refinedList)
    # makeShadowMap(refinedList) #Out of service.




######## HELPER FUNCTIONS ##############


############################
# Function: percentInRange
# Parameters:
#    num:    Integer; The target number
#    low:    Integer; Range bottom number
#    high:   Integer; Range top number
#
# Returns:
#    Float, between 0.0 and 1.0
#
# Finds the percentage of a number within a given range
def percentInRange(num, low, high):
    return float(num - low) / (high - low)

############################
# Function: convertToRange
# Parameters:
#    num:    Integer; The target number
#    low:    Integer; Range bottom number
#    high:   Integer; Range top number
#    newhigh:Integer; Top number of new range
#                NOTE: 0 is assumed to be the bottom of the new range
#
# Returns:
#    Integer, new number translated to coordinate percentage point on new scale
#
# If you've got a number, say num=50, and it's between low=20 and high=145,
#  and you want to know where it would fall if the scale were 0 through newhigh=255,
#  this function will tell you that number.
def convertToRange(num, low, high, newhigh):
    return int(float(num - low) / (high - low) * newhigh)


