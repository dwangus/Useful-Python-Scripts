from __future__ import print_function
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import webbrowser as wwindow
import numpy as np

####################################################################################################
commandHelp = '''
***NOTE***: This script is only really for plotting 2D functions/lines, but can
            handle multiple lines for a single graph.

Options for running script:
 - 'filename.ext': input filename that will be opened; cannot be ommitted, and must
                     be first argument after script!!!

 - '-c' or '-r': for each line's y-value points being in columns or rows; cannot be
                     ommitted!!!
                     (e.g., if you have a line whose data points are like
                     1,2,3,4 for -r
                         vs.
                     ...,1,...
                     ...,2,...
                     ...,3,...
                     ...,4,... for -c)
 
 - '-firstlabel': if the first row/column encountered during parsing a section is
                     going to indicate the columns'/rows' label
 
 - '-section __(some integer)__': if the inputted data is broken up by blank
                                    lines/wordy text into sections, which section to
                                    choose; if left out, makes graphs for each section
                                    in data (e.g., if your data looked like...
                                    
                                    header1,header2,header3
                                    1,1,1
                                    2,3,4
                                    3,5,7

                                    *blah blah blah...*

                                    header4,header5,header6
                                    0,0,0
                                    5,10,15
                                    10,20,30
                                    
                                    ...then because of all those newline characters in
                                    the middle, my script would interpret that as 2
                                    different, sections of data, the first being integer
                                    index 0 and the second being integer index 1) (P.S.
                                    in the example above, that would also be specified
                                    as -c for axis-organization)
                                    
 - '-select __(int1),(int2),(...)__'
                     OR
   '-select __(int1)-(int2),(int3),(...)__': which rows/columns of the given section to plot
                                             lines for (NO spaces in 2nd argument!); if ommitted,
                                             plots data for each line (interpreting different
                                             lines depending on -c/-r); can also do ranges of
                                             lines, with start and ends of ranges inclusive
                                             (e.g. 2-5,12,14 means lines 2,3,4,5,12,14)

 - '-xclude __(int1),(int2),(...)__': which data-points, across all lines, you want to leave
                                         out from data-set; i.e., if for x = 2,3,4, we have
                                         Line1 = 8,9,14, and Line2 = 12,-2,3, setting the
                                         flag "-xclude 0,1" would leave out Line1(2), Line2(2),
                                         Line1(3), Line2(3). (ONLY INTEGERS FOR 2nd ARGUMENT)
                                         (New addition: you can also do 0-5,6-9,10,... for
                                         ranges of excluded data-points!)
                                         
 - '-xrange __(lower limit),(upper limit)__': lower and upper range for x-axis ticks
                                                (NO spaces in 2nd argument!)
 
 - '-yrange __(lower limit),(upper limit)__': lower and upper range for y-axis ticks
                                                 (NO spaces in 2nd argument!)
 
 - '-xaxis': if set, chooses the first row/column's values as the corresponding x-values for
             all other lines' y-values (e.g. if you had -c and something like...
                 
                 0,5.0,6.75
                 1,4.0,7.0
                 2,3.0,7.25
                 3,2.0,7.5
             ...and you set this flag, it would interpret the first column as the x-axis, so
             each other column would be interpreted as having x,y points of (0,__), (1,__),
             (2,__), (3,__) based on values of this first column)

 - '-t __(some title)__': graph title; if ommitted, script will prompt user to manually type
                             it in later, for each graph

 - '-x __(some label)__': x-axis label; if ommitted, script will prompt user to manually
                             type it in later, for each graph

 - '-y __(some label)__': y-axis label; if ommitted, script will prompt user to manually
                             type it in later, for each graph

 - '-beauty': if you set this flag, when the time comes to create the graph, you'll be
                 manually prompted to enter in the specifications for various parameters of
                 the matplotlib utility functions; if ommitted, uses hardcoded default
                 values/options; I'm still adding various options to greater manipulate
                 specifications of the matplotlib graphs!

 - '-display': if you set this flag, will attempt to open up the saved graph-picture in
                 either a photo viewer or matplotlib's utilities; shouldn't use this if
                 you're executing this script from command-line, unless you have some sort of
                 GUI for display

 - '-linename __(some base name for lines)__': basically to avoid typing in line names/labels
                                                 for many lines, if you set this flag with a
                                                 base line name, say "program", then for as many
                                                 lines in your graph, you'll have line labels of
                                                 "program0, program1, program2, ...". Also, if
                                                 you set the base line name as "program1", it
                                                 will begin to increment the line names from there,
                                                 so with line labels of "program1, program2, ...".

 - '-linenames __(some name1),(some name2),(...)__': ditto with the '-linename' arg, except if you
                                                         want to input custom line-names and not
                                                         want to manually type them in each time,
                                                         you can simply specify them beforehand,
                                                         IN ORDER, comma-separated (WITHOUT SPACES)
                                                         (e.g. linename1,LINENAME2, LiNeNaMe3)

 - '-slope __(int1)-(int2),(int3),(...)__'
                             OR
   '-slope __(int1)-(int2),(int3),(int4)-e__': basically computes the slope for each line in your
                                               data, for a given selection of points (first point is
                                               0, second point is 1, etc.); can simply specify the
                                               second argument to be '0-e' for the entire data range,
                                               where 'e' stands for 'till the end'.
                                               (e.g. '-regression 0,2-4,6-e' would specify the first
                                               point, the 2nd-4th points, and rest of the points from
                                               the 6th onwards as the input points to calculate the
                                               linear regression slope for each line)

 - '-o __(some filename)__' or just '__(some filename)__': output base filename; can be specified
                                                             with the -o flag or not; if there
                                                             are multiple graphs, then we name each
                                                             saved file with just an incremented
                                                             integer appended to the original "base"
                                                             filename; if ommitted altogether, will
                                                             just use "1", "2", "3", etc. as the
                                                             filenames; if no extension in the
                                                             filename provided, default is to save
                                                             it in a .png file format.
'''
####################################################################################################
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

def userInput(prompt, vers3):
    if vers3:
        return input(prompt)
    else:
        try:
            return raw_input(prompt)
        except NameError:
            print("Wrong input function based on version.")
            pass
#Only splits by ',' and '-'
def splitParse(string):
    temp = string.split(",")
    output = []
    for o in range(len(temp)):
        if "-" in temp[o]:
            hyphenated = temp[o].split("-")
            if len(hyphenated) != 2:
                print("Incorrect formatting of ranges!")
                sys.exit()
            output.append((hyphenated[0],hyphenated[1]))
        else:
            output.append(temp[o])
    return output
######################################################################


######################################################################
def makeGraph(data, flags, opts, is3, appendToFilename=""):
    if len(flags[opts["select"]]) > 0:
        selection = flags[opts["select"]]
    else:
        if flags[opts["axis"]]:
            selection = [i for i in range(len(data[int(round(len(data)/2.0))]))]
        else:
            selection = [i for i in range(len(data))]

    #In case someone forgot, I just do it for them
    if flags[opts["xaxis"]] and 0 not in selection:
        selection.insert(0, 0)
    ### FirstLabel, Axis,  
    lineNames = []
    lineData = []
    if flags[opts["firstlabel"]]:
        if flags[opts["axis"]]:
            begin = 0
            if not any([isFloat(x) for x in data[0]]):
                increment = 0
                while not (True not in [isFloat(x) for x in data[increment]] and any([isFloat(x) for x in data[(increment+1)]])):
                    increment += 1
                    if increment > (len(data)-1):
                        print("Something went wrong with parsing the data, with flags of -firstlabel and -c set.")
                        return
                begin = increment + 1
            lineNames = [data[begin][n] for n in range(len(data[begin])) if n in selection and len(data[begin][n]) > 0]
            for i in selection:
                lineData.append([])
                for j in range(begin, len(data)):
                    lineData[-1].append(float(data[j][i]))
        else:
            if any([isFloat(x) for x in data[0]]):
                start = 0
            else:
                start = 1
                while not any([isFloat(x) for x in data[start]]):
                    start += 1
                    if start > (len(data)-1):
                        print("Something went wrong with parsing the data, with flags of -firstlabel and -r set.")
                        return
            lineNames = [data[w][0] for w in range(start, len(data)) if w in selection and len(data[w][0]) > 0]

            for l in range(start, len(data)):
                if l in selection:
                    lineData.append([float(d) for d in data[l][1:]])
    else:
        if flags[opts["axis"]]:
            begin = 0
            if not any([isFloat(x) for x in data[0]]):
                increment = 0
                while not (True not in [isFloat(x) for x in data[increment]] and any([isFloat(x) for x in data[(increment+1)]])):
                    increment += 1
                    if begin > (len(data)-1):
                        print("Something went wrong with parsing the data, with flags of -c set.")
                        return
                begin = increment-1
            for i in selection:
                lineData.append([])
                for j in range(begin, len(data)):
                    lineData[-1].append(float(data[j][i]))
        else:
            if any([isFloat(x) for x in data[0]]):
                start = 0
            else:
                start = 1
                while not any([isFloat(x) for x in data[start]]):
                    start += 1
                    if start > (len(data)-1):
                        print("Something went wrong with parsing the data, with flags of -r set.")
                        return
            startingColumn = 0
            while not isFloat(data[start][startingColumn]):
                startingColumn += 1
                if startingColumn > (len(data[start])-1):
                    print("Something went wrong with parsing the data, with flags of -r set.")
                    return
            
            for l in range(start, len(data)):
                if l in selection:
                    lineData.append([float(d) for d in data[l][startingColumn:]])

    ### Exclude
    if len(flags[opts["exclude"]]) > 0:
        xp = flags[opts["exclude"]]
        xpoints = xp.split("-")
        if len(xpoints) == 0:
            xpoints = [int(w.strip()) for w in xp.split(",") if isInt(w.strip())]
        if len(xpoints) == 2:
            xpoints = [a for a in range(int(xpoints[0].strip()), int(xpoints[1].strip())+1)]
        else:
            temp = [[int(a.strip()) for a in xpoints[0].split(',')[:-1] if isInt(a.strip())] + [b for b in range(int(xpoints[0].split(',')[-1].strip()), int(xpoints[1].split(',')[0].strip())+1)]] +\
                   [[int(a.strip()) for a in xpoints[x].split(',')[1:-1] if isInt(a.strip())] + [b for b in range(int(xpoints[x].split(',')[-1].strip()), int(xpoints[x+1].split(',')[0].strip())+1)] for x in range(1, len(xpoints)-1)] +\
                   [[int(a.strip()) for a in xpoints[-1].split(',')[1:] if isInt(a.strip())]]
            flatten = []
            for t in temp:
                flatten += t
            xpoints = flatten
        #print("Excluding data points: ", xpoints)
        temp = []
        for i in range(len(lineData)):
            temp.append([])
            for j in range(len(lineData[i])):
                if j not in xpoints:
                    temp[-1].append(lineData[i][j])
        lineData = temp

    ### XAxis
    if flags[opts["xaxis"]]:
        xs = lineData[0]
        lineData = lineData[1:]
    else:
        xs = [i for i in range(1, len(lineData[0])+1)]#Maybe this needs to be 0-indexed someday... but not today!

    defaults = {'mark': 'o', 'line':'--', 'loc':2,\
                'bbox':(1.05, 1), 'bottom':0.02, 'ms':4}
                #'bbox':None
    markerShape = defaults['mark']
    lineStyle = defaults['line']
    locOption = defaults['loc']
    bboxAnchor = defaults['bbox']
    bottomRoom = defaults['bottom']
    markerSize = defaults['ms']

    ### Beauty
    if flags[opts["beauty"]]:
        print("Simply skip any options if you want the default by pressing -enter-.")
        '''
        print("\nEnter a marker shape for all lines in this graph (Default: {}) (see matplotlib docs for examples): ".format(defaults['mark']), end='')
        mark = sys.stdin.readline().strip()
        print("\nEnter a line-style for all lines in this graph (Default: {}) (see matplotlib docs for examples): ".format(defaults['line']), end='')
        linetype = sys.stdin.readline().strip()
        print("\nEnter a location option for the graph's legend (Default: {}) (see matplotlib docs for examples): ".format(defaults['loc']), end='')
        locChoice = sys.stdin.readline().strip()
        print("\nEnter a relative anchor X location for the graph's legend (Default: None) (see matplotlib docs for examples): ", end='')
        bboxAnchorX = sys.stdin.readline().strip()
        print("\nEnter a relative anchor Y location for the graph's legend (Default: None) (see matplotlib docs for examples): ", end='')
        bboxAnchorY = sys.stdin.readline().strip()
        #'''
        mark = userInput("Enter a marker shape for all lines in this graph (Default: {}) (see matplotlib docs for examples): ".format(defaults['mark']), is3)
        markerS = userInput("Enter a size for the data-point markers (Default: {}) (see matplotlib docs for examples): ".format(defaults['ms']), is3)
        linetype = userInput("Enter a line-style for all lines in this graph (Default: {}) (see matplotlib docs for examples): ".format(defaults['line']), is3)
        locChoice = userInput("Enter a location option for the graph's legend (Default: {}) (see matplotlib docs for examples): ".format(defaults['loc']), is3)
        bboxAnchorX = userInput("Enter a relative anchor X location for the graph's legend (Default: None) (see matplotlib docs for examples): ", is3)
        bboxAnchorY = userInput("Enter a relative anchor Y location for the graph's legend (Default: None) (see matplotlib docs for examples): ", is3)
        bottomR = userInput("Enter a space for room on the bottom of the graph figure, if it might get cut off (Default: {}) (see matplotlib docs for examples): ".format(defaults['bottom']), is3)
        if len(mark) != 0:
            markerShape = mark
        if len(linetype) != 0:
            lineStyle = linetype
        if len(locChoice) != 0:
            locOption = int(locChoice)
        if len(bboxAnchorX) != 0 and len(bboxAnchorY) != 0:
            bboxAnchor = (float(bboxAnchorX), float(bboxAnchorY))
        if len(bottomR) != 0:
            bottomRoom = bottomR
        if len(markerS) != 0:
            markerSize = markerS
            
    ##### *Begin Plotting!* #####
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for l in lineData:
        #print(lineData.index(l), l)
        line, = ax.plot(xs, l, marker=markerShape, linestyle=lineStyle, markersize=markerSize)

    ### XRange, YRange
    if flags[opts["xrange"]][0] != flags[opts["xrange"]][1]:
        print("\nX-axis Range: ", flags[opts["xrange"]])
        ax.set_xlim(flags[opts["xrange"]][0], flags[opts["xrange"]][1])
    if flags[opts["yrange"]][0] != flags[opts["yrange"]][1]:
        print("Y-axis Range: ", flags[opts["yrange"]])
        ax.set_ylim(flags[opts["yrange"]][0], flags[opts["yrange"]][1])

    ### LineName
    if not flags[opts["firstlabel"]]:
        if len(flags[opts["linename"]]) > 0:
            inputLineName = flags[opts["linename"]]
            if any(char.isdigit() for char in inputLineName):
                count = -1
                while inputLineName[count].isdigit():
                    count -= 1
                if count == -1:
                    appendInt = 0
                    offset = len(inputLineName)
                else:
                    appendInt = int(inputLineName[(count+1):])
                    offset = len(inputLineName) + count + 1
            else:
                appendInt = 0
                offset = len(inputLineName)
            for l in range(len(lineData)):
                '''
                print("\nEnter a name for line{}: ".format(li), end='')
                lineNames.append(sys.stdin.readline().strip())
                #'''
                lineNames.append(inputLineName[:offset] + str(appendInt + l))
        elif len(flags[opts["linenames"]]) > 0:
            lineNames = [lName.strip() for lName in flags[opts["linenames"]].split(",")]
        else:
            for l in range(len(lineData)):
                lineNames.append(userInput("Enter a name for line{}: ".format(l), is3))
    print("\nLabels for Lines:\n{}\n".format(lineNames))

    ### XLabel, YLabel
    if len(flags[opts["xlabel"]]) == 0:
        #print("\nX-Axis Label: ", end='')
        #ax.set_xlabel(sys.stdin.readline().strip())
        ax.set_xlabel(userInput("X-Axis Label: ", is3))
    else:
        print("X-axis label of graph is: ", flags[opts["xlabel"]])
        ax.set_xlabel(flags[opts["xlabel"]])
    if len(flags[opts["ylabel"]]) == 0:
        #print("\nY-Axis Label: ", end='')
        #ax.set_ylabel(sys.stdin.readline().strip())
        ax.set_ylabel(userInput("Y-Axis Label: ", is3))
    else:
        print("Y-axis label of graph is: ", flags[opts["ylabel"]])
        ax.set_ylabel(flags[opts["ylabel"]])

    ### Regression
    if len(flags[opts["slope"]]) > 0:
        rawdataset = splitParse(flags[opts["slope"]])
        regdataset = []
        for r in rawdataset:
            if type(r) is str and isInt(r):
                regdataset.append(int(r))
            elif type(r) is tuple and isInt(r[0]) and (isInt(r[1]) or r[1] == 'e'):
                if r[1] == 'e':
                    regdataset += [integ for integ in range(int(r[0]), len(xs))]
                else:
                    regdataset += [integ for integ in range(int(r[0]), int(r[1])+1)]
            else:
                print("Incorrect data-type formatting for ranges of slope data!")
                sys.exit()
        print("\n")
        for l in range(len(lineData)):
            print("Slope of {} line: ".format(lineNames[l]), end='')
            lineSlope = np.polyfit(np.array([xs[i] for i in range(len(xs)) if i in regdataset]),\
                                   np.array([lineData[l][i] for i in range(len(xs)) if i in regdataset]),\
                                   1)[0]
            print(lineSlope)
            lineNames[l] += " (slope {:.3f} of points {})".format(lineSlope, flags[opts["slope"]])
        print("\n")

    legend = ax.legend(lineNames, bbox_to_anchor=bboxAnchor, loc=locOption)
    
    ### Title
    if len(flags[opts["title"]]) == 0:
        #print("\nTitle of Graph: ", end='')
        #ax.set_title(sys.stdin.readline().strip())
        ax.set_title(userInput("Title of Graph: ", is3))
    else:
        print("Title of graph is: ", flags[opts["title"]])
        ax.set_title(flags[opts["title"]])

    ax.grid('on')
    fig.subplots_adjust(bottom=bottomRoom)

    ### SaveFile
    ##### *Begin Saving!* #####
    if len(flags[opts["savefile"]]) == 0 and len(appendToFilename) == 0:
        outputfilename = "graph_test1"
    else:
        filenameParts = flags[opts["savefile"]].split(".")
        if len(filenameParts) == 1:
            outputfilename = filenameParts[0] + appendToFilename + ".png"
        else:
            outputfilename = filenameParts[0] + appendToFilename + filenameParts[1]#base-name, numbering-order, extension
    fig.savefig(outputfilename, bbox_extra_artists=(legend,), bbox_inches='tight')

    print("\n\nSaved file to name {}.".format(outputfilename))
    print("####### Finished. #######\n\n")

    ### Display
    if is3 and flags[opts["display"]]:
        wwindow.open(outputfilename)
    elif flags[opts["display"]]:
        plt.show()
######################################################################


######################################################################
def main(fileData, flags, opts):
    if (sys.version_info > (3, 0)):
        is3 = True
    else:
        is3 = False

    for l in range(len(fileData)):
        fileData[l] = [w.strip() for w in fileData[l].split(",") if len(w.strip()) > 0]
    
    encountered = False
    sections = []
    for line in fileData:
        if len(line) >= 2 and not encountered:
            encountered = True
            sections.append([line])
        elif len(line) >= 2 and encountered:
            sections[-1].append(line)
        elif len(line) < 2 and encountered:
            encountered = False
    
    if flags[opts["section"]] > -1:
        makeGraph(sections[flags[opts["section"]]], flags, opts, is3)
    elif len(sections) == 1:
        makeGraph(sections[0], flags, opts, is3)
    else:
        filenameCounter = 0
        for s in sections:
            makeGraph(s, flags, opts, is3, str(filenameCounter))
            filenameCounter += 1
######################################################################




######################################################################
if __name__ == "__main__":
    args = sys.argv[1:]

    if '-help' in args or '-h' in args:
        print(commandHelp)
        sys.exit()
    
    file = args[0]
    usedArgs = [1] + [0]*(len(args)-1)

    opts = {"axis": 0, "firstlabel": 1, "section": 2, "select": 3, "xrange": 4, "yrange": 5, "xaxis": 6,\
            "title":7, "xlabel":8, "ylabel":9, "beauty":10, "display":11, "savefile":12, "linename":13,\
            "exclude":14, "linenames":15, "slope":16}
    flags = [None, False, -1, [], (0,0), (0,0), False, "", "", "", False, False, "", "", "", "", ""]

    ### Choose which axis of data to interpret as X/Y
    if '-c' in args:
        # So it means if each dimension is uniquely identified by columns, and
        # each row is a data point defined by dimensions
        flags[opts["axis"]] = True
        usedArgs[args.index('-c')] = 1
    elif '-r' in args:
        # Otherwise, each row is a series of X points, and
        # there are multiple lines in the graph, each row being a line, and
        # X-range is incremented by 1 for each column
        flags[opts["axis"]] = False
        usedArgs[args.index('-r')] = 1
    else:
        print("Incorrect formatting of axes specified.")
        sys.exit(0)

    ### Choose if the first column/row contains the respective header names for the lines
    if "-firstlabel" in args:
        flags[opts["firstlabel"]] = True
        usedArgs[args.index('-firstlabel')] = 1

    ### Pick a section of data (newline-separated) if there are multiple in the output; 0-indexed
    if "-section" in args:
        argIndex = args.index("-section")
        temp = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1
        
        if isInt(temp):
            flags[opts["section"]] = int(temp)
        else:
            print("Wrong formatting for section number!")
            sys.exit(0)

    ### Choose which rows/columns are actually plotted as lines; 0-indexed or 1-indexed depending on -first
    ### The argument after it looks like "1,4,6" for the 1st, 4th, and 6th rows/columns
    if "-select" in args:
        argIndex = args.index("-select")
        temp = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1
        #flags[opts["select"]] = [int(x) for x in temp.split(",") if isInt(x)]

        stringIndices = [x for x in temp.split(",")]
        tempIndices = []
        for ti in stringIndices:
            if "-" in ti:
                ranges = ti.split("-")
                if len(ranges) != 2 or not (isInt(ranges[0]) and isInt(ranges[1])):
                    print("Incorrect formatting for select argument!")
                    sys.exit()
                tempIndices += [str(integer) for integer in range(int(ranges[0]), int(ranges[1])+1)]
            elif isInt(ti):
                tempIndices.append(ti)
            else:
                print("Incorrect formatting for select argument!")
                sys.exit()
        
        flags[opts["select"]] = [int(x) for x in tempIndices]
    
    ### Choose x-axis range for data points
    ### The argument after it looks like "0,5000" for a range of [0, 5000] on the x-axis of the plot
    if "-xrange" in args:
        argIndex = args.index("-xrange")
        xrange = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1
        
        temp = [float(x) for x in xrange.split(",") if isFloat(x)]
        flags[opts["xrange"]] = (temp[0], temp[1])

    ### Ditto for y-axis range
    if "-yrange" in args:
        argIndex = args.index("-yrange")
        yrange = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1
        
        temp = [float(y) for y in yrange.split(",")]
        flags[opts["yrange"]] = (temp[0], temp[1])

    ### Determines if first row/column are the corresponding x-values for each line's data points
    if "-xaxis" in args:
        flags[opts["xaxis"]] = True
        usedArgs[args.index('-xaxis')] = 1

    ### Graph Title
    if "-t" in args:
        flags[opts["title"]] = args[(args.index("-t") + 1)]
        usedArgs[args.index('-t')] = 1
        usedArgs[(args.index('-t')+1)] = 1

    ### x-axis Label
    if "-x" in args:
        flags[opts["xlabel"]] = args[(args.index("-x") + 1)]
        usedArgs[args.index('-x')] = 1
        usedArgs[(args.index('-x')+1)] = 1

    ### y-axis Label
    if "-y" in args:
        flags[opts["ylabel"]] = args[(args.index("-y") + 1)]
        usedArgs[args.index('-y')] = 1
        usedArgs[(args.index('-y')+1)] = 1

    ### Flag set to determine if you want to manually enter in matplotlib graph parameters to "beautify" your graphs
    if "-beauty" in args:
        flags[opts["beauty"]] = args[args.index("-beauty")]
        usedArgs[args.index('-beauty')] = 1

    if "-display" in args:
        flags[opts["display"]] = True
        usedArgs[args.index('-display')] = 1

    if "-linename" in args:
        argIndex = args.index('-linename')
        flags[opts["linename"]] = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1
    if "-linenames" in args:
        argIndex = args.index('-linenames')
        flags[opts["linenames"]] = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1

    if "-xclude" in args:
        argIndex = args.index('-xclude')
        flags[opts["exclude"]] = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1

    if "-slope" in args:
        argIndex = args.index('-slope')
        flags[opts["slope"]] = args[(argIndex + 1)]
        usedArgs[argIndex] = 1
        usedArgs[(argIndex+1)] = 1

    ### Output base filename (base meaning, if you're trying to make multiple graphs with
    ### one execution of this script, it'll just append incremented integers to the filename
    ### for each new graph it saves)
    if "-o" in args:
        flags[opts["savefile"]] = args[(args.index("-o") + 1)]
        print("")
        print(args)
        usedArgs[args.index('-o')] = 1
    elif sum(usedArgs) == len(usedArgs)-1:
        print("")
        print(args)
        #print(usedArgs)
        for i in range(len(usedArgs)):
            if usedArgs[i] == 0:
                flags[opts["savefile"]] = args[i]
                break
    else:
        print("")
        print(args)
        print(usedArgs)
        print("\n***Warning***: should probably specify a base output filename for the saved picture...\n")
    
    try:
        data = []
        with open(file, "r") as f:
            for line in f:
                data.append(line)
    except:
        print("Could not open file/not found!")
        sys.exit(0)

    main(data, flags, opts)
    
    
