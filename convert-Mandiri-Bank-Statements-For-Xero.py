import re
from re import sub
from decimal import Decimal
import pdfplumber
import pandas as pd
from collections import namedtuple
import datetime
import os
from enum import Enum
from decimal import Decimal

pathToPdfs = os.getcwd()+"/dropPdfHere/"
pathToCSVs = os.getcwd()+"/dropCSVHere/"

for _, _, files in os.walk(pathToCSVs):
	for filename in files:
		if '.csv' in filename:
			df = pd.read_csv(pathToCSVs + filename)
			bank_account_number = df.iloc[0,0]
			date_series = df.iloc[:,1] # Date Column
			description_1_series = df.iloc[:,4] # description_1 Column
			description_2_series = df.iloc[:,5] # description_2 Column
			debit_series = df.iloc[:,7] # debit Column
			credit_series = df.iloc[:,8] # credit Column

			# Concatenating description 1 and 2
			description_1_series = description_1_series.fillna('') # replace NaN with empty space.
			description_2_series = description_2_series.fillna('') # replace NaN with empty space.
			full_description_series = description_1_series + description_2_series
			full_description_series = full_description_series.str.strip()
			
			# Getting the Nett Amount Series
			debit_series = debit_series.replace(',','', regex=True).astype('float')
			credit_series = credit_series.replace(',','', regex=True).astype('float')
			amount_series = credit_series.subtract(debit_series)

			# Making new Data Frame
			frame = {
				'Date': date_series,
				'Description': full_description_series,
				'Amount': amount_series,
			}
			df_new = pd.DataFrame(frame)
			outputFileName = str(bank_account_number) + '.csv'
			df_new.to_csv(outputFileName, index=False)
			print (outputFileName + " has been created.")


#######################################################
# class Bank(Enum):
# 	BCA = 1
# 	POSB = 2

# class StatementLineStatus(Enum):
# 	newLine = 1 # new statement line
# 	continueLine = 2 # next line but same statement line
# 	lastLine = 3 # last statement line of the PDF

# class bankStatements:
# 	def __init__(self, bank, **kwargs):
# 		self.bank = bank
# 		self.fileName = ""
# 		self.month = ""
# 		self.year = ""

# 	def getPeriod(self, choice, **kwargs):
# 		month = None
# 		year = None

# 		## depends on which bank
# 		if self.bank == Bank.BCA:
# 			with pdfplumber.open(pathToPdfs+self.fileName) as pdf:
# 				# get first page
# 				page = pdf.pages[0]

# 				# setting size parameters (Customised for BCA bank statements only)
# 				from_width = Decimal(0.73) * page.width
# 				to_width = Decimal(0.90) * page.width
# 				from_height = Decimal(0.1475) * page.height
# 				to_height = Decimal(0.165) * page.height
				
# 				# crop the page
# 				croppedPage = self.cropPage(page=page, from_width=from_width, to_width=to_width, from_height=from_height, to_height = to_height)
# 				text = croppedPage.extract_text()
# 				month = text.split()[0]
# 				year = text.split()[1]
		
# 		## return output choice
# 		if choice == "month":
# 			return month
# 		elif choice == "year":
# 			return year
	
# 	def buildAllCSV(self):
# 		description = ""
# 		description_list = []
# 		Line = namedtuple('Line', ['date', 'amount'])
# 		lines = []
# 		date_re = re.compile(r'\d{2}/\d{2}')
# 		for _, _, files in os.walk(pathToPdfs):
# 			for filename in files:
# 				if '.pdf' in filename:
# 					self.fileName = filename
# 					self.month = self.getPeriod("month")
# 					self.year = self.getPeriod("year")
# 					if self.bank == Bank.BCA:
# 						with pdfplumber.open(pathToPdfs + self.fileName) as pdf:
# 							pages = pdf.pages
# 							page_number = 0
# 							transaction_number = 0
# 							print("################ File {} ################".format(self.fileName))

# 							for pageIndex in range(len(pages)):
# 								page = pages[pageIndex]
# 								page_number += 1
# 								# Cropping parameters
# 								from_width = Decimal(0.05) * page.width
# 								to_width = Decimal(0.8) * page.width
# 								from_height = Decimal(0.30) * page.height
# 								to_height = Decimal(0.88) * page.height
								
# 								cropped_page = page.crop((from_width, from_height, to_width, to_height))

# 								print("######### Page {} #########".format(page_number))
# 								text = cropped_page.extract_text()
# 								listOfStatementLines = text.split('\n')
								
# 								# For each line
# 								for lineIndex in range(len(listOfStatementLines)):
# 									line = listOfStatementLines[lineIndex]
# 									line = line.split() # Split line into a list of words, separated by a space.
# 									badLine = self.checkBadLine(line)
									
# 									if(not badLine and len(line)>0):
# 										if date_re.search(line[0]):  
# 											transaction_number += 1
# 											date = datetime.datetime.strptime(line[0] + "/" + self.year, '%d/%m/%Y').date()
# 											line.pop(0) # removes the date
											
# 											# if the last element is DB
# 											if line[-1] == "DB":
# 												amount_string = '-'+line[-2]
# 												line.pop() # removes DB
# 												line.pop() # removes amount
# 											else:
# 												amount_string = line[-1]
# 												line.pop() # removes amount
											
# 											completed_line = Line(date,amount_string)
# 											lines.append(completed_line)

# 											description += self.concatenate_list_of_words(line)
											
# 										else:
# 											description += self.concatenate_list_of_words(line)
										
# 										# if next line has date (ensure this is not last line)
# 										if (lineIndex < len(listOfStatementLines)-1):
# 											nextline = listOfStatementLines[lineIndex+1]
# 											if date_re.search(nextline.split()[0]):
# 												description_list.append(description)
# 												description = ""

# 										# if last line, but got next page,
# 										if (lineIndex == len(listOfStatementLines)-1 and pageIndex < len(pages)-1):
# 											nextPage = pages[pageIndex+1]
# 											cropped_nextPage = nextPage.crop((from_width, from_height, to_width, to_height))
# 											textOfNextPage = cropped_nextPage.extract_text()
# 											listOfStatementLinesInNextPage = textOfNextPage.split('\n')
# 											firstLineOfNextPage = listOfStatementLinesInNextPage[0].split()

# 											if (not self.checkBadLine(firstLineOfNextPage)):
# 												if date_re.search(firstLineOfNextPage[0]):
# 													description_list.append(description)
# 													description = ""
# 											else:
# 												description_list.append(description)
# 												description = ""
											
										
# 										# if last statement, last page,
# 										if (pageIndex == len(pages)-1 and lineIndex == len(listOfStatementLines)-6): # -6 because there are 5 additional lines of "saldo awal" etc
# 											description_list.append(description)
# 											description = ""

# 							print(len(description_list), len(lines))
# 		df = pd.DataFrame(lines)
# 		df['description'] = description_list
# 		df.to_csv('output.csv')

# 	## helper functions
# 	def cropPage(self, page, from_width, to_width, from_height, to_height, **kwargs):
# 		return page.crop((from_width, from_height, to_width, to_height))
	
# 	def checkBadLine(self, line):
# 		badLine = False
# 		if(len(line)>=2):
# 			isSaldoAwal = line[1] == "SALDO" and line[2] == "AWAL"
# 			isSaldoAwalEnd = line[0] == "SALDO" and line[1] == "AWAL"
# 			isMutasi = line[0] == "MUTASI"
# 			isSaldoAkhir = line[0] == "SALDO" and line[1] == "AKHIR"
# 			badLine = isSaldoAwal or isSaldoAwalEnd or isMutasi or isSaldoAkhir
# 		return badLine
	
# 	def concatenate_list_of_words(self, word_list):
# 		full_word = ""
# 		for word in word_list:
# 			full_word += word
# 			full_word += " "
# 		full_word.strip() #remove leading and trailing white spaces
# 		return full_word

# # Executor
# bankStatements(bank=Bank.BCA).buildAllCSV()


			




