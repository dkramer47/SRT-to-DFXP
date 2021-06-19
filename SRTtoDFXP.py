import os
import glob
import time
from datetime import datetime

offset=0

def str_data_to_num(str_data):
    rtnValue=0
    rtnValue=(datetime.strptime(str_data+'000', '%H:%M:%S,%f') - datetime.strptime('00', '%H')).total_seconds()*1000
    rtnValue=int(rtnValue+offset)*10000
    return str(rtnValue)+"t"

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

    # newFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<tt xml:lang='en' xmlns='http://www.w3.org/2006/10/ttaf1' xmlns:tts='http://www.w3.org/2006/10/ttaf1#style'>\n<head></head>\n<body>\n<div xml:id=\"captions\">\n")
    newFile.write('''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<tt xmlns:tt="http://www.w3.org/ns/ttml" xmlns:ttm="http://www.w3.org/ns/ttml#metadata" xmlns:ttp="http://www.w3.org/ns/ttml#parameter" xmlns:tts="http://www.w3.org/ns/ttml#styling" ttp:tickRate="10000000" ttp:timeBase="media" xmlns="http://www.w3.org/ns/ttml">
<head>
<ttp:profile use="http://netflix.com/ttml/profile/dfxp-ls-sdh"/>
<styling>
<style tts:color="white" tts:fontSize="100%" tts:fontWeight="normal" xml:id="s1"/>
<style tts:color="white" tts:fontSize="100%" tts:fontStyle="italic" tts:fontWeight="normal" xml:id="s1_1"/>
</styling>
<layout>
<region tts:displayAlign="after" tts:extent="80.00% 80.00%" tts:origin="10.00% 10.00%" tts:textAlign="center" xml:id="bottomCenter"/>
<region tts:displayAlign="before" tts:extent="80.00% 80.00%" tts:origin="10.00% 10.00%" tts:textAlign="center" xml:id="topCenter"/>
</layout>
</head>
<body>
<div xml:space="preserve">\n''')
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
                # times = (line.replace(",", ".")).split("-->")
                # newFile.write("<p begin=\"" + times[0].strip() + "\" end=\"" + times[1].strip() + "\">")
                times = line.replace(" ", "").split("-->")
                newFile.write("<p begin=\"" + str_data_to_num(times[0]).strip() + "\" end=\"" + str_data_to_num(times[1]).strip() + "\" region=\"bottomCenter\" style=\"s1\" xml:id=\"subtitle"+str(section-2)+"\">")

            elif sectionLine > 2:
                newFile.write("<br />" + line)
                
            elif sectionLine > 1:
                newFile.write(line)

    newFile.write("</p>\n</div>\n</body>\n</tt>")

    srtFile.close()
    newFile.close()
