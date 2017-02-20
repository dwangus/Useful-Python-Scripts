import imageio
#imageio.plugins.ffmpeg.download()
from moviepy.editor import *
import sys
import os
#######################################
comments = """
 - Must have arguments of times in 'start-end' (e.g. 30-40 (in terms of seconds)) format and
         specify output file with '-o some_outputfilename.mp4'.

 - Also, you can specify numbers as either 'X_Y' between X and Y seconds, or 'A-B_X-Y' for
         clips between (A minutes, B seconds) to (X minutes, Y seconds) in the video.
 
 - Example usage of script:
 
     \'python clip.py inputvideo_filename.mp4 3-5_4-16 12-1_12-45 -o some_output_filename.mp4\'
     
   (This will basically clip inputvideo_filename.mp4 into 2 separate clips, one between 3:05 and
       4:16 minutes, another between 12:01 and 12:45 minutes -- and then stitch the two clips
       together into one final video called some_output_filename.mp4!)
     
 - Additional arguments are, for now, the \'-separate\' flag -- if set and there are multiple clips
         in the original video, it just clips them into separate, stand-alone video files with the
         name some_output_filename0.mp4, some_output_filename1.mp4, etc. etc.
"""
#######################################

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def clip(args, inputfile, outputfile, separate=False):
    clips = []
    for time in args:
        parsed = [t for t in time.split("_") if (isFloat(t) or ("-" in t and all([isFloat(m) for m in t.split("-")])))]
        if len(parsed) != 2:
            print("Incorrect formatting of start-end argument for clipping video based on start and end times.")
            sys.exit()
        for p in range(len(parsed)):
            if "-" in parsed[p]:
                parsed[p] = parsed[p].split("-")
                parsed[p] = float(parsed[p][0])*60 + float(parsed[p][1])
            else:
                parsed[p] = float(parsed[p])

        clips.append(VideoFileClip(inputfile).subclip(parsed[0], parsed[1]))

    if separate:
        fileParts = outputfile.split(".")
        basename = fileParts[0]
        extension = fileParts[1]
        for c in range(len(clips)):
            clips[c].write_videofile(basename + "-" + str(c) + extension)
            print("Successfully written output video to {}.".format(basename + "-" + str(c) + extension))
    else:
        finalClip = concatenate_videoclips(clips)
        finalClip.write_videofile(outputfile)
        print("Successfully written output video to {}.".format(outputfile))
        inputSize = os.path.getsize(inputfile)
        outputSize = os.path.getsize(outputfile)
        print("Original input video size was {} MB (or {} bytes).\nNew output video size is {} MB (or {} bytes).".format(inputSize/float(10 ** 6)*0.953, inputSize,\
                                                                                             outputSize/float(10 ** 6)*0.953, outputSize))

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 3 or "-h" in args or "-help" in args:
        if len(args) < 3 and "-h" not in args and "-help" not in args:
            print("Error in number of arguments: see below comments...")
        print(comments)
        sys.exit()

    videofile = args[0]

    if '-o' not in args:
        print("Must have output filename in form of '-o outputfilename.mp4'!")
        sys.exit()
    else:
        argIndex = args.index("-o")
        outputfile = args[(argIndex + 1)]
        args = args[1:argIndex] + args[(argIndex+2):]
    
    if '-separate' in args:
        sep = True
        args = args[:args.index("-separate")] + args[(args.index("-separate")+1):]
    else:
        sep = False
    
    clip(args, videofile, outputfile, sep)
