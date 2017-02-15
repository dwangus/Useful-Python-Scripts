import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import webbrowser as wwindow

####################################################################################################
commandHelp = '''
***NOTE***: This script is only really for plotting 2D functions/lines, but can handle multiple lines for a single graph.

Options for running script:
 - 'filename.ext': input filename that will be opened; cannot be ommitted, and must be first argument after script!!!

 - '-c' or '-r': for each line's y-value points being in columns or rows; cannot be ommitted!!! (e.g., if you have a line
                     whose data points are like "1,2,3,4" for -r vs. "...,1,...\n...,2,...\n...,3,...\n...,4,..." for -c)
 
 - '-firstlabel': if the first row/column encountered during parsing a section is going to indicate the columns'/rows' label
 
 - '-section __(some integer)__': if the inputted data is broken up by blank lines/wordy text into sections,
                                    which section to choose; if left out, makes graphs for each section in data
                                    (e.g., if your data looked like "header1,header2,header3\n1,1,1\n2,3,4\n3,5,7\n\n\n\n
                                    blah blah blah\nheader4,header5,header6\n0,0,0\n5,10,15\n10,20,30", then because of all
                                    those newline characters in the middle, my script would interpret that as 2 different, 
                                    sections of data, the first being integer index 0 and the second being integer index 1)
                                    (P.S. in the example above, that would also be specified as -c for the axis-organization)
                                    
 - '-select __(int1),(int2),(...)__': which rows/columns of the given section to plot lines for (NO spaces in 2nd argument!);
                                         if ommitted, plots data for each line (interpreting different lines depending on -c/-r)
                                         
 - '-xrange __(lower limit),(upper limit)__': lower and upper range for x-axis ticks (NO spaces in 2nd argument!)
 
 - '-yrange __(lower limit),(upper limit)__': lower and upper range for y-axis ticks (NO spaces in 2nd argument!)
 
 - '-xaxis': if set, chooses the first row/column's values as the corresponding x-values for all other lines' y-values
                 (e.g. if you had -c and something like "0,5.0,6.75\n1,4.0,7.0\n2,3.0,7.25\n3,2.0,7.5", and you set this flag,
                 it would interpret the first column as the x-axis, so each other column would be interpreted as having x,y points
                 of (0,__), (1,__), (2,__), (3,__) based on the values of this first column)

 - '-t __(some title)__': graph title; if ommitted, script will prompt user to manually type it in later, for each graph

 - '-x __(some label)__': x-axis label; if ommitted, script will prompt user to manually type it in later, for each graph

 - '-y __(some label)__': y-axis label; if ommitted, script will prompt user to manually type it in later, for each graph

 - '-beauty': if you set this flag, when the time comes to create the graph, you'll be manually prompted to enter in the specifications
                for various parameters of the matplotlib utility functions; if ommitted, uses hardcoded default values/options; I'm still
                adding various options to greater manipulate specifications of the matplotlib graphs!

 - '-display': if you set this flag, will attempt to open up the saved graph-picture in either a photo viewer or matplotlib's utilities;
                 shouldn't use this if you're executing this script from command-line, unless you have some sort of GUI for display

 - '-o __(some filename)__' or just '__(some filename)__': output base filename; can be specified with the -o flag or not; if there
                                                             are multiple graphs, then we name each saved file with just an incremented
                                                             integer appended to the original "base" filename; if ommitted altogether,
                                                             will just use "1", "2", "3", etc. as the filenames; if no extension in the
                                                             filename provided, default is to save it in a .png file format.
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
        
    lineNames = []
    lineData = []
    if flags[opts["firstlabel"]]:
        if flags[opts["axis"]]:
            begin = 0
            if not any([isFloat(x) for x in data[0]]):
                while not (True not in [isFloat(x) for x in data[begin]] and any([isFloat(x) for x in data[(begin+1)]])):
                    begin += 1
                    if begin > (len(data)-1):
                        print("Something went wrong with parsing the data, with flags of -firstlabel and -c set.")
                        return
            lineNames = [data[begin][n] for n in range(len(data[begin])) if n in selection and len(data[begin][n]) > 0]
            for i in selection:
                lineData.append([])
                for j in range((begin+1), len(data)):
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
                while not (True not in [isFloat(x) for x in data[begin]] and any([isFloat(x) for x in data[(begin+1)]])):
                    begin += 1
                    if begin > (len(data)-1):
                        print("Something went wrong with parsing the data, with flags of -c set.")
                        return
            for i in selection:
                lineData.append([])
                for j in range((begin+1), len(data)):
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

    if flags[opts["xaxis"]]:
        xs = lineData[0]
        lineData = lineData[1:]
    else:
        xs = [i for i in range(1, len(lineData[0])+1)]#Maybe this needs to be 0-indexed someday... but not today!

    defaults = {'mark': 'o', 'line':'--', 'loc':2,\
                #'bbox':(1.05, 1)}
                'bbox':None}
    markerShape = defaults['mark']
    lineStyle = defaults['line']
    locOption = defaults['loc']
    bboxAnchor = defaults['bbox']

    if flags[opts["beauty"]]:
        print("Simply skip any options if you want the default by pressing -enter-.")
        mark = userInput("Enter a marker shape for all lines in this graph (Default: {}) (see matplotlib docs for examples): ".format(defaults['mark']), is3)
        linetype = userInput("Enter a line-style for all lines in this graph (Default: {}) (see matplotlib docs for examples): ".format(defaults['line']), is3)
        locChoice = userInput("Enter a location option for the graph's legend (Default: {}) (see matplotlib docs for examples): ".format(defaults['loc']), is3)
        bboxAnchorX = userInput("Enter a relative anchor X location for the graph's legend (Default: None) (see matplotlib docs for examples): ", is3)
        bboxAnchorY = userInput("Enter a relative anchor Y location for the graph's legend (Default: None) (see matplotlib docs for examples): ", is3)
        if len(mark) != 0:
            markerShape = mark
        if len(linetype) != 0:
            lineStyle = linetype
        if len(locChoice) != 0:
            locOption = int(locChoice)
        if len(bboxAnchorX) != 0 and len(bboxAnchorY) != 0:
            bboxAnchor = (float(bboxAnchorX), float(bboxAnchorY))
            
    ##### *Begin Plotting!* #####
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for l in lineData:
        line, = ax.plot(xs, l, marker=markerShape, linestyle=lineStyle)

    if flags[opts["xrange"]][0] != flags[opts["xrange"]][1]:
        ax.set_xlim(flags[opts["xrange"]][0], flags[opts["xrange"]][1])
    if flags[opts["yrange"]][0] != flags[opts["yrange"]][1]:
        ax.set_ylim(flags[opts["yrange"]][0], flags[opts["yrange"]][1])

    if not flags[opts["firstlabel"]]:
        for l in range(len(lineData)):
            lineNames.append(userInput("Enter a name for line{}: ".format(l), is3))
    print("Labels for Lines:\n{}".format(lineNames))
    legend = ax.legend(lineNames, bbox_to_anchor=bboxAnchor, loc=locOption)

    if len(flags[opts["xlabel"]]) == 0:
        ax.set_xlabel(userInput("X-Axis Label: ", is3))
    else:
        ax.set_xlabel(flags[opts["xlabel"]])
    if len(flags[opts["ylabel"]]) == 0:
        ax.set_ylabel(userInput("Y-Axis Label: ", is3))
    else:
        ax.set_ylabel(flags[opts["ylabel"]])

    if len(flags[opts["title"]]) == 0:
        ax.set_title(userInput("Title of Graph: ", is3))
    else:
        ax.set_title(flags[opts["title"]])

    ax.grid('on')

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
        fileData[l] = [w.strip() for w in fileData[l].split(",")]
    
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
            "title":7, "xlabel":8, "ylabel":9, "beauty":10, "display":11, "savefile":12}
    flags = [None, False, -1, [], (0,0), (0,0), False, "", "", "", False, False, ""]

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
        
        flags[opts["select"]] = [int(x) for x in temp.split(",") if isInt(x)]

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
        
        temp = [float(x) for x in xrange.split(",")]
        flags[opts["yrange"]] = (temp[0], temp[1])

    ### Determines if first row/column are the corresponding x-values for each line's data points
    if "-xaxis" in args:
        flags[opts["xaxis"]] = True
        usedArgs[args.index('-xaxis')] = 1

    ### Graph Title
    if "-t" in args:
        flags[opts["title"]] = args[(args.index("-t") + 1)]
        usedArgs[args.index('-t')] = 1

    ### x-axis Label
    if "-x" in args:
        flags[opts["xlabel"]] = args[(args.index("-x") + 1)]
        usedArgs[args.index('-x')] = 1

    ### y-axis Label
    if "-y" in args:
        flags[opts["ylabel"]] = args[(args.index("-y") + 1)]
        usedArgs[args.index('-y')] = 1

    ### Flag set to determine if you want to manually enter in matplotlib graph parameters to "beautify" your graphs
    if "-beauty" in args:
        flags[opts["beauty"]] = args[args.index("-beauty")]
        usedArgs[args.index('-beauty')] = 1

    if "-display" in args:
        flags[opts["display"]] = True
        usedArgs[args.index('-display')] = 1

    ### Output base filename (base meaning, if you're trying to make multiple graphs with
    ### one execution of this script, it'll just append incremented integers to the filename
    ### for each new graph it saves)
    if "-o" in args:
        flags[opts["savefile"]] = args[(args.index("-o") + 1)]
        usedArgs[args.index('-o')] = 1
    elif sum(usedArgs) == len(usedArgs)-1:
        print(usedArgs)
        print(args)
        for i in range(len(usedArgs)):
            if usedArgs[i] == 0:
                flags[opts["savefile"]] = args[i]
                break
    else:
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
    
    
