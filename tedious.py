import sys

#############################################
'''
***NOTE***: Tabs and spaces will be counted as individual characters as well!
            However, newline characters do not count as characters, and even
            when they're encapsulated in strings, they're counted as 2 separate
            characters when parsing through.

##### Referred Example Text/Program: #####

    //1\tABCDEFG\n
    //2\n
    //3\n
    //4\t\t\tHELLO WORLD\n
    //5\t\t\tprintf("Goodbye cruel world")\n
    //6\n
    //7print("5.6")\n
    //8\sTrue,false

##### Flag Options #####

(What is O1/O2/O3/O4? See "Task-Argument Formats" section.)

- '-rchar O1/O2 O3 O1/O2 O3 (...)':
            Begins parsing at the specified position in the line for the
            first occurrence of a ' or " character (NOT a \' or \" string),
            and once it finds that character, it proceeds to replace the
            entire string found from thereon out (i.e., between that start
            position until the next respective closing ' or " character
            is found) with whatever you've inputted for O3. Allows for
            multiple arguments/replacements to occur after "-rchar" to be
            executed simultaneously.

        E.g. -rchar 5-22 "\"Hello good world\"" ==>
                 \t\t\tprintf(""Hello good world"")\n
                 
             -rchar 5-22 "\\\"Hello good world\\\"" ==>
                 \t\t\tprintf("\"Hello good world\"")\n
                 
             -rchar 5-22 "Hello good world" ==>
                 \t\t\tprintf("Hello good world")\n

             -rchar 5-"'\"Goodbye cruel'" "Hello" == -rchar 5-"'\"Goodbye'" Hello ==>
                 \t\t\tprintf("Hello")\n

             -rchar 5-"'Goodbye'" "Hello" ==>
                 ERROR -- because it began searching at:
                     \t\t\tprintf("<HERE>Goodbye cruel world")\n
                 from <HERE> on, it only finds one " character, which is
                 therefore not a string

- '-ins O1/O2 O3 O1/O2 O3 (...)':
            At the specified starting position, it inserts the O3 text
            specified.Allows for multiple arguments/replacements to occur
            after "-ins" to be executed simultaneously.

        E.g. -ins 5-22 "\"Hello" ==> \t\t\tprintf("Hello"Goodbye cruel world")\n


- '-del O1/O2 O1/O2 O1/O2 O1/O2 (...)':
            Begins parsing at the specified position in the first O1/O2
            of each (O1/O2 O1/O2) pair, and then based on the second O1/O2
            in the pair and interpreting that as another position, it simply
            deletes all characters between that range, ends exclusive. Allows
            for multiple arguments/replacements to occur after "-del" to be
            executed simultaneously.
            
            (Be careful! The second O1/O2 arg in a pair, if specifying the
            same line, should have its (# char from end) variable as LESS
            than the first O1/O2 arg's (# char from end) variable -- since
            we're counting from the end! If it's >= than the first's, my
            program throws an error!)

        E.g. -del 5-22 5-16 ==> \t\t\tprintf(ye cruel world")\n

             -del 5-22 5-28 ==> ERROR!
            
- '-rflo O1/O2 O3 O1/O2 O3 (...)':
            Begins parsing at the specified position in the line for the
            first occurrence of a float, either starting with a "." and
            trailing with digits immediately after or starting with a digit
            itself. Allows for multiple arguments/replacements to occur
            after "-rflo" to be executed simultaneously.

            (Be careful! It searches ONLY for floats/doubles with a decimal
            somewhere in the character -- if it doesn't find a decimal, it
            will return an error! Also, it does not search for long data types
            if it has some kind of specifier (like in Python, a "3.5L" is a
            long, but my program would only parse up to "3.5"))

        E.g. -rflo 7-"'\"5'" 7.8 ==> print("7.8")\n

             -rflow 7-"'6'" 7.8 ==> ERROR!

- '-rint O1/O2 O3 O1/O2 O3 (...)':
            Begins parsing at the specified position in the line for the
            first occurrence of a digit, starting with a digit character and
            ending at any non-digit character. Allows for multiple
            arguments/replacements to occur after "-rint" to be executed
            simultaneously.

        E.g. -rint 7-"'\"5'" 506 == -rint 5-"'5'" "506" ==> print("506.6")\n

- '-rbool O1/O2 O1/O2 O1/O2 (...)':
            Begins parsing at the specified position in the line for the
            first occurrence of a word that says "True", "true", "False", or
            "false", and simply flips it to the opposite value. Allows for
            multiple arguments/replacements to occur after "-rbool" to be
            executed simultaneously.

        E.g. -rbool 8-s ==> \sFalse,false

             -rbool 8-s+2 ==> \sTrue,true

- '-delall O1/O2 O3 O1/O2 O3 (...)':
            Begins parsing at the specified position in the line, and from
            thereon out, within the same line, it deletes all occurrences
            of the specified arg O3. Allows for multiple arguments/replacements
            to occur after "-delall" to be executed simultaneously.

        E.g. -delall 5-s "o" ==> \t\t\tprintf("Gdbye cruel wrld")\n

             -delall 5-s "\t" ==> printf("Goodbye cruel world")\n

- '-insall O1/O2 O3/O4 O3 O1/O2 O3/O4 O3 (...)':
            Of the triplet argument options for a single task (O1/O2 O3/O4 O3),
            it begins parsing at the specified position in the line in the the
            first of the triplet, then at specified occurrences of a string (O3)
            OR at specified integer-offsets (O4) from the specified position in
            the first argument, it proceeds to insert the third triplet argument
            at those positions in the line. Allows for multiple
            arguments/replacements to occur after "-insall" to be executed
            simultaneously.

        E.g. -insall 7-s "\"" "\"Hi" ==> print("Hi5.6"Hi)\n

             -insall 1-s 2,3,4,5,6,7 "_" == -insall 1-s 2thr5*1,6,7 "_" ==>
                 \tA_B_C_D_E_F_G\n

             -insall 1-s 2thr

- '-incr __(some integer)__ O1/O2 O4 __(some integer)__ O1/O2 O4 (...)':
            #Also, it implicitly just finds the next integer like -rint
            #First argument __(some integer)__ is how much to increment by;
                if it's only by 1, you must specify 1
             
##### Task-Argument Formats #####

==> O1 = __(line #)-(# char from end)__
                    OR
         __(line #)-s__
                    OR
         __(line #)-s+(some integer)__

        E.g.:   5-0     ==>     \t\t\tprintf("Goodbye cruel world")<HERE>\n
        
                5-1     ==>     \t\t\tprintf("Goodbye cruel world"<HERE>)\n
                
                5-2     ==>     \t\t\tprintf("Goodbye cruel world<HERE>")\n

                5-s     ==>     <HERE>\t\t\tprintf("Goodbye cruel world")\n

                5-s+3   ==>     \t\t\t<HERE>printf("Goodbye cruel world")\n
        
        (Note: line # is 1-indexed, # char from end/start is 0-indexed!)
    
==> O2 = __(line #)-"'(...exact piece of text to begin at...)'"__

        E.g.:   5-"'Goodbye cruel world'" ==>
                    \t\t\tprintf("<HERE>Goodbye cruel world")\n
                    
                5-"'\"Goodbye cruel world\"'" ==>
                    \t\t\tprintf(<HERE>"Goodbye cruel world")\n
        
==> O3 = __"(...some text...)"__

==> O4 = __(some integer),(some integer),(...)__
                     OR
         __(some integer1)thr(some integer2 > integer1)*(some integer)__
                     OR
         __(combine the above 2 syntaxes!)__

        E.g.:   5,6,9,167

                5thr21*1    ==> 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21

                2thr12*2,18,19,20thr30*10    ==> 2,4,6,8,10,12,18,19,20,30
                
        (Note: if it's 2thr12*1, the ends are inclusive so it also adds the
            specified text at the end-offset of 12; if it's 2thr12*6, it only
            adds up to, but not exceeding, the end of the range -- so it would
            only add text at offsets of 2,8.)
        (Note: This argument is NOT space-separated!!! ONLY commas!)
'''




commandHelp = '''

'''
#############################################



if __name__ == "__main__":
    args = sys.argv[1:]

    if '-help' in args or '-h' in args:
        print(commandHelp)
        sys.exit()

    if len(args) == 1:
        print("Need more arguments, try using \'-h\' to see options.")
        sys.exit()

    opts = {"-f": 0, "-ext": 1, "-o": 2}
    flags = ["", "", ""]
    
    if "-f" not in args:
        filename = args[1]
    else:
        toFind = "-f"
        argIndex = args.index(toFind)
        flags[opts[toFind]] = args[(argIndex+1)]
        filename = flags[opts[toFind]]

    if "-ext" not in args and len(filename.split(".")) < 2:
        print("Must specify extension for output program or have input program with some extension!")
        sys.exit()
    elif "-ext" not in args:
        flags[opts["-ext"]] = filename.split(".")[-1]
        extension = flags[opts["-ext"]]
    else:
        toFind = "-ext"
        argIndex = args.index(toFind)
        flags[opts[toFind]] = args[(argIndex+1)]
        extension = flags[opts[toFind]]
        

    try:
        f = open(filename, "r")
    except:
        print("Could not open file/file was not found!")
        sys.exit()

    pseudo = f.readlines()

    if "-o" not in args:
        base = filename.split(".")
        if len(base) > 1:
            base = ".".join(base[:-1])
        else:
            base = base[0]
        if extension[0] == ".":
            output = base + "-changed" + extension
        else:
            output = base + "-changed." + extension
    else:
        toFind = "-o"
        argIndex = args.index(toFind)
        flags[opts[toFind]] = args[(argIndex+1)]
        output = flags[opts[toFind]]
        if "-ext" in args:
            if extension[0] == ".":
                output += extension
            else:
                output += "." + extension

    






















    
