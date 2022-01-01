import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
startTime = time.time() #start time to calculate length of program execution

pd.set_option('colheader_justify', 'center')
schema = {'Name': [],
         'Price_Per_Pound': [],
         'Cupping_Score': [],
         'Score_Per_Dollar': [],
         'Price_Per_Score': [],
         'Arrival_Date': [],
         'Processing': [],
         'Drying_Method': [],
         'Cultivar': [],
         'Region': [],
         'Grade': [],
         'Appearance': [],
         'Farm_Gate?': [],
         'URL': []}
coffeeData = pd.DataFrame(schema)

#To get a list of all the urls for the coffee's in stock###
url = 'https://www.sweetmarias.com/green-coffee.html?amp%3Bsm_status=1&product_list_limit=all&sm_status=1'
results = requests.get(url)
soup = BeautifulSoup(results.text, 'html.parser')

for url in soup.find_all('a',class_="product-item-link"):
    pages = url.get('href')
    if pages != None:
        row = {'Name': [None],
         'Price_Per_Pound': [None],
         'Cupping_Score': [None],
         'Score_Per_Dollar': [None],
         'Price_Per_Score': [None],
         'Arrival_Date': [None],
         'Processing': [None],
         'Drying_Method': [None],
         'Cultivar': [None],
         'Region': [None],
         'Grade': [None],
         'Appearance': [None],
         'Farm_Gate?': [None],
         'URL': [pages]}
        dfRow = pd.DataFrame(row)
        coffeeData = coffeeData.append(dfRow)

# Clean up Coffee Data Table 
coffeeData = coffeeData.reset_index(drop=True)

for url in coffeeData['URL']:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get Name
    name = soup.title.text
    coffeeData.loc[coffeeData['URL'] == url, ['Name']] = name

    # Get prices
    price_div = soup.find('div',class_='price-box price-final_price')
    if type(price_div) == type(None) or type(price_div.find('span', class_='price')) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Pound']] = 'N/A'
    else:
        cost = price_div.find('span', class_='price').text.strip('$')
        coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Pound']] = float(cost)

    # Get cupping score
    score_div = soup.find('div',class_='total-score')
    if type(score_div) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Cupping_Score']] = 'N/A'
    else:
        score = score_div.h5.text
        coffeeData.loc[coffeeData['URL'] == url, ['Cupping_Score']] = float(score)

    # Get arrival date
    if type(soup.find("td",{"data-th":"Arrival date"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Arrival_Date']] = 'N/A'
    else:
        Date = soup.find("td",{"data-th":"Arrival date"}).text
        ADate = Date.rstrip(' Arrival').strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Arrival_Date']] = ADate

    # Get region
    if type(soup.find("td",{"data-th":"Region"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Region']] = 'N/A'
    else:
        region = soup.find("td",{"data-th":"Region"}).text
        region = region.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Region']] = region

    # Get cultivar
    if type(soup.find("td",{"data-th":"Cultivar Detail"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Cultivar']] = 'N/A'
    else:
        cultivar = soup.find("td",{"data-th":"Cultivar Detail"}).text
        cultivar = cultivar.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Cultivar']] = cultivar

    # Get Processing
    if type(soup.find("td",{"data-th":"Processing"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Processing']] = 'N/A'
    else:
        processing = soup.find("td",{"data-th":"Processing"}).text
        processing = processing.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Processing']] = processing

    # Get Dry Method
    if type(soup.find("td",{"data-th":"Drying Method"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Drying_Method']] = 'N/A'
    else:
        drying = soup.find("td",{"data-th":"Drying Method"}).text
        drying = drying.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Drying_Method']] = drying

    # Get grade
    if type(soup.find("td",{"data-th":"Grade"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Grade']] = 'N/A'
    else:
        grade = soup.find("td",{"data-th":"Grade"}).text
        grade = grade.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Grade']] = grade

    # Get appearance
    if type(soup.find("td",{"data-th":"Appearance"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Appearance']] = 'N/A'
    else:
        appearance = soup.find("td",{"data-th":"Appearance"}).text
        appearance = appearance.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Appearance']] = appearance


    # Get Farm Gate
    if type(soup.find("td",{"data-th":"Farm Gate"})) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Farm_Gate?']] = 'No'
    else:
        farmgate = soup.find("td",{"data-th":"Farm Gate"}).text
        farmgate = farmgate.strip('\n')
        coffeeData.loc[coffeeData['URL'] == url, ['Farm_Gate?']] = farmgate

    # Get Score Per Dollar and Price Per Score
    try:
        cuppingScore = float(coffeeData.loc[coffeeData['URL'] == url, ['Cupping_Score']].values[0][0]) 
        price = float(coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Pound']].values[0][0])     

        ScorePerDollar = cuppingScore / price  # Score Per Dollar
        coffeeData.loc[coffeeData['URL'] == url, ['Score_Per_Dollar']] = ScorePerDollar
        
        PricePerScore = price / cuppingScore  # Price Per Score
        coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Score']] = PricePerScore

    except:  # Catches error if cupping score or price is missing ("N/A") 
        coffeeData.loc[coffeeData['URL'] == url, ['Score_Per_Dollar']] = 'N/A'
        coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Score']] = 'N/A'

   
## ASverage columns at bottom of table?
coffeeData.to_csv('CoffeeBuyingGuide_SweetMarias_Pandas.csv', index=False, encoding = 'UTF-8')

print("--- %s seconds ---" % (time.time() - startTime)) #Print how long program takes to execute
