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
         'Altitude': [],
         'Processing_Method': [],
         'Country': [],
         'Region': [],
         'Varietals': [],
         'Inventory (Lbs)': [],
         'Cupping_Notes': [],
         'URL': []}
coffeeData = pd.DataFrame(schema)

#To get a list of all the urls for the coffee's in stock###
url = 'https://u-roast-em.com/ure-products/green-coffee-beans/'
results = requests.get(url)
soup = BeautifulSoup(results.text, 'html.parser')
for offering in soup.find_all('div',class_='banner'):
    bannerTitle = offering.find('h2').text
    if bannerTitle.upper() == 'ALL OFFERINGS':  # True for section of everything currently in stock
        allOfferings_div = offering.next_sibling
        for url in allOfferings_div.find_all('a',class_="product-link"):
            pages = url.get('href')
            if pages != None:
                row = {'Name': [None],
                       'Price_Per_Pound': [None],
                       'Cupping_Score': [None],
                       'Score_Per_Dollar': [None],
                       'Price_Per_Score': [None],
                       'Altitude': [None],
                       'Processing_Method': [None],
                       'Country': [None],
                       'Region': [None],
                       'Varietals': [None],
                       'Inventory (Lbs)': [None],
                       'Cupping_Notes': [None],
                       'URL': [pages]}
                dfRow = pd.DataFrame(row)
                coffeeData = coffeeData.append(dfRow)


# Clean up Coffee Data Table 
coffeeData = coffeeData.reset_index(drop=True)

# Optain List of column headers in all caps
columnNames = []
columnHeaders = coffeeData.columns.tolist()
for col in columnHeaders:
    columnNames.append(col.upper())

for url in coffeeData['URL']:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get coffee names
    name_div = soup.find('div',class_='info-card')
    name = name_div.find('h1').text
    coffeeData.loc[coffeeData['URL'] == url, ['Name']] = name

    # Get prices
    price_div = soup.find('div',class_='cart-add-units')
    if type(price_div) == type(None) or type(price_div.find_all('label', class_='uroastem-radio')) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Pound']] = 'N/A'
    else:
        costLst = price_div.find_all('label', class_='uroastem-radio')  # Finds price for each unit offered
        for unit in costLst:  # Iterate through each unit
            price = unit.text.upper()
            if '1 LB' in price or '1LB' in price:  # True if price is for 1 pound
                costLB = price.split("-")[1]  # Obtain string of price per pound
                costLB = costLB.strip().strip('$')
                coffeeData.loc[coffeeData['URL'] == url, ['Price_Per_Pound']] = float(costLB)

    # Get inventory
    stock = soup.find('span', class_='inventory')
    if type(stock) == type(None) or type(stock.text) == type(None):
        coffeeData.loc[coffeeData['URL'] == url, ['Inventory (Lbs)']] = 'N/A'
    else:
        lbsRemaining = stock.text.split()[2]  # Number of pounds of inventory remaining
        coffeeData.loc[coffeeData['URL'] == url, ['Inventory (Lbs)']] = float(lbsRemaining)

    # Get product info item
    for item in soup.find_all('div', class_='info-item'):
        col = item.find('label').text
        val = item.find('label').next_sibling
        if col.upper() in columnNames:
            coffeeData.loc[coffeeData['URL'] == url, [col.title()]] = val
        elif col.upper() == 'Cupping Score'.upper():
            try:
                cuppingScore = float(val)
                coffeeData.loc[coffeeData['URL'] == url, ['Cupping_Score']] = cuppingScore
            except:
                coffeeData.loc[coffeeData['URL'] == url, ['Cupping_Score']] = 'N/A'
        elif col.upper() == 'Processing Method'.upper():
            coffeeData.loc[coffeeData['URL'] == url, ['Processing_Method']] = val
        elif col.upper() == 'Cupping Notes'.upper() or col.upper() == 'Cupping Notes:'.upper():
            coffeeData.loc[coffeeData['URL'] == url, ['Cupping_Notes']] = val
        elif col.upper() == 'Countries'.upper():
            coffeeData.loc[coffeeData['URL'] == url, ['Country']] = val
        else:
            pass

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

coffeeData.to_csv('CoffeeBuyingGuide_U-Roast-Em_Pandas.csv', index=False, encoding = 'UTF-8')

print("--- %s seconds ---" % (time.time() - startTime)) #Print how long program takes to execute
