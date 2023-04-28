import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#for more wider page and page title
st.set_page_config(layout='wide',page_title='startup analysis')

#df= pd.read_csv('startup_funding.csv')
df= pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year
df['city']=df['city'].str.replace('Bangalore','Bengaluru')


# ************************  working on overall analysis    *******************************************************************

def load_overall_analysis():
    st.title('overall analysis')

    # total invested amount

    total_invested=round(df['amount'].sum(),2)

    # max amount infuse in a start up
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    # avg ticket size
    avg_funding=df.groupby('startup')['amount'].sum().mean()

    # total funded startup

    num_startups=df['startup'].nunique()


# use diff col to display these matrix in the columns
    col1,col2,col3,col4=st.columns(4)


    # metric for total invested amount
    with col1:
        st.metric('Total',str(total_invested)+' cr ')

    with col2:
        st.metric('Max',str(max_funding)+'cr')

    with col3:
        st.metric('Avg',str(round(avg_funding))+'cr')

    with col4:
        st.metric('Funded startup',num_startups)


    
    # month on month graph

    st.header('Month on Month graph')

    selected_option=st.selectbox('Select Type',['Total','Count'])

    if selected_option =='Total':

        tempp_df=df.groupby(['year','month'])['amount'].sum().reset_index()

    else:

        tempp_df=df.groupby(['year','month'])['amount'].count().reset_index()


    tempp_df['x-axis']=tempp_df['month'].astype('str') + '-' + tempp_df['year'].astype('str')

    fig5,ax5=plt.subplots()
    #plt.figure().set_figwidth(15)
    ax5.plot(tempp_df['x-axis'],tempp_df['amount'])
   
    ax5.set_xticklabels(tempp_df['x-axis'], fontsize=5)
    plt.xticks(rotation='vertical')
    st.pyplot(fig5)

    # sector analysis

    st.header('Top sector analysis')
    option=st.selectbox('Select Type',['sum','Count'])
    
    if option =='sum':

        sector_analysis= df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)

    else:

        sector_analysis= df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
    

    fig6,ax6=plt.subplots()
    ax6.pie(sector_analysis,labels=sector_analysis.index,autopct="%0.01f%%")
    st.pyplot(fig6)


    col1,col2=st.columns(2)

    with col1:
        st.header('Type of Funding')

        type_of_funding =pd.DataFrame(df['round'].unique(),columns =['Funding type'])

        st.dataframe(type_of_funding)

    with col2:
        st.header('Top 10 City wise funding')

        
        city_funding =df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)

        fig8,ax8=plt.subplots()
       
        ax8.bar(city_funding.index,city_funding.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig8)

    # top investor

    st.header('Top Investor')
    top_investor=df.groupby('investor')['amount'].max().sort_values(ascending=False).head(1)
    st.dataframe(top_investor)

   

# ********************************** STARTUP *********************************************************************************

def load_startp_details(startup):
    st.title(startup)

    col1,col2,col3=st.columns(3)

    with col1:
    # realted to which indusrty
    
        industry=df[df['startup'].str.contains(startup)]['vertical']

        st.header('Related Industry')
        st.dataframe(industry)

    with col2:
    # related to which sub industry
        sub_industry=df[df['startup'].str.contains(startup)]['subvertical']

        st.header('Sub Industry')
        st.dataframe(sub_industry)

    with col3:
        location=df[df['startup'].str.contains(startup)]['city'].unique()

        st.header('Location')
        st.dataframe(location)

    
    col1,col2,col3=st.columns(3)
    with col1:
        stage=df[df['startup'].str.contains(startup)]['round']
        st.header('Investment round')
        st.dataframe(stage)

    with col2:
        investment=df[df['startup'].str.contains(startup)]['investor']
        st.header('Investor')
        st.dataframe(investment)

    with col3:
        date=df[df['startup'].str.contains(startup)]['date']
        st.header('Investment date')
        st.dataframe(date)

    
    amount=pd.DataFrame(df[df['startup'].str.contains(startup)]['amount']).sum()
    st.header('Invested Amount')
    st.dataframe(amount)

# ************************  working on investor dropdown   *******************************************************************

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 incestment of a investor
    last5_df= df[df['investor'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]

    st.subheader('Most Recent Investemnt')
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    with col1:
    #bigges investemnt
        big_invest_series=df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('largest investment by a investor')

    
    # plotting graph using streamlit
        fig,ax=plt.subplots()
        ax.bar(big_invest_series.index,big_invest_series.values)
        st.pyplot(fig)

    with col2:
    # plotting graph
        vertical_series=df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum()
    
        st.subheader('Sector invested in')
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)


    col3,col4=st.columns(2)
    with col3:
    # investemnt at which stage

        investemnt_stage=df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('stage at which invested')
        fig2,ax2=plt.subplots()
        ax2.pie(investemnt_stage,labels=investemnt_stage.index,autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        # city
        
        investemnt_city=df[df['investor'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('city at which invested')
        fig3,ax3=plt.subplots()
        ax3.pie(investemnt_city,labels=investemnt_city.index,autopct="%0.01f%%")
        st.pyplot(fig3)

    # work on year on year graph
    df['year']=df['date'].dt.year
    year_series=df[df['investor'].str.contains(investor)].groupby('year')['amount'].sum()

    
    st.subheader('year on year investment')
    fig4,ax4=plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)








# ***************************************  DROP DOWN MENU  ***********************************************************

st.sidebar.title('startup Funding Analysis')

option=st.sidebar.selectbox('select one',['overall analysis','startup','Investor'])

if option == 'overall analysis':

    #btn0=st.sidebar.button('show overall analysis')

    #checking button is clicked or not

    #if btn0:
    load_overall_analysis()


elif option=='startup':

    select_Startup = st.sidebar.selectbox('select startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('find startup detail')
    #st.title('startup analysis')

    if btn1:
        load_startp_details(select_Startup)

else:

    selected_investor = st.sidebar.selectbox('select investor',sorted(set(df['investor'].str.split(',').sum())))
    btn2=st.sidebar.button('find startup detail')
    #check button is clicked or not
    if btn2:
        load_investor_details(selected_investor)

    

    