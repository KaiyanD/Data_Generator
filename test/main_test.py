'''
Created on Oct 19, 2017

@author: kading
TO-DO
Check on how to verify date format, Country, State, City, Zip code and word and add comments to each accordingly

'''
## Change the working directory to be main folder.

import os.path
import unittest
import codecs
import json
import os
import shutil
import setup

#sys.path.insert(0, os.path.abspath(os.curdir))
#print(Path(sys.path.append(os.getcwd())).parent)
rootpath = os.path.dirname(setup.path()) + "\\testdatageneration\\"
class Main_Test(unittest.TestCase):
    def test_dataCount(self):
        print("rootpath: " + rootpath)
        f = codecs.open(rootpath + "/testdata/input/dataCount.json", 'r', 'utf-8')
        getDataCount = json.load(f)
        f.close()
        ls = [a for a in getDataCount.keys() if getDataCount[a]["skip"] == "No"]
        print(ls)
        '''for keyl1 in getDataCount.keys():
            if (getDataCount[keyl1]['skip'] == "No"):
                print("for " + keyl1 + "skip status: " + getDataCount[keyl1]['skip'])
                outputpath = rootpath + "testdata/output/"
                if not os.path.exists(outputpath + keyl1):
                    os.makedirs(outputpath + keyl1)
                    print(outputpath + keyl1 + " - created")
                else:
                    print(outputpath + keyl1 + " - found")
            else:
                print(keyl1 + " - skipped")'''
        pass

    def test_deleteTestDataFiles(self):
        outputtestdata = rootpath + "testdata\\output\\"
        allsubFlder = os.listdir(outputtestdata)
        allsubFlder.remove("dummy")
        for the_file in allsubFlder:
            file_path = os.path.join(outputtestdata, the_file)
            try:
                if os.path.isfile(outputtestdata):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
