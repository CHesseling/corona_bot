

#%%
import pandas as pd
from datetime import timedelta, date
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import matplotlib.image as img 
import matplotlib
import geopandas as gpd
from PIL import Image
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import io
import requests
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') 



pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)



#%%
nordlaender = ['Schleswig-Holstein', 'Hamburg', 'Niedersachsen', 'Bremen', 'Mecklenburg-Vorpommern']


#%%
dtypes = {'IdLandkreis': str}
#df = pd.read_csv('https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv', parse_dates=['Meldedatum', 'Refdatum'], dtype=dtypes)
url = ('https://storage.cloud.google.com/ndrdata-csv-cors/csv/current_cases_regions.csv')




#%%

# parameters
matplotlib.rcParams['font.family'] = "NDRSansCondBlack"

style_dachzeile = dict(size=50, color='#0c1754')#color='#222222')
style_zahl = dict(size=180, color='#0c1754')
style_diff = dict(size=80, color='#2568b4')
style_tote = dict(size=80, color='#4f4f4f')  


#%%
def textgenerator(thema, zahl, stand):
    font = ImageFont.truetype("/font/IBMPlexSans-Regular.ttf",80)
    font2 = ImageFont.truetype("/font/IBMPlexSans-Regular.ttf",40)
    font3 = ImageFont.truetype("/font/IBMPlexSans-Regular.ttf",10)
    img=Image.new("RGBA", (440,220),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.text((45, 30), thema,(0,0,0),font=font2)
    draw.text((45, 80), str(f'{zahl:n}'),(0,0,0),font=font)
    draw.text((100, 190), "Datenstand: " + str(stand),(0,0,0),font=font3)
    draw = ImageDraw.Draw(img)
    dateiname = "wort.png"
    img.save(dateiname)
    

#%%
dtypes = {'IdLandkreis': str}
df2 = pd.read_csv('https://storage.googleapis.com/public.ndrdata.de/rki_covid_19_bulk/bulk/covid_19_bereitstellung.tsv', sep='\t', parse_dates=['Datenstand'], dtype=dtypes)


df2


#%%
dtypes = {'IdLandkreis': str, 'IdBundesland': str}

df3 = pd.read_csv('https://storage.googleapis.com/public.ndrdata.de/rki_covid_19_bulk/daily/covid_19_daily_latest.tsv.gz', compression='gzip', sep="\t")
df3


#%%
df_neue_faelle = df3[(df3['NeuerFall'] != 0)]
neue_faelle_total = df_neue_faelle.AnzahlFall.sum()
datenstand = df3['Datenstand'].max()
textgenerator('Neue Infektionen', neue_faelle_total, datenstand)

#%%
# Altersverteilung der neuen Fälle

altersverteilung_neue_faelle = pd.pivot_table(df_neue_faelle, index='Altersgruppe', values='AnzahlFall', aggfunc='sum').reset_index()
sns.color_palette("autumn_r", as_cmap=True)
fig, ax = plt.subplots(figsize=(16,9))
ax = sns.barplot(x="Altersgruppe", y="AnzahlFall", data=altersverteilung_neue_faelle, palette="autumn_r")
fig = sns.despine(ax=ax, top=True, right=True, left=False, bottom=False,offset=0)
plt.savefig("altersverteilung_neue_faelle.png" , dpi=300, bbox_inches="tight" )


#%%
# Länderverteilung der neuen Fälle
bundeslaender_geojson = gpd.read_file('https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/master/2_bundeslaender/4_niedrig.geo.json')

bundeslaender_geojson = bundeslaender_geojson.reset_index()
laenderverteilung_neue_faelle = pd.pivot_table(df_neue_faelle, index='Bundesland', values='AnzahlFall', aggfunc='sum').reset_index()
laenderverteilung_neue_faelle.sort_values(by='AnzahlFall', ascending=False, inplace=True)
laenderverteilung_neue_faelle


#%%
merged = pd.merge(bundeslaender_geojson, laenderverteilung_neue_faelle, left_on='name', right_on='Bundesland')

fig, ax = plt.subplots(1, figsize=(16, 9), frameon=False, dpi=100)
merged.plot(column='AnzahlFall', cmap='autumn_r', k=3, linewidth=0.3, ax=ax, edgecolor='0.8') 
ax.axis('off')
#ax.text(0, "Neue Infketionen nach Bundesland",**style_dachzeile)

# %%
