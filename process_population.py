import json
import pandas as pd
import requests
import primefac

headers = {'content-type': 'applicaiton/json'}
url = "https://datausa.io/api/data?drilldowns=State&measures=Population"

r = requests.get(url, headers=headers)
data = json.loads(r.text)

df = pd.DataFrame.from_dict(data.get('data'))

sy_df = df.groupby(['State', 'Year'], as_index=False).sum()
first_year = int(sy_df['Year'].min())
last_year = int(sy_df['Year'].max())

years = []
for year in range(first_year, last_year +1):
    years.append(str(year))

str_years = ""
for year in years:
    str_years = str_years + "'" + year + "', "
str_years = str_years[:-2]

cols = 'State\', ' + str_years + ', \''  + str(years[-1]) + ' Factors '
out_df = pd.DataFrame(columns=[cols])

def calc_change(yr1, yr2):
    diff = yr2-yr1
    if diff < 0:
        sign = '-'
    else:
        sign = ''
    new_str = str(yr2) + ' (' + sign + str(round(abs(diff)/yr1*100,2)) + '%)'
    return new_str

ser = {}
curr_state = None
for index, row in sy_df.iterrows():
    if row['State'] != curr_state:
        curr_state = row['State']
        if ser.get('2013') is not None:
            pop_2013 = ser.get('2013')
            pop_2014 = ser.get('2014')
            new_pop_2014 = calc_change(pop_2013, pop_2014)
            pop_2015 = ser.get('2015')
            new_pop_2015 = calc_change(pop_2014, pop_2015)
            pop_2016 = ser.get('2016')
            new_pop_2016 = calc_change(pop_2015, pop_2016)
            pop_2017 = ser.get('2017')
            new_pop_2017 = calc_change(pop_2016, pop_2017)
            pop_2018 = ser.get('2018')
            new_pop_2018 = calc_change(pop_2017, pop_2018)
            pop_2019 = ser.get('2019')
            new_pop_2019 = calc_change(pop_2018, pop_2019)
            factors = list( primefac.primefac(pop_2019) )
            ser.update({'2014': new_pop_2014, '2015': new_pop_2015, '2016': new_pop_2016, '2017': new_pop_2017, '2018': new_pop_2018, '2019': new_pop_2019, '2019 Factors': ';'.join(map(str, factors))})
            out_df.append(ser, ignore_index=True)
            print(ser)
            ser = {}
    ser.update({'State': row['State'], str(row['Year']): row['Population']})
pop_2013 = ser.get('2013')
pop_2014 = ser.get('2014')
new_pop_2014 = calc_change(pop_2013, pop_2014)
pop_2015 = ser.get('2015')
new_pop_2015 = calc_change(pop_2014, pop_2015)
pop_2016 = ser.get('2016')
new_pop_2016 = calc_change(pop_2015, pop_2016)
pop_2017 = ser.get('2017')
new_pop_2017 = calc_change(pop_2016, pop_2017)
pop_2018 = ser.get('2018')
new_pop_2018 = calc_change(pop_2017, pop_2018)
pop_2019 = ser.get('2019')
new_pop_2019 = calc_change(pop_2018, pop_2019)
factors = list( primefac.primefac(pop_2019) )
ser.update({'2014': new_pop_2014, '2015': new_pop_2015, '2016': new_pop_2016, '2017': new_pop_2017, '2018': new_pop_2018, '2019': new_pop_2019, '2019 Factors': ';'.join(map(str, factors))})
out_df.append(ser, ignore_index=True)
print(ser)
