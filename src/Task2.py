'''
Created on Mar 10, 2013

@author: metagrapher
'''
########################################################################################
# 2) Create an image for each 0.25 seconds and output them to a directory,
# using FFMPEG or other lib to combine them all together into a movie.
# Hint, create all images first then, in a separate step, call FFMPEG
# to have it combine them itself.
########################################

import Task1, os, subprocess, tempfile, shutil, Image
import pprint


########################################################
# Function: generateGazeFrames
# Parameters:
#    eyetrackList:    A list of dictionaries; expecting at least "ContentID", "Time", and "AbsoluteY" as properties
#    dirname:        OPTIONAL String; the name of the directory to save the gaze image files in
#    granularity:    Integer; Frequency, in milliseconds, of composite polling segments. Similar to frame rate.
# Returns:
#    Nothing.
#
# Designed to generate a set of gaze images based on eyetrackList data, set to the millisecond polling granularity
#
def generateGazeFrames(eyetrackList, dirname="./gaze_frames/", granularity=250):

    # TODO: Check for a final "/" in the dirname, and add if necessary
    # TODO: Enforce "/gaze_frames/" directory
    if (not os.path.isdir(dirname)): os.mkdir(dirname)

    # generate gaze frames
    maxTime = 0
    time = 0
    i = 0
    contentID = eyetrackList[0]["ContentID"]
    for eyetrack in eyetrackList:
        if maxTime < eyetrack["Time"]: maxTime = eyetrack["Time"]
    while time <= maxTime:
        eyetrackSegment = Task1.refineTimeframe(eyetrackList, (time, time + granularity))
        # print(time)
        # pprint(eyetrackSegment)
        if len(eyetrackSegment) > 0:
            path = dirname + contentID + "-" + str(i) + ".png"
            Task1.makeMap(eyetrackSegment, path)
        elif time == 0:
            # Create a blank image
            img = Image.new("RGBA", (eyetrackList[0]["OriginWidth"], eyetrackList[0]["OriginHeight"]), (0, 0, 0, 0))
            img.save(dirname + contentID + "-" + str(i) + ".png", "PNG")
        else:
            # use the last image.
            print "Skipping segment", time, "-", time + granularity
            shutil.copyfile(dirname + contentID + "-" + str(i - 1) + ".png", dirname + contentID + "-" + str(i) + ".png")

        time += granularity
        i += 1


def run(sessions, eventList, eyetrackList):
    # Get the directory to use
    defaultdirname = tempfile.mkdtemp()
    dirname = raw_input("In what directory should I store your movie?\n")
    if dirname == '':
        dirname = defaultdirname
        print "OK. I'll use", dirname
    else:
        while not os.path.isdir(dirname):
            dirname = raw_input("Sorry, I'm not allowed to go to the path you showed me. Let's try again.\nWhat is the full path to the directory where you want the movie, please?\n")
            if dirname == '':
                dirname = defaultdirname
                print "OK. I'll just grab a temporary folder. Look here when we're done:\n", dirname

    # Make Gaze Frames
    generateGazeFrames(eyetrackList, dirname + "/gaze_frames/")
    print "Look here for your frames:\n", dirname + "/gaze_frames/"

    # subprocess out to ffmpeg to composite images to video
    # ffmpeg -f image2 -r 4 -i CT13C39DD417BLYWHILLT-SJJ-%d.png -vcodec mpeg4 -r 30 CT13C39DD417BLYWHILLT-SJJ-gaze.mp4
    ''' Commenting out becuase execution is not reliable.
    args = {
            "inputfilesmask":    dirname + "/gaze_frames/" + eyetrackList[0]["ContentID"] + "-%d.png",
            "fps":          4,
            "outputfilename": dirname + "/" + eyetrackList[0]["ContentID"] + "-gaze.mp4"
            }

    command = "ffmpeg -f image2 -r %(fps)d -i %(inputfilesmask)s -vcodec mpeg4 -r 30 %(outputfilename)s" % args
    print("Now lets pull all those images into a movie for your enjoyment")
    # TODO: Figure out why making this movie hangs python...
    #    it's worked before. It only hangs sometimes.  Memory issues? I think my machine has memory issues.
    ffmpeg_proc = subprocess.Popen(command, shell=True, bufsize= -1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    io = ffmpeg_proc.communicate()
    print(io[0])
    if not io[1] == None: pass  # TODO: Automagically troubleshoot ffmpeg
    else:
        print "Success! Your gaze movie is located here:\n", args["outputfilename"]
    '''



