# This code will process the yearly property sales data files from the NSW government website.
# The file format changed in 2001, so this assumes only data after that year.
#
# The following should be set up on your computer before running this code.
#
# 1) Download each of the yearly files. 
# 2) If a year is incomplete and there is no single yearly file, download the individuals then zip them up into a yearly file.
# 3) Choose an empty directory to act as the root. Set the dirRoot variable to the path of that directory.
# 4) Create a "Files" sub-directory with the the root directory and place all of the yearly zip files in that folder.
# 
# Notes:
# 
# - All other directories will be created at run-time if they do not already exist.
# - The output file, Combined.txt, will be placed in a directory called "Extracts3" on the root directory.

import zipfile
import os
import datetime

dirRoot     = 'E:\Data'
dirDATFiles = dirRoot + '\Files'
dirExtract1 = dirRoot + '\Extract1'
dirExtract2 = dirRoot + '\Extract2'
dirExtract3 = dirRoot + '\Extract3'
outFile     = dirExtract3 + '\Combined.txt'

#-------------------------------------------------------------------------------------
# Log a message.
#-------------------------------------------------------------------------------------
def log(msg):
    timeStamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(timeStamp + ': ' + msg)


#-------------------------------------------------------------------------------------
# Check to see if the directory exists. If not, create it.
#-------------------------------------------------------------------------------------
def createDir(dirPath):
    dirExists = os.path.exists(dirPath)
    if not dirExists:
        os.makedirs(dirPath)


#-------------------------------------------------------------------------------------
# Process the files.
#-------------------------------------------------------------------------------------

log("Starting to process top level zip files")

# Create all the directories if they don't already exist.
createDir(dirExtract1)
createDir(dirExtract2)
createDir(dirExtract3)

# Change the working directories.
os.chdir(dirExtract1)

# Loop through year files in the DAT file directory.
for filename in os.listdir(dirDATFiles):
    fName = os.path.join(dirDATFiles, filename)

    if zipfile.is_zipfile(fName):
        # Valid zip file so open it.
        with zipfile.ZipFile(fName, 'r') as zFile:
            # Extract all the files. 
            log ("Unzipping '" + fName + "'")
            zFile.extractall()
    
    else:
        log ("Not a zip file: '" + fName + "'")

log("Finished processing top level zip files.")

# Now that all year files have been extracted, loop through each year folder and extract the zip files.

# Change the working directory.
os.chdir(dirExtract2)

log("Starting to process sub-folder zip files.")

for filename in os.listdir(dirExtract1):
    fName = os.path.join(dirExtract1, filename)
    log("Procssing sub-folder '" + fName + "'")

    if os.path.isdir(fName):
        # This should be a year directory. Loop through and extract all zip files.
        for filename2 in os.listdir(fName):
            filenameZip = os.path.join(fName, filename2)

            if zipfile.is_zipfile(filenameZip):
                # Valid zip file so open it.
                with zipfile.ZipFile(filenameZip, 'r') as zFile:
                    # Extract all the files. 
                    log ("Unzipping '" + filenameZip + "'")
                    zFile.extractall()
            
            else:
                log ("Not a zip file: '" + filenameZip + "'")  
    
    else:
        log ("Not a directory: '" + fName + "'")  

log("Finished processing sub-folder zip files.")

# Now loop through all the DAT files, open them, read the B records, then write to the combined output file.

# Open the output file and write a line containing the field names.
out = open(outFile, 'w') 
colHeader = "Record Type;District Code;Property ID;Sale Counter;Download Datetime;Property Name;Unit Number;House Number;Street Name;Locality;Post Code;Area;Area Type;Contract Date;Settlement Date;Purchase Price;Zoning;Nature of Property;Primary Purpose;Strata Lot Number;Component Code;Sale Code;Interest Percent;Dealing Number;Unknown Field"
out.write(colHeader)
out.write("\n")

# Loop through all the individual files (should be almost all DAT files).
for filename in os.listdir(dirExtract2):
    fName = os.path.join(dirExtract2, filename)
    
    if os.path.isfile(fName):
        # Valid file, check to see if it's a DAT file.
        if fName[-3:].lower() == "dat":
            log("Procssing file '" + fName + "'")

            # Open the file and begin reading it.
            readFile = open(fName, "r")
            lines = readFile.readlines()
  
            # Read each line in the file and process B records.
            for line in lines:
                if line[0:1] == "B":
                    # This is B record so write it to the file.
                    out.write (line)
        
        else:
            log ("Not a dat file, skipping: '" + fName + "'")    

log("Finished writing the combined file.")