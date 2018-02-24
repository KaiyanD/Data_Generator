# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2017

@author: kading
TO-DO
Check on how to verify date format, Country, State, City, Zip code and word and add comments to each accordingly

'''
## Change the working directory to be main folder.
import os
import sys
import xlrd
import unittest
sys.path.insert(0, os.path.abspath(os.curdir))
from src_pkg.generate import *
import config

rootpath = os.path.dirname(setup.path()) + "\\testdatageneration\\"

class Core_Test(unittest.TestCase):

### Unit test functions for methods that generate random unit data.
    ## Unit test for testing Changer.add_null
    def testadd_null(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_null(dicofcols,table,metadata_DF)
        self.assertEqual("" in result_table.values, 1, "the result table do not contain null as ''")
    ## Unit test for testing Changer.add_thousandseparatercomma
    def test_add_thousandseparatercomma_tosinglevalue(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        f=open(rootpath + "testdata\\input\\testschema.json","r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result = changer._add_thousandseparatercomma_tosinglevalue("")
        self.assertEqual(result == '', 1, "The add_thousandseparatercomma_tosinglevalue function should not change ''")
    #Unit test fir testing Changer.gen_random_set
    def test_gen_random_set(self):
        parentset_before = random.sample(set(range(0,10)),10)
        int_size = 6
        randomset_before = [5,7,1]
        generator = Generator()
        parentset_after,randomset_after = generator.gen_random_set(parentset_before,randomset_before,int_size)
        self.assertEqual(randomset_after not in parentset_before and randomset_before!=randomset_after and len(randomset_after)==int_size,1, "Functoin should exclude mentioned set(randomset) and generate new from parent set")
    ## Unit test for testing Changer.add_thousandseparatercomma
    def testadd_thousandseparatercomma(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        f=open(rootpath + "testdata\\input\\testschema.json","r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_thousandseparatercomma(dicofcols,table,metadata_DF)
        self.assertEqual("," in result_table["Bottler_Gross_Revenue"][1], 1, "the thousand separater is not comma")
        self.assertEqual("thousand separater as comma" in result_metadata_DF.values, 1, "The changed field has not been labeled as 'thousand separater as comma'")
    ## Unit test for testing Changer.add_decimalseparatercomma
    def testadd_decimalseparatercomma(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_decimalseparatercomma(dicofcols,table,metadata_DF)
        self.assertEqual("," in result_table["Bottler_Gross_Revenue"][1], 1, "the thousand separater is not comma")
        self.assertEqual("decimal separater as comma" in result_metadata_DF.values, 1, "The changed field has not been labeled as 'decimal separater as comma'")
    ## Unit test for testing Changer.add_keyvaluetojson
    def testadd_keyvaluetojson(self):
        changer = Changer()
        changer.add_keyvaluetojson(rootpath + "testdata\\input\\test_addkeyvalue.json","testkey","testvalue")
        with open(rootpath + "testdata\\input\\test_addkeyvalue.json","r") as json_file:
            result = json.load(json_file)
        self.assertEqual(result["testkey"]=="testvalue", 1, "the key value pair has not been successfully added")
        del result["testkey"]
        with open(rootpath + "testdata\\input\\test_addkeyvalue.json", 'w') as json_file:
            json.dump(result, json_file)
        json_file.close()

    # Unit test for changer.add_specialtostring
    def testadd_specialcharactertostring(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_specialcharactertostring(dicofcols,table,metadata_DF,"Simplified Chinese")
        self.assertEqual("This field contains simplified Chinese character" in result_metadata_DF.loc[:,"Invoice_Number"].tolist(), True, "Simplified Chinese is not added in the dataframe")

    # Unit test for changer.add_notinoptiontocat
    def testadd_notinoptiontocat(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_notinoptiontocat(dicofcols,table,metadata_DF)
        #self.assertEqual("not in option" in result_table.loc[:,"Record_Type"].tolist(), True, "'not in option' is not added in the dataframe")
        self.assertEqual("This field is not in option." in result_metadata_DF.loc[:,"Record_Type"].tolist(), True, "'not in option' is not added in the metadata")

    ## Unit test for testing gen_digitcode
    ##Validates the number of letters and digits generated by gen_digitcode are within the expected range
    def testGenDigit(self):
        generator = Generator()
        result = generator.gen_digitcode(2)
        #print(result)
        self.assertLess(len(result), 3, "The gen_digitcode is not generating number with digit as expected")

    ## Unit test for testing gen_code
        ##Validates the number of digits generated by gen_code are within the expected range
    def testGenString(self):
        generator = Generator()
        result = generator.gen_code(10)
        #print(result)
        self.assertLess(len(result), 11, "The gen_code is generating words length less than expected")

    ## Unit test for testing gen_yn
        ##Validates the random output from testGenBinary is either Y/N and not any other letter
    def testGenBinary(self):
        generator = Generator()
        result = generator.gen_yn()
        #print(result)
        self.assertRegex(result, "Y|N", "The Binary is neither Y or N")

    ## Unit test for testing pick_cat
        ##Validates the random output from expected list of values and not any other value
    def testPickCat(self):
        generator = Generator()
        result = generator.pick_cat(["A","B","C"])
        #print(result)
        self.assertRegex(result, "A|B|C", "The pick is not from the expected list of option")

    ### Unit test functions for methods that generate data for CSV file.
    ##Validates the number of date generated in  generate_ls_datetime is as expected

    def testDate(self):
        generator = Generator()
        result = generator.generate_ls_datetime("YYYYMMDD",2)
        #print(result)
        self.assertEqual(len(result), 2, "the date count is not as expected")

     ##Validates the number of strings generated in  generate_ls_code is as expected
     ##Validates the number of character in each string is generated within the limit passed to generate_ls_code
    def testString(self):
        generator = Generator()
        result = generator.generate_ls_code(40,100,1)
        #print(result)
        self.assertEqual(len(result), 100, "the date count is not as expected")
        for x in result:
            self.assertLess(len(x), 41, "the character count is not as expected")

    ##Validates the number of strings generated in  generate_ls_code is as expected
     ##Validates the number of character in each string is generated within the limit passed to generate_ls_code
    def testSentence(self):
        generator = Generator()
        result = generator.generate_ls_sentence(100,2)
        #print(result)
        self.assertEqual(len(result), 2, "the sentence count is not as expected")
        for x in result:
            self.assertLess(len(x), 101, "the character count is not as expected")


    #generate_ls_word(self,max_length,numrows):
    def testGenerateWord(self):
        generator = Generator()
        result = generator.generate_ls_word(10,2)
        #print(result)
        self.assertEqual(len(result), 2, "the word count is not as expected")
        for x in result:
            self.assertLess(len(x), 11, "the character count is not as expected")



    #generate_ls_address(self, max_length,numrows):
    def testGenerateAddress(self):
        generator = Generator()
        result = generator.generate_ls_address(10,2)
        #print(result)
        self.assertEqual(len(result), 2, "the address count is not as expected")
        for x in result:
            self.assertLess(len(x), 11, "the address character count is not as expected")


    #generate_ls_currency(self, max_length,numrows):
    def testGenerateCurrency(self):
        generator = Generator()
        result = generator.generate_ls_currency(3,2)
        #print(result)
        self.assertEqual(len(result), 2, "the count of currency number is not as expected")
        for x in result:
            self.assertEqual(len(x), 3, "the total amount is not as expected")


    #generate_ls_city(self,max_length,numrows):
    def testGenerateCity(self):
        generator = Generator()
        result = generator.generate_ls_city(15,2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of cities generated is not as expected")
        for x in result:
            self.assertLess(len(x), 16, "the character count in the city name is not as expected")


    #generate_ls_state(self,max_length,numrows):
    def testGenerateState(self):
        generator = Generator()
        result = generator.generate_ls_state(15,2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of state generated is not as expected")
        for x in result:
            self.assertLess(len(x), 16, "the character count in the state name is not as expected")

    #generate_ls_country(self,max_length,numrows):
    def testGenerateCountry(self):
        generator = Generator()
        result = generator.generate_ls_country(10,2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of Country generated is not as expected")
        for x in result:
            self.assertLess(len(x), 11, "the character count in the COuntry name is not as expected")

    #generate_ls_postalcode(self,max_length,numrows):
    #Validates the number of rows generated
    def testPostalCode(self):
        generator = Generator()
        result = generator.generate_ls_postalcode(5,2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of Country generated is not as expected")
        for x in result:
            self.assertLess(len(x), 11, "the character count in the COuntry name is not as expected")


    #Validates that each value is either Y/N
    #Validates the number of rows generated
    def testyn(self):
        generator = Generator()
        result = generator.generate_ls_yn(2)
        #print(result)
        self.assertEqual(len(result), 2, "The number of Y/N generated is not as expected")
        for x in result:
            self.assertRegex(x, "Y|N", "The character is neither Y nor N")


    #generate_ls_digitcode(self,max_length,numrows,unique=False):
    #Validates the number of rows generated
    def testDigitCode(self):
        generator = Generator()
        result = generator.generate_ls_digitcode(10,2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of string generated are not same as expected")
        for x in result:
            self.assertLess(len(x), 11, "the character count in the string is not as expected")

    #Validates for latitude range (+90 to -90) to validate the value
    #Validates the number of rows generated
    def testGenerateLat(self):
        generator = Generator()
        result = generator.generate_ls_latitude(2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of string generated are not same as expected")
        for x in result:
            self.assertEqual((90 >= float(x) >= -90), True, "the latitude value is not withing the expected range")

    #Validates for longitude range (+180 to -180) to validate the value
    #Validates the number of rows generated
    def testGenerateLongi(self):
        generator = Generator()
        result = generator.generate_ls_longitude(2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of string generated are not same as expected")
        for x in result:
            self.assertEqual((180 >= float(x) >= -180), True, "the character count in the string is not as expected")

    #Validates the number of rows generated
    #Validates each number generated is a float with a decimal place
    def testGenerateDecimal(self):
        generator = Generator()
        result = generator.generate_ls_decimal(2)
        #print(result)
        self.assertEqual(len(result), 2, "the number of float values generated are not same as expected")
        for x in result:
            self.assertEqual(isinstance(x, float),True,"the number is not a float")

    #Validates if the generated character is Chinese
    def testGenerateTraditionalChinese(self):
        generator = Generator()
        chi = generator.gen_ChineseTraditional()
        res = 0
        if (chi > u'\u4e000') and (chi < u'\u9fff'):
            res = 1
        #print(result)
        self.assertEqual(res, 1, "The character generated is not Chinese")

    #Validates if the generated character is Chinese
    def testGenerateSimplifiedChinese(self):
        generator = Generator()
        chi = generator.gen_ChineseSimplified()
        res = 0
        if (chi > u'\u4e000') and (chi < u'\u9fff'):
            res = 1
        #print(result)
        self.assertEqual(res, 1, "The character generated is not Chinese")

    #Validates if the generated character is Spanish
    def testGenerateSpanish(self):
        generator = Generator()
        spa = generator.gen_Spanish()
        #print(result)
        self.assertEqual(spa in ['ô', 'É', 'º', 'ó', 'Í', 'Ú', 'õ', 'á', 'ñ', 'í', 'Ê', 'è', 'â', 'ò', 'ª', 'ö', 'Ô', 'ã', 'ü', 'Á', '»', '¡', 'é', 'î', '€', 'ú', 'Ã', 'Â', 'À', 'Ó', '¿', '’', 'ç', '«', 'à', 'ê', 'Ç'], 1, "The character generated is not Special Spanish")

    #Validates if the generated character is Special German
    def testGenerateGerman(self):
        generator = Generator()
        spa = generator.gen_German()
        #print(result)
        self.assertEqual(spa in ['Ü', 'ö', 'ä', 'ß', 'ü', 'Ä','Ö','ẞ'], 1, "The character generated is not Special Spanish")

    # Validates the number of rows generated
    #Validates the value is available in the source file
    def testForeignKey(self):
        generator = Generator()
        ls = ["A1","A 2 test","A3 asd","A4 12"]
        result = generator.generate_ls_foreignkey(["Source_Product_Code"], "data_ForeignKey.csv", ["Column A"], 5, rootpath)
        #print(result)
        lresult = result['Source_Product_Code']
        self.assertEqual(len(lresult), 5, "the number of rows generated are not same as expected")
        for x in lresult:
            #print(x)
            self.assertEqual(x in ls, True, "The value captured does not exist in the list")

    # Validates the number of rows generated
    # Validates the value is category to be selected
    def testCategoricalData(self):
        generator = Generator()
        result = generator.generate_ls_categorical(["A","B","C","D","E"],2)
        #print(result)
        self.assertEqual(len(result), 2, "the number decimals generated are not same as expected")
        for x in result:
            self.assertRegex(x, "[A-E]", "the number has a decimal place")



    #Validates the column generated in dataframe for test data and metadata matches to the schema
    #Validates the number of test data rows and metadata generated is same as expected
    def testCSVData(self):
        testGenMain = Generate_Main()
        schemaCol = ["scTest1","scTest2","scTest3","Promo_Indicator","Day_Code"]
        f=open(rootpath + "testdata\\input\\SchemaTest.json","r")
        testSchema=json.load(f)
        table, metadata_DF, table_name, num_rows = testGenMain.run(testSchema,"data",2, rootpath)
        dicofcolsTest = testSchema["columns"]
        f.close()
        # Validates the number of rows generated for csv data file is same as expected
        self.assertEqual(table['scTest1'].count(), 2, "Column is missing in csv file")
        # Validates the column to be written in csv matches to the columns in JSON scehma
        for x in table.columns.tolist():
            self.assertEqual(x in schemaCol, True,"Column is missing in csv file")


    # Unit Test for Generate_Main.mixedpack
    def testGenerateMain_mixedpack(self):
        testGenMain = Generate_Main()
        f=open(rootpath + "testdata\\input\\test_mixedpack.json","r")
        schema=json.load(f)
        bottlername_prefix = "test_"
        table, metadata_DF, table_name, num_rows = testGenMain.mixedpack(schema,bottlername_prefix,rootpath)
        f.close()
        dic1 = schema["columns"][0]
        referfile1 = codecs.open(rootpath+"output/positive/"+bottlername_prefix+"_"+dic1["refertotable"],'r','utf-8')
        refertable1 = pd.read_csv(referfile1)
        refervalue1 = list(refertable1.loc[refertable1[dic1['condition'][0]] == dic1['condition'][1], dic1["refertocol"][0]])
        referfile1.close()
        dic2 = schema["columns"][1]
        referfile2 = codecs.open(rootpath+"output/positive/"+bottlername_prefix+"_"+dic2["refertotable"],'r','utf-8')
        refertable2 = pd.read_csv(referfile2)
        refervalue2 = list(refertable2.loc[refertable2[dic2['condition'][0]] == dic2['condition'][1], dic2["refertocol"][0]])
        referfile2.close()
        dic3 = schema["columns"][2]
        self.assertEqual(len([x for x in table[dic1['name'][0]] if x not in refervalue1]), 0,"column %s have values not in original table"% dic1["name"][0])
        self.assertEqual(len([x for x in table[dic2['name'][0]] if x not in refervalue2]), 0,"column %s have values not in original table"% dic2["name"][0])
        self.assertEqual(list(table.groupby(dic1["name"][0])[dic3["name"]].sum().round(1).unique())==[100.0], 1,"column %s do not add up to 100 when groub by %s"% (dic3["name"],dic1["name"]))

    ''' 
    This part is for Unit Testing the FileCreater class, saved for later    
    ### Unit test for object： FileCreater
    # for positive
    def test_FileCreater_positive(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.positive()
        print(rootpath + "testdata\\ - This is test")
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output"), 1, "The csv file has not been successfully created at 'output'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output"), 1, "The json file has not been successfully created at 'output'")
    # for neg_excel
    def test_FileCreater_neg_excel(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_excel()
        self.assertEqual("testfilecreater.xls" in os.listdir(rootpath + "testdata\\output\\in_excel\\"), 1, "The csv file has not been successfully created at 'output/in_excel/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\in_excel\\"), 1, "The json file has not been successfully created at 'output/ex_excel/'")
    # for neg_txt
    def test_FileCreater_neg_txt(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_txt()
        self.assertEqual("testfilecreater.txt" in os.listdir(rootpath + "testdata\\output/in_txt/"), 1, "The csv file has not been successfully created at 'output/in_txt/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output/in_txt/"), 1, "The json file has not been successfully created at 'output/in_txt/'")
    # for neg_notcommaseparated
    def test_FileCreater_neg_notcommaseparated(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_notcommaseparated()
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output/not_commaseparated/"), 1, "The csv file has not been successfully created at 'output/not_commaseparated/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output/not_commaseparated/"), 1, "The json file has not been successfully created at 'output/not_commaseparated/'")
    # for neg_notutf8
    def test_FileCreater_neg_notutf8(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_notutf8()
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output\\not_utf8\\"), 1, "The csv file has not been successfully created at 'tables/not_utf8/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\not_utf8\\"), 1, "The json file has not been successfully created at 'tables/not_utf8/'")
    # for neg_notdoublequoted
    def test_FileCreater_neg_notdoublequoted(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_notdoublequoted()
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output/not_doublequoted/"), 1, "The csv file has not been successfully created at 'output/not_doublequoted/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output/not_doublequoted/"), 1, "The json file has not been successfully created at 'output/not_doublequoted/'")
    # for neg_notallpresent
    def test_FileCreater_neg_notallpresent(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_notallpresent(5)
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output/not_allpresent/"), 1, "The csv file has not been successfully created at 'output/not_allpresent/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output/not_allpresent/"), 1, "The json file has not been successfully created at 'output/not_allpresent/'")

    # for neg_thousandseparatercomma
    def test_FileCreater_neg_thousandseparatercomma(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_thousandseparatercomma(dicofcols)
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output/thousandseparatercomma/"), 1, "The csv file has not been successfully created at 'output/thousandseparatercomma/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output/thousandseparatercomma/"), 1, "The json file has not been successfully created at 'output/thousandseparatercommat/'")
    # for neg_decimalseparatercomma
    def test_FileCreater_neg_decimalseparatercomma(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_decimalseparatercomma(dicofcols)
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output\\decimalseparatercomma\\"), 1, "The csv file has not been successfully created at 'output\\decimalseparatercomma/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\decimalseparatercomma\\"), 1, "The json file has not been successfully created at 'output\\decimalseparatercomma\\'")
    # for neg_addnulltomandatory_nothing
    def test_FileCreater_neg_addnulltomandatory_nothing(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_addnulltomandatory_nothing(dicofcols)
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_nothing/"), 1, "The csv file has not been successfully created at 'output\\nulltomandatory_nothing\\")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_nothing/"), 1, "The json file has not been successfully created at 'output\\nulltomandatory_nothing\\'")
    # for neg_addnulltomandatory_space
    def test_FileCreater_neg_addnulltomandatory_space(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_addnulltomandatory_space(dicofcols)
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_space\\"), 1, "The csv file has not been successfully created at 'output\\nulltomandatory_space/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_space/"), 1, "The json file has not been successfully created at 'output\\nulltomandatory_space\\'")
    # for neg_addnulltomandatory_Null
    def test_FileCreater_neg_addnulltomandatory_Null(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\output\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        filecreater = FileCreater(table,metadata_DF,table_name_all,rootpath)
        filecreater.neg_addnulltomandatory_Null(dicofcols)
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_Null\\"), 1, "The csv file has not been successfully created at 'output\\nulltomandatory_Null/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_Null\\"), 1, "The json file has not been successfully created at 'output\\nulltomandatory_Null\\'")
        self.assertEqual("testfilecreater.csv" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_Null\\"), 1, "The csv file has not been successfully created at 'tables/nulltomandatory_Null/'")
        self.assertEqual("testfilecreater_metadata.json" in os.listdir(rootpath + "testdata\\output\\nulltomandatory_Null\\"), 1, "The json file has not been successfully created at 'tables/nulltomandatory_Null/'")'''

#For duplicate primary key # In Memory
    def test_FileCreater_neg_addduplicateprimarykey(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_duplicateprimarykey(dicofcols, table, metadata_DF)
        ls = ["Day_Code","Source_Ship_from_Code","Source_Ship_To_Code","Vending_Machine_Code","Vending_Machine_Location_Code","Source_Product_Code","Source_Channel_Code","Source_Sales_Type_Code","Record_Type", "Operation_Route_Type","Invoice_Number"]
        nonBlankCols = [cName for cName in ls if("This field is duplicated for combined primary key" not in result_metadata_DF.loc[:,cName].tolist())]
        self.assertEqual(len(nonBlankCols) == 0, True,"Columns " + str(nonBlankCols) + " does not contain primary cols with duplicate values")
    #Add blank values for combined primary keys# In Memory
    def test_FileCreater_neg_blankmultipleprimarykey(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table,result_metadata_DF = changer.add_blankmultipleprimarykey(dicofcols, table, metadata_DF)
        ls = ["Day_Code","Source_Ship_from_Code","Source_Ship_To_Code","Vending_Machine_Code","Vending_Machine_Location_Code","Source_Product_Code","Source_Channel_Code","Source_Sales_Type_Code","Record_Type","Operation_Route_Type","Invoice_Number"]
        nonBlankCols = [cName for cName in ls if("This field is '' for combined primary key" not in result_metadata_DF.loc[:,cName].tolist())]
        self.assertEqual(len(nonBlankCols)==0,True,"Columns "+ str(nonBlankCols) + " does not contain primary cols with blank values")

    # To add incorrect string code
    def test_FileCreater_neg_incrStringCode(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_incorStringCode(dicofcols, table, metadata_DF)
        ls = ["This field is incorrect code with special characters","This field is incorrect code, contains code with sign",
              "This field is invalid code with different language","This field is code with length more than max length"
              ]
        ls_tmp = ls.copy()
        # for colList in result_metadata_DF
        cols_ls = result_metadata_DF.columns.values
        for str_msg in ls:
            for colName in cols_ls:
                if (str_msg in result_metadata_DF.loc[:, colName].tolist()):
                    ls_tmp.remove(str_msg)
        self.assertEqual(len(ls_tmp) == 0, True, "Incorrect String Code:No negative cases found for " + str(ls_tmp))
    # To add incorrect digit code
    def test_FileCreater_neg_incrDigitCode(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index)+1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_incorDigitCode(dicofcols, table, metadata_DF)
        ls = ["This field is invalid Digit code with special characters","This field is invalid Digit code, contains code with sign",
              "This field is invalid Digit code with incorrect language","This field is invalid Digit code with length more than max length"
              ]
        ls_tmp = ls.copy()
        # for colList in result_metadata_DF
        cols_ls = result_metadata_DF.columns.values
        for str_msg in ls:
            for colName in cols_ls:
                if (str_msg in result_metadata_DF.loc[:, colName].tolist()):
                    ls_tmp.remove(str_msg)
        self.assertEqual(len(ls_tmp) == 0, True, "Incorrect Digit Code:No negative cases found for " + str(ls_tmp))

    '''Validate bottler name and datetime prefix for filename NSRP 929 - Generate File name condition - postive and negative'''

# Unit test for all negative in single csv
    def test_add_generic_neg(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        table_name_all = "testfilecreater"
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table,result_metadata_DF = changer.add_alltoone(dicofcols,table,metadata_DF)
        '''Add the message in followoing list when new negative condition is included'''
        ls = ["thousand separater as comma","decimal separater as comma","This field is ''", "This field is ' '",
              "This field is 'Null'","This field is not in option.","This field contains simplified Chinese character", "This field contains traditional Chinese character",
              "This field contains Spanish character","This field contains German character","This Foreign key is incorrect","This Foreign key is swapped",
              "This field is incorrect code with special characters","This field is incorrect code, contains code with sign",
               "This field is invalid code with different language","This field is code with length more than max length",
              "This field is invalid Digit code with special characters","This field is invalid Digit code, contains code with sign",
               "This field is invalid Digit code with different language","This field is invalid Digit code with length more than max length",
              "This field is abnormal Character, punctuation for string fields","This field is longer than max length for string fields",
              "This field is abnormal Character, punctuation for currency and other fields","This field is longer than max length for currency and other fields"
              ]
        ls_tmp = ls.copy()
        #for colList in result_metadata_DF
        cols_ls = result_metadata_DF.columns.values
        for str_msg in ls:
            for colName in cols_ls:
                if(str_msg in result_metadata_DF.loc[:, colName].tolist() and str_msg in ls_tmp):
                    ls_tmp.remove(str_msg)
        self.assertEqual(len(ls_tmp) == 0, True,"No negative cases found for " + str(ls_tmp))

    def testFileNameFormat(self):
        fileNameFormat = FileNameFormater()
        ls_testFileNameFormat = fileNameFormat.fileNameFormat("testBottlerName")
        for x in ls_testFileNameFormat:
            self.assertEqual(x.find("testBottlerName") != -1, True, "The bottler file name is not as expected")
        #ls_testFileNameFormat.remove(ls_testFileNameFormat[0])
        #print(ls_testFileNameFormat)'''

    # for negative cases for foreign key
    # Validates the foriegn key column has invalid data and also checks for the incorrect composite foreign key
    def test_FileCreater_neg_ForeinKey(self):
        gen = Generate_Main()
        ch = Changer()
        f = open(rootpath + "testdata\\input\\SchemaTest.json", "r")
        schema = json.load(f)
        f.close()
        #table_name = schema["title"]
        dicofcols = schema["columns"]
        #This is to give reference table for FK, this is only used for unit test
        config.data_ForeignKey = pd.read_csv(rootpath + "testdata\\input\\ForeignKey.csv",dtype=object)

        table, metadata_DF, table_name, num_rows = gen.run(schema,"data",10,rootpath)
        metadata_DF.index = range(1, num_rows + 1)
        '''print("--------------DataFrame---------------")
        print(table)
        print("--------------MetaData---------------")
        print(metadata_DF)'''
        dataframe_fk, metadata_DF_fk = ch.add_IncorFK(dicofcols,table,metadata_DF)
        '''print("--------------Incorrect DataFrame---------------")
        print(dataframe_fk)
        print("--------------Incorrect MetaData---------------")
        print(metadata_DF_fk)'''
        self.assertEqual("This Foreign key is incorrect" in metadata_DF_fk.loc[:,"scTest2"].tolist(), True, "The incorrect foreign key is not added in the dataframe")
        self.assertEqual("This Foreign key is swapped" in metadata_DF_fk.loc[:,"scTest3"].tolist(), True, "The composite foreign key is not updated in the dataframe")

    def test_datacount(self):
        fpath_rowct = rootpath + "testdata\\input\\dataCount.json"
        f_rowct = codecs.open(fpath_rowct, 'r', 'utf-8')
        rowcounts = json.load(f_rowct)
        # print(rowcounts["customer"])
        self.assertEqual(rowcounts["TD_001_Positive_Data_Files"]["channel"], 25, "Incorrect row count")
    ### To validate that incorrect language/punctation marks are added to string
    def testFileCreater_neg_incrstring_language_string(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table,result_metadata_DF = changer.add_incorstring_language_string(dicofcols, table, metadata_DF)
        ls = result_metadata_DF.columns.values
        negCols = [cName for cName in ls if("This field is abnormal Character, punctuation for string fields" not in result_metadata_DF.loc[:,cName].tolist())]
        self.assertEqual(len(negCols)!=len(ls),True,"No abnormal character or punctuation found in generated data")
    ### To validate that string of incorrect length is added
    def testFileCreater_neg_incrstring_length_string(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table,result_metadata_DF = changer.add_incorstring_length_string(dicofcols, table, metadata_DF)
        ls = result_metadata_DF.columns.values
        negCols = [cName for cName in ls if("This field is longer than max length for string fields" not in result_metadata_DF.loc[:,cName].tolist())]
        self.assertEqual(len(negCols)!=len(ls),True,"No string found containing more characters than it's max length")
    ### To validate that incorrect language/punctation marks are added to currency and other fields
    def testFileCreater_neg_incrstring_language_addressAndcurrency(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_incorstring_language_addressAndcurrency(dicofcols, table, metadata_DF)
        ls = result_metadata_DF.columns.values
        negCols = [cName for cName in ls if ("This field is abnormal Character, punctuation for currency and other fields" not in result_metadata_DF.loc[:,cName].tolist())]
        self.assertEqual(len(negCols) != len(ls), True,"No abnormal character or punctuation found in generated data")
    ### To validate that string of incorrect length is added
    def testFileCreater_neg_incrstring_length_addressAndcurrency(self):
        table = pd.read_csv(rootpath + "testdata\\input\\testtable.csv")
        metadata_DF = pd.read_csv(rootpath + "testdata\\input\\testmetadata.csv")
        metadata_DF.index = range(1, len(metadata_DF.index) + 1)
        f = open(rootpath + "testdata\\input\\testschema.json", "r")
        dicofcols = json.load(f)["columns"]
        f.close()
        changer = Changer()
        result_table, result_metadata_DF = changer.add_incorstring_length_addressAndcurrency(dicofcols, table, metadata_DF)
        ls = result_metadata_DF.columns.values
        negCols = [cName for cName in ls if (
        "This field is longer than max length for currency and other fields" not in result_metadata_DF.loc[:, cName].tolist())]
        self.assertEqual(len(negCols) != len(ls), True,"No string found containing more characters than it's max length")
    def test_readFile(self):
        refertocol = ["Source_Channel_Desc","ISSCOM_SubTrade_Channel_Code"]
        #refertablename = "C:\\Users\\o68454\\Documents\\Padmanabh\\Projects\\bitbucket\\testdatageneration\\testdata\\input\\testDataRead1.xls"
        refertablename = rootpath + "testdata\\input\\testDataRead.txt"
        if os.path.exists(refertablename):
            referfile = codecs.open(refertablename, 'r', 'utf-8')
            refertable = pd.read_csv(referfile).loc[:, refertocol]
            referfile.close()
        elif os.path.exists(refertablename.replace(".csv",".xls")):
            refertable = pd.read_excel(refertablename).loc[:, refertocol]
            print(refertable)
        elif os.path.exists(refertablename.replace(".csv",".txt")):
            refertable = pd.read_csv(refertablename, sep=",").loc[:, refertocol]
            print(refertable)
        #print(refertable.loc[:, "Source_Channel_Desc"])


    def test_getFileName_IncorFileName(self):
        pathname = rootpath + "testdata\\output\\TD_002_Incorrect_Data_File_Name_test"
        getFileNames = [x.replace("__channel.csv","") for x in os.listdir(pathname) if x.endswith("__channel.csv")]
        for eachfilename in getFileNames:
            assert eachfilename.startswith("Currency Neutral"),"bottler name in file name is incorrect"
            assert eachfilename.find("_1459"),"file name does not contain correct HHMM"


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()