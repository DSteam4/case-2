#!/usr/bin/env python
# coding: utf-8

# # Case 2: Blogpost

project_title = 'Blogpost_ziekteverzuim'

# Namen: Vincent Kemme (500838439), Rhodé Rebel (500819128), Amber van der Pol (500803136) en Oussama Abou <font color = 'red'>(...)

# # 1 System setup

# **Credits:**  
# https://www.cbs.nl/nl-nl/onze-diensten/open-data/open-data-v4/snelstartgids-odata-v4

# **Working directory setup**
# * **/Data/** for all data related maps
# * **/Data/raw/** for all raw incoming data
# * **/Data/clean/** for all clean data to be used during analysis
# * **/Data/staging/** for all data save during cleaning 
# * **/Data/temp/** for all tempral data saving 
# * **/Figs/temp/** for all tempral data saving 
# * **/Docs/** reference documentation
# * **/Results/** reference documentation
# * **/Code/** reference documentation
# 
# 
# **References:**
# https://docs.python-guide.org/writing/structure/

# Import packages

# In[2]:


import pandas as pd
import os
import requests
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Verberg waarschuwingen om verwarring te voorkomen
import warnings
warnings.filterwarnings('ignore')

import session_info
session_info.show()

st.title("Ziekteverzuim en fysieke arbeidsbelasting")
st.header("Inleiding")
st.markdown('''Waar werk is, is ziekteverzuim. In het midden van de coronapandemie waarin thuiswerken de norm is geworden en we te maken hebben met verspreiden van ziektes op de werkvloer speelt ziekteverzuim een belangrijke rol bij zowel alle beroepssegmenten. De blogpost *Ziekteverzuim en fysieke arbeidsbelasting* brengt het verband tussen ziekteverzuim en beroep aan het licht met betrekking tot factoren als herhaalde bewegingen tijdens het werk, stoffen op huid, het inademen van stoffen, et cetera. De data die is gebruikt om de informatie grafisch in beeld te brengen is door het CBS verstrekt.''')
# Set working directories

# In[3]:


print("Current working directory: {0}".format(os.getcwd()))


# Create project structure

# In[4]:


arr_map_structure  = [os.getcwd() + map for map in   ['/Data','/Data/raw','/Data/clean','/Data/staging',
                      '/Data/temp','/Figs','/Figs/temp','/Docs','/Results','/Code'] ]

#[os.makedirs(map) for map in arr_map_structure if  not os.path.exists( map)]


# # 2 Import data
def main():
    menu = ["Inleiding", "Analyse van de data", "Visualisatie van de data"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Inleiding':
        st.subheader('Inleiding')
    elif choice == 'Analyse van de data':
        st.subheader('Analyse van de data')
    else:
        st.subheader('Visualisatie van de data')
if __name__== '__main__':
  main()
        
st.header("Analyse van de data")
st.markdown('''Om te onderzoeken hoe de ziekteverzuim verdeeld is per beroepsklasse is er gebruikt gemaakt van de data van het CBS. Er is gebruik gemaakt van de volgende twee datasets: *ziekteverzuim volgens werknemers; beroep* en *fysieke arbeidsbelasting werknemers; beroep*. Dit zijn twee openbare API’s die we hebben opgevraagd:  

Ziekteverzuim volgens werknemers; beroep - https://opendata.cbs.nl/ODataApi/odata/84437NED/TypedDataSet  
Fysieke arbeidsbelasting werknemers; beroep - https://opendata.cbs.nl/ODataApi/odata/84435NED/TypedDataSet  

We hebben onderstaande functie gedefinieerd om de API’s mee op te vragen.''')
code1 = '''def get_odata(target_url):
    data = pd.DataFrame()
    while target_url:
        r = requests.get(target_url).json()
        data = data.append(pd.DataFrame(r['value']))
        
        if '@odata.nextLink' in r:
            target_url = r['@odata.nextLink']
        else:
            target_url = None
            
    return data'''
st.code(code1, language = 'python')

st.markdown('Vervolgens hebben we de twee dataset gemergd op de variabelen *Beroep* en *Perioden*, met onderstaande code.''')
code2 = '''df_merged = ziekteverzuim.merge(fysiekearbeidsbelasting,
                                how = 'outer',
                                on = ['Beroep', 'Perioden'],
                                validate = 'one_to_one')'''
st.code(code2, language = 'python')
            
st.subheader('Kwaliteit van de dataset')
st.markdown('''De dataset ziekteverzuim bevat data van het jaar 2014 tot het jaar 2021. De dataset is ontstaan uit een enquête. Deze dataset is gecombineerd met de dataset fysieke arbeidsbelasting werknemers. Dit is gedaan op de variabelen beroep en perioden. De dataset fysieke arbeidsbelasting komt net als de andere dataset uit 2014 tot 2020. Er is middels een enquête informatie gewonnen. ''')
st.subheader('Variabelen uit de dataset')
st.markdown('''De belangrijke variabelen in deze datasets zijn Beroep, Perioden en Ziekteverzuimpercentage. De variabele beroep zijn ingedeeld in beroepsklasse. Die klasse zijn weer in gedeeld in beroepssegment en dat per beroep. De perioden zijn ingedeeld in jaren.  Het ziekteverzuimpercentage is het aantal ziektedagen die een werknemer heeft opgenomen in procenten van het totaal aantal beschikbare werkdagen. ''')

# Functie get_odata wordt gedefinieerd.  
# Credits: https://www.cbs.nl/nl-nl/onze-diensten/open-data/open-data-v4/snelstartgids-odata-v4

# In[5]:


def get_odata(target_url):
    data = pd.DataFrame()
    while target_url:
        r = requests.get(target_url).json()
        data = data.append(pd.DataFrame(r['value']))
        
        if '@odata.nextLink' in r:
            target_url = r['@odata.nextLink']
        else:
            target_url = None
            
    return data
  



# ### 2.1 Ziekteverzuim volgens werknemers; beroep

# In[6]:


ziekteverzuim_url = "https://opendata.cbs.nl/ODataApi/odata/84437NED"

ziekteverzuim_api = get_odata(ziekteverzuim_url)
print(ziekteverzuim_api)


# Geef een beschrijving van de variabelen

# In[7]:


DataProperties_zv_url = ziekteverzuim_api.iloc[3, 1]

DataProperties_zv = get_odata(DataProperties_zv_url)[['Key', 'Description', 'Unit']]
print(DataProperties_zv)


# Laad de UntypedDataSet in

# In[8]:


zv_uds_url = ziekteverzuim_api.iloc[1, 1]

zv_uds = get_odata(zv_uds_url)
print(zv_uds)


# In[9]:


#print(zv_uds.info())


# Laad de TypedDataSet in

# In[10]:


zv_tds_url = ziekteverzuim_api.iloc[2, 1]

zv_tds = get_odata(zv_tds_url)
print(zv_tds.head())


# In[11]:


print(zv_tds.info())


# We zien dat de TypedDataSet alle 'objects' behalve die van de kolommen 'Beroep' en 'Perioden' heeft omgezet naar 'floats'. We kiezen daarom om gebruik te maken van de TypedDataSet.

# In[12]:


ziekteverzuim = zv_tds
ziekteverzuim.to_csv(arr_map_structure[1]+'_ziekteverzuim.csv', index=False) # Dataframe als csv opslaan als 'raw_ziekteverzuim'


# ### 2.1 Fysieke arbeidsbelasting werknemers; beroep

# In[13]:


fysiekearbeidsbelasting_url = "https://opendata.cbs.nl/ODataApi/odata/84435NED"

fysiekearbeidsbelasting_api = get_odata(fysiekearbeidsbelasting_url)
print(fysiekearbeidsbelasting_api)


# Geef een beschrijving van de variabelen

# In[14]:


DataProperties_fa_url = fysiekearbeidsbelasting_api.iloc[3, 1]

DataProperties_fa = get_odata(DataProperties_fa_url)[['Key', 'Description', 'Unit']]
print(DataProperties_fa)


# Laad de TypedDataSet in

# In[15]:


fysiekearbeidsbelasting_url = fysiekearbeidsbelasting_api.iloc[2, 1]

fysiekearbeidsbelasting = get_odata(fysiekearbeidsbelasting_url)
print(fysiekearbeidsbelasting.head())


# In[16]:


print(fysiekearbeidsbelasting.info())


# In[17]:


# Dataframe als csv opslaan als 'raw_fysiekearbeidsbelasting'
fysiekearbeidsbelasting.to_csv(arr_map_structure[1]+'_fysiekearbeidsbelasting.csv', index=False)


# # 3 Exploratory Data Analysis

# ## 3.1 Inspectie van de variabelen

# ## 3.2 EDA per dataframe

# Kijken naar shape, veldnamen en datatypes.

# In[18]:


print("shape ziekteverzuim: " + str(ziekteverzuim.shape))
print("shape fysiekearbeidsbelasting: " + str(fysiekearbeidsbelasting.shape))


# In[19]:


print(ziekteverzuim.info())


# In[20]:


print(fysiekearbeidsbelasting.info())


# Beide datasets hebben de variabelen 'ID', 'Beroep' en 'Perioden'. We kunnen de datasets eventueel joinen op 'Beroep' en 'Perioden'.

# ### 3.2.1 Datasets samenvoegen

# In[21]:


df_merged = ziekteverzuim.merge(fysiekearbeidsbelasting,
                                how = 'outer',
                                on = ['Beroep', 'Perioden'],
                                validate = 'one_to_one')
print(df_merged.columns)



# ### 3.2.1 Kolommen splitsen / verwijderen / hernoemen

# Vervang de waarden van de kolom 'Beroep' met de namen van de beroepen.

# In[22]:


beroep_url = ziekteverzuim_api.iloc[5, 1]
r = requests.get(beroep_url)
beroep = r.json()
beroep = beroep.get('value')
beroep = pd.DataFrame.from_dict(beroep)
beroep = beroep[['Key', 'Title']]
print(beroep.head())


# In[23]:


df_beroep = df_merged.merge(beroep, left_on = 'Beroep', right_on = 'Key', validate = 'many_to_one')
title_beroep = df_beroep['Title']
df_beroep.drop(labels=['Beroep', 'Key', 'Title'], axis = 1, inplace = True)
df_beroep.insert(1, 'Beroep', title_beroep)
print(df_beroep.head())


# Vervang de waarden van de kolom 'Perioden' met jaartallen.

# In[24]:


perioden_url = ziekteverzuim_api.iloc[6, 1]
r = requests.get(perioden_url)
perioden = r.json()
perioden = perioden.get('value')
perioden = pd.DataFrame.from_dict(perioden)
perioden = perioden[['Key', 'Title']]
perioden.head()


# In[25]:


df_beroep_perioden = df_beroep.merge(perioden, left_on = 'Perioden', right_on = 'Key', validate = 'many_to_one')
title_perioden = df_beroep_perioden['Title']
df_beroep_perioden.drop(labels=['Perioden', 'Key', 'Title'], axis = 1, inplace = True)
df_beroep_perioden.insert(2, 'Perioden', title_perioden)
df_beroep_perioden.sort_values(by = ['ID_x'], inplace = True)
df_beroep_perioden.head()


# Verwijder de ID kolommen

# In[26]:


df_beroep_perioden.drop(labels = ['ID_x', 'ID_y'], axis = 1, inplace = True)


#  Waarden in de kolom 'Beroep' omzetten naar string

# In[27]:


df_beroep_perioden['Beroep'] = df_beroep_perioden['Beroep'].astype('string')


# Waarden in de kolom 'Perioden' omzetten naar integer

# In[28]:


df_beroep_perioden['Perioden'] = df_beroep_perioden['Perioden'].astype('int')


# In[29]:


df = df_beroep_perioden.reset_index(drop=True)
df.head()


# ### 3.2.2 Duplicates checken

# In[30]:


duplicate = df[["Beroep", "Perioden"]].duplicated() # checken voor duplicates (met dezelfde combinatie beroep en jaar)
true_count = sum(duplicate) # True values tellen
print(true_count)


# Er zijn geen duplicates in deze dataset.

# ### 3.2.3 Generieke verkenning

# **Missende waarden**

# In[31]:


print(df.isnull().sum()) # Missende waarden checken


# Er zijn aardig wat missende waarden te zien

st.subheader('Data manipuleren om nieuwe variabelen te krijgen')
st.markdown('''De kolom *Beroep* bevat nu 5 verschillende soorten groepen.  

Allereerst hebben we *Totaal* en *Beroepsniveau*.  
Verder wordt *Beroep* (aangeduid met een 4-digit cijfer) onderverdeeld in *Beroepssegment* (aangeduid met een 3-digit cijfer) en wordt dat weer onderverdeeld in *Beroepsklasse* (aangeduid met een 2-digit cijfer).  

Ter verduidelijking:  
01 Beroepsklasse  
011 Beroepssegment  
0111 Beroep  

We willen uiteindelijk een dataset waarin de kolom *Beroep* alleen de beroepen (4-digits) bevat en de beroepssegmenten en -klassen in een eigen kolom staan.''')

# **Dataset opsplitsen**

# De kolom 'Beroep' bevat een soort levelsysteem.  
# Allereerst:
# - Per jaar wordt het totaal gegeven van alle beroepen
# - Per jaar wordt het totaal gegeven per beroepsniveau
#  
# Verder worden beroepen (aangeduid met een 4-digit cijfer) onderverdeeld in beroepssegment (aangeduid met een 3-digit cijfer). Beroepssegment wordt weer opgedeeld in beroepsklasse (aangeduid met een 2-digit cijfer).
# 
# We splitsen de data dus op in 5 datasets:
# - Totaal
# - Beroepsniveau
# - Beroepsklasse
# - Beroepssegment
# - Beroep

# In[32]:

st.markdown('**Stap 1**: Splits de dataset op in 5 datasets (totaal, beroepsniveau, beroepsklasse, beroepssegment, beroep)')

# Index getallen per 'level' in een lijst zetten
id_totaal = list(map(int, df.index[df['Beroep'].str.contains('Totaal')]))
id_beroepsniveau = list(map(int, df.index[df['Beroep'].str.contains('Beroepsniveau')]))
id_beroepsklasse = list(map(int, df.index[df['Beroep'].str.contains('^\d{2}\s')]))
id_beroepssegment = list(map(int, df.index[df['Beroep'].str.contains('^\d{3}\s')]))
id_beroep = list(map(int, df.index[df['Beroep'].str.contains('^\d{4}\s')]))

# Dataframes aanmaken per 'level'
df_totaal = df.iloc[id_totaal]
df_beroepsniveau = df.iloc[id_beroepsniveau]
df_beroepsklasse = df.iloc[id_beroepsklasse]
df_beroepssegment = df.iloc[id_beroepssegment]
df_beroep = df.iloc[id_beroep]

code3 = '''# Index getallen per 'level' in een lijst zetten
id_totaal = list(map(int, df.index[df['Beroep'].str.contains('Totaal')]))
id_beroepsniveau = list(map(int, df.index[df['Beroep'].str.contains('Beroepsniveau')]))
id_beroepsklasse = list(map(int, df.index[df['Beroep'].str.contains('^\d{2}\s')]))
id_beroepssegment = list(map(int, df.index[df['Beroep'].str.contains('^\d{3}\s')]))
id_beroep = list(map(int, df.index[df['Beroep'].str.contains('^\d{4}\s')]))

# Dataframes aanmaken per 'level'
df_totaal = df.iloc[id_totaal]
df_beroepsniveau = df.iloc[id_beroepsniveau]
df_beroepsklasse = df.iloc[id_beroepsklasse]
df_beroepssegment = df.iloc[id_beroepssegment]
df_beroep = df.iloc[id_beroep]'''
st.code(code3, language = 'python')

# Ook maken we een dataset aan waarin zowel 'Beroep', 'Beroepssegment' als 'Beroepsklasse' een variabele is.

# In[33]:
st.markdown('**Stap 2**: Verkrijg de cijfers van de beroepen, beroepssegmenten en beroepsklassen en stop deze in nieuwe kolommen (zodat we kunnen daarop kunnen mergen)')

# Verkrijg de eerste twee en eerste 3 cijfers uit de kolom 'Beroep' en stop deze in nieuwe kolommen
df_beroep['ID2'] = df_beroep['Beroep'].str.extract('(^\d{2})')
df_beroep['ID3'] = df_beroep['Beroep'].str.extract('(^\d{3})')

# Verkrijg de drie cijfers uit de kolom 'Beroepssegment' en stop deze in een nieuwe kolom
df_beroepssegment['ID3'] = df_beroepssegment['Beroep'].str.extract('(^\d{3})')

# Verkrijg de twee cijfers uit de kolom 'Beroepsklasse' en stop deze in een nieuwe kolom
df_beroepsklasse['ID2'] = df_beroepsklasse['Beroep'].str.extract('(^\d{2})')

code4 = '''# Verkrijg de eerste twee en eerste 3 cijfers uit de kolom 'Beroep' en stop deze in nieuwe kolommen
df_beroep['ID2'] = df_beroep['Beroep'].str.extract('(^\d{2})')
df_beroep['ID3'] = df_beroep['Beroep'].str.extract('(^\d{3})')

# Verkrijg de drie cijfers uit de kolom 'Beroepssegment' en stop deze in een nieuwe kolom
df_beroepssegment['ID3'] = df_beroepssegment['Beroep'].str.extract('(^\d{3})')

# Verkrijg de twee cijfers uit de kolom 'Beroepsklasse' en stop deze in een nieuwe kolom
df_beroepsklasse['ID2'] = df_beroepsklasse['Beroep'].str.extract('(^\d{2})')'''
st.code(code4, language = 'python')
        
# In[34]:
st.markdown('**Stap 3**: Verwijder van de datasets met betrekking tot beroepssegment en beroepsklasse de duplicates, zodat elk beroepssegment of -klasse maar één keer voorkomt (en we kunnen mergen als een many_to_one)')

# Pak de kolommen Beroep en ID(2/3)
df_sm = df_beroepssegment[['Beroep','ID3']]
df_bk = df_beroepsklasse[['Beroep','ID2']]

# Drop duplicates om een dataframe te krijgen met unieke combinaties
df_sm.drop_duplicates(inplace = True)
df_bk.drop_duplicates(inplace = True)

code5 = '''# Pak de kolommen Beroep en ID(2/3)
df_sm = df_beroepssegment[['Beroep','ID3']]
df_bk = df_beroepsklasse[['Beroep','ID2']]

# Drop duplicates om een dataframe te krijgen met unieke combinaties
df_sm.drop_duplicates(inplace = True)
df_bk.drop_duplicates(inplace = True)'''
st.code(code5, language = 'python')

# In[35]:
st.markdown('**Stap 4**: Merge de drie datasets tot een dataset met als eerste drie kolommen: *Beroep*, *Beroepssegment* en *Beroepsklasse*.')

# Merge beroep met de unieke combinaties van beroepsklasse
df_beroep_klasse = df_beroep.merge(df_bk, on = 'ID2', validate = 'many_to_one', suffixes = ['', '_y'])
klasse = df_beroep_klasse['Beroep_y']
df_beroep_klasse.drop(labels=['Beroep_y', 'ID2'], axis = 1, inplace = True)
df_beroep_klasse.insert(1, 'Beroepsklasse', klasse)

# Merge de verkregen dataframe met de unieke combinaties van beroepssegment
df_beroep_segklas = df_beroep_klasse.merge(df_sm, on = 'ID3', validate = 'many_to_one', suffixes = ['', '_y'])
segment = df_beroep_segklas['Beroep_y']
df_beroep_segklas.drop(labels=['Beroep_y', 'ID3'], axis = 1, inplace = True)
df_beroep_segklas.insert(1, 'Beroepssegment', segment)

code6 = '''# Merge beroep met de unieke combinaties van beroepsklasse
df_beroep_klasse = df_beroep.merge(df_bk, on = 'ID2', validate = 'many_to_one', suffixes = ['', '_y'])
klasse = df_beroep_klasse['Beroep_y']
df_beroep_klasse.drop(labels=['Beroep_y', 'ID2'], axis = 1, inplace = True)
df_beroep_klasse.insert(1, 'Beroepsklasse', klasse)

# Merge de verkregen dataframe met de unieke combinaties van beroepssegment
df_beroep_segklas = df_beroep_klasse.merge(df_sm, on = 'ID3', validate = 'many_to_one', suffixes = ['', '_y'])
segment = df_beroep_segklas['Beroep_y']
df_beroep_segklas.drop(labels=['Beroep_y', 'ID3'], axis = 1, inplace = True)
df_beroep_segklas.insert(1, 'Beroepssegment', segment)'''
st.code(code6, language = 'python')

st.write(df_beroep_segklas.head()) # Laat de eerste 5 waarnemingen zien


# In[36]:


print(df_beroep_segklas.columns)


# ### 3.2.4 Visuele data-analyse

# Labels aanmaken voor een aantal variabelen

# In[37]:


labeldict = {'Perioden':'Jaar',
             'ZiekteverzuimpercentageWerknemers_1':'Ziekteverzuimpercentage',
             'AandeelWerknemersDatHeeftVerzuimd_2':'Aandeel werknemers dat heeft verzuimd',
             'GemiddeldeVerzuimfrequentie_3':'Gemiddelde verzuimfrequentie',
             'GemiddeldeVerzuimduur_4':'Gemiddelde verzuimduur (in werkdagen)',
             'k_1Tot5Werkdagen_5':'1 tot 5 werkdagen',
             'k_5Tot20Werkdagen_6':'5 tot 20 werkdagen',
             'k_20Tot210Werkdagen_7':'20 tot 210 werkdagen',
             'k_210WerkdagenOfMeer_8':'210 werkdagen of meer',
             'JaHoofdzakelijkGevolgVanMijnWerk_9':'Ja, hoofdzakelijk gevolg van mijn werk',
             'JaVoorEenDeelGevolgVanMijnWerk_10':'Ja, voor een deel gevolg van mijn werk',
             'NeeGeenGevolgVanMijnWerk_11':'Nee, geen gevolg van mijn werk',
             'WeetNiet_12':'Weet ik niet',
             'RegelmatigVeelKrachtZetten_1':'Percentage werknemers dat regelmatig veel kracht verzet',
             'RegelmatigHardPraten_2':'Percentage werknemers dat regelmatig hard moet praten',
             'RegelmatigTeMakenMetTrillingen_3':'Percentage werknemers dat te maken krijg met trillingen',
             'GevaarlijkWerkTot2018_4':'Percentage werknemers dat gevaarlijk werk uitvoert (tot 2018)',
             'GevaarlijkWerkVanaf2018_5':'Percentage werknemers dat gevaarlijk werk uitvoert (vanaf 2018)',
             'Vallen_6':'Percentage werknemers dat werk uitvoert met valgevaar',
             'Struikelen_7':'Percentage werknemers dat werk uitvoert met struikelgevaar',
             'Bekneld_8':'Percentage werknemers dat werk uitvoert met knelgevaar',
             'Snijden_9':'Percentage werknemers dat werk uitvoert met snijgevaar',
             'Botsen_10':'Percentage werknemers dat werk uitvoert met botsgevaar',
             'GevaarlijkeStoffen_11':'Percentage werknemers dat werk uitvoert met gevaarlijke stoffen',
             'Geweld_12':'Percentage werknemers dat werk uitvoert waarbij geweld kan ontstaan',
             'Verbranden_13':'Percentage werknemers dat werk uitvoert met verbrandingsgevaar',
             'Verstikking_14':'Percentage werknemers dat werk uitvoert met verstikkingsgevaar',
             'Anders_15':'Percentage werknemers dat werk uitvoert met een ander gevaarsoort',
             'WaterigeOplossingen_16':'Percentage werknemers dat werkt met waterige oplossingen',
             'StoffenOpHuid_17':'Percentage werknemers dat werk uitvoert waarbij stoffen op de huid komen',
             'AdemtStoffenIn_18':'Percentage werknemers dat tijdens het werk stoffen inademt',
             'BesmettePersonen_19':'Percentage werknemers dat tijdens het werk in contact komt met besmette personen',
             'InOngemakkelijkeWerkhoudingWerken_20':'Percentage werknemers dat in een ongemakkelijke werkhouding werkt',
             'TijdensWerkRepeterendeBewegingMaken_21':'Percentage werknemers dat tijdens het werk repeterende bewegingen maakt',
             'UurPerDagAanBeeldschermVoorWerk_22':'Gemiddeld aantal schermuren voor werk'}

labeldict_breaks = {'Perioden':'Jaar',
             'ZiekteverzuimpercentageWerknemers_1':'Ziekteverzuimpercentage',
             'AandeelWerknemersDatHeeftVerzuimd_2':'Aandeel werknemers dat heeft verzuimd',
             'GemiddeldeVerzuimfrequentie_3':'Gemiddelde verzuimfrequentie',
             'GemiddeldeVerzuimduur_4':'Gemiddelde verzuimduur (in werkdagen)',
             'k_1Tot5Werkdagen_5':'1 tot 5 werkdagen',
             'k_5Tot20Werkdagen_6':'5 tot 20 werkdagen',
             'k_20Tot210Werkdagen_7':'20 tot 210 werkdagen',
             'k_210WerkdagenOfMeer_8':'210 werkdagen of meer',
             'JaHoofdzakelijkGevolgVanMijnWerk_9':'Ja, hoofdzakelijk gevolg van mijn werk',
             'JaVoorEenDeelGevolgVanMijnWerk_10':'Ja, voor een deel gevolg van mijn werk',
             'NeeGeenGevolgVanMijnWerk_11':'Nee, geen gevolg van mijn werk',
             'WeetNiet_12':'Weet ik niet',
             'RegelmatigVeelKrachtZetten_1':'Percentage werknemers<br>dat regelmatig veel<br>kracht verzet',
             'RegelmatigHardPraten_2':'Percentage werknemers dat regelmatig hard moet praten',
             'RegelmatigTeMakenMetTrillingen_3':'Percentage werknemers dat te maken krijg met trillingen',
             'GevaarlijkWerkTot2018_4':'Percentage werknemers dat gevaarlijk werk uitvoert (tot 2018)',
             'GevaarlijkWerkVanaf2018_5':'Percentage werknemers dat gevaarlijk werk uitvoert (vanaf 2018)',
             'Vallen_6':'Percentage werknemers dat werk uitvoert met valgevaar',
             'Struikelen_7':'Percentage werknemers dat werk uitvoert met struikelgevaar',
             'Bekneld_8':'Percentage werknemers dat werk uitvoert met knelgevaar',
             'Snijden_9':'Percentage werknemers dat werk uitvoert met snijgevaar',
             'Botsen_10':'Percentage werknemers dat werk uitvoert met botsgevaar',
             'GevaarlijkeStoffen_11':'Percentage werknemers dat werk uitvoert met gevaarlijke stoffen',
             'Geweld_12':'Percentage werknemers dat werk uitvoert waarbij geweld kan ontstaan',
             'Verbranden_13':'Percentage werknemers dat werk uitvoert met verbrandingsgevaar',
             'Verstikking_14':'Percentage werknemers dat werk uitvoert met verstikkingsgevaar',
             'Anders_15':'Percentage werknemers dat werk uitvoert met een ander gevaarsoort',
             'WaterigeOplossingen_16':'Percentage werknemers dat werkt met waterige oplossingen',
             'StoffenOpHuid_17':'Percentage werknemers dat werk uitvoert waarbij stoffen op de huid komen',
             'AdemtStoffenIn_18':'Percentage werknemers dat tijdens het werk stoffen inademt',
             'BesmettePersonen_19':'Percentage werknemers dat tijdens het werk in contact komt met besmette personen',
             'InOngemakkelijkeWerkhoudingWerken_20':'Percentage werknemers<br>dat in een ongemakkelijke<br>werkhouding werkt',
             'TijdensWerkRepeterendeBewegingMaken_21':'Percentage werknemers dat tijdens het werk repeterende bewegingen maakt',
             'UurPerDagAanBeeldschermVoorWerk_22':'Gemiddeld aantal schermuren voor werk'}

st.header('Visualisatie van de data')

fig = px.box(data_frame = df_beroep_segklas, x = 'Perioden', y = 'ZiekteverzuimpercentageWerknemers_1',
            color = 'Perioden')
st.plotly_chart(fig)

st.markdown('''
Allereerst beginnen we met een boxplot waar alle banen bij elkaar gezet zijn. Er wordt puur gekeken naar het ziekteverzuimpercentage van werknemers per jaar, over de jaren 2014-2020.  

In deze data lijkt een licht stijgende trend te zitten door de jaren heen. Kijkend naar de medianen zien we een stijging van 3.5% in 2014 naar 4.3% in 2020. Toch is het erg moeilijk om hier een duidelijke conclusie uit te trekken omdat de onzekerheid van de boxplots erg hoog is, en het zijn ook maar zeven jaren die getoond worden.  

De komst van het Coronavirus is nog niet te zien op deze visualisatie. Met data van 2021 erbij zou dit misschien anders zijn, maar men lijkt zich juist net iets minder vaak ziek te melden in 2020 dan in 2019.  Dit zou kunnen komen door dat mensen voorzichtiger waren en over het algemeen minder ziek werden, of doordat mensen bij het thuiswerken zich minder snel ziek melden omdat er geen kans is dat ze collega’s besmetten.''') 


# In[40]:


df_beroep_segklas_groupby = df_beroep_segklas.groupby(['Beroep', 'Beroepssegment', 'Beroepsklasse']).mean()

fig = px.scatter_matrix(df_beroep_segklas_groupby,
                        dimensions=["ZiekteverzuimpercentageWerknemers_1", "RegelmatigVeelKrachtZetten_1", "InOngemakkelijkeWerkhoudingWerken_20"],
                        color = df_beroep_segklas_groupby.index.get_level_values('Beroepsklasse'),
                        labels = labeldict_breaks)

fig.update_traces(diagonal_visible=False) # laat diagonale grafieken weg
fig.update_layout(width=1000, height=700, # Maak grafiek groter
                  legend_title = 'Beroepsklasse')

st.plotly_chart(fig)

st.markdown('''
Om een beter idee te krijgen van de verhoudingen tussen ziekteverzuim, werknemers die regelmatig veel kracht zetten en het percentage medewerkers dat in een ongemakkelijke houding werken is er een spreidingsmatrix opgesteld. Daaronder volgt een correlatiematrix die overeenkomt met de spreiding van de spreidingsmatrix.  

Ten eerste het verband tussen ziekteverzuim en het percentage werknemers dat regelmatig veel kracht zet. Dit verband heeft iets weg van een toetervorm, wat zou betekenen dat het verband wel lineair is maar geen constante variantie heeft. In de correlatiematrix is te zien dat er een correlatie van 0,27 is tussen de twee variabelen. Een zwak tot medium verband dus.  

Tussen ziekteverzuimpercentage en werknemers die in een ongemakkelijke houding werken is een vergelijkbaar verband te zien. Weer heeft het iets weg van een toetervorm. Deze keer is de correlatie wel iets hoger, namelijk 0,35, maar nog steeds is dat absoluut geen sterk verband.  

Wat opvallend is bij die twee spreidingsmatrices is dat vooral de technische- en de zorg en welzijn beroepen heel breed verdeeld zijn. Zij hebben bepaalde beroepen die een stuk meer kracht vergen en waar je in ongemakkelijkere houdingen staat dan gemiddeld.  

Dan het derde plaatje, regelmatig kracht verzetten tegenover een ongemakkelijke werkhouding, hier zien we een sterke correlatie met een correlatiecoëfficiënt van 0,89. Een ongemakkelijke werkhouding lijkt dus te maken te hebben met het regelmatig veel kracht moeten zetten, of andersom. Hier lijken vooral technische beroepen de kroon te spannen met de zwaarste banen. Door deze hoge correlatie weten we ook dat we in latere figuren deze niet meer allebei met andere variabelen hoeven te vergelijken omdat je dan zeer waarschijnlijk tot dezelfde conclusie komt.  
''')

st.table(df_beroep_segklas_groupby[["ZiekteverzuimpercentageWerknemers_1", 
                                    "RegelmatigVeelKrachtZetten_1", 
                                    "InOngemakkelijkeWerkhoudingWerken_20"]].corr().rename(columns={
  "ZiekteverzuimpercentageWerknemers_1": "Ziekteverzuimpercentage", 
  "RegelmatigVeelKrachtZetten_1": "Veel kracht zetten", 
  "InOngemakkelijkeWerkhoudingWerken_20": "Ongemakkelijke werkhouding"}, index ={
  "ZiekteverzuimpercentageWerknemers_1": "Ziekteverzuimpercentage", 
  "RegelmatigVeelKrachtZetten_1": "Veel kracht zetten", 
  "InOngemakkelijkeWerkhoudingWerken_20": "Ongemakkelijke werkhouding"}))


# <font color = 'red'> Trompetvorm tussen ziekteverzuimpercentage - ongemakkelijke werkhouding en ziekteverzuimpercentage - veel kracht verzetten. Ook sterke samenhang te zien tussen veel kracht verzetten en ongemakkelijke werkhouding.

# Tussen de beroepsklasse staat nu geen '02 Creatieve en taalkundige beroepen' meer, omdat deze geen specifieke beroepen bevatten in de dataset.
# <font color = 'red'> Hierdoor komen de kleuren niet overeen met de kleuren van het volgende plaatje in de legenda.

# In[ ]:


fig = px.box(data_frame = df_beroepsklasse, x = 'Beroep', y = 'ZiekteverzuimpercentageWerknemers_1',
            color = 'Beroep')

fig.update_xaxes(title = 'Beroepsklasse')
fig.update_yaxes(range = [0, df_beroepsklasse['ZiekteverzuimpercentageWerknemers_1'].max() + 0.5],
                 title = 'Ziekteverzuimpercentage')
fig.update_layout(legend_title = 'Beroepsklasse')

st.plotly_chart(fig)

st.markdown('''Om een algemeen beeld te krijgen van het ziekteverzuimpercentage (over de jaren 2014 tot en met 2020) per beroepsklasse, zijn deze boxplots afgebeeld.

**Ligging**  
Het is duidelijk te zien dat de boxplots van *Openbaar bestuur, veiligheid en justitie* (mediaan: 5,1%) en *Zorg en welzijn beroepen* (mediaan 5,4%) hoger ligt dan de rest.  
De beroepsklasse *Openbaar bestuur, veiligheid en justitie* bevat onder andere beveiligingswerkers zoals politie, brandweer en militaire beroepen. Deze beroepen krijgen over het algemeen vaker te maken met geweld (en vuur), wat meer risico op gewond raken met zich meebrengt. Dit zou een reden kunnen zijn dat het percentage hoog ligt.  
Het hoge percentage bij de beroepsklasse *Zorg en welzijn beroepen* zou kunnen komen door een hogere kans op besmetting en eventuele fysieke en mentale werkdruk.  

Het is ook opvallend dat de beroepsklasse *Managers* (mediaan: 2,7%) vrij laag ligt, gevolgd door de beroepsklasse *ICT beroepen* (mediaan: 3,2%) die iets hoger ligt.  
Het lage percentage bij *Managers* doet vermoeden dat managers vaker doorwerken bij ziekte, of zich in ieder geval niet ziek melden. Dit blijkt ook uit cijfers van het Sociaal Cultureel Planbureau (https://mtsprout.nl/management-leiderschap/mt-onderzoek-zieke-manager-werkt-altijd-door).  
Bij de beroepsklasse *ICT beroepen* is het aannemelijk dat het voor werknemers makkelijker is om thuis door te werken als op kantoor werken niet mogelijk is. Dit zou dan ook de reden kunnen zijn van het lage ziekteverzuimpercentage (maar dit is slechts een aanname).  

**Spreiding**  
De spreiding van *Beroepsklasse overig* valt het meeste op. De spreiding van deze klasse is waarschijnlijk te verklaren door de verschillende beroepen die hierin vallen. Deze beroepen zijn niet gespecificeerd in de dataset, maar het is aannemelijk dat deze beroepen aardig verschillen van elkaar en daardoor ook verschillende ziekteverzuimpercentages hebben.  

De beroepsklasse *Creatieve en taalkundige beroepen* heeft ook een redelijk grote spreiding. De verwachting is dat dit komt door het brede spectrum aan beroepen binnen die beroepsklasse. Ook deze beroepen zijn niet gespecificeerd in de dataset, maar de beroepssegmenten die hieronder vallen wel: *Auteurs en kunstenaars* en *Vakspecialisten op artistiek en cultureel gebied*.  

De kleine spreiding van de *Pedagogische beroepen* valt ook op. Dit heeft waarschijnlijk als reden het tegenovergestelde van het bovengenoemde. De beroepssegmenten die onder deze klasse vallen zijn: *Docenten*, *Sportinstructeurs* en *Leidsters kinderopvang en onderwijs*. Het beroepssegment *Sportinstructeurs* verschilt qua werkzaamheden van de andere twee beroepssegmenten - je zou dus eigenlijk niet zo’n kleine spreiding verwachten – maar dit segment bevat geen data over het ziekteverzuimpercentage en doet dus niet mee in de boxplot.''')


# Het valt op dat de ziekteverzuimpergentages van 'Openbaar bestuur, veiligheid en justitie' en 'Zorg en welzijn' hoger liggen dan de rest. 'Zorg en welzijn' ligt het hoogst.

# In[ ]:


# Credits: https://plotly.com/python/sliders/

fig = px.scatter(data_frame = df_beroep_segklas, x = 'Beroep', y = 'ZiekteverzuimpercentageWerknemers_1',
                color = 'Beroepsklasse',
                animation_frame = 'Perioden',
                labels = labeldict_breaks)

fig.update_xaxes(showticklabels=False)
fig.update_yaxes(range = [0, df_beroep_segklas['ZiekteverzuimpercentageWerknemers_1'].max() + 0.5],
                 title = 'Ziekteverzuimpercentage')

st.plotly_chart(fig)

st.markdown('''In de vorige visualisatie was het ziekteverzuimpercentage per beroepsgroep te zien over de jaren 2014 tot en met 2020. In bovenstaande visualisatie zijn deze gegevens iets specifieker weergegeven, namelijk per beroep (elk punt is een beroep) en per jaar (hiervoor wordt de slider gebruikt). De kleuren van de punten geven aan in welke beroepsklasse dit beroep valt.  
In de legenda mist de beroepsklasse *Creatieve en taalkundige beroepen*. Dit komt doordat deze klasse alleen is opgedeeld in beroepssegmenten en niet in beroepen. Om ook deze klasse duidelijk per jaar in beeld te krijgen, kan het handig zijn om nog een visualisatie te maken met de beroepssegmenten in plaats van de beroepen. Voor nu zijn we vooral geïnteresseerd in het totaalplaatje.  

De animatie van de slider laat zien dat de puntenwolk elk jaar iets hoger komt te liggen. Ook is het interessant om te zien dat de spreiding van de puntenwolk groter is in 2020, als je deze vergelijkt met de puntenwolk van 2014.  

Een andere opvallende situatie doet zich voor wanneer we 2019 vergelijken met 2020. Kijkend naar de blauwe puntenwolk aan de linkerkant (*Pedagogische beroepen*), zien we een punt opeens omhoog schieten. Dit is het punt dat hoort bij de beroepen *Leidsters kinderopvang en onderwijsassistenten*. Dat dit punt in 2020 opeens omhoogschiet doet erg vermoeden dat dit iets te maken heeft met de coronacrisis.''')


# Tussen de beroepsklasse staat nu geen '02 Creatieve en taalkundige beroepen' meer, omdat deze geen specifieke beroepen bevatten in de dataset.
# <font color = 'red'> Hierdoor komen de kleuren niet overeen met de kleuren van het vorige plaatje in de legenda.


# In[ ]:


df19 = df_beroep_segklas[df_beroep_segklas['Perioden']==2019]
df20 = df_beroep_segklas[df_beroep_segklas['Perioden']==2020]
index_vals = df19['Beroepsklasse'].astype('category').cat.codes # maak categorieën van beroepsklassen (voor de markerkleur)

fig = go.Figure()

fig.add_trace(go.Bar(x = df19['Beroep'], y = df19['ZiekteverzuimpercentageWerknemers_1'],
                     name = '2019', marker={'color':index_vals, 'colorscale': px.colors.qualitative.Light24}, visible = True))
fig.add_trace(go.Bar(x = df20['Beroep'], y = df20['ZiekteverzuimpercentageWerknemers_1'],
                     name = '2020', marker={'color':index_vals, 'colorscale': px.colors.qualitative.Light24}, visible = False))

year_buttons = [{'label': '2019', 'method': 'update', 'args': [{'visible': [True, False]}]},
                {'label': '2020', 'method': 'update', 'args': [{'visible': [False, True]}]}]

fig.update_layout({'updatemenus':[{'active': True, 'type': 'buttons', 'buttons':year_buttons}]},
                  showlegend = False)

fig.update_xaxes(showticklabels=False)
fig.update_yaxes(range=[0, 8], title = 'Ziekteverzuimpercentage')

st.plotly_chart(fig)


# <font color = 'red'> Een legenda maken per kleur (beroepsklasse) lukt me niet.

# In[ ]:


df_beroepsklasse_groupby = df_beroepsklasse.groupby('Beroep').mean()
fysiekearbeid = df_beroepsklasse_groupby.columns.tolist()[13:-1]
fysiekearbeid_labels = list(labeldict.values())[13:-1]
st.markdown('''In deze barplot is het ziekteverzuimpercentage per beroepsklasse te zien. Via de button is het jaar 2019 en 2020 te zien. Door op een balkje te gaan staan is te zien welk beroep het is en hoe hoog het percentage is.  
In 2019 is te zien dat buschauffeurs en taxibestuurders een uitschieter zijn, met ongeveer 7%. Er is ook te zien dat algemeen directeuren een relatief lage uitval hebben met 1,5%.   
In 2020 is te zien dat het percentage ziekteverzuim is toegenomen vergeleken met 2019. Hierin is te zien dat hulpkrachten in de bouw en industrie een relatief hoog percentage hebben namelijk 7,6%.  Net als in 2019 hebben algemeen directeuren een relatief laag uitval percentage met 1,1%. Dit percentage ligt lager dan in 2019.   
Aan de hand van de barplot is dus het ziekteverzuimpercentage per beroepsklasse te zien. Uit de grafieken blijkt dat algemeen directeuren een relatief laag ziekteverzuimpercentage hebben. Er is niet duidelijk te zien welke beroepsklasse een relatief hoog ziekteverzuimpercentage hebben.''')

fig2 = go.Figure()

j = 0
dropdown_buttons = []
for i in fysiekearbeid:
    if j == 0:
        v = True
    else:
        v = False
    
    fig2.add_trace(go.Bar(x = df_beroepsklasse_groupby.index, y = df_beroepsklasse_groupby[i],
                        name = i, text=df_beroepsklasse_groupby[i], visible = v))

    dropdown_buttons.append({'label':fysiekearbeid_labels[j],
                             'method': 'update',
                             'args': [{"visible":[x==i for x in fysiekearbeid]},
                                      {'yaxis':{'title':fysiekearbeid_labels[j],
                                                'range':[0, df_beroepsklasse_groupby[fysiekearbeid].max().max()+10]}}]})
    j += 1

fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig2.update_layout({'updatemenus':[{'active':True, 'buttons': dropdown_buttons,
                                   'x': 1, 'y': 1.2}]},
                  annotations = [{'text':"Fysiekse arbeidsbelasting", 'font_size':15,
                                'x': 1, 'xref':"paper", 'y':1.3, 'yref':"paper",
                                'showarrow':False}],
                  showlegend = False,
                  height = 800)

st.plotly_chart(fig2)


# In[ ]:


df_groupby_beroep = df_beroep_segklas.groupby(['Beroep', 'Beroepssegment', 'Beroepsklasse']).mean()
df_transpose = df_groupby_beroep.transpose()
df_transpose.head()
st.markdown('''In deze barplot is de fysieke arbeidsbelasting per gevaar per beroepsklasse te zien. Door middel van de dropdown box is per gevaar te zien welke gevaar een hoog of laag arbeidsbelasting percentage heeft. Bij de eerste elf gevaren blijkt dat Agrarische, Technische en Logistieke beroepen een hoog percentage scoren. Uit de overige gevaren blijkt dat vaak specifieke beroepen een hoog percentage scoren.  Zo is de kans dat iemand van zorg en welzijn het snelst in contact komt met een besmet persoon het hoogst.  
Tussen alle fysieke arbeidsbelasting variabelen zit twee keer de variabele ‘Percentage werknemers dat gevaarlijk werk uitvoert’. Eén keer tot 2018 en één keer vanaf 2018. Dit komt omdat de informatie tot 2018 op een andere manier is verkregen dan daarna. Te zien is dat het gemiddelde percentage vanaf 2018 hoger ligt dan het gemiddelde percentage tot 2018. Een mogelijke oorzaak zou kunnen zijn dat tot 2018 mensen met de hand konden aangeven of ze een gevaarlijk beroep uit voerden. Terwijl het vanaf 2018 zo was dat als men 1 van de 10 gevaren aanvinkte het automatisch viel onder gevaarlijk beroep.''')

fig = px.scatter(data_frame = df_beroepsklasse, x = 'UurPerDagAanBeeldschermVoorWerk_22', y = 'ZiekteverzuimpercentageWerknemers_1', 
            color = 'Beroep')

fig.update_xaxes(title = 'Uren per dag achter beeldscherm')
fig.update_yaxes(range = [0, df_beroepsklasse['ZiekteverzuimpercentageWerknemers_1'].max() + 0.5],
                 title = 'Ziekteverzuimpercentage')
fig.update_layout(legend_title = 'Verhouding schermuren en ziekteverzuim')

st.plotly_chart(fig)

st.markdown('''De variabele met betrekking tot het aantal schermuren per dag is, in tegenstelling tot de andere variabelen van de dataset *Fysieke arbeidsbelasting*, niet gegeven in percentages maar in uren. Daarom onderzoeken we deze variabele op een andere manier.  

In bovenstaande grafiek is te zien dat het percentage ziekteverzuim heel geclusterd is bij een laag aantal schermuren. Des te meer het aantal uren dat het personeel naar een scherm kijkt toeneemt, des te meer het ziekteverzuim tot het toppunt van ± 4 uur. Alhoewel we zien dat het ziekteverzuimpercentage nogal van elkaar kan afwijken, en er zowel beroepsgroepen zijn die uitschieten ten opzichte van de overige beroepsgroepen. Naarmate het personeel meer dan ± 4 uur schermtijd heeft, daalt het ziekteverzuim en clustert het zich meer.''')

st.header('Conclusie')


