import time
startTime = time.time() #start time to calculate length of program execution

import requests
from requests import get
from bs4 import BeautifulSoup
import xlsxwriter


#initialize lists with headers that I'll store my data in. List without headers are used for iteration or math operations
Name = ['Name']
ScorePerDollar = ['Score Per Dollar']
PricePerScore = ['Price Per Score']
ArrivalDate = ['Arrival Date']
Region = ['Region']
Cultivar = ['Cultivar']
Processing = ['Processing']
DryingMethod = ['Drying Method']
Grade = ['Grade']
Appearance = ['Appearance']
FarmGate = ['Farm Gate?']
URLs = []
Price = []
CuppingScore = []

#To get a list of all the urls for the coffee's in stock###
url = 'https://www.sweetmarias.com/green-coffee.html?amp%3Bsm_status=1&product_list_limit=all&sm_status=1'
results = requests.get(url)
soup = BeautifulSoup(results.text, 'html.parser')
for url in soup.find_all('a',class_="product-item-link"):
    pages = url.get('href')
    if pages != None:
        URLs.append(pages)
for urls in URLs:
    page = requests.get(urls)
    soup = BeautifulSoup(page.text, 'html.parser')

#Get titles
    title = soup.title.text
    Name.append(title)

#Get prices
    price_div = soup.find('div',class_='price-box price-final_price')
    if type(price_div) == type(BeautifulSoup(requests.get(URLs[0]).text,'html.parser').find('div',class_='price-box price-final_price')):
        if type(price_div.find('span', class_='price')) == type(None):
            Price.append('N/A')
        else:
            cost = price_div.find('span', class_='price').text.strip('$')
            Price.append(float(cost))
    else:
        Price.append('N/A')

#Get cupping score
    score_div = soup.find('div',class_='total-score')
    if type(score_div) == type(None):
        CuppingScore.append('N/A')
    else:
        score = score_div.h5.text
        CuppingScore.append(float(score))

#Get arrival date
    if type(soup.find("td",{"data-th":"Arrival date"})) == type(None):
        ArrivalDate.append('N/A')
    else:
        Date = soup.find("td",{"data-th":"Arrival date"}).text
        ADate = Date.rstrip(' Arrival').strip('\n')
        ArrivalDate.append(ADate)

#Get region
    if type(soup.find("td",{"data-th":"Region"})) == type(None):
        Region.append('N/A')
    else:
        region = soup.find("td",{"data-th":"Region"}).text
        region = region.strip('\n')
        Region.append(region)

#Get cultivar
    if type(soup.find("td",{"data-th":"Cultivar Detail"})) == type(None):
        Cultivar.append('N/A')
    else:
        cultivar = soup.find("td",{"data-th":"Cultivar Detail"}).text
        cultivar = cultivar.strip('\n')
        Cultivar.append(cultivar)

#Get Processing
    if type(soup.find("td",{"data-th":"Processing"})) == type(None):
        Processing.append('N/A')
    else:
        processing = soup.find("td",{"data-th":"Processing"}).text
        processing = processing.strip('\n')
        Processing.append(processing)

#Get Dry Method
    if type(soup.find("td",{"data-th":"Drying Method"})) == type(None):
        DryingMethod.append('N/A')
    else:
        drying = soup.find("td",{"data-th":"Drying Method"}).text
        drying = drying.strip('\n')
        DryingMethod.append(drying)

#Get grade
    if type(soup.find("td",{"data-th":"Grade"})) == type(None):
        Grade.append('N/A')
    else:
        grade = soup.find("td",{"data-th":"Grade"}).text
        grade = grade.strip('\n')
        Grade.append(grade)

#Get appearance
    if type(soup.find("td",{"data-th":"Appearance"})) == type(None):
        Appearance.append('N/A')
    else:
        appearance = soup.find("td",{"data-th":"Appearance"}).text
        appearance = appearance.strip('\n')
        Appearance.append(appearance)


#Get Farm Gate
    if type(soup.find("td",{"data-th":"Farm Gate"})) == type(None):
        FarmGate.append('No')
    else:
        farmgate = soup.find("td",{"data-th":"Farm Gate"}).text
        farmgate = farmgate.strip('\n')
        FarmGate.append(farmgate)

#Get Score Per Dollar
for i in range(0, len(URLs)):
    if Price[i] == 'N/A' or CuppingScore[i] == 'N/A':
        ScorePerDollar.append('N/A')
    else:
        ScorePerDollarMath = CuppingScore[i] / Price[i]
        ScorePerDollar.append(ScorePerDollarMath)

#Get Price Per Score
for i in range(0, len(URLs)):
    if Price[i] == 'N/A' or CuppingScore[i] == 'N/A':
        PricePerScore.append('N/A')
    else:
        PricePerScoreMath = Price[i] / CuppingScore[i]
        PricePerScore.append(PricePerScoreMath)

#Add headers to lists previously initialized empty
URLs.insert(0,'URL')
Price.insert(0,'Price Per Pound')
CuppingScore.insert(0,'Cupping Score')

Name.append('') #create blank space between table and numeric calculations
Name.append('Average (mean)') #create row of averages for average values

#Calculate Average Price
PriceAccum = 0
PriceCount = 0

for price in Price:
    if type(price) != type(str()):
        PriceAccum += price
        PriceCount += 1

AveragePrice = (PriceAccum/PriceCount)
Price.append('') # create blank space between table and numeric calculations
Price.append(AveragePrice)

#Calculate Average Cupping Score
CuppingScoreAccum = 0
CuppingScoreCount = 0

for score in CuppingScore:
    if type(score) != type(str()):
        CuppingScoreAccum += score
        CuppingScoreCount += 1

AverageCuppingScore = (CuppingScoreAccum/CuppingScoreCount)
CuppingScore.append('') # create blank space between table and numeric calculations
CuppingScore.append(AverageCuppingScore)

#Calculate Average ScorePerDollar
ScorePerDollarAccum = 0
ScorePerDollarCount = 0

for score2 in ScorePerDollar:
    if type(score2) != type(str()):
        ScorePerDollarAccum += score2
        ScorePerDollarCount += 1

AverageScorePerDollar = (ScorePerDollarAccum/ScorePerDollarCount)
ScorePerDollar.append('') # create blank space between table and numeric calculations
ScorePerDollar.append(AverageScorePerDollar)

#Calculate Average ScorePerDollar
PricePerScoreAccum = 0
PricePerScoreCount = 0

for score3 in PricePerScore:
    if type(score3) != type(str()):
        PricePerScoreAccum += score3
        PricePerScoreCount += 1

AveragePricePerScore = (PricePerScoreAccum/PricePerScoreCount)
PricePerScore.append('') # create blank space between table and numeric calculations
PricePerScore.append(AveragePricePerScore)

###Write data into Excel file###
workbook = xlsxwriter.Workbook('CoffeeBuyingGuide_SweetMarias.xlsx')
worksheet = workbook.add_worksheet()

#Fill Column A with Coffee Names
for row_num, data in enumerate(Name):
    worksheet.write(row_num, 0, data)

#Fill Column B with Coffee Price
for row_num, data in enumerate(Price):
    worksheet.write(row_num, 1, data)

#Fill Column C with Coffee Cupping Score
for row_num, data in enumerate(CuppingScore):
    worksheet.write(row_num, 2, data)

#Fill Column D with Coffee Score Per Dollar
for row_num, data in enumerate(ScorePerDollar):
    worksheet.write(row_num, 3, data)

#Fill Column E with Coffee Price Per Score
for row_num, data in enumerate(PricePerScore):
    worksheet.write(row_num, 4, data)

#Fill Column F with Coffee Arrival Date
for row_num, data in enumerate(ArrivalDate):
    worksheet.write(row_num, 5, data)

#Fill Column G with Coffee Processing
for row_num, data in enumerate(Processing):
    worksheet.write(row_num, 6, data)

#Fill Column H with Coffee Drying Method
for row_num, data in enumerate(DryingMethod):
    worksheet.write(row_num, 7, data)

#Fill Column I with Coffee Cultivar
for row_num, data in enumerate(Cultivar):
    worksheet.write(row_num, 8, data)

#Fill Column J with Coffee Region
for row_num, data in enumerate(Region):
    worksheet.write(row_num, 9, data)

#Fill Column K with Coffee Grade
for row_num, data in enumerate(Grade):
    worksheet.write(row_num, 10, data)

#Fill Column L with Coffee Appearance
for row_num, data in enumerate(Appearance):
    worksheet.write(row_num, 11, data)

#Fill Column M with Farm Gate Status
for row_num, data in enumerate(FarmGate):
    worksheet.write(row_num, 12, data)

#Fill Column N with Purchasing URL
for row_num, data in enumerate(URLs):
    worksheet.write(row_num, 13, data)

workbook.close()

print("--- %s seconds ---" % (time.time() - startTime)) #Print how long program takes to execute
