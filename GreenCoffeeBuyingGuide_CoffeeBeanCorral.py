import time
startTime = time.time() #start time to calculate length of program execution

import requests
from requests import get
from bs4 import BeautifulSoup
import math
import xlsxwriter

#initialize lists with headers that I'll store my data in. List without headers are used for iteration or math operations
name = ['Name']
score_per_dollar = ['Score Per Dollar']
price_per_score = ['Price Per Score']
harvest_date = ['Harvest Date']
country = ['Country']
region = ['Region']
cultivar = ['Cultivar']
processing = ['Processing']
drying = ['Drying Method']
organic = ['Organic?']
fair_trade = ['Fair Trade?']
rainforest_alliance  = ['Rainforest Alliance?']
decaffeinated = ['Decaffeinated?']
altitude = ['Altitude (meters)']
URLs = []
price = []
cupping_score = []
dict = {}


#To calculate number of paginations to parse through (FINAL)
url = 'https://www.coffeebeancorral.com/categories/Green-Coffee-Beans/All-Coffees.aspx?q=&o=7&p=1&i=12&d=12'
results = requests.get(url)
soup = BeautifulSoup(results.text, 'html.parser')
item_div = soup.find('div',id='products')
ps = item_div.find('p').text
items = int(ps[:3])
pageNumbers = math.ceil(items/12)


#To get a list of all the urls for the coffees### (FINAL)
for j in range(1, pageNumbers + 1):
    url = 'https://www.coffeebeancorral.com/categories/Green-Coffee-Beans/All-Coffees.aspx?q=&o=7&p='+str(j)+'&i=12&d=12'
    results = requests.get(url)
    soup = BeautifulSoup(results.text, 'html.parser')
    for i in range(1,13):
        if i < 10:
            for url in soup.find_all('a',id='ctl00_MainContentHolder_ucDevelisysFacetedSearchProductGrid_ucProductGridDisplay_rpProductGrid_ctl0'+str(i)+'_SingleProductDisplay_NameHyperLink'):
                pages = url.get('href')
                if pages != None:
                    URLs.append('https://www.coffeebeancorral.com/'+pages)
        else:
            for url in soup.find_all('a',id='ctl00_MainContentHolder_ucDevelisysFacetedSearchProductGrid_ucProductGridDisplay_rpProductGrid_ctl'+str(i)+'_SingleProductDisplay_NameHyperLink'):
                pages = url.get('href')
                if pages != None:
                    URLs.append('https://www.coffeebeancorral.com/'+pages)


#To parse through each URL of instock coffee looking for attributes below (FINAL)
for urls in URLs:
    page = requests.get(urls)
    soup = BeautifulSoup(page.text, 'html.parser')


#Get Coffee Name (FINAL)
    title = soup.find('span',id='ctl00_MainContentHolder_lblName').text
    name.append(title)


#Get prices (FINAL)
    price_span = soup.find('span',id='ctl00_MainContentHolder_VolumeDiscounts1_rptVolumeDiscounts_ctl02_lbYourPrice')
    if type(price_span) == type(None):
        price.append('Out of Stock')
    else:
        pound_price = float(price_span.text.strip('$'))
        price.append(pound_price)

#Create Dictionary of table information (FINAL)
    cup_span_labels = soup.find_all('span',class_='productpropertylabel')
    cup_span_values = soup.find_all('span',class_='productpropertyvalue')
    for i in range(0,len(cup_span_labels)):
        dict[cup_span_labels[i].text.strip(':')] = cup_span_values[i].text


#Get cupping score  (FINAL)
    try:
        cupping_value = ((int(dict['Brightness']) + int(dict['Body']) + int(dict['Aroma']) + int(dict['Complexity']) + int(dict['Balance']) + int(dict['Sweetness']))/(7*6))*100
        cupping_score.append(cupping_value)
    except KeyError:
        cupping_score.append('Missing Attribute(s)')
    except:
        cupping_score.append('Other Error')


#Get harvest date (FINAL)
    try:
        harvest_date.append(dict['Harvest'].replace('\r\n','; ').replace('     ',': ').replace('   ',': '))
    except KeyError:
        harvest_date.append('Missing Attribute')
    except:
        harvest_date.append('Other Error')
   
#Get country (FINAL)
    try:
        country.append(dict['Country'])
    except KeyError:
        country.append('Missing Attribute')
    except:
        country.append('Other Error')


#Get region (FINAL)
    try:
        region.append(dict['Region'].replace('\r\n',' '))
    except KeyError:
        region.append('Missing Attribute')
    except:
        region.append('Other Error')
  
#Get cultivar (FINAL)
    try:
        cultivar.append(dict['Variety'])
    except KeyError:
        cultivar.append('Missing Attribute')
    except:
        cultivar.append('Other Error')


#Get Processing (FINAL)
    try:
        processing.append(dict['Process'])
    except KeyError:
        processing.append('Missing Attribute')
    except:
        processing.append('Other Error')

#Get Dry Method (FINAL)
    try:
        drying.append(dict['Drying'])
    except KeyError:
        drying.append('Missing Attribute')
    except:
        drying.append('Other Error')


#Get Organic Certification (FINAL)
    try:
        organic.append(dict['Organic Certification'])
    except KeyError:
        organic.append('Missing Attribute')
    except:
        organic.append('Other Error')


#Get Fair Trade Certified (FINAL)
    try:
        fair_trade.append(dict['Fair Trade Certified'])
    except KeyError:
        fair_trade.append('Missing Attribute')
    except:
        fair_trade.append('Other Error')

#Get Rainforest Alliance Certified (FINAL)
    try:
        rainforest_alliance.append(dict['Rainforest Alliance Certified'])
    except KeyError:
        rainforest_alliance.append('Missing Attribute')
    except:
        rainforest_alliance.append('Other Error')

#Get decaffeinated information (FINAL)
    try:
        decaffeinated.append(dict['Decaffeinated'])
    except KeyError:
        decaffeinated.append('Missing Attribute')
    except:
        decaffeinated.append('Other Error')

#Get Altitude (meters) (FINAL)
    try:
        altitude.append(dict['Altitude (meters)'])
    except KeyError:
        altitude.append('Missing Attribute')
    except:
        altitude.append('Other Error')

    dict = {}


#Get Score Per Dollar
for i in range(0, len(URLs)):
    if price[i] == 'Out of Stock' or cupping_score[i] == 'Missing Attribute(s)' or cupping_score[i] == 'Other Error':
        score_per_dollar.append('N/A')
    else:
        score_per_dollar_math = cupping_score[i] / price[i]
        score_per_dollar.append(score_per_dollar_math)

#Get Price Per Score
for i in range(0, len(URLs)):
    if price[i] == 'Out of Stock' or cupping_score[i] == 'Missing Attribute(s)' or cupping_score[i] == 'Other Error':
        price_per_score.append('N/A')
    else:
        price_per_score_math = price[i] / cupping_score[i]
        price_per_score.append(price_per_score_math)



#Add headers to lists previously initialized empty
URLs.insert(0,'URL')
price.insert(0,'Price Per Pound')
cupping_score.insert(0,'Cupping Score')


name.append('') #create blank space between table and numeric calculations
name.append('Average (mean)') #create row of averages for average values

#Calculate Average Price
price_accum = 0
price_count = 0

for value in price:
    if type(value) != type(str()):
        price_accum += value
        price_count += 1

average_price = (price_accum/price_count)
price.append('') # create blank space between table and numeric calculations
price.append(average_price)

#Calculate Average Cupping Score
cupping_score_accum = 0
cupping_score_count = 0

for score in cupping_score:
    if type(score) != type(str()):
        cupping_score_accum += score
        cupping_score_count += 1

average_cupping_score = (cupping_score_accum/cupping_score_count)
cupping_score.append('') # create blank space between table and numeric calculations
cupping_score.append(average_cupping_score)

#Calculate Average ScorePerDollar
score_per_dollar_accum = 0
score_per_dollar_count = 0

for score2 in score_per_dollar:
    if type(score2) != type(str()):
        score_per_dollar_accum += score2
        score_per_dollar_count += 1

average_score_per_dollar = (score_per_dollar_accum/score_per_dollar_count)
score_per_dollar.append('') # create blank space between table and numeric calculations
score_per_dollar.append(average_score_per_dollar)

#Calculate Average ScorePerDollar
price_per_score_accum = 0
price_per_score_count = 0

for score3 in price_per_score:
    if type(score3) != type(str()):
        price_per_score_accum += score3
        price_per_score_count += 1

average_price_per_score = (price_per_score_accum/price_per_score_count)
price_per_score.append('') # create blank space between table and numeric calculations
price_per_score.append(average_price_per_score)

###Write data into Excel file###
workbook = xlsxwriter.Workbook('CoffeeBuyingGuide_CoffeeBeanCorral.xlsx')
worksheet = workbook.add_worksheet()

#Fill Column A with Coffee Names
for row_num, data in enumerate(name):
    worksheet.write(row_num, 0, data)

#Fill Column B with Coffee Price
for row_num, data in enumerate(price):
    worksheet.write(row_num, 1, data)

#Fill Column C with Coffee Cupping Score
for row_num, data in enumerate(cupping_score):
    worksheet.write(row_num, 2, data)

#Fill Column D with Coffee Score Per Dollar
for row_num, data in enumerate(score_per_dollar):
    worksheet.write(row_num, 3, data)

#Fill Column E with Coffee Price Per Score
for row_num, data in enumerate(price_per_score):
    worksheet.write(row_num, 4, data)

#Fill Column F with Coffee Harvest Date
for row_num, data in enumerate(harvest_date):
    worksheet.write(row_num, 5, data)

#Fill Column G with Altitude
for row_num, data in enumerate(altitude):
    worksheet.write(row_num, 6, data)
    
#Fill Column H with Coffee Processing
for row_num, data in enumerate(processing):
    worksheet.write(row_num, 7, data)

#Fill Column I with Coffee Drying Method
for row_num, data in enumerate(drying):
    worksheet.write(row_num, 8, data)

#Fill Column J with Coffee Cultivar
for row_num, data in enumerate(cultivar):
    worksheet.write(row_num, 9, data)

#Fill Column K with Coffee Country
for row_num, data in enumerate(country):
    worksheet.write(row_num, 10, data)

#Fill Column L with Coffee Region
for row_num, data in enumerate(region):
    worksheet.write(row_num, 11, data)

#Fill Column M with Decaffeinated Status
for row_num, data in enumerate(decaffeinated):
    worksheet.write(row_num, 12, data)

#Fill Column N with Fair Trade Status
for row_num, data in enumerate(fair_trade):
    worksheet.write(row_num, 13, data)

#Fill Column O with Organic Status
for row_num, data in enumerate(organic):
    worksheet.write(row_num, 14, data)

#Fill Column P with Rainforest Alliance Status
for row_num, data in enumerate(rainforest_alliance):
    worksheet.write(row_num, 15, data)

#Fill Column Q with Purchasing URL
for row_num, data in enumerate(URLs):
    worksheet.write(row_num, 16, data)

workbook.close()

print("--- %s seconds ---" % (time.time() - startTime)) #Print how long program takes to execute
