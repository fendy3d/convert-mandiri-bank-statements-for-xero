import pandas as pd
import os

pathToCSVs = os.getcwd()+"/dropCSVHere/"

for _, _, files in os.walk(pathToCSVs):
	for filename in files:
		if '.csv' in filename:
			# Detect format by checking if the file uses semicolons
			with open(pathToCSVs + filename, 'r') as f:
				header = f.readline()

			if ';' in header:
				# Old Mandiri format: semicolon-separated
				# Columns: AccountNo;Ccy;PostDate;Remarks;AdditionalDesc;Credit Amount;Debit Amount;Close Balance
				df = pd.read_csv(pathToCSVs + filename, sep=';')
				bank_account_number = df.iloc[0,0]
				date_series = pd.to_datetime(df['PostDate']).dt.date
				full_description_series = df['Remarks'].fillna('').astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
				debit_series = df['Debit Amount'].astype(str).str.replace(',','', regex=False).astype('float')
				credit_series = df['Credit Amount'].astype(str).str.replace(',','', regex=False).astype('float')
			else:
				# New Mandiri format: comma-separated
				# Columns: Account No,Date,Val. Date,Transaction Code,Description,Description,Reference No.,Debit,Credit
				df = pd.read_csv(pathToCSVs + filename)
				bank_account_number = df.iloc[0,0]
				date_series = pd.to_datetime(df['Date'], dayfirst=True).dt.date

				# Combine the two Description columns (pandas renames duplicate to Description.1)
				desc_1 = df['Description'].fillna('').astype(str).str.strip()
				desc_2 = df['Description.1'].fillna('').astype(str).str.strip()
				full_description_series = (desc_1 + ' ' + desc_2).str.replace(r'\s+', ' ', regex=True).str.strip()

				debit_series = df['Debit'].astype(str).str.replace(',','', regex=False).astype('float')
				credit_series = df['Credit'].astype(str).str.replace(',','', regex=False).astype('float')

			# Amount: credit is positive, debit is negative
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
			print(outputFileName + " has been created.")


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
