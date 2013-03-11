'''
Created on Mar 8, 2013

@author: metagrapher
'''
'''
You will need Python 2.7 to run this and FFMPEG installed also to create the videos.
You probably don't need to use NumPy or SciPy to accomplish these tasks.

Please read through the code until you understand what is currently done to get the
data and how it is formatted. Arrays and Dictionaries are used for it.

You can use pprint( str ), which pretty-prints the data to make it easier to understand.

We have take an eye tracking project for a single full screen video for you to use. All
the data is hosted in the cloud on our API and the code below downloads the data to
make it accessible to you.

Below that, I have listed a set of tasks to implement on the data, which will result in
images, videos or test files outputting the raw results.
'''

from pprint import pprint
try:
    import json
except ImportError:
    import simplejson as json
import urllib2

import Task1, Task2, Task4

########################################################################################
# SETUP and HTTP Method
# You don't need to change any of this
COOKIE_NAME = 'G3_Account_Cookie'
storedCookie = None
studyName = 'ST13C39DD6AA9LCCMFEMF-DNF'

def HTTPGet(url, cookie=None):
    '''
    This is a helper method for you that downloads data from the API and returns it
    as a string
    '''
    if(cookie == None): cookie = storedCookie

    print('Get: ' + url)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    if(cookie != None):
        opener.addheaders.append(('Cookie', COOKIE_NAME + '=' + cookie))
    request = urllib2.Request(url)
    request.get_method = lambda: 'GET'
    url = opener.open(request)

    a = url.read()
    return a

########################################################################################

# Cache the security cookie so you don't have to log in each time
storedCookie = HTTPGet('https://g3api.eyetrackshop.com/accounts/chetan/login?password=dfasdflkjasdfasdfl')

# The helper.HTTPGet( ) returns the resulting data from a HTTP GET call to the URL
# Note that we have security, so if you want to look at this in a browser, you must
# first type this query into the browser to authenticate yourself. You can then run
# queries by typing in the commands you see below:
# HTTPGet('https://g3api.eyetrackshop.com/accounts/chetan/login?password=dfasdflkjasdfasdfl')

# This returns all the sessions in the study as a string that is JSON formatted
jsonSessionString = HTTPGet('https://g3api.eyetrackshop.com/studies/' + studyName + "/sessions")

# print( str( jsonSessionString))
# exit()

# This converts the string JSON representation of the data into a Python Array of
# sessions which each have a dictionary object with their details
sessions = json.loads(jsonSessionString)

# This outputs all the elements of the sessions objects so you can see them.
# Comment this out once you understand it.
pprint(sessions)

# This will hold the Python objects for each person, indexed by their ids
events = {}
eyetrack = {}

# This loops through all the sessions, checking if they have acceptable eye-
# tracking and, if so, it downloads the event file and the eye track data file.
# It then adds them to the dictionary of all events and eye tracking in the
# 'events' and 'eyetrack' Dictionaries
for session in sessions:
    # Many sessions do not have usable data, so we skip them
    if(session['eyetrack.quality'] != 'GOOD'):
        continue

    eventsStr = HTTPGet('https://g3api.eyetrackshop.com/studies/' + studyName + "/sessions/" + session['id'] + "/events")
    events[session['id']] = json.loads(eventsStr)

    # The eye tracking data is loaded into a Dictionary with tracking and
    # timing data included
    eyeTrackStr = HTTPGet('https://g3api.eyetrackshop.com/studies/' + studyName + "/sessions/" + session['id'] + "/eyetrack")
    eyetrack[session['id']] = json.loads(eyeTrackStr)

# At this point, all the data is downloaded that is necessary to calculate a
# gaze map and the other things below. Please view it ( pprint( ) ) until you understand
# what the elements mean and ask questions about pieces that seem pertinent.


# Now, you can loop through by each session and do whatever you want with them.
for session in events.keys():
    eventList = events[session]
    eyetrackList = eyetrack[session]

print("\n\n\n\nEVENT DATA LIST:\n")
pprint(eventList)
print("\n\n\n\nEYE TRACKING DATA LIST:\n")
pprint(eyetrackList)

########################################################################################
########################################################################################

# For the tasks below, I would recommend creating a separate python module for each
# one and just pass in the parameters from this file so that this file does not become
# huge. Below is commented out code which would run each task.

# We should be able to run this file ourselves and create the same outputs. The
# deliverable is both the code and a directory including the pictures/movies which
# are created with it.

# If you get stuck on one of them, please go on to the rest and then come back to it.

########################################################################################
########################################################################################


########################################################################################
# 1) Create an image which shows the heat map of where people are looking from
# time = 3 to time = 4 seconds on a black background in dots or a false color temp
# gradient.
# It should look roughly like this, but without the web page:
#     http://johnnyholland.org/wp-content/uploads/193383382_cf3b3bd6d0_o.png
# Help on drawing: http://quickies.seriot.ch/index.php?id=256
########################################

Task1.run(sessions, eventList, eyetrackList)



########################################################################################
# 2) Create an image for each 0.25 seconds and output them to a directory,
# using FFMPEG or other lib to combine them all together into a movie.
# Hint, create all images first then, in a separate step, call FFMPEG
# to have it combine them itself.
########################################

Task2.run(sessions, eventList, eyetrackList)




########################################################################################
# 3) Identify the central point(s) of gaze over a period of time and
# overlay a transparent white dot on the 1-3 areas of interest.
# the number should depend on if everyone is looking in a single
# place of if they are all looking in different places.
#
# Central points of gaze mean the "clusters" of gaze. If this doesn't make sense, please
# ask for clarification or skip it.
########################################

# ...



########################################################################################
# 3b) Create a separate movie showing this.
########################################





########################################################################################
# 4) Figure out how to overlay the pictures on top of the actual video. The video can
# be found here: http://g3.eyetrackshop.com/content/CT13C39DD417BLYWHILLT-SJJ
########################################


Task4.run(sessions, eventList, eyetrackList)


########################################################################################
# 5) Output a quality report in a test file, listing the % of sessions which are:
#     Complete - attribute session.last_state = "7.COMPLETE"
#     Usable - attribute eyetrack.quality = "GOOD"
#     Group eyetrack.quality failure reasons and output % of each
########################################




########################################################################################
# 6) For each frame, add 4 'area of interest' rectangles which are the 4 quadrants of
# the image. On each eye tracking frame, output a % noting in the middle of the frame in text
# which says what percent of people who have data during that time period were looking
# within the area of interest.
########################################



########################################################################################
# 7) Sometimes, when videos are played over the internet, they take time to buffer in
# the middle, which causes a delay. Using the event data, identify the distribution of
# this delay over all '7.COMPLETE' sessions and output as a text file.
#
# Hint: Look at the event data for alignment and errors in timing and parse it.
########################################





########################################################################################
# 7) Think of some additional things you could do with this data and what you have created
# and try implementing them and describe them below.
########################################






########################################################################################
