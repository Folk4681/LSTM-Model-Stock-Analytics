import json, shutil, os, dateutil.parser, time
from dataMiner import loadingBar, MONTHS, YEARS


oldFileFolder = '../data/NYT_ArticlesJSON/'
newFileFolder = '../data/NYT_ArticlesTXT/'

def dataDirCRUD(data_folder,create = True):
	if os.path.exists(data_folder):
		shutil.rmtree(data_folder)
	if create:
		os.makedirs(data_folder)

"""def leadParaErrorHandling(key):
	try:
		para = key['lead_paragraph']
		para = para.encode("ascii", "ignore")
	except(KeyError, AttributeError) as e:
		para = ""
	return para"""

def processData():
	length = len(YEARS)*MONTHS
	count = 0
	print("Converting JSON to TXT...")
	for file in os.listdir(oldFileFolder):
		with open(oldFileFolder+file, "r") as f:
			data = json.load(f)
			createTXTFile(data, file)
			count = count+1
			loadingBar(length, count)
	print("Finished formatting JSON. Check your " + newFileFolder + " folder.")

def createTXTFile(data, oldFile):
	newFile = open(newFileFolder + oldFile[:-4] + "txt", 'a')
	for key in data['response']['docs']:
		headline = key['headline']['main']
		#lead_para = leadParaErrorHandling(key)
		pub_date = key['pub_date']
		date = str(dateutil.parser.parse(pub_date).date())
		content = (headline + "|" + date + "\n").encode("ascii", "ignore")
		newFile.write(content)
	newFile.close()


def main():
	dataDirCRUD(newFileFolder)
	processData()
	dataDirCRUD(oldFileFolder,False)


if __name__ == '__main__':
	main()