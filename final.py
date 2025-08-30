# Importing important libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
#average daily used appliance list 
appliances = {
    'Fridge': {'power_watt': 150, 'hours_per_day': 24},
    'TV': {'power_watt': 120, 'hours_per_day': 4},
    'Laptop': {'power_watt': 60, 'hours_per_day': 6},
    'Air Conditioner': {'power_watt': 2000, 'hours_per_day': 5},
    'Washing Machine': {'power_watt': 500, 'hours_per_day': 1},
    'Microwave': {'power_watt': 1100, 'hours_per_day': 0.5}
}


#appliance value settings sidebar
st.sidebar.subheader("Appliance value settings")

for appliance in appliances:
    appliances[appliance]['power_watt'] = st.sidebar.number_input(
        f"{appliance} Power (W)", value=appliances[appliance]['power_watt']
    )
    appliances[appliance]['hours_per_day'] = st.sidebar.number_input(
        f"{appliance} Usage (Hour/Day)", value=appliances[appliance]['hours_per_day']
    )
    
#add appliance 


#total daily power usage per appliance in wh  
appliance_daily_power_usage = {}

for q in appliances:
      x = appliances[str(q)]["power_watt"]
      y = appliances[str(q)]["hours_per_day"]
      daily_power = x* y 
      appliance_daily_power_usage[q] = daily_power
     
      
#organising data     
data = pd.DataFrame.from_dict(appliance_daily_power_usage, orient="index").reset_index(drop=False)

data.columns = ["Appliance", "Total power (Wh) used in 24h"]


prices_data = pd.read_csv("C:/Users/omers/OneDrive/Masaüstü/Projects Folder/1st Project home energy usage/cost-of-electricity-by-country-2025.csv",sep ="," )


#cleaning thedata
columns = list(prices_data.columns)

new_columns = []
for i in columns:    
    i = i.lower()
    i = i.replace(" " , "_")
    new_columns.append(i)
    print(i)
    
prices_data.columns = new_columns
    
maindata_columns = list(data.columns)

data_new_columns = []
for i in maindata_columns:    
    i = i.lower()
    i = i.replace(" " , "_")
    data_new_columns.append(i)
    print(i)

data.columns = data_new_columns

prices_data = prices_data[prices_data["costofelectricity_electricitycost_usdperkwh_2024march"] > 0]




#calculating total cost per country and turning power to kwh

total_power_spent = data.iloc[:,1].astype(float).sum() / 1000

total_money_for_countries = []
for i in prices_data.iloc[:,2].astype(float):
    total_money_for_countries.append(i*total_power_spent)
    
prices_data["total_daily_money_spent_usd"] = total_money_for_countries

prices_data_index = (prices_data.total_daily_money_spent_usd.sort_values(ascending = True)).index
prices_data = prices_data.reindex(prices_data_index)


#creating a streamlit web app
st.title("Home Energy Usage and Cost Analysis")



st.subheader("Appliance Power Usages Data")

st.dataframe(pd.DataFrame.from_dict(appliances))

st.subheader("Appliances Power Usage Ratio (Piechart)")


#appliance power usage pie chart
fig , ax = plt.subplots(figsize = (10,10))
colors = sns.color_palette('plasma')

plt.pie( data.iloc[:,1], labels = data.iloc[:,0],startangle= 90, colors= colors)

plt.show()

st.pyplot(fig)


st.subheader("Enery Cost per Country Data")


st.dataframe(prices_data)

country = st.selectbox("Select Country", list(prices_data.country))
price_per_kwh = prices_data.loc[prices_data["country"] == country, prices_data.columns[-1]].values[0]
zoer = data.iloc[:,1].astype(float).sum() 
st.success(f"Selected Country: {country}")
st.metric("Total Daily Enegy Cost", f"{price_per_kwh:.2f} $")
st.metric("Total Used Wh", f"{zoer:.2f} WH")

fig , ax = plt.subplots(figsize = (50,50))
sns.barplot(x= np.array(prices_data.iloc[:,1]), y= np.array(prices_data.total_daily_money_spent_usd), data=prices_data , palette ="plasma")

plt.xlabel("Country")
plt.xticks(rotation = 90 ,size = 5)
plt.ylabel("Daily money spent (USD)")
plt.show()
st.pyplot(fig)

























