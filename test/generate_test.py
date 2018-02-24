'''
Created on Oct 19, 2017

@author: kading
TO-DO
Check on how to verify date format, Country, State, City, Zip code and word and add comments to each accordingly

'''
## Change the working directory to be main folder.

import os.path
import unittest

import setup

rootpath = os.path.dirname(setup.path()) + "\\testdatageneration\\"


class Generate_Test(unittest.TestCase):
    def test(self):
        pass