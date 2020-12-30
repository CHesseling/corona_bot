

#%%
import pandas as pd
import datetime 
import requests
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') 



pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

#%%
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%Y %H:%M:%S")
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    pro_string = f'\r{prefix} |{bar}| {percent}% {suffix} {current_time}'
    return pro_string

#%%

df = pd.read_excel('https://storage.googleapis.com/ndrdata-impfungen/rki_data/rki_impfquotenmonitoring_latest.xlsx', sheet_name=1)


#%%
impfungen = df[(df['Bundesland'] == 'Gesamt')].iloc[0,1]

bev = 83166711

impfquote = impfungen / bev * 100
#%%
string = printProgressBar(impfquote, 100, prefix = 'Impffortschritt Deutschland:', suffix = 'komplett (Erstimpfung)', length = 40)

print (string)

#%%
