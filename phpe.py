import streamlit as st
import pandas as pd
import mysql.connector as db
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(
    page_title="Phone Pe Pulse",
    layout="wide",
    initial_sidebar_state="expanded")


db_connection=db.connect(
    host="localhost",
    user="root",
    password="roots",
    database="ppproj"
)
mycursor = db_connection.cursor()

def execute_query(query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    Dataf = pd.DataFrame(result, columns=mycursor.column_names)
    return Dataf
# CSS styling for the header and subheader
st.markdown(
    """
    <style>
    .header-container {
        background-color: purple; /* Purple background */
        padding: 20px; /* Increased padding */
        border-radius: 15px; /* Rounded corners */
        width: 100%; /* Make the container broader */
        margin-left: 20px; /* Align to left margin */
        margin-bottom: 20px; /* Reduce gap between header and subheader */
    }
    .header-text {
        font-family: Arial, sans-serif;
        color: white; /* White text color */
        margin: 0; /* Remove default margin */
        font-size: 24px; /* Increase font size */
    }
    .subheader-container {
        background-color: purple; /* Purple background */
        padding: 5px; /* Padding around the text */
        border-radius: 10px; /* Rounded corners */
        width: 100%; /* Width of the container */
        margin-left: 20px; /* Align to left margin */
        margin-top: -10px; /* Reduce gap between header and subheader */
    }
    .subheader-text {
        font-family: Arial, sans-serif;
        color: white; /* White text color */
        font-size: 24px; /* Font size */
        margin: 0; /* Remove default margin */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the header with custom styling
st.markdown('<div class="header-container"><p class="header-text">Phone Pe Pulse| The Beat of Progress</p></div>', unsafe_allow_html=True)

# Display the subheader with custom styling
st.markdown('<div class="subheader-container"><p class="subheader-text">India</p></div>', unsafe_allow_html=True)
# Custom CSS for table
custom_css = """
<style>
    .row0 { /* Table header row */
        font-family: Arial, sans-serif; /* Font family */
        color: blue; /* Text color */
    }
    .row1, .row2 { /* Alternate rows */
        font-family: Arial, sans-serif; /* Font family */
        color: green; /* Text color */
    }
</style>
"""

with st.container(height=1000,border=True):
     st.image('D:/phonepe/pp2.jpg',caption='Phone Pe,One App For All Your Needs')
     



col_drop,col_map=st.columns(2)
with col_drop:
           

        option1 = st.selectbox('Type',('Transactions','User'))
        
        option2=st.selectbox('Quarter',('1','2','3','4'))
        option3=st.selectbox('Year',('2018','2019','2020','2021','2022','2023'))
        if option1=='Transactions':
            query=f"select format(sum(transacion_count),0) as `All Phone Pe Transactions` from ppproj.agg_trans where Quarter='{option2}' and Year='{option3}';"
            query1=f"select concat('₹',format(sum(transacion_amount),0)) as `Total payment value` from ppproj.agg_trans where Quarter='{option2}'and Year='{option3}';"
            query2=f"select concat('₹',format(sum(transacion_amount)/sum(transacion_count),0)) as `Average transaction value` from ppproj.agg_trans where Quarter='{option2}' and Year='{option3}';"
            cursor = db_connection.cursor()
            cursor1= db_connection.cursor()
            cursor2=db_connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor1.execute(query1)
            data1=cursor1.fetchall()
            cursor2.execute(query2)
            data2=cursor2.fetchall()
            columns = [i[0] for i in cursor.description]
            columns1 = [i[0] for i in cursor1.description]
            columns2 = [i[0] for i in cursor2.description]
        # Convert data to DataFrame
    
            df = pd.DataFrame(data, columns=columns)
            
            df1=pd.DataFrame(data1,columns=columns1)
            df2=pd.DataFrame(data2,columns=columns2)
           
    # Display the data
            st.write("<span style='color: purple; font-size: 24px;'>All Phone Pe Transactions:   </span><br>", 
              f"<span style='color: blue; font-size: 24px;'>{df['All Phone Pe Transactions'].iloc[0]}</span>", 
             unsafe_allow_html=True)
            st.write("<span style='color: purple; font-size: 24px;'>Total payment value:   </span><br>", 
              f"<span style='color: green; font-size: 24px;'>{df1['Total payment value'].iloc[0]}</span>", 
             unsafe_allow_html=True)
            st.write("<span style='color: purple; font-size: 24px;'>Average transaction value:   </span><br>", 
              f"<span style='color: green; font-size: 24px;'>{df2['Average transaction value'].iloc[0]}</span>", 
              unsafe_allow_html=True)
           
            
        elif option1=='User':
            print("user inside")
            queryu1=f"select sum(regusers) as `Registered Users` from ppproj.map_user where Quarter='{option2}' and Year='{option3}';"
            queryu2=f"select sum(appopens) as `Phone Pe App opens` from ppproj.map_user where Quarter='{option2}' and Year='{option3}';"
            cursoru1=db_connection.cursor()
            cursoru2=db_connection.cursor()
            cursoru1.execute(queryu1)
            datau1=cursoru1.fetchall()
            cursoru2.execute(queryu2)
            datau2=cursoru2.fetchall()
            columnsu1=[i[0] for i in cursoru1.description]
            columnsu2=[i[0] for i in cursoru2.description]
            df_u1=pd.DataFrame(datau1,columns=columnsu1)
            df_u2=pd.DataFrame(datau2,columns=columnsu2)
            
            st.write("<span style='color: purple; font-size: 24px;'>Registered Users:   </span><br>", 
              f"<span style='color: blue; font-size: 24px;'>{df_u1['Registered Users'].iloc[0]}</span>", 
             unsafe_allow_html=True)
            
            st.write("<span style='color: purple; font-size: 24px;'>Phone Pe App opens:   </span><br>", 
              f"<span style='color: green; font-size: 24px;'>{df_u2['Phone Pe App opens'].iloc[0]}</span>", 
             unsafe_allow_html=True)


             
     
with col_map:
            if option1=='Transactions':
        
                query="select State, sum(Transacion_amount) as total from ppproj.agg_trans group by State;"
                df=execute_query(query)

                fig = go.Figure(data=go.Choropleth(

                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locationmode='geojson-id',
                locations=df["State"],
                z=df["total"],
                autocolorscale=False,
                colorscale='Blues',
                marker_line_color='peachpuff',
                colorbar=dict(
                title={'text': "total"},

                thickness=15,
                len=0.35,
                bgcolor='rgba(255,255,255,0.6)',

                tick0=0,
                dtick=20000,

                xanchor='left',
                x=0.01,
                yanchor='bottom',
                y=0.05
                )
                 ))
                fig.update_geos(
                visible=False,
                projection=dict(
                type='conic conformal',
                parallels=[12.472944444, 35.172805555556],
                rotation={'lat': 24, 'lon': 80}
                 ),
                lonaxis={'range': [68, 98]},
                lataxis={'range': [6, 38]}
                )
                fig.update_layout(
                title=dict(
                text="Phone Pe Total transaction since 2018",
                xanchor='center',
                x=0.5,
                yref='paper',
                yanchor='bottom',
                y=1,
                pad={'b': 10}
                 ),
                margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
                height=550,
                width=550
                )
    # Display the choropleth map
                st.plotly_chart(fig)

            if option1=='User':
        
                query="select State,sum(regusers)as Users from ppproj.map_user group by State;"
                df=execute_query(query)

                fig = go.Figure(data=go.Choropleth(

                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locationmode='geojson-id',
                locations=df["State"],
                z=df["Users"],
                autocolorscale=False,
                colorscale='mint',
                marker_line_color='peachpuff',
                colorbar=dict(
                title={'text': "total"},

                thickness=15,
                len=0.35,
                bgcolor='rgba(255,255,255,0.6)',

                tick0=0,
                dtick=20000,

                xanchor='left',
                x=0.01,
                yanchor='bottom',
                y=0.05
                )
                 ))
                fig.update_geos(
                visible=False,
                projection=dict(
                type='conic conformal',
                parallels=[12.472944444, 35.172805555556],
                rotation={'lat': 24, 'lon': 80}
                 ),
                lonaxis={'range': [68, 98]},
                lataxis={'range': [6, 38]}
                )
                fig.update_layout(
                title=dict(
                text="Phone Pe Total Users since 2018",
                xanchor='center',
                x=0.5,
                yref='paper',
                yanchor='bottom',
                y=1,
                pad={'b': 10}
                 ),
                margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
                height=550,
                width=550
                )
    # Display the choropleth map
                st.plotly_chart(fig)    

col_group,col_tops=st.columns(2)
with col_group:
    st.write("Categories")
    if option1=='Transactions':
            query3=f"select Transacion_type as `Category`,sum(transacion_count) as `Transaction` from ppproj.agg_trans where Quarter='{option2}' and Year='{option3}' group by Transacion_type;"
            cursor3=db_connection.cursor()
            cursor3.execute(query3)
            data3 = cursor3.fetchall()
            columns3 = [i[0] for i in cursor3.description]
            df3 = pd.DataFrame(data3, columns=columns3)
            st.write(df3)

    elif option1=='User':
            st.image('D:/phonepe/pp.jpg',caption='Phone Pe,Connecting People')
with col_tops:
        tab1,tab2,tab3=st.tabs(["States","Districts","Postal Codes"])
        with tab1:
            if option1=='Transactions':
                query4=f"select State,sum(Transacion_count) as `Transaction`  from ppproj.agg_trans where Quarter='{option2}' and Year='{option3}' group by State order by sum(Transacion_count) desc limit 10;"
                cursor4 = db_connection.cursor()
                cursor4.execute(query4)
                data4 = cursor4.fetchall()
                columns4 = [i[0] for i in cursor4.description]
                df4 = pd.DataFrame(data4, columns=columns4)
                st.write(df4)
            elif option1=='User':
                queryt1=f"select State,sum(regusers) as `Registered Users` from ppproj.map_user where Quarter='{option2}' and Year='{option3}' group by State order by sum(regusers) desc limit 10;"
                cursort1 = db_connection.cursor()
                cursort1.execute(queryt1)
                datat1 = cursort1.fetchall()
                columnst1 = [i[0] for i in cursort1.description]
                df_t1 = pd.DataFrame(datat1, columns=columnst1)
                st.write(df_t1)
                 
            
        with tab2:
            if option1=='Transactions':    
                query5=f"select dtname as `District`, sum(dtcount) as `Transaction` from ppproj.top_dtpintrans where Quarter='{option2}' and Year='{option3}' group by dtname order by sum(dtcount) desc limit 10;"
                cursor5= db_connection.cursor()
                cursor5.execute(query5)
                data5=cursor5.fetchall()
                columns5 = [i[0] for i in cursor5.description]
                df5=pd.DataFrame(data5,columns=columns5)
                st.write(df5)
            elif option1=='User':
                queryt2=f"select dtname as `District`,sum(regusers) as `Registered Users` from ppproj.top_dtpinuser where Quarter='{option2}' and Year='{option3}' group by dtname order by sum(regusers) desc limit 10;"
                cursort2 = db_connection.cursor()
                cursort2.execute(queryt2)
                datat2 = cursort2.fetchall()
                columnst2 = [i[0] for i in cursort2.description]
                df_t2 = pd.DataFrame(datat2, columns=columnst2)
                st.write(df_t2)
        with tab3:
            if option1=='Transactions':
                query6=f"select pincodes,sum(pincount) as `Transaction`  from ppproj.top_dtpintrans where Quarter='{option2}' and Year='{option3}' group by pincodes order by sum(pincount) desc limit 10;"
                cursor6=db_connection.cursor()    
                cursor6.execute(query6)
                data6=cursor6.fetchall()           
                columns6 = [i[0] for i in cursor6.description]
                df6=pd.DataFrame(data6,columns=columns6)
                st.write(df6)
            elif option1=='User':
                queryt3=f"select pincodes as `Pincode`,sum(pincode_regusers) as `Registered Users` from ppproj.top_dtpinuser where Quarter='{option2}' and Year='{option3}' group by pincodes order by sum(pincode_regusers) desc limit 10;"
                cursort3 = db_connection.cursor()
                cursort3.execute(queryt3)
                datat3 = cursort3.fetchall()
                columnst3 = [i[0] for i in cursort3.description]
                df_t3 = pd.DataFrame(datat3, columns=columnst3)
                st.write(df_t3)
st.header(" PHONE PE PULSE - REVELATIONS | INSIGHTS ")
col_plot1,col_plot2=st.columns(2)
with col_plot1:
    option_plot1=st.selectbox('Clarity on Phone Pe Pulse',
    ('Leading States - Total Transactions since 2018',
     'Categories Distribution On Count'))
    if option_plot1=='Leading States - Total Transactions since 2018':
        query_p1=f"select State, sum(Transacion_amount) as `Transaction` from ppproj.agg_trans group by State order by sum(Transacion_amount) desc limit 10;"
        cursor_p1 = db_connection.cursor()
        cursor_p1.execute(query_p1)
        data_p1 = cursor_p1.fetchall()
        columns_p1 = [i[0] for i in cursor_p1.description]
        df_p1 = pd.DataFrame(data_p1, columns=columns_p1)
        fig=px.bar(df_p1,x='State',y='Transaction',title='Bar Plot on Total Transaction Vs States',labels={'x':'State','y':'Total Transaction'})
        st.write(fig)
    if option_plot1=='Categories Distribution On Count':
        query_p2=f"select Transacion_type,sum(Transacion_count) as Count from ppproj.agg_trans group by Transacion_type;"
        cursor_p2 = db_connection.cursor()
        cursor_p2.execute(query_p2)
        data_p2 = cursor_p2.fetchall()
        columns_p2 = [i[0] for i in cursor_p2.description]
        df_p2 = pd.DataFrame(data_p2, columns=columns_p2)
        fig=px.pie(df_p2,names='Transacion_type',values='Count',title='Pie Chart on Category types Vs Count')
        # Apply styling to the plot
        fig.update_layout(
        title={'text': 'Pie Chart on Category types Vs Count', 'x': 0.5},  # Center the title
        paper_bgcolor='#f0f0f0',  # Background color
        plot_bgcolor='#f0f0f0',  # Plot area background color
        font_color='black',  # Font color
        font_family='Arial',  # Font family
        margin=dict(t=50, b=50, l=50, r=50),  # Margin around the plot
        showlegend=True,  # Show legend
        legend=dict(
            bgcolor='#f0f0f0',  # Legend background color
            bordercolor='black',  # Legend border color
            borderwidth=1,  # Legend border width
            font=dict(color='black'),  # Legend font color
         ),
         )
        st.plotly_chart(fig)
with col_plot2:
    option_plot2=st.selectbox('Clarity on Phone Pe Pulse',
    ('Leading Brands-Registered in India',
     'Growth Trend-Phone Pe'))
    if option_plot2=='Leading Brands-Registered in India':
        query_p3=f"select brand as `Brand`, sum(count) as count from ppproj.agg_user group by brand order by sum(count) desc limit 10 ;"
        cursor_p3 = db_connection.cursor()
        cursor_p3.execute(query_p3)
        data_p3 = cursor_p3.fetchall()
        columns_p3 = [i[0] for i in cursor_p3.description]
        df_p3 = pd.DataFrame(data_p3, columns=columns_p3)
        # Create a Donut pie chart using Plotly Graph Objects
        fig = go.Figure(data=[go.Pie(labels=df_p3['Brand'], values=df_p3['count'], hole=0.4)])
       
        fig.update_layout(
        title={'text': 'Donut Chart on Brands Vs Count', 'x': 0.5},  # Center the title
        paper_bgcolor='#f0f0f0',  # Background color
        plot_bgcolor='#f0f0f0',  # Plot area background color
        font_color='black',  # Font color
        font_family='Arial',  # Font family
        margin=dict(t=50, b=50, l=50, r=50),  # Margin around the plot
        showlegend=True,  # Show legend
        legend=dict(
            bgcolor='#f0f0f0',  # Legend background color
            bordercolor='black',  # Legend border color
            borderwidth=1,  # Legend border width
            font=dict(color='black'),  # Legend font color
         ),
         )
        st.plotly_chart(fig)
    if option_plot2=='Growth Trend-Phone Pe':
        query_l1=f"select sum(Transacion_count) as `Transaction`,Year from ppproj.agg_trans group by Year ;"
        cursor_l1= db_connection.cursor()
        cursor_l1.execute(query_l1)
        data_l1 = cursor_l1.fetchall()
        columns_l1 = [i[0] for i in cursor_l1.description]
        df_l1 = pd.DataFrame(data_l1, columns=columns_l1)
        fig = px.line(df_l1, x='Year', y='Transaction', title='Growth Trend - Phone Pe')
        fig.update_layout(
        xaxis_title='Year',  # X-axis title
        yaxis_title='Transaction Count',  # Y-axis title
        plot_bgcolor='pink',  # Plot background color
        paper_bgcolor='lightgreen',  # Paper background color
        font=dict(color='black'),  # Font color
        legend_title='Legend',  # Legend title
        legend=dict(font=dict(size=10)),  # Legend font size
) 
        st.plotly_chart(fig)
         
         
col_plot3,col_plot4=st.columns(2)
with col_plot3:
     option_plot3=st.selectbox('Quarters Vs States-Distribution of Users-',
    ('Quarter 1',
     'Quarter 2',
     'Quarter 3',
     'Quarter 4' ))
     if option_plot3=='Quarter 1':
        query_q1=f"select State,sum(regusers) as `Registered Users` from ppproj.map_user where Quarter='1' group by State; "
        cursor_q1 = db_connection.cursor()
        cursor_q1.execute(query_q1)
        data_q1 = cursor_q1.fetchall()
        columns_q1 = [i[0] for i in cursor_q1.description]
        df_q1 = pd.DataFrame(data_q1, columns=columns_q1)
        # Create a Plotly Express scatter plot
        fig = px.scatter(df_q1, x='State', y='Registered Users', title="Scatter Plot of Registered Users Vs State")
        # Display the Plotly figure using st.plotly_chart
        fig.update_layout(
        xaxis_title="State",
        yaxis_title="Registered Users",
        title="Registered Users- Trend in Quarter 1 of the Years",
        plot_bgcolor="purple",  # Background color of the plot area
        font=dict(family="Arial", size=12, color="black"),  # Font style
        legend=dict(
            bgcolor="#f0f0f0",  # Background color of the legend
            bordercolor="black",  # Border color of the legend
            borderwidth=1,  # Border width of the legend
            font=dict(color="purple")  # Font color of the legend
        )
         )
        st.plotly_chart(fig)
     if option_plot3=='Quarter 2':
        query_q2=f"select State,sum(regusers) from ppproj.map_user where Quarter='2' group by State; "
        cursor_q2 = db_connection.cursor()
        cursor_q2.execute(query_q2)
        data_q2 = cursor_q2.fetchall()
        columns_q2 = [i[0] for i in cursor_q2.description]
        df_q2 = pd.DataFrame(data_q2, columns=columns_q2)
        # Create a Plotly Express scatter plot
        fig = px.scatter(df_q2, x='State', y='sum(regusers)', title="Scatter Plot")
        # Display the Plotly figure using st.plotly_chart
        fig.update_layout(
        xaxis_title="State",
        yaxis_title="Sum of Registered Users",
        title="Registered Users- Trend in Quarter 2 of the Years",
        plot_bgcolor="blue",  # Background color of the plot area
        font=dict(family="Arial", size=12, color="black"),  # Font style
        legend=dict(
            bgcolor="#f0f0f0",  # Background color of the legend
            bordercolor="black",  # Border color of the legend
            borderwidth=1,  # Border width of the legend
            font=dict(color="purple")  # Font color of the legend
        )
         )
        st.plotly_chart(fig)
     if option_plot3=='Quarter 3':
        query_q3=f"select State,sum(regusers) from ppproj.map_user where Quarter='3' group by State; "
        cursor_q3 = db_connection.cursor()
        cursor_q3.execute(query_q3)
        data_q3 = cursor_q3.fetchall()
        columns_q3 = [i[0] for i in cursor_q3.description]
        df_q3 = pd.DataFrame(data_q3, columns=columns_q3)
        # Create a Plotly Express scatter plot
        fig = px.scatter(df_q3, x='State', y='sum(regusers)', title="Scatter Plot")
        # Display the Plotly figure using st.plotly_chart
        fig.update_layout(
        xaxis_title="State",
        yaxis_title="Sum of Registered Users",
        title="Registered Users- Trend in Quarter 3 of the Years",
        plot_bgcolor="green",  # Background color of the plot area
        font=dict(family="Arial", size=12, color="black"),  # Font style
        legend=dict(
            bgcolor="#f0f0f0",  # Background color of the legend
            bordercolor="black",  # Border color of the legend
            borderwidth=1,  # Border width of the legend
            font=dict(color="purple")  # Font color of the legend
        )
         )
        st.plotly_chart(fig)
     if option_plot3=='Quarter 4':
        query_q4=f"select State,sum(regusers) from ppproj.map_user where Quarter='4' group by State; "
        cursor_q4 = db_connection.cursor()
        cursor_q4.execute(query_q4)
        data_q4 = cursor_q4.fetchall()
        columns_q4 = [i[0] for i in cursor_q4.description]
        df_q4 = pd.DataFrame(data_q4, columns=columns_q4)
        # Create a Plotly Express scatter plot
        fig = px.scatter(df_q4, x='State', y='sum(regusers)', title="Scatter Plot")
        # Display the Plotly figure using st.plotly_chart
        fig.update_layout(
        xaxis_title="State",
        yaxis_title="Sum of Registered Users",
        title="Registered Users- Trend in Quarter 4 of the Years",
        plot_bgcolor="green",  # Background color of the plot area
        font=dict(family="Arial", size=12, color="black"),  # Font style
        legend=dict(
            bgcolor="#f0f0f0",  # Background color of the legend
            bordercolor="black",  # Border color of the legend
            borderwidth=1,  # Border width of the legend
            font=dict(color="purple")  # Font color of the legend
        )
         )
        st.plotly_chart(fig)
with col_plot4:
     option_plot4=st.selectbox('Brand Interest of Users',
    ('Impact Of Brand On States',
     'Leading Districts of the states' ))
     if option_plot4=='Impact Of Brand On States':
        query_b=f"SELECT State, brand, count AS highest_user_count FROM (SELECT State, brand, count,DENSE_RANK() OVER (PARTITION BY State ORDER BY count DESC) AS rn FROM ppproj.agg_user) as ranked where rn=1;"
        cursor_b = db_connection.cursor()
        cursor_b.execute(query_b)
        data_b = cursor_b.fetchall()
        columns_b = [i[0] for i in cursor_b.description]
        df_b = pd.DataFrame(data_b, columns=columns_b)
        fig = px.scatter(df_b, x='State', y='brand', size='highest_user_count', title='Bubble Plot On Brand Interest',
                 size_max=30)

        fig.update_layout(xaxis_title='State',
                  yaxis_title='brand',
                  legend_title='Color',  # Legend title for the color variable
                  legend=dict(title='Color', # Legend title for the color variable
                              font=dict(size=10)),  # Font size of the legend
                  plot_bgcolor='lightblue',  # Plot background color
                  paper_bgcolor='lightgray')  # Paper background color
        st.plotly_chart(fig)
     if option_plot4=='Leading Districts of the states':
        query_d1=f"select State,dtname as `District`, sum(dtcount) as`Count` from ppproj.top_dtpintrans group by State,dtname order by sum(dtcount) desc limit 10 ;"
        cursor_d1 = db_connection.cursor()
        cursor_d1.execute(query_d1)
        data_d1 = cursor_d1.fetchall()
        columns_d1 = [i[0] for i in cursor_d1.description]
        df_d1 = pd.DataFrame(data_d1, columns=columns_d1)
        fig = px.bar(df_d1, x='Count', y='State', color='District', orientation='h', 
             title='Top 10 Districts in States')
        fig.update_layout(
        xaxis_title='Total count',  # X-axis title
        yaxis_title='State',  # Y-axis title
        legend_title='Category',  # Legend title
        legend=dict(font=dict(size=10)),  # Legend font size
        plot_bgcolor='red',  # Plot background color
        paper_bgcolor='yellow',  # Paper background color
        font=dict(color='purple')  # Font color
         )
        st.plotly_chart(fig)
          
          
     
          
          
     


          
       



         

            
      
    
                             

      