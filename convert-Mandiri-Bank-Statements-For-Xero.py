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
			df = pd.read_csv(pathToCSVs + filename, sep=';')
			bank_account_number = df.iloc[0,0] #iloc[row,column]
			date_series = df.iloc[:,2] # Date Column
			full_description_series = df.iloc[:,3] # description_1 Column
			full_description_series = full_description_series.str.replace(r'\s+', ' ', regex=True) #Replace consecutive spaces with a single space in each element
			credit_series = df.iloc[:,5] # credit Column
			debit_series = df.iloc[:,6] # debit Column
			
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


#### OLD MANDIRI CSV ####
# for _, _, files in os.walk(pathToCSVs):
# 	for filename in files:
# 		if '.csv' in filename:
# 			df = pd.read_csv(pathToCSVs + filename)
# 			bank_account_number = df.iloc[0,0]
# 			date_series = df.iloc[:,1] # Date Column
# 			description_1_series = df.iloc[:,4] # description_1 Column
# 			description_2_series = df.iloc[:,5] # description_2 Column
# 			debit_series = df.iloc[:,7] # debit Column
# 			credit_series = df.iloc[:,8] # credit Column

# 			# Concatenating description 1 and 2
# 			full_description_series = description_1_series + description_2_series
# 			full_description_series = full_description_series.str.strip()
			
# 			# Getting the Nett Amount Series
# 			debit_series = debit_series.replace(',','', regex=True).astype('float')
# 			credit_series = credit_series.replace(',','', regex=True).astype('float')
# 			amount_series = credit_series.subtract(debit_series)

# 			# Making new Data Frame
# 			frame = {
# 				'Date': date_series,
# 				'Description': full_description_series,
# 				'Amount': amount_series,
# 			}
# 			df_new = pd.DataFrame(frame)
# 			outputFileName = str(bank_account_number) + '.csv'
# 			df_new.to_csv(outputFileName, index=False)
# 			print (outputFileName + " has been created.")
