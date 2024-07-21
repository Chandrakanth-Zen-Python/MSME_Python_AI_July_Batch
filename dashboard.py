import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


st.set_page_config(page_title='dashboard-market_analysis',
                   layout='wide',
                   page_icon=":crown:")

st.title('Dashboard - Market Analysis')


@st.cache_data
def load_data():

    # read the dataset 

    data = pd.read_csv('Assignment-1_Data.csv',sep=';')

    # preprocessing

    data['Price'].replace(',','.',regex=True,inplace=True)

    data.loc[:,'Date']=pd.to_datetime(data['Date'],format='%d.%m.%Y %H:%M')
    data.loc[:,"Price"]=data['Price'].astype('Float32')
    data.loc[:,"Quantity"]=data['Quantity'].astype('Float32')

    data.loc[:,'Amount']=data['Quantity']*data['Price']

    return data


data=load_data()

# sidebar to control the categories of information we see in the chart
sidebar= st.sidebar.title('Filters')

countries=sidebar.multiselect(label='Country',
                    options=list(data['Country'].unique()))

if len(countries)>0:

    data=data.loc[data['Country'].isin(countries)]


# Barchart
st.write("### Itemwise Top Quantities")

analysis1=pd.pivot_table(data,values=['Quantity'],
                         index=['Itemname'],aggfunc='sum')
analysis1.sort_values('Quantity',ascending=False,inplace=True)
analysis1.reset_index(inplace=True)

st.bar_chart(analysis1.head(100),x="Itemname",y='Quantity',
             x_label='Item',
             y_label='Quantity')

# Donut chart - Countrywise Sale Amount
st.write('### Countrywise Sale Amount')

col1,col2 = st.columns(2)

analysis2=data[["Country",'Amount']].groupby('Country').sum().reset_index()


with col1:

    st.subheader('Donut chart :office:')

    fig,ax = plt.subplots(figsize=(6,4), 
                          subplot_kw=dict(aspect="equal"))


    wedges,text,autotexts=ax.pie(analysis2['Amount'],wedgeprops=dict(width=0.5),autopct='%1.1f%%')

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)

    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(list(analysis2['Country'])[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    st.pyplot(fig)

with col2:

    st.subheader('Bar chart')

    fig2,ax2=plt.subplots(figsize=(6,6))

    ax2.bar(analysis2['Country'],analysis2['Amount'])

    ax2.set_xlabel('Country')

    ax2.set_ylabel('Sales Amount')

    st.pyplot(fig2)

# Datewise aggregated sales figures

analysis3=pd.pivot_table(data,values=['Amount'],index=['Date',"Country"],aggfunc=sum)

analysis3.reset_index(inplace=True)

st.subheader('Daywise aggregated sales for each country')

fig=px.line(analysis3,x='Date',y='Amount',color='Country',markers=True)

st.plotly_chart(fig)


