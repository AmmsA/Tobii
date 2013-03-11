'''
Created on Mar 10, 2013

@author: metagrapher
'''
########################################################################################
# 4) Figure out how to overlay the pictures on top of the actual video. The video can
# be found here: http://g3.eyetrackshop.com/content/CT13C39DD417BLYWHILLT-SJJ
########################################

import Task2, urllib2, os, tempfile, subprocess, Image, ImageMath


def run(sessions, eventList, eyetrackList):
    print "Downloading session video for parsing..."
    # download session video
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request("http://g3.eyetrackshop.com/content/" + eyetrackList[0]["ContentID"])
    request.get_method = lambda: "GET"
    url = opener.open(request)
    tempdir = tempfile.tempdir = tempfile.mkdtemp()
    movie = tempfile.NamedTemporaryFile(mode="w+", suffix=".mp4", delete=False)
    movie.write(url.read())
    moviename = movie.name
    movie.close()
    print "I've loaded it into:\n", moviename

    # split apart session video into frame images
    # ffmpeg -i inputfile.avi -r 12 -f image2 CT13C39DD417BLYWHILLT-SJJ-f%4d.jpeg
    print "Using superhuman strength to split movie into images..."
    movieframedir = tempdir + "/movieframes/"
    os.mkdir(movieframedir)
    args = {
            "inputfile":    moviename,
            "framerate":    12,
            "outputfilename":movieframedir + eyetrackList[0]["ContentID"] + "-f%4d.png"
            }
    command = "ffmpeg -i %(inputfile)s -r %(framerate)d -f image2 %(outputfilename)s" % args
    ffmpeg_proc = subprocess.Popen(command, shell=True, bufsize= -1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    io = ffmpeg_proc.communicate()
    if not io[1] == None: pass  # TODO: Automagically troubleshoot ffmpeg
    print "Success! We have movie frames!\n", movieframedir

    # generate gaze images
    print "Generating Gaze Frames..."
    gazedir = tempdir + "/gaze_frames/"
    granule = 1000 / args["framerate"]
    print granule
    Task2.generateGazeFrames(eyetrackList, dirname=gazedir, granularity=granule)
    print "Done Gazing into the gazes of others. See what I saw here:\n", gazedir

    # add session frame images and gaze images together
    # Image.composite(sessionframe, gazeimage, gazeimage)
    print "Making composite frames..."
    compdir = tempdir + "/composite_frames/"
    os.mkdir(compdir)
    i = 0
    movieframelist = os.listdir(movieframedir)
    gazeframelist = os.listdir(gazedir)
    for gazeframename in gazeframelist:
        movieframe = Image.open(movieframedir + movieframelist[i])
        gazeframe = Image.open(gazedir + gazeframename)
        # compimg = Image.composite(movieframe, gazeframe, gazeframe)
        # compimg.save(compdir + str(i) + ".png", "PNG")
        movieframe.paste(gazeframe, (0, 0), gazeframe)
        movieframe.save(compdir + str(i) + ".png", "PNG")
        i += 1
    print "Done! Find your composite frames here:\n", compdir

    # TODO: recomposite images into video
    # ffmpeg -f image2 -r 4 -i CT13C39DD417BLYWHILLT-SJJ-gaze-comp-%4d.png -vcodec mpeg4 -r 30 CT13C39DD417BLYWHILLT-SJJ-gaze-overlay.mp4
    args = {
            "fps":          12,
            "inputfilesmask":    compdir + "%d.png",
            "outputfilename": tempdir + "/" + eyetrackList[0]["ContentID"] + "-gaze_composite.mp4"
            }

    command = "ffmpeg -f image2 -r %(fps)d -i %(inputfilesmask)s -vcodec mpeg4 -r 30 %(outputfilename)s" % args
    print("Now lets pull all those images into a movie for your gazing enjoyment")
    # TODO: Figure out why making this movie hangs python...
    #    it's worked before. It only hangs sometimes.  Memory issues? I think my machine has memory issues.
    ffmpeg_proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    io = ffmpeg_proc.communicate()
    print(io[0])
    if not io[1] == None: print "Houston, we had a problem. with ffmpeg"  # TODO: Automagically troubleshoot ffmpeg
    else:
        print "Success! Your gaze movie is located here:\n", args["outputfilename"]

