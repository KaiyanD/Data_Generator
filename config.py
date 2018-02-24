import pandas as pd
#This is global negative cases to be covered in a data range 1-100 : 1 means only 1 negative record per 100 , 100 means all records
#should be negative
negative_coverage = 50
#Variables that will store dataframe values at run time
data_channel = pd.DataFrame()
data_product = pd.DataFrame()
data_customer = pd.DataFrame()
data_sales = pd.DataFrame()
data_salestype = pd.DataFrame()
data_shipfrom = pd.DataFrame()
data_shipto = pd.DataFrame()
data_mixedpack = pd.DataFrame()
#Used in generate fk
refertable = pd.DataFrame()
#Used in mixedpack data generation
refertable1 = pd.DataFrame()
refertable2 = pd.DataFrame()
#For Incorrect FK Unit test
data_ForeignKey = pd.DataFrame()

class req_count(object):
    def __init__(self):
        #Used for all_toone negative case
        self.req_decimalseparatercomma = 1
        self.req_nulltoMandatory_nothing = 1
        self.req_thousandseparatercomma = 1
        self.req_nulltoMandatory_Null = 1
        self.req_nulltoMandatory_space = 1
        self.req_notinoptiontocat = 1
        self.req_traditional_chinese_string = 1
        self.req_simplified_chinese_string = 1
        self.req_german_string = 1
        self.req_spanish_string = 1
        self.req_IncorFK = 6
        self.req_incorStringCode = 10
        self.req_incorDigitCode = 10
        self.req_incorstring_language_string = 10
        self.req_incorstring_length_string = 2
        self.req_incorstring_language_addressAndcurrency = 10
        self.req_incorstring_length_addressAndcurrency = 2
        self.req_duplicateprimarykey = 2
        self.req_add_blankmultipleprimarykey = 1