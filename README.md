# Useful-Python-Scripts

## List of Scripts
- graph.py
	- Basically takes in a .csv file of data you want to plot and creates a matplotlib graph figure and saves the picture to a specified output-filename.
	- Still adding more diverse options to expand the script!
	- You can run it with "python graph.py -h" to print out comments/documentation on what flags/arguments the script takes
	- (Note: I realized that in some Ubuntu versions, the script is a bit buggy when you try to backspace when users are prompted for input; this is fixed by (I think) updating/installing "pip install readline")
	
- clip.py
	- Basically just takes in a video filename and a list of start-time_end-time arguments, an output-filename, and creates/saves a video of just the clips you specified of the original video!
	- **Requires the installation of the moviepy module!** (see https://pypi.python.org/pypi/moviepy and try "pip install moviepy")
		- Also, to initially run the script, you're required a one-time download of the ImageIO ffmpeg library -- just un-comment out the first comment near the top of the import statements in the script before running it
	- You can also run it with "python clip.py -h" to print out some helpful comments on usage
	- Still working on adding more diverse options to expand the script!

- pypipe.py
	- Essentially just runs the commands found in a .txt file in a terminal! Like a "meta-script" that allows you to run several terminal commands in sequential order from a text file.
	- Kind of like an alternate way to pipe commands -- great for editing sequences of terminal commands in a text editor, rather than slowly and tediously on one line in the terminal.
	- Run "python pypipe.py example.txt" for a demonstration of its capacities -- examine the corresponding files/scripts specified in example.txt to understand what's happening.
	- Run "python pypipe.py -h" for comments/details/documentation

- csv-vertical-append.py
	- Just takes a few .csv files of the same length (in terms of # of lines) and appends them vertically together, comma-separated, into a specified output file (good for formatting data separated across several files into a table)
	- Basically a helper script that'll probably be commonly executed alongside **graph.py**
	- Run "python csv-vertical-append.py -h" for comments/details/documentation
	
- tedious.py
	- **NOT YET FINISHED**
	- Basically has a few commands that allows you to automate the tedious task of manually inserting/deleting large sections of code and copying/pasting tiny incremented portions of code before running each time
	- Essentially works by just specifying a position in the original code (by line and position/searched values), specifying what you want to insert/delete/change in the code, and then an output file for you to save your new code to
	- Coupled with pypipe.py, should be great for executing (that *feels* like in parallel rather than tediously sequentially) multiple versions of code to compare the outputs/results of all versions at once
	- Run "python tedious.py -h" for comments/details/documentation on optional flags and arguments to execute this script

### (See respective scripts' comments for more extensive documentation on how to use them)
### (If you want to fork this repository or submit a pull-request to expand any scripts here -- go for it!)