# -*- coding: utf-8 -*-
## Import all dependencies.
import random
import string
import pandas as pd
import mimesis
import codecs
import xlrd
import datetime
import json
import setup
import os
import numpy as np
import config

gen_text = mimesis.Text()
gen_addr = mimesis.Address()
gen_time = mimesis.Datetime()
gen_bis = mimesis.Business()
rootpath = os.path.dirname(setup.path()) + "\\testdatageneration\\"

class Generator:

    ###  Second level function that generate a list of random data in different type.
    ## Generate a list contains random datetime in different format.
    def generate_ls_datetime(self,fmt, numrows):
        ls = []
        _gen_time=mimesis.Datetime()
        if fmt == "YYYYMMDD":
            for i in range(numrows):
                ls.append(_gen_time.date(fmt="%Y%m%d"))
        elif fmt == "YYYYMMDD HH:MM:SS":
            for i in range(numrows):
                ls.append(_gen_time.date(fmt="%Y%m%d")+" "+_gen_time.time())
        return ls

    ## Generate a list contains random Code 
    def generate_ls_code(self, max_length, numrows, unique=False):
        ls = []
        if unique:
            while (len(ls) != numrows):
                expnumrows = numrows - len(ls)
                ls += list(set([self.gen_code(max_length) for x in range(expnumrows)]))
                ls = list(set(ls))
        else:
            ls = [self.gen_code(max_length) for x in range(numrows)]
        return ls

    ## Generate a list contains random Sentences.
    def generate_ls_sentence(self,max_length,numrows):
        ls = []
        _gen_text = mimesis.Text()
        for i in range(numrows):
            item = _gen_text.sentence()
            while len(item) > max_length:
                item = _gen_text.sentence()
            ls.append(item)
        return ls

    ## Generate a list contains random words.
    def generate_ls_word(self,max_length,numrows):
        ls = []
        _gen_text = mimesis.Text()
        for i in range(numrows):
            item = _gen_text.word()
            while len(item) > max_length:
                item = _gen_text.word()
            ls.append(item)
        return ls

    ## Generate a list contains random addresses.
    def generate_ls_address(self, max_length,numrows):
        ls = []
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            item = _gen_addr.address()
            while len(item) > max_length:
                item = _gen_addr.address()
            ls.append(item)
        return ls

    ## Generate a list contains random currency code.
    def generate_ls_currency(self, max_length,numrows):
        ls = []
        _gen_bis = mimesis.Business()
        for i in range(numrows):
            item = _gen_bis.currency_iso()
            while len(item) > max_length:
                item = _gen_bis.currency_iso()
            ls.append(item)
        return ls

    ## Generate a list contains random city name.
    def generate_ls_city(self,max_length,numrows):
        ls = []
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            item = _gen_addr.city()
            while len(item) > max_length:
                item = _gen_addr.city()
            ls.append(item)
        return ls

    ## Generate a list contains random state name.
    def generate_ls_state(self,max_length,numrows):
        ls = []
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            item = _gen_addr.state()
            while len(item) > max_length:
                item = _gen_addr.state()
            ls.append(item)
        return ls

    ## Generate a list contains random country name.
    def generate_ls_country(self,max_length,numrows):
        ls = []
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            item = _gen_addr.country()
            while len(item) > max_length:
                item = _gen_addr.country()
            ls.append(item)
        return ls

    ## Generate a list contains random postal code.
    def generate_ls_postalcode(self,max_length,numrows):
        ls = []
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            item = _gen_addr.postal_code()
            while len(item) > max_length:
                item = _gen_addr.postal_code()
            ls.append(item)
        return ls

    ## Generate a list contains random Y/N.
    def generate_ls_yn(self,numrows):
        ls = []
        for i in range(numrows):
            ls.append(self.gen_yn())
        return ls

    ## Generate a list contains random Code only in diget
    def generate_ls_digitcode(self,max_length,numrows,unique=False):
        ls = []
        if unique:
            item = self.gen_digitcode(max_length)
            while item in ls:
                item = self.gen_digitcode(max_length)
            ls.append(item)
        else:    
            for i in range(numrows):
                ls.append(self.gen_digitcode(max_length))
        return ls

    ## Generate a list contains latitude.
    def generate_ls_latitude(self,numrows):
        ls = []
        fmt = "{:.5f}"
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            ls.append(fmt.format(_gen_addr.latitude()))
        return ls

    ## Generate a list contains latitude.
    def generate_ls_longitude(self,numrows):
        ls = []
        fmt = "{:.5f}"
        _gen_addr = mimesis.Address()
        for i in range(numrows):
            ls.append(fmt.format(_gen_addr.longitude()))
        return ls

    ## Generate a list contains Decimal(18,5).
    def generate_ls_decimal(self,numrows):
        ls = []
        for i in range(numrows):
            ls.append(random.randint(-10000000,1000000000)/100000)
        return ls

    # Generate a dataframe, of which rows refer to the columns from another table.
    def generate_ls_foreignkey(self,colname, refertablename, refercolumnname, numrows, rootpath_fk):
        # *****added code  for fix to NSRP 1110, to read the get a read handle of file that has mulitlingual name
        # *****tested the change through pyunit for this method in core_test.py
        table_name = (refertablename.replace(".csv","")).split("_")[-1]
        exec("config.refertable=config.data_"+table_name)
        nrows = len(config.refertable.index)
        res_df = pd.DataFrame(columns=colname)
        for x in range(numrows):
            index =  random.randint(1,nrows)-1
            record = config.refertable.loc[[index],refercolumnname]
            res_df = res_df.append(record)
        return res_df

    ## Generate a list contains categorical data randomly chosen from options.
    def generate_ls_categorical(self,option,numrows):
        ls = [option[random.choice(range(len(option)))] for x in range(numrows)]
        return ls

    ### Unit functions that generate random unit data
    ## Generate a string of letters and digits with length between 1 and max_length
    def gen_code(self,max_length):
        l = random.randint(1,max_length)
        res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(l)])
        return res

    ## Generate a string of digits with length between 1 and max_length
    def gen_digitcode(self,max_length):
        l = random.randint(1,max_length)
        res = ''.join([random.choice(string.digits) for n in range(l)])
        return res

    ## Generate binaries. Either "Y" or "N".
    def gen_yn(self):
        return random.choice(["Y","N"])

    ## Pick an option from the list.
    def pick_cat(self,ls):
        return random.choice(ls)            
    
    ## Generate Chinese traditional and character.
    def gen_ChineseTraditional(self):
        val = random.randint(0x4E00, 0x9FBF)
        return chr(val)

    ## Generate Chinese simplified character
    def gen_ChineseSimplified(self):
        while True:
            try:
                head = random.randint(0xB0, 0xCF)
                body = random.randint(0xA, 0xF)
                tail = random.randint(0, 0xF)
                val = ( head << 8 ) | (body << 4) | tail
                str = "%x" % val
                res = bytes.fromhex(str).decode('gb2312')
                break
            except UnicodeDecodeError:
                continue
        return res

    ## Generate Spanish Special character
    def gen_Spanish(self):
        char_ls = ['ô', 'É', 'º', 'ó', 'Í', 'Ú', 'õ', 'á', 'ñ', 'í', 'Ê', 'è', 'â', 'ò', 'ª', 'ö', 'Ô', 'ã', 'ü', 'Á', '»', '¡', 'é', 'î', '€', 'ú', 'Ã', 'Â', 'À', 'Ó', '¿', '’', 'ç', '«', 'à', 'ê', 'Ç']
        return random.choice(char_ls)

    ## Generate German Special character
    def gen_German(self):
        char_ls = ['Ü', 'ö', 'ä', 'ß', 'ü', 'Ä','Ö','ẞ']
        return random.choice(char_ls)

    ## Generate random set from parent set for specified size
    def gen_random_set(self, parentset, excludeset, int_size):
        try:
            parentset = [x for x in parentset if x not in excludeset]
            int_random_set = random.sample(parentset, int_size)
            return parentset, int_random_set
        except:
            print(parentset)
            print(excludeset)
            print(int_size)
            raise Exception('Crashed!!')

class Changer:
    def get_cols(self,dicofcols,attribute,value):
        ls = [''.join(p["name"]) for p in dicofcols if p[attribute] == value]
        for p in dicofcols:
            if type(p[attribute]) == list:
                iC = 0
                for x in p[attribute]:
                    if x == value:
                        ls.append(p["name"][iC])
                        iC = iC + 1
        return ls
    def add_null(self,dicofcols,dataframe,metadata_DF):
        for dicofcol in dicofcols:
            if dicofcol["mandatory"] == 0:
                numofnull = random.choice(dataframe.index)
                ind = random.sample(set(dataframe.index),numofnull)
                dataframe.loc[ind,dicofcol["name"]] = ""
                metadata_DF.loc[[x for x in ind],dicofcol["name"]] = "P"
        return dataframe,metadata_DF
    def _add_thousandseparatercomma_tosinglevalue(self,value):
        if value != "":
            value = "{:,}".format(float(value))
        return value
    def add_thousandseparatercomma(self, dicofcols, dataframe,metadata_DF):
        for dicofcol in dicofcols:
            if dicofcol["type"] == "Decimal":
                dataframe[dicofcol["name"]] = pd.Series([self._add_thousandseparatercomma_tosinglevalue(val) for val in dataframe[dicofcol["name"]]], index = dataframe.index)
                metadata_DF[dicofcol["name"]] = "thousand separater as comma"
        return dataframe, metadata_DF
    def add_decimalseparatercomma(self, dicofcols,dataframe,metadata_DF):
        for dicofcol in dicofcols:
            if dicofcol["type"] == "Decimal":
                dataframe[dicofcol["name"]] = [str(x).replace(".",",") for x in dataframe[dicofcol["name"]]]
                metadata_DF[dicofcol["name"]] = ["decimal separater as comma"]*len(metadata_DF[dicofcol["name"]])
        return dataframe, metadata_DF
    def add_keyvaluetojson(self,path,key,value):
        with open(path,"r") as json_file:
            json_decoded = json.load(json_file)
        json_decoded[key] = value
        json_file.close()
        with open(path, 'w') as json_file:
            json.dump(json_decoded, json_file)
        json_file.close()
    def add_nulltoMandatory_nothing(self,dicofcols,dataframe,metadata_DF):
        for dic in dicofcols:
            if dic["mandatory"] == 1:
                numofnull = random.choice(range(len(dataframe.index)))+1
                ind = random.sample(set(dataframe.index),numofnull)
                dataframe.loc[ind,dic["name"]] = ""
                metadata_DF.loc[[x+1 for x in ind],dic["name"]] = "This field is ''"
        return dataframe,metadata_DF
    def add_nulltoMandatory_space(self,dicofcols,dataframe,metadata_DF):
        for dic in dicofcols:
            if dic["mandatory"] == 1:
                numofnull = random.choice(range(len(dataframe.index)))+1
                ind = random.sample(set(dataframe.index),numofnull)
                dataframe.loc[ind,dic["name"]] = " "
                metadata_DF.loc[[x+1 for x in ind],dic["name"]] = "This field is ' '"
        return dataframe,metadata_DF
    def add_nulltoMandatory_Null(self,dicofcols,dataframe,metadata_DF):
        for dic in dicofcols:
            if dic["mandatory"] == 1:
                numofnull = random.choice(range(len(dataframe.index)))+1
                ind = random.sample(set(dataframe.index),numofnull)
                dataframe.loc[ind,dic["name"]] = "Null"
                metadata_DF.loc[[x+1 for x in ind],dic["name"]] = "This field is 'Null'"
        return dataframe,metadata_DF
    def add_notinoptiontocat(self,dicofcols,dataframe,metadata_DF):
        generator = Generator()
        for dic in dicofcols:
            if dic["type"] == "Categorical":
                numofnot = random.choice(range(len(dataframe.index)))+1
                ind = random.sample(set(dataframe.index),numofnot)
                dataframe.loc[ind,dic["name"]] = generator.gen_code(10)
                metadata_DF.loc[[x+1 for x in ind],dic["name"]] = "This field is not in option."
        return dataframe,metadata_DF
    def add_specialcharactertostring(self, dicofcols, dataframe, metadata_DF,language):
        for dic in dicofcols:
            if dic["type"] == "String":
                if dic["sub-type"] not in ["Currency","Postal_Code"]:
                    numofchinese = 1 if len(dataframe.index)==1 else random.choice(range(1,len(dataframe.index)))
                    ind = random.sample(set(dataframe.index),numofchinese)
                    for i in ind:
                        stringtoreplace = str(dataframe.loc[i,dic["name"]])
                        if len(stringtoreplace) < 3:
                            stringtoreplace = "abc"
                        position = random.randint(1,(len(stringtoreplace)-2))
                        generator = Generator()
                        if language == "Simplified Chinese":
                            stringtoreplace = stringtoreplace[:(position-1)] + generator.gen_ChineseSimplified() + stringtoreplace[(position+2):]
                            metadata_DF.loc[(i+1),dic["name"]] = "This field contains simplified Chinese character"
                        elif language == "Traditional Chinese":
                            stringtoreplace = stringtoreplace[:(position-1)] + generator.gen_ChineseTraditional() + stringtoreplace[(position+2):]
                            metadata_DF.loc[(i+1),dic["name"]] = "This field contains traditional Chinese character"
                        elif language == "Spanish":
                            stringtoreplace = stringtoreplace[:(position-1)] + generator.gen_Spanish() + stringtoreplace[(position+2):]
                            metadata_DF.loc[(i+1),dic["name"]] = "This field contains Spanish character"
                        elif language == "German":
                            stringtoreplace = stringtoreplace[:(position-1)] + generator.gen_German() + stringtoreplace[(position+2):]
                            metadata_DF.loc[(i+1),dic["name"]] = "This field contains German character"
                        else:
                            print("This language is not available")
                        dataframe.loc[i,dic["name"]] = stringtoreplace
        return dataframe, metadata_DF
    def add_alltoone(self,dicofcols,dataframe,metadata_DF):
        int_len = len(dataframe.index) -1
        int_set = set(dataframe.index)
        count = config.req_count()
        vars_dict = vars(count)
        count = None
        value_vars = [vars_dict[item] for item in vars_dict]
        total_count = sum(value_vars)
        vars_keys = [item for item in vars_dict]
        if total_count >= int_len:
            diff_ = total_count-int_len
            while(diff_!=0):
                vars_list = [item for item in vars_keys if vars_dict[item]>0]
                item_ = random.choice(vars_list)
                vars_dict[item_] = vars_dict[item_] - 1
                diff_ = diff_-1
        else:
            diff_ = int_len-total_count
            while (diff_ != 0):
                item_ = random.choice(vars_keys)
                # exec("count."+item_+"=count."+item_+" + 1")
                vars_dict[item_] = vars_dict[item_] + 1
                diff_ = diff_ - 1
        int_random_set=[0]
        generator = Generator()
        m_dataframe = dataframe.copy()
        m_metadata_DF = metadata_DF.copy()
        #Add for thousand separator
        if(vars_dict["req_thousandseparatercomma"]>0):
            int_set,int_random_set = generator.gen_random_set(int_set,int_random_set,vars_dict["req_thousandseparatercomma"])
            int_random_set_m = [x+1 for x in int_random_set]
            dataframe_c,metadata_DF_c= self.add_thousandseparatercomma(dicofcols,dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set]=dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m]=metadata_DF_c.loc[int_random_set_m]
        #Add for decimal separated comma
        if(vars_dict["req_decimalseparatercomma"]>0):
            int_set,int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_decimalseparatercomma"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_decimalseparatercomma(dicofcols,dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add for nothing
        if(vars_dict["req_nulltoMandatory_nothing"]>0):
            int_set,int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_nulltoMandatory_nothing"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_nulltoMandatory_nothing(dicofcols,dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add for Null
        if(vars_dict["req_nulltoMandatory_Null"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_nulltoMandatory_Null"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_nulltoMandatory_Null(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add for space
        if(vars_dict["req_nulltoMandatory_space"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_nulltoMandatory_space"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_nulltoMandatory_space(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add for not in category
        if(vars_dict["req_notinoptiontocat"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_notinoptiontocat"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_notinoptiontocat(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add special characters in mentioned languages
        #Add Simplified chinese
        if(vars_dict["req_simplified_chinese_string"]>0):
            int_set,int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_simplified_chinese_string"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c,metadata_DF_c= self.add_specialcharactertostring(dicofcols,dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m],"Simplified Chinese")
            dataframe.loc[int_random_set]=dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m]=metadata_DF_c.loc[int_random_set_m]
        #Add Traditional chinese
        if(vars_dict["req_traditional_chinese_string"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set, vars_dict["req_traditional_chinese_string"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_specialcharactertostring(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m],"Traditional Chinese")
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add spanish
        if(vars_dict["req_spanish_string"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_spanish_string"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_specialcharactertostring(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m],"Spanish")
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #Add German
        if(vars_dict["req_german_string"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set, vars_dict["req_german_string"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_specialcharactertostring(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m],"German")
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #For negative_ foreign key
        if(vars_dict["req_IncorFK"]>6):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_IncorFK"])
            dataframe_c = m_dataframe.copy()
            metadata_DF_c = m_metadata_DF.copy()
            dataframe_c, metadata_DF_c = self.add_IncorFK(dicofcols, dataframe_c, metadata_DF_c)
            inds = list(metadata_DF_c[metadata_DF_c.apply(lambda x: min(x) != max(x) != "P", 1)].index)
            inds = [indx for indx in inds if indx != inds[0] and indx != inds[len(inds) - 1] and (
            inds[inds.index(indx) - 1] == indx - 1 and inds[inds.index(indx) + 1] == indx + 1)]
            ls_tmp = []
            for indx in inds:
                ls_tmp.append(indx - 1)
                ls_tmp.append(indx)
                ls_tmp.append(indx + 1)
            int_c = 0
            int_req = len(int_random_set) - len(int_random_set) % 3
            int_req_set = random.sample(int_random_set, int_req)
            if (len(ls_tmp) > 1):
                for int_rw in int_req_set:
                    if (int_c == len(ls_tmp)):
                        break
                    dataframe.loc[int_rw] = dataframe_c.loc[ls_tmp[int_c] - 1]
                    metadata_DF.loc[int_rw + 1] = metadata_DF_c.loc[ls_tmp[int_c]]
                    int_c = int_c + 1
        # Negative case:for invalid string code
        if(vars_dict["req_incorStringCode"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_incorStringCode"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_incorStringCode(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        # Negative case:for invalid digit code
        if(vars_dict["req_incorDigitCode"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_incorDigitCode"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_incorDigitCode(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        ### negative case: contains incorrect language and punctuations for string fields like sentence,word,address and city
        if(vars_dict["req_incorstring_language_string"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set, vars_dict["req_incorstring_language_string"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_incorstring_language_string(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        ### negative case: contains more length than max length for string fields like sentence,word,address and city
        if(vars_dict["req_incorstring_length_string"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_incorstring_length_string"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_incorstring_length_string(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        ### negative case: contains incorrect language and punctuations for state,country,postalcode and curruency fields
        if(vars_dict["req_incorstring_language_addressAndcurrency"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_incorstring_language_addressAndcurrency"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_incorstring_language_addressAndcurrency(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        ### negative case: contains more length than max length for state,country,postalcode and curruency fields
        if(vars_dict["req_incorstring_length_addressAndcurrency"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_incorstring_length_addressAndcurrency"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_incorstring_length_addressAndcurrency(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        #For negative : Duplicate primary keys
        if(vars_dict["req_duplicateprimarykey"]>1):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_duplicateprimarykey"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_duplicateprimarykey(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]
        # For negative : Blank multiple primary keys
        if(vars_dict["req_add_blankmultipleprimarykey"]>0):
            int_set, int_random_set = generator.gen_random_set(int_set, int_random_set,vars_dict["req_add_blankmultipleprimarykey"])
            int_random_set_m = [x + 1 for x in int_random_set]
            dataframe_c, metadata_DF_c = self.add_blankmultipleprimarykey(dicofcols, dataframe.ix[int_random_set],metadata_DF.ix[int_random_set_m])
            dataframe.loc[int_random_set] = dataframe_c.loc[int_random_set]
            metadata_DF.loc[int_random_set_m] = metadata_DF_c.loc[int_random_set_m]

        return dataframe, metadata_DF
    '''TODO - Check in case the composite values after swaping the data for foreign key is yet valid'''
    def add_IncorFK(self, dicofcols, dataframe, metadata_DF):
        gen = Generator()
        for dic in dicofcols:
            if dic["type"] == "Foreign_Key":
                '''Add incorrect Foreign Key'''
                numFK = random.choice(range(3)) + 1
                res_fk_df = pd.DataFrame(columns=dic["name"])
                ls_fk = (res_fk_df.columns.values.tolist())
                #ind = random.sample(set(dataframe.index), numFK)
                ind = random.sample(set(dataframe.index) - {0} - {len(dataframe.index)-1}, numFK)
                ls_sampleDF = dataframe.loc[:, ls_fk[0]].tolist()
                while True:
                    incorrectFK = gen.generate_ls_code(5, 1)
                    if (incorrectFK in ls_sampleDF):
                        continue
                    else:
                        break
                dataframe.loc[ind, ls_fk[0]] = incorrectFK
                metadata_DF.loc[[x + 1 for x in ind], ls_fk[0]] = "This Foreign key is incorrect"
                '''Change sequence of composite foreign key'''
                if (len(res_fk_df.columns) > 1):
                    for swapVal in ind:
                        if ({dataframe.loc[swapVal + 1, ls_fk[0]], dataframe.loc[swapVal + 1, ls_fk[1]]} != {dataframe.loc[swapVal - 1, ls_fk[0]], dataframe.loc[swapVal - 1, ls_fk[1]]}):
                            dataframe.loc[swapVal + 1, ls_fk[1]], dataframe.loc[swapVal - 1, ls_fk[1]] = \
                                dataframe.loc[swapVal - 1,ls_fk[1]],dataframe.loc[swapVal + 1,ls_fk[1]]
                            metadata_DF.loc[swapVal + 2, ls_fk[1]] = "This Foreign key is swapped"
                            metadata_DF.loc[swapVal, ls_fk[1]] = "This Foreign key is swapped"
                        else:
                            dataframe.loc[swapVal, ls_fk[1]], dataframe.loc[swapVal - 1, ls_fk[1]] = \
                                dataframe.loc[swapVal - 1, ls_fk[1]], dataframe.loc[swapVal, ls_fk[1]]
                            metadata_DF.loc[swapVal + 1, ls_fk[1]] = "This Foreign key is swapped"
                            metadata_DF.loc[swapVal, ls_fk[1]] = "This Foreign key is swapped"
                        # return res_fk_df,metadata_DF
        return dataframe, metadata_DF
    ##Updated
    def add_incorstring_language_string(self, dicofcols, dataframe, metadata_DF):
        generator = Generator()
        for dic in dicofcols:
            if "sub-type" in dic:
                if dic["sub-type"] == "Sentence"  or dic["sub-type"] == "Word" or dic["sub-type"] == "Address" or dic["sub-type"] == "City":
                    mxChr = random.choice(range(1, dic["max_length"]))
                    negative_cases = ["trd_chn_lng", "smp_chn_lng", "spnsh_lng", "germn_lng", "punctuation_marks"]

                    if (len(dataframe.index) < len(negative_cases)):
                        _rows = list(dataframe.index)
                        _cases = random.sample(negative_cases, len(_rows))
                    else:
                        _rows = random.sample(list(dataframe.index),int((len(dataframe.index)*config.negative_coverage)/100))
                        _cases = [negative_cases[i%len(negative_cases)] for i in range(0,len(_rows))]
                        # _rows = random.sample(list(dataframe.index), negative_cases.__len__())
                        # _cases = negative_cases
                    int_case = 0
                    for rw in _rows:
                        if ("trd_chn_lng" == _cases[int_case]):
                            lng = [generator.gen_ChineseTraditional() for x in range(0, mxChr)]
                        if ("smp_chn_lng" == _cases[int_case]):
                            lng = [generator.gen_ChineseSimplified() for x in range(0, mxChr)]
                        if ("spnsh_lng" == _cases[int_case]):
                            lng = [generator.gen_Spanish() for x in range(0, mxChr)]
                        if ("germn_lng" == _cases[int_case]):
                            lng = [generator.gen_German() for x in range(0, mxChr)]
                        if ("punctuation_marks" == _cases[int_case]):
                            lng = list(string.punctuation)

                        if str(dataframe.loc[rw, dic["name"]]) != "":
                            xData = list(str(dataframe.loc[rw, dic["name"]]))
                            xData[random.choice(range(0, len(xData)))] = lng[random.randint(0, len(lng)-1)]
                        else:
                            xData = []
                            xData.append(lng[random.randint(0, len(lng)-1)])
                        dataframe.loc[rw, dic["name"]] = ''.join(xData)
                        metadata_DF.loc[rw + 1, dic["name"]] = "This field is abnormal Character, punctuation for string fields"
                        int_case = int_case + 1
        return dataframe, metadata_DF
    ##Updated
    def add_incorstring_length_string(self, dicofcols, dataframe, metadata_DF):
        for dic in dicofcols:
            if "sub-type" in dic:
                if dic["sub-type"] == "Sentence" or dic["sub-type"] == "Word" or dic["sub-type"] == "Address" or dic["sub-type"] == "City":
                    negative_cases = ["max_length", "boundry_length"]
                    if (len(dataframe.index) < len(negative_cases)):
                        _rows = list(dataframe.index)
                        _cases = random.sample(negative_cases, len(_rows))
                    else:
                        _rows = random.sample(list(dataframe.index),int((len(dataframe.index)*config.negative_coverage)/100))
                        _cases = [negative_cases[i%len(negative_cases)] for i in range(0,len(_rows))]
                        # _rows = random.sample(list(dataframe.index), negative_cases.__len__())
                        # _cases = negative_cases
                    int_case = 0
                    for rw in _rows:
                        if ("boundry_length" == _cases[int_case]):
                            res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(dic["max_length"])])
                            dataframe.loc[rw, dic["name"]] = res
                        elif("max_length" == _cases[int_case]):
                            l = random.randint(dic["max_length"]+1, dic["max_length"] + 10)
                            res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(l)])
                            dataframe.loc[rw, dic["name"]] = res
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is longer than max length for string fields"
                        int_case = int_case + 1
        return dataframe, metadata_DF
    ##Updated
    def add_incorstring_language_addressAndcurrency(self, dicofcols, dataframe, metadata_DF):
        generator = Generator()
        for dic in dicofcols:
            if "sub-type" in dic:
                if dic["sub-type"] == "State"  or dic["sub-type"] == "Country" or dic["sub-type"] == "Postal_Code" or dic["sub-type"] == "Currency":
                    mxChr = random.choice(range(1, dic["max_length"]))
                    negative_cases = ["trd_chn_lng", "smp_chn_lng", "spnsh_lng","germn_lng", "punctuation_marks"]

                    if (len(dataframe.index) < len(negative_cases)):
                        _rows = list(dataframe.index)
                        _cases = random.sample(negative_cases, len(_rows))
                    else:
                        _rows = random.sample(list(dataframe.index),int((len(dataframe.index)*config.negative_coverage)/100))
                        _cases = [negative_cases[i%len(negative_cases)] for i in range(0,len(_rows))]
                        # _rows = random.sample(list(dataframe.index), len(negative_cases))
                        # _cases = negative_cases
                    int_case = 0
                    for rw in _rows:
                        if ("trd_chn_lng" == _cases[int_case]):
                            lng = [generator.gen_ChineseTraditional() for x in range(0, mxChr)]
                        if ( "smp_chn_lng"== _cases[int_case]):
                            lng = [generator.gen_ChineseSimplified() for x in range(0, mxChr)]
                        if ( "spnsh_lng"== _cases[int_case]):
                            lng =  [generator.gen_Spanish() for x in range(0, mxChr)]
                        if ("germn_lng" == _cases[int_case]):
                            lng = [generator.gen_German() for x in range(0, mxChr)]
                        if ("punctuation_marks"== _cases[int_case]):
                            lng = list(string.punctuation)
                        xData = []
                        if str(dataframe.loc[rw, dic["name"]]) !="":
                            xData = list(str(dataframe.loc[rw, dic["name"]]))
                            xData[random.choice(range(0, len(xData)))] = lng[random.randint(0, len(lng)-1)]
                        else:
                            xData =[]
                            xData.append(lng[random.randint(0, len(lng)-1)])
                        dataframe.loc[rw, dic["name"]] = ''.join(xData)
                        metadata_DF.loc[rw + 1, dic["name"]] = "This field is abnormal Character, punctuation for currency and other fields"
                        int_case = int_case + 1
        return dataframe, metadata_DF
    ##Updated
    def add_incorstring_length_addressAndcurrency(self, dicofcols, dataframe, metadata_DF):
        for dic in dicofcols:
            if "sub-type" in dic:
                if dic["sub-type"] == "State"  or dic["sub-type"] == "Country" or dic["sub-type"] == "Postal_Code" or dic["sub-type"] == "Currency":
                    negative_cases = ["max_length","boundry_length"]
                    if (len(dataframe.index) < len(negative_cases)):
                        _rows = list(dataframe.index)
                        _cases = random.sample(negative_cases, len(_rows))
                    else:
                        _rows = random.sample(list(dataframe.index),int((len(dataframe.index)*config.negative_coverage)/100))
                        _cases = [negative_cases[i%len(negative_cases)] for i in range(0,len(_rows))]
                        # _rows = random.sample(list(dataframe.index), negative_cases.__len__())
                        # _cases = negative_cases
                    int_case = 0
                    for rw in _rows:
                        if ("boundry_length"==_cases[int_case]):
                            res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(dic["max_length"])])
                            dataframe.loc[rw, dic["name"]] = res
                        elif ("max_length" == _cases[int_case]):
                            l = random.randint(dic["max_length"]+1, dic["max_length"] + 10)
                            res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(l)])
                            dataframe.loc[rw, dic["name"]] = res
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is longer than max length for currency and other fields"
                        int_case = int_case +1
        return dataframe, metadata_DF
    ##Updated
    def add_incorStringCode(self,dicofcols, dataframe, metadata_DF):
        generator = Generator()
        for dic in dicofcols:
            if "sub-type" in dic:
                if dic["type"] == "String" and dic["sub-type"] == "Code":
                    mxChr = random.choice(range(1, dic["max_length"]))
                    l = random.randint(dic["max_length"] + 1, dic["max_length"] + 10)
                    negative_cases = ["incr_spChars", "incr_sign", "trd_chn_lng", "smp_chn_lng", "spnsh_lng","germn_lng", "boundry_lengh", "max_length"]
                    if (len(dataframe.index) < len(negative_cases)):
                        _rows = list(dataframe.index)
                        _cases = random.sample(negative_cases, len(_rows))
                    else:
                        _rows = random.sample(list(dataframe.index),int((len(dataframe.index)*config.negative_coverage)/100))
                        _cases = [negative_cases[i%len(negative_cases)] for i in range(0,len(_rows))]
                        # _rows = random.sample(list(dataframe.index), negative_cases.__len__())
                        # _cases = negative_cases
                    int_case = 0
                    for rw in _rows:
                        # Special characters
                        if("incr_spChars"==_cases[int_case]):
                            spList = list("!@#$%^&*(){}<>?:”;’.|")
                            xData = list(str(dataframe.loc[rw,dic["name"]]))
                            if xData == "" or len(xData)<2:
                                xData = xData + list(random.choice(spList))
                            else:
                                xData[random.choice(range(0,len(xData)-1))] = random.choice(spList)#spList[random.choice(range(0,len(spList)-1))]
                            dataframe.loc[rw,dic["name"]] = ''.join(xData)
                            metadata_DF.loc[rw+1,dic["name"]] = "This field is incorrect code with special characters"
                        # Incorrect sign
                        elif("incr_sign" == _cases[int_case]):
                            replacingSign = ['+','-']
                            xData = list(str(dataframe.loc[rw,dic["name"]]))
                            if xData == "" or len(xData)<2:
                                xData.append(random.choice(replacingSign))
                            else:
                                xData[random.choice(range(0,len(xData)-1))] = random.choice(replacingSign)
                            dataframe.loc[rw,dic["name"]] = ''.join(xData)
                            metadata_DF.loc[rw+1,dic["name"]] = "This field is incorrect code, contains code with sign"
                        #Incorrect language
                        elif ("trd_chn_lng" == _cases[int_case]):
                            trd_chn = [generator.gen_ChineseTraditional() for x in range(0, mxChr) if x*len(generator.gen_ChineseTraditional().encode('utf-8')) < dic["max_length"]]
                            dataframe.loc[rw, dic["name"]] = ''.join(random.sample(trd_chn, len(trd_chn)))
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid code with different language"
                        elif("smp_chn_lng" == _cases[int_case]):
                            smp_chn = [generator.gen_ChineseSimplified() for x in range(0, mxChr) if x*len(generator.gen_ChineseSimplified().encode('utf-8')) < dic["max_length"]]
                            dataframe.loc[rw, dic["name"]] = ''.join(random.sample(smp_chn, len(smp_chn)))
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid code with different language"
                        elif("spnsh_lng" == _cases[int_case]):
                            spnsh = [generator.gen_Spanish() for x in range(0, mxChr) if x*len(generator.gen_Spanish().encode('utf-8')) < dic["max_length"]]
                            dataframe.loc[rw, dic["name"]] = ''.join(random.sample(spnsh, len(spnsh)))
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid code with different language"
                        elif("germn_lng" == _cases[int_case]):
                            germn = [generator.gen_German() for x in range(0, mxChr) if x*len(generator.gen_German().encode('utf-8')) < dic["max_length"]]
                            dataframe.loc[rw, dic["name"]] = ''.join(random.sample(germn, len(germn)))
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid code with different language"
                        #Boundry length
                        elif("boundry_length"==_cases[int_case]):
                            res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(dic["max_length"])])
                            dataframe.loc[rw, dic["name"]] = res
                        #More than max length
                        elif("max_length"==_cases[int_case]):
                            res = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(l)])
                            dataframe.loc[rw, dic["name"]] = res
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is code with length more than max length"
                        int_case = int_case +1
        return dataframe,metadata_DF
    ##Updated
    def add_incorDigitCode(self,dicofcols, dataframe, metadata_DF):
        generator = Generator()
        for dic in dicofcols:
            if "sub-type" in dic:
                if dic["type"] == "Integer" and dic["sub-type"] == "Code":
                    mxChr = random.choice(range(1, dic["max_length"]))
                    l = random.randint(dic["max_length"] + 1, dic["max_length"] + 10)
                    negative_cases = [
                        "incr_Digit","incr_spChars","incr_sign","trd_chn_lng","smp_chn_lng","spnsh_lng","germn_lng","boundry_lengh","max_length"
                        ]
                    if(len(dataframe.index)<len(negative_cases)):
                        _rows = list(dataframe.index)
                        _cases = random.sample(negative_cases,len(_rows))
                    else:
                        _rows = random.sample(list(dataframe.index),int((len(dataframe.index)*config.negative_coverage)/100))
                        _cases = [negative_cases[i%len(negative_cases)] for i in range(0,len(_rows))]
                        # _rows = random.sample(list(dataframe.index),negative_cases.__len__())
                        # _cases = negative_cases
                    int_case = 0
                    for rw in _rows:
                        # Digit replaced by string
                        if ("incr_Digit" == _cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([random.choice(string.ascii_letters) for n in range(0, 3)])
                            metadata_DF.loc[rw+1, dic["name"]] = "This field is incorrect Digit code replaced by string"
                        # Special characters
                        elif("incr_spChars"  == _cases[int_case]):
                            xData = list(str(dataframe.loc[rw,dic["name"]]))
                            if xData == "" or len(xData)<2:
                                xData.append(random.choice(list("!@#$%^&*(){}<>?:”;’|")))
                            else:
                                xData[random.choice(range(0,len(xData)-1))] = random.choice(list("!@#$%^&*(){}<>?:”;’|"))
                            dataframe.loc[rw,dic["name"]] = ''.join(xData)
                            metadata_DF.loc[rw+1,dic["name"]] = "This field is invalid Digit code with special characters"
                        #Incorrect sign
                        elif("incr_sign" == _cases[int_case]):
                            xData = list(str(dataframe.loc[rw,dic["name"]]))
                            if xData != "":
                                if len(xData)< dic["max_length"]:
                                    xData.insert(0,random.choice(['+', '-']))
                                else:
                                    xData[0] = random.choice(random.choice(['+', '-']))
                                dataframe.loc[rw,dic["name"]] = ''.join(xData)
                                metadata_DF.loc[rw+1,dic["name"]] = "This field is invalid Digit code, contains code with sign"
                        #Incorrect language
                        elif ("trd_chn_lng" == _cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([generator.gen_ChineseTraditional() for x in range(0, mxChr) if x * len(generator.gen_ChineseTraditional().encode('utf-8')) < dic["max_length"]])
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid Digit code with incorrect language"
                        elif ("smp_chn_lng" == _cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([generator.gen_ChineseTraditional() for x in range(0, mxChr) if x * len(generator.gen_ChineseSimplified().encode('utf-8')) < dic["max_length"]])
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid Digit code with incorrect language"
                        elif ("spnsh_lng" == _cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([generator.gen_ChineseTraditional() for x in range(0, mxChr) if x * len(generator.gen_Spanish().encode('utf-8')) < dic["max_length"]])
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid Digit code with incorrect language"
                        elif ("germn_lng" == _cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([generator.gen_ChineseTraditional() for x in range(0, mxChr) if x * len(generator.gen_German().encode('utf-8')) < dic["max_length"]])
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid Digit code with incorrect language"
                        #More than max length
                        elif("max_length" == _cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([random.choice(string.digits) for n in range(l)])
                            metadata_DF.loc[rw + 1, dic["name"]] = "This field is invalid Digit code with length more than max length"
                        #Boundry length
                        elif("boundry_length"==_cases[int_case]):
                            dataframe.loc[rw, dic["name"]] = ''.join([random.choice(string.digits) for n in range(dic["max_length"])])
                        int_case = int_case + 1
        return dataframe,metadata_DF

    def add_duplicateprimarykey(self, dicofcols, dataframe, metadata_DF):
        ls = Changer().get_cols(dicofcols,"partofKey",1)
        for cName in ls:
            if(len(dataframe.index)>1):
                numofdpk = int(len(dataframe.index)*config.negative_coverage/100)
                numofdpk = numofdpk if numofdpk>2 else 2
                ind = random.sample(set(dataframe.index), numofdpk)
            else:
                return dataframe, metadata_DF
            dataframe.loc[ind, ls] = dataframe.loc[min(ind), ls].values
            metadata_DF.loc[[x + 1 for x in ind if x != min(ind)], ls] = "This field is duplicated for combined primary key"
            break
        return dataframe, metadata_DF
    #Make combined primary key blank
    def add_blankmultipleprimarykey(self, dicofcols, dataframe, metadata_DF):
        ls = Changer().get_cols(dicofcols, "partofKey", 1)
        for cName in ls:
            if (len(dataframe.index) > 0):
                numofdpk = int(len(dataframe.index) * config.negative_coverage / 100)
                numofdpk = numofdpk if numofdpk > 1 else 1
                ind = random.sample(set(dataframe.index), numofdpk)
            else:
                return dataframe, metadata_DF
            ind = random.sample(set(dataframe.index), numofdpk)
            dataframe.loc[ind, ls] = ""
            metadata_DF.loc[[x + 1 for x in ind], ls] = "This field is '' for combined primary key"
            break
        return dataframe, metadata_DF
'''NSRP 929 - Generate File name condition - postive and negative'''
class FileNameFormater:
    def fileNameFormat(self,bottlername):
        presenttime = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        #Correct bottlername with datetime format (YYYYmmdd_HHMM)
        bottlername_prefix = bottlername + "_" + presenttime + "_"
        #Incorrect bottlername with correct datetime format
        bottlername_prefixIncor1 = bottlername + "InCor_" + presenttime + "_"
        # Correct bottler name with incorrect datetime format (HHMM_YYYYmmdd)
        presenttime_InCor = datetime.datetime.now().strftime('%H%M_%Y%m%d')
        bottlername_prefixIncor2 = bottlername + "_" + presenttime_InCor + "_"
        # Correct bottler name with past datetime format (HHMM_YYYYmmdd)
        pasttime_InCor = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y%m%d_%H%M')
        bottlername_prefixIncor3 = bottlername + "_" + pasttime_InCor + "_"
        # Correct bottler name with future datetime format (HHMM_YYYYmmdd)
        futuretime_InCor = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y%m%d_%H%M')
        bottlername_prefixIncor4 = bottlername + "_" + futuretime_InCor + "_"

        ls_fileFormat = [bottlername_prefix,bottlername_prefixIncor1,bottlername_prefixIncor2,bottlername_prefixIncor3,bottlername_prefixIncor4]
        return ls_fileFormat
