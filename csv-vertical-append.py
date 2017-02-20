import sys

comments = '''
This script basically just takes a list of csv files (hopefully all of the same
length in terms of # of lines) and appends them into some specified output file,
comma-separated and neatly formatted. Great for aggregating vertical data into
a table. (Could even be some .txt file -- but it delimits by ","!)

Run like so:

    python csv-vertical-append.py SOME_FILE1.csv SOME_FILE2.csv SOME_FILE3.txt
        -o aggregate_data_file.csv

Example:
SOME_FILE1.csv:
    100,200
    200,400
    300,800

SOME_FILE2.csv:
    , hello! ,
    
    , 105 ,
    , 110 ,
    , 115 ,

SOME_FILE3.csv:
    ,1000
    , 200
    560
    480

Running the above example command gets you the following file:
aggregate_data_file.csv:
    100,200,105,1000
    200,400,110,200
    300,800,115,560

'''

def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def getFileContent(filename):
    return open(filename, 'r').readlines()

def firstLine(filename):
    contents = getFileContent(filename)
    while not any([isFloat(w.strip()) for w in contents[0].split(",")]):
        contents.pop(0)
    return contents

def processNums(filename):
    contents = firstLine(filename)
    for c in range(len(contents)):
        processed = [w.strip() for w in contents[c].split(",")]
        contents[c] = [n for n in processed if isFloat(n)]
    return contents

if __name__ == '__main__':
    args = sys.argv[1:]
    data = []

    if "-h" in args or "-help" in args:
        print(comments)
        sys.exit()

    if "-o" not in args:
        print("Need an output file to write the aggregated data!")
        sys.exit()
    else:
        argIndex = args.index("-o")
        output = args[(argIndex+1)]
        args.pop(argIndex)
        args.pop(argIndex)

    print("List of files to append together:\n", args)
    for files in args:
        data.append(processNums(files))

    outputData = []
    columnLengths = [len(data[x]) for x in range(len(data))]
    print("Column Lengths of Vertical Data to Append: ", columnLengths)
    numDataPoints = min(columnLengths)
    
    for j in range(numDataPoints):
        outputData.append([])
        for i in range(len(args)):
            outputData[-1] += data[i][j]

    for x in range(len(outputData)):
        outputData[x] = ",".join(outputData[x])

    with open(output, 'w') as f:
        f.write("\n".join(outputData))
        f.close()
    
