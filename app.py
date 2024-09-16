import streamlit as st
from sql import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title('Flight Analysis')

user_option = st.sidebar.selectbox('Menu',['Select One','Check flights','Analytics'])

if user_option == "Check flights":
    st.title("Check flights")
    col1,col2 = st.columns(2)

    city = db.fetch_city_names()
    with col1:
        Origin = st.selectbox("Origin",sorted(city))
    with col2:
        Destination = st.selectbox("Destination", sorted(city))

    if st.button('Search'):
        results = db.fetch_all_flights(Origin,Destination)
        st.dataframe(results)
elif user_option == 'Analytics':
    st.title("Analytics")

    city,frequency = db.busy_airport()
    fig = go.Figure(
    go.Bar(
        x=city,           # x-axis labels (categories)
        y=frequency,      # y-axis values
        hoverinfo="x+y",  # Show x and y info on hover
        text=frequency,   # Display values on the bars
        textposition='auto'  # Automatically position the text
    ))
    st.header("Bar chart For top 5 busy airport")
    st.plotly_chart(fig)


    airline,count = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Bar(
            x=airline,  # x-axis values (Cities)
            y=count,  # y-axis values (Number of Flights)
            text=count,  # display values on bars
            textposition='auto',  # position text on the bars
        )
    )


    st.header("Bar chart")
    st.plotly_chart(fig)


    airline, num_flights = db.daily_frequency()

    # Create a tree map
    fig = px.pie(
        names=airline,  # Labels for each section of the tree
        values=num_flights,  # Size of each section based on the number of flights
    )

    # Display the tree map in Streamlit
    st.header("Pie Chart for number of flights run by each airline company")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    st.title("project")