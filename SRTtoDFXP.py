import os
import glob

gettingPath = True
while gettingPath:
    path = input("Enter the path to the file or folder of files you want to convert: \n")

    if not os.path.exists(path):
        print("No such path exists.\n")
    else:
        gettingPath = False

files = glob.glob(os.path.join(path, '*.srt'))
pathArray = path.split("\\")

try:
    
    if len(files) == 0:
        oldFilename = pathArray[len(pathArray) - 1]

        if oldFilename[-4:] == ".srt":
            files = [path]

        path = path.replace(oldFilename, "")
        
    os.mkdir(path + "\\converted")

except FileExistsError:
    pass

for filepath in files:

    filesArray = filepath.split("\\")
    fileName = filesArray[len(filesArray) - 1]

    newFile = open(path + "\\converted\\" + fileName.replace("srt", "dfxp"), "a", encoding="utf-8-sig")
    srtFile = open(filepath, "r", encoding="utf-8-sig")

    newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<tt xml:lang='en' xmlns='http://www.w3.org/2006/10/ttaf1' xmlns:tts='http://www.w3.org/2006/10/ttaf1#style'>\n<head></head>\n<body>\n<div xml:id=\"captions\">\n")

    section = 1
    sectionLine = 0

    for line in srtFile:

        line = line.strip()

        if line != "":

            if line.isdigit() and int(line) == section:

                if section != 1: newFile.write("</p>\n")

                section += 1
                sectionLine = 0

            else:
                sectionLine += 1

            if sectionLine == 1:
                times = (line.replace(",", ".")).split("-->")
                newFile.write("<p begin=\"" + times[0].strip() + "\" end=\"" + times[1].strip() + "\">")

            elif sectionLine > 2:
                newFile.write("<br />" + line)
                
            elif sectionLine > 1:
                newFile.write(line)

    newFile.write("</p>\n</div>\n</body>\n</tt>")

    srtFile.close()
    newFile.close()