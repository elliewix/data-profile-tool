# AutoDocish: Data Profile/Documentation tool

This is a tool created as a project for the Spring 2016 GSLIS Data Cleaning course.

The products of this tool will sit somewhere between auto-documentaiton and data profiling.

## Basic purpose

Point the tool at a folder of files and it will create a markdown file with basic statistics about each column along with template areas for you to write a narrative about each column.  You can then render that into HTML or simply include it in your data package as documentation.

## Core caveats

Still mostly a proof of concept.

Path issues for windows.

Unknown bugs.

## Basic use

This was written using Python 2.7. Maybe it would work with Python 3 if I updated the print statements.  Anyhow. Run it on the command line.

`python data_profile.py source output missing_code`

`python data_profile.py vagrants/ vagrant-profiles/ [missing]`

This works out to:

* `python data_profile.py` runs the script
* `vagrants/`
	* Provide single file path or folder with many files
	* Currently only built to work with CSV data
* `vagrant-profiles/` 
	* This is the destination folder for the profile files
	* Will either create the folder or overwrite the named contents
	* Will create:
		* one JSON file with all profile data
		* one md file per source file with profile data
* `[missing]` 
	* this is the missing code, use `''` for empty
	* optional, but presumes empty string if not provided
	* cannot currently specify multiple missing values for single files

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
