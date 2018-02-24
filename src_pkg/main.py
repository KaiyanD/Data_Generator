# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 14:59:51 2017

@author: kading
"""
## Change the working directory to be main folder.
import sys
import time
import os, shutil

sys.path.insert(0, os.path.abspath(os.curdir))
from src_pkg.generate import *
# Provide the path to the schema.
rootpath = os.path.dirname(setup.path()) + "\\testdatageneration\\"
outputtestdata = rootpath + "output\\"

allTestDataFlder = os.listdir(outputtestdata)
allTestDataFlder.remove("dummy")
for the_file in allTestDataFlder:
    file_path = os.path.join(outputtestdata, the_file)
    try:
        if os.path.isfile(outputtestdata):
            os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)


start_time = time.time()
# Run the genertor.
if __name__ == "__main__":
    # *****code added as part of NSRP 1038
    # *****get all schema names from schemas folder and reorder to put header schemas first in the list
    ls_schema = os.listdir(rootpath + "input")
    if "Product_Mixed_Pack_Header.json" in ls_schema:
        Mixed_Pack_Table_Option = 1
    else:
        Mixed_Pack_Table_Option = 0
    #removing the test json file since this is not needed for real test. This is only for unit test.
    ls_schema = [x for x in ls_schema if x not in ["Product_Mixed_Pack_Header.json","bottlername.csv","dataCount.json"]]
    for x in ls_schema:
        if(x.find("Header") == -1):
            ls_schema.append(x)
            ls_schema.remove(x)

    '''get bottler name'''
    bottlernametable = pd.read_csv(rootpath + "\\input\\bottlername.csv")
    bottlername = random.choice(bottlernametable["bottlername"])
    changer = Changer()
    filenameformater = FileNameFormater()
    ls_filenamePrefix = filenameformater.fileNameFormat(random.choice(bottlernametable["bottlername"]))
    expFileName = ls_filenamePrefix[0]
    if Mixed_Pack_Table_Option == 1:
        ls_schema.append("Product_Mixed_Pack_Header.json")

    '''Getting test data cases and creating folders if not available'''
    fpath_rowct = rootpath + "input\\dataCount.json"
    f_rowct = codecs.open(fpath_rowct, 'r', 'utf-8')
    rowcounts = json.load(f_rowct)
    f_rowct.close()
    testCaseDataFolder = [key_lvl1 for key_lvl1 in rowcounts.keys() if rowcounts[key_lvl1]["skip"] == "N"]

    '''Create test data files for each case with skip = No in dataCount.json'''
    for eachTestCaseDataFolder in testCaseDataFolder:
        '''Create the test data directory for each case'''
        if not os.path.exists(outputtestdata + eachTestCaseDataFolder):
            os.makedirs(outputtestdata + eachTestCaseDataFolder)
            print("creating test data files for %s" % eachTestCaseDataFolder)
        else:
            print(outputtestdata + eachTestCaseDataFolder + " - available")
        for eachSchema in ls_schema:
            # Read json schema
            fpath = rootpath + "input\\" + eachSchema
            f= codecs.open(fpath, 'r', 'utf-8')
            schema = json.load(f)
            table_name = schema["title"]
            dicofcols = schema["columns"]
            # Create Generator object and run to create data frame based on schema
            gen_main = Generate_Main()
            # ****Passed bottlername_Prefix for fix NSRP
            if eachSchema != "Product_Mixed_Pack_Header.json":
                table, metadata_DF, table_name, num_rows = gen_main.run(schema,expFileName,rowcounts[eachTestCaseDataFolder][table_name],outputtestdata + eachTestCaseDataFolder)
                if Mixed_Pack_Table_Option == 0 and eachSchema == "Product_Header_Schema.json":
                    table["MP_Indicator"] = ["N"] * rowcounts[eachTestCaseDataFolder][table_name]
            elif eachTestCaseDataFolder != "TD_002_Incorrect_Data_File_Name":
                table, metadata_DF, table_name, num_rows = gen_main.mixedpack(schema,expFileName,outputtestdata + eachTestCaseDataFolder)
            ## Add Null to non-mandatory fields
            table,metadata_DF = changer.add_null(dicofcols,table,metadata_DF)
            f.close()
            # Save the result table as csv encoded.
            #table.to_csv("output/%s_%s_%s.csv"% (bottlername,presenttime,table_name),index=False,encoding = "utf-8",sep=",",quoting=csv.QUOTE_ALL)
            metadata_DF.index = range(1,num_rows+1)
            #metadata_DF.to_json("output/%s_%s_metadata.json"% (expFileName,table_name),orient="index")

            # Create filecreater object to write data.
            filecreater = FileCreater(table,metadata_DF,"%s_%s" % (expFileName, table_name),outputtestdata + eachTestCaseDataFolder)
            # positive file
            if eachTestCaseDataFolder == "TD_001_Positive_Data_Files":
                filecreater.positive_Data_Files()
            ### negative case : Create files with incorrect file name format
            elif eachTestCaseDataFolder == "TD_002_Incorrect_Data_File_Name":
                for eachNegFileNm in ls_filenamePrefix[1:]:
                    filecreater.incorrect_Data_File_Name(eachNegFileNm + "_" + table_name)
            ### negative case : Add incorrect ForeignKey for the respective schemas
            elif eachTestCaseDataFolder == "TD_003_Incorrect_Foreign_Key":
                filecreater.incorrect_Foreign_Key(dicofcols)
            ### negative case 1.1.1: not in csv but in excel.
            elif eachTestCaseDataFolder == "TD_004_Incorrect_File_Format_XLS":
                filecreater.incorrect_File_Format_XLS()
            ### negative case 1.1.2: not in csv but in txt.
            elif eachTestCaseDataFolder == "TD_005_Incorrect_File_Format_TXT":
                filecreater.incorrect_File_Format_TXT()
            ### negative case 8: traditional Chinese to string
            elif eachTestCaseDataFolder == "TD_006_Traditional_Chinese_Data_Included":
                filecreater.neg_addspecialcharactertostring(dicofcols, "Traditional Chinese")
            ### negative case 8: simplified Chinese to string
            elif eachTestCaseDataFolder == "TD_007_Simplified_Chinese_Data_Included":
                filecreater.neg_addspecialcharactertostring(dicofcols, "Simplified Chinese")
            ### negative case 8: Spanish to string
            elif eachTestCaseDataFolder == "TD_008_Spanish_Data_Included":
                filecreater.neg_addspecialcharactertostring(dicofcols, "Spanish")
            ### negative case 8: German to string
            elif eachTestCaseDataFolder == "TD_009_German_Data_Included":
                filecreater.neg_addspecialcharactertostring(dicofcols, "German")
            ### negative case 1.2: not comma separated.
            elif eachTestCaseDataFolder == "TD_010_Incorrect_Format_Not_Comma_Separated":
                filecreater.incorrect_Format_Not_Comma_Separated()
            ### negative case 3: not double quoted.
            elif eachTestCaseDataFolder == "TD_012_Incorrect_Format_Not_Double_Quoted":
                filecreater.incorrect_Format_Not_Double_Quoted()
            ### negative case 2: not utf-8.
            elif eachTestCaseDataFolder == "TD_013_Incorrect_Format_Not_UFT8":
                filecreater.incorrect_Format_Not_UFT8()
            ### negative case 5: thousand separater as comma
            elif eachTestCaseDataFolder == "TD_014_Incorrect_Format_Thousand_Comma_Separator":
                filecreater.incorrect_Format_Thousand_Comma_Separator(dicofcols)
            ### negative case 6: decimal separater as comma
            elif eachTestCaseDataFolder == "TD_015_Incorrect_Format_Thousand_Decimal_Separator":
                filecreater.incorrect_Format_Thousand_Decimal_Separator(dicofcols)
            ### negative case: not_in_option to categorical field
            elif eachTestCaseDataFolder == "TD_016_Incorrect_Optional_Category":
                filecreater.incorrect_Optional_Category(dicofcols)
            ### negative case 7: null to mandatory as ''
            elif eachTestCaseDataFolder == "TD_017_Incorrect_Data_Blank_Mandatory_Value":
                filecreater.incorrect_Data_Blank_Mandatory_Value(dicofcols)
            ### negative case 7: null to mandatory as 'Null'
            elif eachTestCaseDataFolder == "TD_018_Incorrect_Data_NULL_Mandatory_Value":
                filecreater.incorrect_Data_NULL_Mandatory_Value(dicofcols)
            ### negative case 7: null to mandatory as ' '
            elif eachTestCaseDataFolder == "TD_019_Incorrect_Data_Space_Mandatory_Value":
                filecreater.incorrect_Data_Space_Mandatory_Value(dicofcols)
            ## negative case: incorrect code with special characters
            elif eachTestCaseDataFolder == "TD_020_Incorrect_String_Code":
                filecreater.incorrect_String_Code(dicofcols)
            ### negative case: contains more length than max length for string fields like sentence,word,address and city
            elif eachTestCaseDataFolder == "TD_021_Incorrect_String_Length":
                filecreater.incorrect_String_Length(dicofcols)
            ### negative case: contains incorrect language and punctuations for string fields like sentence,word,address and city
            elif eachTestCaseDataFolder == "TD_022_Incorrect_String_Language_wPunctuation":
                filecreater.incorrect_String_Language_wPunctuation(dicofcols)
            ### negative case: contains more length than max length for state,country,postalcode and curruency fields
            elif eachTestCaseDataFolder == "TD_023_Incorrect_String_Address_Currency_Length":
                filecreater.incorrect_String_Address_Currency_Length(dicofcols)
            ### negative case: contains incorrect language and punctuations for state,country,postalcode and curruency fields
            elif eachTestCaseDataFolder == "TD_024_Incorrect_String_Address_Currency_Language":
                filecreater.incorrect_String_Address_Currency_Language(dicofcols)
            ## negative case: incorrect digit code with string
            elif eachTestCaseDataFolder == "TD_025_Incorrect_Digit_Code":
                filecreater.incorrect_Digit_Code(dicofcols)
            ### negative case : Duplicate multiple primary key
            elif eachTestCaseDataFolder == "TD_026_Duplicate_Multiple_Primary_Key":
                filecreater.neg_addduplicateprimarykey(dicofcols)
            ### negative case : Add blank column data of combined primary key
            elif eachTestCaseDataFolder == "TD_027_Blank_Combined_Primary_Key":
                filecreater.neg_blankmultipleprimarykey(dicofcols)
            ### negative case : Add all possible negative/positive cases in common file
            elif eachTestCaseDataFolder == "TD_028_All_In_One":
                filecreater.all_In_One(dicofcols)

            ### ************** negative case 4: not all present.
            #elif eachTestCaseDataFolder == "":
            #   filecreater.neg_notallpresent(5)

            else:
                print(eachTestCaseDataFolder + " - invalid case")


print("--- %s seconds ---" % (time.time() - start_time))