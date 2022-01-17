#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np

HoP="Resources/purchase_data.csv"
HoP_df = pd.read_csv(HoP)

gamer_counts= HoP_df["SN"].value_counts()

gamer_counts_df = pd.DataFrame({
    "Total Players": [len(gamer_counts)]})

unique_items= HoP_df["Item Name"].value_counts()
average_price=HoP_df["Price"].mean()
total_revenue=HoP_df["Price"].sum()
no_of_purchases=HoP_df["Purchase ID"].value_counts()

purchase_analysis_df = pd.DataFrame([
    {"Number of Unique Items": len(unique_items), "Average Price": average_price,
     "Number of Purchases": len(no_of_purchases), "Total Revenue" : total_revenue}
])

purchase_analysis_df["Total Revenue"] = purchase_analysis_df["Total Revenue"].astype(float).map("${:,.2f}".format)
purchase_analysis_df["Average Price"] = purchase_analysis_df["Average Price"].astype(float).map("${:,.2f}".format)

player_and_genders = []
for index, row in HoP_df.iterrows():
    player = row["SN"]
    gender = row["Gender"]
    if (player, gender) not in player_and_genders:
        player_and_genders.append((player, gender))
        
p_g_df = HoP_df.groupby("Gender").count()
len(player_and_genders)
HoP_df2=HoP_df
HoP_df3=HoP_df
#Test2=HoP_df[HoP_df['Gender'].str.contains("Male")]
HoP_Unique_DF = HoP_df2.drop_duplicates(subset=['SN'])
Males=HoP_Unique_DF[HoP_Unique_DF['Gender'].str.contains("Male")]
Females=HoP_Unique_DF[HoP_Unique_DF['Gender'].str.contains("Female")]
Others=HoP_Unique_DF[HoP_Unique_DF['Gender'].str.contains("Other / Non-Disclosed")]

#Gender_df = pd.DataFrame({
 #   "Male": len(Males),
  #  "Female": len(Females),
   # "Other / Non-Disclosed": len(Others)
#})

genders = ({"Male": len(Males),
    "Female": len(Females),
    "Other / Non-Disclosed": len(Others)
           })
genders_df=pd.Series(genders).to_frame('Total Count')

PoP = ({"Male": len(Males)/len(player_and_genders),
    "Female": len(Females)/len(player_and_genders),
    "Other / Non-Disclosed": len(Others)/len(player_and_genders)}
           )
PoP_df=pd.Series(PoP).to_frame('Percentage of Players')
PoP_df["Percentage of Players"] = PoP_df["Percentage of Players"].astype(float).map("{:,.2%}".format)


Gender_PoP_df= pd.merge(genders_df, PoP_df, left_index=True, right_index=True)

gender_purchase = HoP_df['Gender'].value_counts()
pd.DataFrame(gender_purchase)

p_g_df = HoP_df.groupby("Gender")
purchase_counts = p_g_df['Purchase ID'].count()
total_purchases = p_g_df['Price'].sum()
average_purchases = total_purchases / purchase_counts

Males_No=len(Males)
Females_No=len(Females)
Others_No=len(Others)

total_purchases["Male"]/Males_No
total_purchases["Female"]/Females_No
total_purchases["Other / Non-Disclosed"]/Others_No

unique_total_purchase=[(total_purchases["Female"]/Females_No),
(total_purchases["Male"]/Males_No),
(total_purchases["Other / Non-Disclosed"]/Others_No)]

purchase_analysis_df2=pd.DataFrame({"Purchase Count": purchase_counts,
             "Average Purchase Count": average_purchases,
             "Total Purchase Value" : total_purchases,
             "Avg Total Purchase per Person" : unique_total_purchase})

purchase_analysis_df2["Average Purchase Count"] = purchase_analysis_df2["Average Purchase Count"].astype(float).map("${:,.2f}".format)
purchase_analysis_df2["Avg Total Purchase per Person"] = purchase_analysis_df2["Avg Total Purchase per Person"].astype(float).map("${:,.2f}".format)
purchase_analysis_df2["Total Purchase Value"] = purchase_analysis_df2["Total Purchase Value"].astype(float).map("${:,.2f}".format)


Age_Demo_df = HoP_df.drop_duplicates(subset="SN",keep="first")

bins = [0,9,14,19,24,29,34,39,45]
age_groups = ["<10","10-14","15-19","20-24","25-29","30-34","35-39","40+"]
Age_Demo_df["Total Count"] = pd.cut(Age_Demo_df["Age"], bins,
                             labels=age_groups, include_lowest=True)


Ages_df = Age_Demo_df["Total Count"].value_counts().sort_index().to_frame()
def division(Total_Counts):
    return "{:,.2%}".format(((Total_Counts/len(gamer_counts))))
def division2(Make_Money):
    return "${:,.2f}".format(Make_Money)
Ages_df["Percentage of Players"]=Ages_df["Total Count"].apply(division)

Purchase_Analysis=pd.DataFrame()
HoP_df["Age Ranges"] = pd.cut(HoP_df["Age"], bins,
                             labels=age_groups, include_lowest=True)

HoP_df=HoP_df.set_index("Age Ranges").sort_index()

Purchase_Count=HoP_df.groupby("Age Ranges").count()["Purchase ID"]
Average_Purchase_Price=HoP_df.groupby("Age Ranges").mean()["Price"]
Total_Purchase_Value=HoP_df.groupby("Age Ranges").sum()["Price"]
Avg_Total_Purchase_per_Person=Total_Purchase_Value/Ages_df["Total Count"]



Purchase_Analysis["Purchase Count"]=Purchase_Count
Purchase_Analysis["Average Purchase Price"]=Average_Purchase_Price.apply(division2)
Purchase_Analysis["Total Purchase Value"]=Total_Purchase_Value.apply(division2)
Purchase_Analysis["Avg Total Purchase per Person"]=Avg_Total_Purchase_per_Person.apply(division2)

HoP_df4 = pd.read_csv(HoP)

HoP_df4.set_index("SN", inplace=True)
HoP_df4['Total Purchase Value'] = HoP_df4.groupby("SN").sum()["Price"]
Buying_Price=HoP_df4.groupby("SN").sum()["Price"]

HoP_df4["Purchase Count"]=HoP_df4.groupby("SN").count()["Purchase ID"]
HoP_df4["Average Purchase Price"]=HoP_df4.groupby("SN").mean()["Price"]

HoP_df4.sort_values("Total Purchase Value", ascending=False, inplace=True)
HoP_df4.drop_duplicates("Total Purchase Value", inplace=True)

neworder = HoP_df4[['Purchase Count', 'Average Purchase Price', 'Total Purchase Value']]
neworder["Average Purchase Price"]=neworder["Average Purchase Price"].apply(division2)
neworder["Total Purchase Value"]=neworder["Total Purchase Value"].apply(division2)

Top_Spender_df=neworder

HoP_df5=HoP_df2
item_purchase_count=HoP_df5["Item ID"].value_counts()

Most_Popular_Items_df=HoP_df5.set_index(['Item ID', 'Item Name'])
Most_Popular_Items_df["Purchase Count"]=HoP_df5.groupby(["Item ID","Item Name"]).count()["Purchase ID"]
Most_Popular_Items_df=Most_Popular_Items_df.sort_values("Purchase Count", ascending=False)
Most_Popular_Items_df["Total Purchase Value"]=Most_Popular_Items_df.groupby(['Item ID', 'Item Name']).sum()["Price"].to_frame()
Most_Popular_Items_df["Item Price"]=HoP_df5.groupby(["Item ID","Item Name"]).mean()["Price"]
Most_Popular_Items_df=Most_Popular_Items_df[~Most_Popular_Items_df.index.duplicated(keep='first')]
Most_Popular_Items_df2=Most_Popular_Items_df.copy()


Most_Popular_Items_df2["Total Purchase Value"]=Most_Popular_Items_df2["Total Purchase Value"].apply(division2)
Most_Popular_Items_df2["Item Price"]=Most_Popular_Items_df2["Item Price"].apply(division2)

Most_Popular_Items_df2=Most_Popular_Items_df2.drop(['Purchase ID', 'SN','Age','Gender','Price','Age Ranges'], axis=1)
neworder2 = Most_Popular_Items_df2[['Purchase Count', 'Item Price', 'Total Purchase Value']]

Most_Popular_Items_df.sort_values("Total Purchase Value", ascending=False,inplace=True)
Most_Popular_Items_df=Most_Popular_Items_df.head()
Most_Popular_Items_df["Total Purchase Value"]=Most_Popular_Items_df["Total Purchase Value"].apply(division2)
Most_Popular_Items_df["Item Price"]=Most_Popular_Items_df["Item Price"].apply(division2)

Most_Popular_Items_df=Most_Popular_Items_df.drop(['Purchase ID', 'SN','Age','Gender','Price','Age Ranges'], axis=1)
Most_Popular_Items_df=Most_Popular_Items_df[['Purchase Count', 'Item Price', 'Total Purchase Value']]


# In[14]:


gamer_counts_df


# In[15]:


purchase_analysis_df


# In[16]:


Gender_PoP_df


# In[17]:


purchase_analysis_df2


# In[18]:


Ages_df


# In[19]:


Purchase_Analysis


# In[20]:


Top_Spender_df.head()


# In[21]:


neworder2.head(6)


# In[22]:


Most_Popular_Items_df


# In[ ]:




