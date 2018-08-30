import requests
from pattern import web
from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt


url = 'http://en.wikipedia.org/wiki/List_of_countries_by_past_and_future_population'
website_html = requests.get(url).text

def get_population_html_tables(html):
    
    dom = web.Element(html)

    #print(dom.by_tag('table'))
    tbls = [t for t in dom.by_tag('table') if t.attributes['class'] == ['sortable', 'wikitable']]
    
    return tbls


tables = get_population_html_tables(website_html)
print(len(tables))
print(tables)
#for t in tables:
    #print(t.attributes)

def table_type(tbl):
    headers = [th.content for th in tbl.by_tag('th')]
    return headers[1]

# group the tables by type
tables_by_type = defaultdict(list)  # defaultdicts have a default value that is inserted when a new key is accessed
for tbl in tables:
    tables_by_type[table_type(tbl)].append(tbl)

#print(tables_by_type)




def get_countries_population(tables):
     
    result = defaultdict(dict)
    
    print(tables)

    for tbl in tables:
        # extract column headers    
        # each table looks a little different, therefore extract columns that store data (i.e., table header is a year)
        tbl_headers = [ th.content for th in tbl.by_tag('th')]
        column_idx_years = [(idx, int(header)) for idx, header in enumerate(tbl_headers) if header.isnumeric()]
        column_idx, column_years = zip(*column_idx_years)
        
        # extract data from table
    
        # get table rows - but skip the ones that have no td element
        tbl_rows = [ row for row in tbl.by_tag('tr') if row.by_tag('td') ]
            
        for row in tbl_rows:
    
            countryname = (row.by_tag('td')[0].by_tag('a')[0].content)
            print(countryname)
            #countryname = (row.by_tag('td')[0].by_tag('a')[0].content).encode('ascii','ignore') 
           
            if row.by_tag('b'):
                countrydata = {column_years[i]:float(row.by_tag('b')[idx].content.replace(',', ''))/1000.0 for i,idx in enumerate(column_idx)}                
            else:
                countrydata = {column_years[i]:float(row.by_tag('td')[idx].content.replace(',', ''))/1000.0 for i,idx in enumerate(column_idx)}
            print(countrydata)


            result[countryname].update(countrydata)
    
    return result


#result = get_countries_population(tables_by_type['Country or territory'])
result=get_countries_population(tables)
print(result)

df=pd.DataFrame.from_dict(result,orient='index')
#df.sort(axis=1,inplace=True)
print(df)


