# Useful-Python-Scripts

## List of Scripts
- graph.py
	- Basically takes in a .csv file of data you want to plot and creates a matplotlib graph figure and saves the picture to a specified output-filename.
	- Still adding more diverse options to expand the script!
	- You can run it with "python graph.py -h" to print out comments/documentation on what flags/arguments the script takes
- clip.py
	- Basically just takes in a video filename and a list of start-time_end-time arguments, an output-filename, and creates/saves a video of just the clips you specified of the original video!
	- **Requires the installation of the moviepy module!** (see https://pypi.python.org/pypi/moviepy and try "pip install moviepy")
		- Also, to initially run the script, you're required a one-time download of the ImageIO ffmpeg library -- just un-comment out the first comment near the top of the import statements in the script before running it
	- You can also run it with "python clip.py -h" to print out some helpful comments on usage
	- Still working on adding more diverse options to expand the script!

### (See respective scripts' comments for more extensive documentation on how to use them)
### (If you want to fork this repository or submit a pull-request to expand any scripts here -- go for it!)