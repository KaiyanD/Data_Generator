# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 14:39:42 2017

@author: kading
"""

# Import all dependencies.
import csv
import itertools
import json
from src_pkg.core import *
import config
rootpath = os.path.dirname(setup.path()) + "\\testdatageneration\\"


class Generate_Main:
    
    def run(self,schema,bottlername_prefix,num_rows,fk_rootpath):
        
        # Create the generator object.
        gen = Generator()

        # Create data frame to store fake data and metadata
        table = pd.DataFrame()
        metadata_DF = pd.DataFrame()
        # Provide the number of rows
        # Read table title and table columns
        table_name = schema["title"]
        col_dics = schema["columns"]
        
        # Read through the columns dictionary
        for col_dic in col_dics:
            # Read column name
            field_name = col_dic["name"]
            meta = ["P"]*num_rows
            # Read through each dictionary, for different type use different function to generate a list of data
            if col_dic["type"] == "String":
                if col_dic["sub-type"] == "Code":
                    ls = gen.generate_ls_code(col_dic["max_length"],num_rows,col_dic["partofKey"])
                elif col_dic["sub-type"] == "Sentence":
                    ls = gen.generate_ls_sentence(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "Word":
                    ls = gen.generate_ls_word(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "Address":
                    ls = gen.generate_ls_address(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "Currency":
                    ls = gen.generate_ls_currency(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "City":
                    ls = gen.generate_ls_city(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "State":
                    ls = gen.generate_ls_state(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "Country":
                    ls = gen.generate_ls_country(col_dic["max_length"],num_rows)
                elif col_dic["sub-type"] == "Postal_Code":
                    ls = gen.generate_ls_postalcode(col_dic["max_length"],num_rows)
            elif col_dic["type"] == "Y/N":
                ls = gen.generate_ls_yn(num_rows)
            elif col_dic["type"] == "Datetime":
                ls = gen.generate_ls_datetime(col_dic["format"],num_rows)
            elif col_dic["type"] == "Integer":
                if col_dic["sub-type"] == "Code":
                    ls = gen.generate_ls_digitcode(col_dic["max_length"],num_rows)
            elif col_dic["type"] == "Decimal":
                if col_dic["sub-type"] == "Latitude":
                    ls = gen.generate_ls_latitude(num_rows)
                elif col_dic["sub-type"] == "Longitude":
                    ls = gen.generate_ls_longitude(num_rows)
                elif col_dic["sub-type"] == "Decimal(18,5)":
                    ls = gen.generate_ls_decimal(num_rows)
            elif col_dic["type"] == "Foreign_Key":
                # ***code added for fix NSRP 1110
                # ***updated schema json "refertotable" element by removing "Header" and removing "_" and all text in lowercase
                if (fk_rootpath.endswith("TD_002_Incorrect_Data_File_Name")):
                    getIncorrectFileNames = [x.replace("__channel.csv", "") for x in os.listdir(fk_rootpath) if x.endswith("__channel.csv")]
                    for eachIncorrectFileName in getIncorrectFileNames:
                        referToTableCSV = eachIncorrectFileName + "__" + col_dic["refertotable"]
                        ls = gen.generate_ls_foreignkey(col_dic["name"], referToTableCSV, col_dic["refertocol"],num_rows, fk_rootpath)
                else:
                    referToTableCSV = bottlername_prefix + "_" + col_dic["refertotable"]
                    ls = gen.generate_ls_foreignkey(col_dic["name"], referToTableCSV, col_dic["refertocol"], num_rows, fk_rootpath)
            elif col_dic["type"] == "Categorical":
                ls = gen.generate_ls_categorical(col_dic["options"],num_rows)
            #print(len(ls))
            # Once each list of data is created, read it into the table as a new column.
            if type(ls) == list:
                table[field_name] = ls
                metadata_DF[field_name] = meta
            else:
                for x in range(len(field_name)):
                    table[field_name[x]] = ls[list(ls)[x]].values
                    metadata_DF[field_name[x]] = meta
        exec("config.data_"+table_name+"=table")
        return table, metadata_DF, table_name, num_rows
        #f.close()
    ## Generate Mixed Pack Table   
    def mixedpack(self,schema,bottlername_prefix,fk_rootpath):
        table = pd.DataFrame()
        metadata_DF = pd.DataFrame()
        table_name = schema["title"]
        dic1 = schema["columns"][0]
        dic2 = schema["columns"][1]
        exec("config.refertable1=config.data_" + dic1["refertotable"].replace(".csv",""))
        refervalue1 = list(config.refertable1.loc[config.refertable1[dic1['condition'][0]] == dic1['condition'][1], dic1["refertocol"][0]])

        exec("config.refertable2=config.data_" + dic2["refertotable"].replace(".csv",""))
        refervalue2 = list(config.refertable2.loc[config.refertable2[dic2['condition'][0]] == dic2['condition'][1], dic2["refertocol"][0]])
        dic3 = schema["columns"][2]
        numofpartition_ls = [random.choice(range(2,7)) for i in range(len(refervalue1))]
        numofrows = sum(numofpartition_ls)
        def numsum1(numofpartition):
            ls = [random.uniform(1,10) for i in range(numofpartition)]
            ratings_ls_unit = [round(x/sum(ls)*100,5) for x in ls]
            return ratings_ls_unit
        table[dic1['name'][0]] = list(itertools.chain(*(itertools.repeat(elem, n) for elem, n in zip(refervalue1, numofpartition_ls))))
        metadata_DF[dic1['name'][0]] = ["P"]*numofrows
        table[dic2['name'][0]] = list(itertools.chain(*(random.sample(refervalue2,n) for n in numofpartition_ls)))
        metadata_DF[dic2['name'][0]] = ["P"]*numofrows
        table[dic3['name']] = list(itertools.chain(*(numsum1(n) for n in numofpartition_ls)))
        metadata_DF[dic3['name']] = ["P"]*numofrows
        return table, metadata_DF, table_name, numofrows

        
class FileCreater:
    def __init__(self, table,metadata_DF,table_name_all,filerootpath):
        self.table = table
        self.metadata_DF = metadata_DF
        self.table_name_all = table_name_all
        self.changer = Changer()
        self.filerootpath = filerootpath
    def positive_Data_Files(self):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        # Save table to csv, metadata to json.
        table_copy.to_csv(self.filerootpath + "\\%s.csv"% self.table_name_all,index=False,encoding = "utf-8",sep=",",quoting=csv.QUOTE_ALL)
        metadata_DF_copy.to_json(self.filerootpath +"\\%s_metadata.json"% self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","positive")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_File_Format_XLS(self):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        excelwriter = pd.ExcelWriter(self.filerootpath + "\\%s.xls" % self.table_name_all,engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        table_copy.to_excel(excelwriter, sheet_name='Sheet1', index=False)
        # Close the Pandas Excel writer and output the Excel file.
        excelwriter.save()
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: not csv but in excel")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_File_Format_TXT(self):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy.to_csv(self.filerootpath + "\\%s.txt" % self.table_name_all, index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: not csv but in txt")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Format_Not_Comma_Separated(self):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep="|", quoting=csv.QUOTE_ALL)
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: not commaseparated")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Format_Not_UFT8(self):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False, encoding="utf-16", sep=",", quoting=csv.QUOTE_ALL)
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: not utf8 but utf16")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Format_Not_Double_Quoted(self):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_MINIMAL)
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: not doublequoted")
        table_copy = None
        metadata_DF_copy = None
    def neg_notallpresent(self,num):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        file = open(self.filerootpath + "\\%s.csv" % self.table_name_all,'r',encoding="utf8")
        r = csv.reader(file)
        lines = [l for l in r]
        numofnotpresent = random.choice(range(num)) + 1
        row_inds = random.sample(range(len(lines)),numofnotpresent)
        for row_ind in row_inds:
            col_ind = random.choice(range(len(lines[row_ind])))
            del lines[row_ind][col_ind]
            metadata_DF_copy.iloc[row_ind-1,col_ind] = "not present"
        with open(self.filerootpath + "\\%s.csv" % self.table_name_all,"w",encoding="utf-8") as f:
            writer = csv.writer(f,delimiter=",",lineterminator='\n')
            writer.writerows(lines)
        file.close()
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: not allpresent")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Format_Thousand_Comma_Separator(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_thousandseparatercomma(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: thousand separater as comma")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Format_Thousand_Decimal_Separator(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_decimalseparatercomma(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: decimal separater as comma")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Data_Blank_Mandatory_Value(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_nulltoMandatory_nothing(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: null as ''")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Data_Space_Mandatory_Value(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_nulltoMandatory_space(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","null as ' '")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Data_NULL_Mandatory_Value(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_nulltoMandatory_Null(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: null as 'Null'")
        table_copy = None
        metadata_DF_copy = None
    ## Function to add "not in option" to categorical data.
    def incorrect_Optional_Category(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_notinoptiontocat(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: 'not in option' for this categorical field")
        table_copy = None
        metadata_DF_copy = None
    ## Function to add special character to string，language has the following options: ["Simplified Chinese","Traditional Chinese","Spanish","German"]
    def neg_addspecialcharactertostring(self, dicofcols,language):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_specialcharactertostring(dicofcols,table_copy,metadata_DF_copy,language)
        if language == "Simplified Chinese":
            table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
            metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
            self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","This string contains simplified Chinese character")
        if language == "Traditional Chinese":
            table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
            metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
            self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","This string contains traditional Chinese character")
        if language == "Spanish":
            table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
            metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
            self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","This string contains Spanish character")
        if language == "German":
            table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
            metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
            self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","This string contains German character")
        table_copy = None
        metadata_DF_copy = None
    #Function to add all combinatins in one file
    def all_In_One(self,difcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_alltoone(difcols,table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        file = open(self.filerootpath + "\\%s.csv" % self.table_name_all, 'r', encoding="utf8")
        r = csv.reader(file)
        lines = [l for l in r]
        numofnotpresent = random.choice(range(1,len(table_copy.index)))
        row_inds = random.sample(range(len(lines)), numofnotpresent)
        for row_ind in row_inds:
             if(all(metadata_DF_copy.iloc[row_ind -1]=="P")):
                 col_ind = random.choice(range(len(lines[row_ind])))
                 del lines[row_ind][col_ind]
                 metadata_DF_copy.iloc[row_ind-1 , col_ind] = "not present"
        with open(self.filerootpath + "\\%s.csv" % self.table_name_all, "w",
                  encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",", lineterminator='\n',quoting=csv.QUOTE_ALL)
            writer.writerows(lines)
        file.close()
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                 orient="index")
        self.changer.add_keyvaluetojson(
            self.filerootpath + "\\%s_metadata.json" % self.table_name_all, "description",
            "negative: All combinations in one file")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Foreign_Key(self, dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_IncorFK(dicofcols, table_copy, metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False, encoding="utf-8",
                     sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all, orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                        "description", "Negative: Foreign key is incorrect")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Data_File_Name(self, eachNegFileNm):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % eachNegFileNm, index=False, encoding="utf-8",
                     sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % eachNegFileNm, orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % eachNegFileNm,
                                      "description", "Negative: Filename format is incorrect")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_String_Code(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy,metadata_DF_copy = self.changer.add_incorStringCode(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json"% self.table_name_all,"description","negative: incorrect code")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_String_Language_wPunctuation(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_incorstring_language_string(dicofcols, table_copy, metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,
                          encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                 orient="index")
        self.changer.add_keyvaluetojson(
            self.filerootpath + "\\%s_metadata.json" % self.table_name_all, "description",
            "negative: This contains incorrect address,word,city and address")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_String_Length(self, dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_incorstring_length_string(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % self.table_name_all, "description",
            "negative: This contains address,word,city and address more than max length")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_String_Address_Currency_Language(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_incorstring_language_addressAndcurrency(dicofcols, table_copy, metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,
                          encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                 orient="index")
        self.changer.add_keyvaluetojson(
            self.filerootpath + "\\%s_metadata.json" % self.table_name_all, "description",
            "negative: This contains incorrect language for State, Country, Postal Code, Currency")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_String_Address_Currency_Length(self, dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_incorstring_length_addressAndcurrency(dicofcols, table_copy,metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % self.table_name_all, "description",
            "negative: This contains State, Country, Postal Code, Currency more than max length")
        table_copy = None
        metadata_DF_copy = None
    def incorrect_Digit_Code(self, dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_incorDigitCode(dicofcols, table_copy, metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,
                          encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        ## Need to edit metadata_DF
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                 orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                        "description", "negative: incorrect code")
        table_copy = None
        metadata_DF_copy = None

    def neg_addduplicateprimarykey(self,dicofcols):
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_duplicateprimarykey(dicofcols, table_copy, metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                 orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,
                                        "description", "negative: duplicated primary key")
        #table_copy.to_csv(self.filerootpath + "output\\neg_duplicateprimarykey\\%s.csv" % self.table_name_all,index=False, encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        #metadata_DF_copy.to_json(self.filerootpath + "output\\neg_duplicateprimarykey\\%s_metadata.json" % self.table_name_all, orient="index")
        #self.changer.add_keyvaluetojson(self.filerootpath + "output\\neg_duplicateprimarykey\\%s_metadata.json" % self.table_name_all, "description","negative: Duplicate primary keys")
        table_copy = None
        metadata_DF_copy = None
    def neg_blankmultipleprimarykey(self,dicofcols):
        ls = [''.join(p["name"]) for p in dicofcols if p["partofKey"] == 1]
        table_copy = self.table.copy()
        metadata_DF_copy = self.metadata_DF.copy()
        table_copy, metadata_DF_copy = self.changer.add_blankmultipleprimarykey(dicofcols, table_copy, metadata_DF_copy)
        table_copy.to_csv(self.filerootpath + "\\%s.csv" % self.table_name_all, index=False, encoding="utf-8", sep=",",quoting=csv.QUOTE_ALL)
        metadata_DF_copy.to_json(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,orient="index")
        self.changer.add_keyvaluetojson(self.filerootpath + "\\%s_metadata.json" % self.table_name_all,"description", "negative: Multiple blank primary keys")
        # table_copy.to_csv(self.filerootpath + "output\\neg_blankprimarykey\\%s.csv" % self.table_name_all, index=False,encoding="utf-8", sep=",", quoting=csv.QUOTE_ALL)
        # metadata_DF_copy.to_json(self.filerootpath + "output\\neg_blankprimarykey\\%s_metadata.json" % self.table_name_all,orient="index")
        # self.changer.add_keyvaluetojson(self.filerootpath + "output\\neg_blankprimarykey\\%s_metadata.json"% self.table_name_all,"description","negative: Multiple blank primary keys")
        table_copy = None
        metadata_DF_copy = None