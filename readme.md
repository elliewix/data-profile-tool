# AutoDocish: Data Profile/Documentation tool

This is a tool created as a project for the Spring 2016 GSLIS Data Cleaning course.

The products of this tool will sit somewhere between auto-documentaiton and data profiling.

## Basic purpose

Point the tool at a folder of files and it will create a markdown file with basic statistics about each column along with template areas for you to write a narrative about each column.  You can then render that into HTML or simply include it in your data package as documentation.

## Core caveats

I haven't finished everything in the script yet and haven't fully tested this.

## Basic use

This was written using Python 2.7. Maybe it would work with Python 3 if I updated the print statements.  Anyhow. Run it on the command line.

`python data_profile.py -m vagrants/ vagrant-profiles/ [missing]`

This works out to:

* `python data_profile` runs the script
* `-m` to generate markdown output or `-h` to generate html.
	* This is not actually implemented and will just make both.
	* The HTML looks super nasty.
* `vagrants/` this is the folder with the source data
	* Currently only built to work with CSV data
* `vagrant-profiles/` this is the destination folder for the profile files
	* Does not currently make the folder if it doesn't exist, ya I need to put this in.
* `[missing]` this is the missing code, use `''` for empty
	* doesn't accept multiple missing values, but this could be done

## License

CC-BY

Fork, whack, republish, whatever. Just cite.

## Developers

Feel free to work on functions or add ons that would work with your kind of data or another format.

## Contributing

This is github, afterall.  Feel free to put in requests or issues and I'll take them into consideration.  Let me know if you'd like to collaborate on the project as well.  This is my first formal tool, so there are obvious limitations, etc.

Keep in mind, however, that this tool will be meant for an average researcher who would just want to download something and run it.  They wouldn't necessary want to use `pip` or `conda` to install.  This tool is in proof of concept mode, so criticisms are expected to be substantive and move the conversation forward.

## References

The vagrant data used as example is from:

Crymble, Adam et al.. (2015). Vagrant Lives: 14,789 Vagrants Processed by Middlesex County, 1777-1786 (version 1.1). Zenodo. [10.5281/zenodo.31026](http://dx.doi.org/10.5281/zenodo.31026).
