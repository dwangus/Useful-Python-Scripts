import subprocess
from subprocess import call
import shlex
import sys
import os
from ast import literal_eval


#######################################
comments = '''
This is a meta-script that basically takes advantage of Python's "subprocess module" and
is able to process .txt files for command-line commands and execute them!

Example: Please run 'python pypipe.py example.txt' to see what I'm talking about. See
            example.txt and savefile.txt pypipe_demo_example.py and the eventually newly-
            created file of savefile_output.txt.

You may call this script like so:

    python pypipe.py ARGUMENT_1 ARGUMENT_2 ARGUMENT_...

Each argument (needs at least 1, but not limited to the number of arguments to be
passed in) is some sort of text file that contains commands to be executed in the
terminal/shell. You can format commands to span multiple lines, and within each text file
there can be multiple commands to execute -- but multiple commands within a text file are
delimited/differentiated by at least 1 newline character, like so:

    python some_script1.py
    arg1 arg2 arg3

    python some_script2.py arg1 arg2
    arg3 arg4

If you were to name this file "execute_some_scripts.txt" and pass it into this pypipe.py
script, it would execute the first command in the .txt file
"python some_script1.py arg1 arg2 arg3" and then execute the next command in the .txt file
"python some_script2.py arg1 arg2 arg3 arg4", as though you'd literally typed those commands
yourself into the terminal and executed them one after the other.

This allows an alternate form of piping commands to be executed on a terminal/shell, with
the added benefit of being able to edit your commands in some text-editor and not worry about
having the entire command span one line, and pressing the arrow keys to slowly shift your
cursor and modify tiny portions of the command with respect to some passed-in arguments to
the script you're trying to execute -- just a whole tedious process that's hard to read and
slow to write on a terminal.

That's why I made this script! You can even write commands within text files that call, AGAIN,
pypipe.py to some other text files (as shown in the demonstration) in a recursive fashion.
Pretty meta, right?

Note: if you specify multiple commands and multiple files as arguments to pypipe.py, then
pypipe.py will essentially execute everything in the sequential order you've specified, one after
the other.

'''
#######################################

#call(["python3", "graph.py", "-h"])
#call(["ls", "-l"])
#x = subprocess.check_output(['ls', '-l'])
#x = subprocess.check_output(['python3', 'graph.py', '-h'])
#print(x.decode("utf-8"))
#print(shlex.split("-o 1 \"hello world\""))

def parseFile(filename):
    contents = open(filename, 'r').readlines()
    commands = [[]]
    for c in contents:
        if c == "\n":
            if len(commands[-1]) > 0:
                commands.append([])
        else:
            commands[-1].append(c)

    if len(commands[-1]) == 0:
        commands = commands[:-1]
    
    for c in range(len(commands)):
        intermediate = " ".join([arg.strip() for arg in commands[c]])

        '''
        #Still need to fix how shlex interprets single quotes ' the same as
        # double quotes " in that it evaluates the string inside it and not
        # the character itself (undesirable), while sys.argv interprets '
        # differently from " in that it interprets ' as characters themselves
        # and " as there being a string inside those quotes (desirable)
        # ==> Google "Shlex python differs from sys.argv when reading ' character"
        
        #Essentially gave up at making shlex work correctly with every case of ' or " quotes
        print(intermediate)

        commands[c] = shlex.split(intermediate)
        #'''
        
        if call("python3 pypipe.py -parse-pypipe_py-never-set-this-flag-intentionally " + intermediate, shell=True) != 0:
            call("python pypipe.py -parse-pypipe_py-never-set-this-flag-intentionally " + intermediate, shell=True)

        sysParsed = open("pypipe_helper_temp_ASDASD111222333_xX_Yy.txt", "r")
        commands[c] = literal_eval(sysParsed.read())
        sysParsed.close()
        os.remove("pypipe_helper_temp_ASDASD111222333_xX_Yy.txt")
            
    return commands
    

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print("Need to have at least 1 argument, of at least some .txt file with command-line commands to execute!")
        sys.exit()

    if "-parse-pypipe_py-never-set-this-flag-intentionally" in args:
        f = open("pypipe_helper_temp_ASDASD111222333_xX_Yy.txt", "w")
        f.write(str(args[1:]))
        f.close()
        sys.exit()

    if "-h" in args or "-help" in args:
        print(comments)
        sys.exit()

    #print(args)

    commands = []
    for f in args:
        commands += parseFile(f)

    #print(commands)

    #'''
    for command in commands:
        #print(subprocess.check_output(command).decode("utf-8"))
        call(command)
    #'''

    
