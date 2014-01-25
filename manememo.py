#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
FILE_INPUT=$1
nkf -w8 ${FILE_INPUT} > ${FILE_INPUT}_1.utf8
sed -e 's/--/0/g' ${FILE_INPUT}_1.utf8 > ${FILE_INPUT}_2.utf8
sed -e '1,6d' ${FILE_INPUT}_2.utf8 > ${FILE_INPUT}_3.utf8
'''

import sys,re

class Manememo:
	_indexOfBank = 0
	_indexOfOther = 1
	_indexOfStock = 2
	_indexOfCard = 3

	def __init__(self):
		return

	def __del__(self):
		return

	def parseCsvFile(self,pathCsvFile):
		self.titleOfBank = []
		self.titleOfOther = []
		self.titleOfStock = []
		self.titleOfCard = []
		self.titleAll = [self.titleOfBank,self.titleOfOther,self.titleOfStock,self.titleOfCard]
		
		self.listDataOfBank = []
		self.listDataOfOther = []
		self.listDataOfStock = []
		self.listDataOfCard = []
		self.dataAll = [self.listDataOfBank,self.listDataOfOther,self.listDataOfStock,self.listDataOfCard]
		
		boolSectionStart = False
		fileCsv = open(pathCsvFile)
		
		# count to array self.titleOfAll and self.dataAll
		countSection = -1
		
		# read csv file and store the data into internal buffer
		for line in fileCsv:
			# translate to unicode and delete line feed code
			stringRawUnicode = unicode(line,'shift-jis').rstrip()
			stringRawUtf8 = stringRawUnicode.encode('utf-8')
			
			# skip blank lines
			if len(stringRawUnicode) > 0:
				# section starts with '*'
				if boolSectionStart is False and stringRawUtf8[0] is '*':
					boolSectionStart = True
					countSection += 1
					
					# skip the first word '*' and store the titles
					self.titleAll[countSection] = stringRawUnicode[1:].split(u',')
				else:
					if boolSectionStart is True:
						# store one line data as list read from CSV file
						listElementOfALine = stringRawUnicode.split(',')
						listTitle = self.titleAll[countSection]
						
						# generate dictionary sorted by title string
						dictElementOfALine = {}
						for title in listTitle:
							indexOfTitle = listTitle.index(title)
							dictElementOfALine.update({title:listElementOfALine[indexOfTitle]})
						
						# store the generated dictionary
						self.dataAll[countSection].append(dictElementOfALine)
			else:
				boolSectionStart = False
		
		fileCsv.close()
		return True

	def getParsedDataAll(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll,self.dataAll)
		else:
			return (None,None)

	def getParsedDataBank(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll[self._indexOfBank],self.dataAll[self._indexOfBank])
		else:
			return (None,None)

	def getParsedDataCard(self):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			return (self.titleAll[self._indexOfCard],self.dataAll[self._indexOfCard])
		else:
			return (None,None)

	def setParsedDataAll(self,titleAll,dataAll):
		if hasattr(self,'dataAll') and hasattr(self,'titleAll'):
			self.titleAll = titleAll
			self.dataAll = dataAll
			return True
		else:
			return False

	def saveParsedDataAllAsCsv(self,pathCsvFile):
		# check error
		if not hasattr(self,'titleAll'):
			return False
		if not hasattr(self,'dataAll'):
			return False
		
		# FIXME:
		return True

	def saveParsedDataBankAsCsv(self,pathCsvFile,titleOfBank=None,dataOfBank=None):
			return self._saveParsedDataToFile(self._indexOfBank,titleOfBank,dataOfBank,pathCsvFile)

	def saveParsedDataCardAsCsv(self,pathCsvFile,titleOfCard=None,dataOfCard=None):
			return self._saveParsedDataToFile(self._indexOfCard,titleOfCard,dataOfCard,pathCsvFile)

	def _saveParsedDataToFile(self,section,titleOfSection,dataOfSection,pathCsvFile):
		# check error
		if not hasattr(self,'titleAll'):
			return False
		if not hasattr(self,'dataAll'):
			return False
		if (titleOfSection is not None and dataOfSection is None) or \
				(titleOfSection is None and dataOfSection is not None):
			return False
		
		# open file with writable if the path is specified.
		fileSaved = open(pathCsvFile,'w')
		
		# generate first line of CSV file
		if titleOfSection is None:
			titleOfSection = self.titleAll[section]
		stringOfLine = titleOfSection[0]
		for title in titleOfSection[1:]:
			stringOfLine = stringOfLine + u',' + title
		stringOfLine = stringOfLine + u'\n'
		
		# write the genareted first line
		fileSaved.write(stringOfLine.encode('utf-8'))
		
		# generate data lines and write them to CSV file
		if dataOfSection is None:
			dataOfSection = self.dataAll[section]
		for data in dataOfSection:
			stringOfLine = data[titleOfSection[0]]
			for title in titleOfSection[1:]:
				stringOfLine = stringOfLine + u',' + data[title]
			stringOfLine = stringOfLine + u'\n'
			fileSaved.write(stringOfLine.encode('utf-8'))
		
		fileSaved.close()
		return True

if __name__ == '__main__':
	try:
		pathCsvFile = sys.argv[1]
		objManememo = Manememo()
		
		errorCode = objManememo.parseCsvFile(pathCsvFile)
		(titleAll,dataAll) = objManememo.getParsedDataAll()
		
		titleOfBank = titleAll[0]
		titleOfCard = titleAll[3]
		dataOfBank = dataAll[0]
		dataOfCard = dataAll[3]
		keyIn = u'預入金額（円）'
		keyOut = u'支払金額（円）'
		keyDiff = u'差額（円）'
		
		# dataAll has list of listOfBank, listOfStock, etc.
		# listOfBank, listOfStock has the list of dictionary data for elements.
		for dataOfEachLine in dataOfBank:
			if dataOfEachLine.get(keyOut) == u'--':
				dataOfEachLine[keyOut] = u'0'
			if dataOfEachLine.get(keyIn) == u'--':
				dataOfEachLine[keyIn] = u'0'
		
		# Add diff data to each line.
		titleOfBank.append(keyDiff)
		for dataOfEachLine in dataOfBank:
			intDiff = int(dataOfEachLine.get(keyIn)) - int(dataOfEachLine.get(keyOut))
			dataOfEachLine[keyDiff] = unicode(str(intDiff))
		
		# save bank data in the instance as CSV file
		pathCsvFileBank = re.sub(r'\.csv$','_bank.csv',pathCsvFile)
		errorCode = objManememo.saveParsedDataBankAsCsv(pathCsvFileBank,titleOfBank,dataOfBank)
		
		# save card data in the instance as CSV file
		pathCsvFileCard = re.sub(r'\.csv$','_card.csv',pathCsvFile)
		errorCode = objManememo.saveParsedDataCardAsCsv(pathCsvFileCard,titleOfCard,dataOfCard)
	except Exception as err:
		print type(err)
		print err
	finally:
		print "end function."
