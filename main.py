# Parser de fichier log PV
# BDafflon - 23/04/21
# DISP-Lab UCBL
import json
from os import listdir
from os.path import isfile, join
from dateutil.parser import parse


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def parseDir(dir):
    onlyfiles = [{'file': f} for f in listdir(dir) if join(dir, f).lower().endswith('log') and isfile(join(dir, f))]

    return onlyfiles


def parseFile(directory,file):
    print(file)
    data={'file': file['file']}
    data['Test']=[]
    log = open(join(directory,file['file']),'r')
    content = log.read()
    dataContent= [[j.split(" : ") if len(j.split(" : "))>1 else j.split(" = ") for j in i.split('\n')[1:]] for i in content.split("******* Démarrage test G7 A180L") if len(i)>1]


    for i,v in enumerate(dataContent):
        dataDict={}
        dataDict['message']=[]
        for j in v:

            if len(j)>1:
                if is_date(j[0]):
                    if 'Erreur' in j[1]:
                        dataDict['message'].append({'date':j[0],'message':j[1]})
                else:
                    dataDict[j[0]]=j[1]
        data['Test'].append(dataDict)
    return data


def log(dir, data):
    f = open(join(dir,"extract.json"),'w')
    json.dump(data, f)
    f.close()


if __name__ == '__main__':
    #configuration
    directory = './data/Log/Log/'

    files = parseDir(directory)
    data = [ parseFile(directory,i) for i in files]
    print(data)
    log(directory,data)

