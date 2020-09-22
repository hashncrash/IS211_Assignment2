import urllib.request
import datetime
import logging
import csv
import argparse
import sys

                   
def downloadData(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.URLError as u:
        print("Reason: " + u.reason)
    except urllib.error.HTTPError as h:
        print("Reason" + h.reason)
    else:
        return html
    

def processData(html):
    
    csvfile=html.decode('utf-8')
    file = csvfile.strip().split("\n")
    reader = csv.reader(file)
    header = next(reader)
    data = []
    for row in reader:
        data.append(row)
   
    di = {}
    count=0
    for i in data:
        key = i[0]
        v1 = i[1]
        v2 = i[2]
        
        
        try:
            bday=datetime.datetime.strptime(v2, '%d/%m/%Y')
        except ValueError:
            logging.error("Error processing line " + str(count) + " for ID #:" + str(key))          
            di[key] = (v1,v2)
        else:
            di[key]=(v1,bday)
        count+=1
    
    return di

def main():

        val = input("Please neter an ID number")
        csvData = downloadData(args.url)
        personData = processData(csvData)
        
        while int(val) > 0:
            try:  
                displayPerson(val,personData)
                val = input("Please neter an ID number?")
            except:
                print("An error has occured")
                sys.exit(1)
        

def displayPerson(id, personData): 
    id=str(id)
    if id in personData.keys(): 
        print("Person " + id +" is " + personData[id][0] + " with a birthday of " + str(personData[id][1]))
    else: 
        print("No User with that id")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="URL needed")
    parser.add_argument("--url", help="The website name", type=str)
    args = parser.parse_args()

    LOG_FILENAME = "/D/Desktop/error.log"
    LOG_FORMAT = "%(message)s"
    logging.basicConfig(filename = LOG_FILENAME,
                        level = logging.ERROR,
                        format = LOG_FORMAT,
                        filemode = 'w'
                        )
    logger = logging.getLogger('assignment2')
        
    main()
