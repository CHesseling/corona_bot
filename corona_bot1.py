

#%%
import pandas as pd
from datetime import timedelta, date
import numpy as np
from google.cloud import storage

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)



#%%
laender = ['Schleswig-Holstein', 'Hamburg', 'Niedersachsen', 'Bremen', 'Mecklenburg-Vorpommern']

dtypes = {'IdLandkreis': str}
df = pd.read_csv('https://storage.googleapis.com/public.ndrdata.de/rki_covid_19_bulk/bulk/covid_19_bereitstellung.tsv', sep='\t', parse_dates=['Datenstand'], dtype=dtypes)
df['infektionen_neu'] = pd.to_numeric(df['infektionen_neu'])

#%%
dtypes = {'ags': str}
df_ags = pd.read_csv('12411-01-01-5-B(1).csv', sep=";", dtype=dtypes)
df_ags['Insgesamt'] = pd.to_numeric(df_ags['Insgesamt'], errors='coerce')



# %%
df2 = pd.pivot_table(df, columns='IdLandkreis', index='Datenstand', values='infektionen_neu', aggfunc='sum' )

print ('Success')