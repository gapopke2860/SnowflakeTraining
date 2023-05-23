import streamlit as st
import pandas as pd
import snowflake.connector as sf

con = sf.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
)

st.title('My Parents New Healthy Diner')

st.header('Car Filter Menu')

query = "SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET LIMIT 50"
df = pd.read_sql_query(query, con)

# Let user define filtering conditions
price_range = st.slider("Price range", float(df["PRICE"].min()), float(df["PRICE"].max()), (float(df["PRICE"].min()), float(df["PRICE"].max())))
mpg_range = st.slider("MPG range", float(df["MPG"].min()), float(df["MPG"].max()), (float(df["MPG"].min()), float(df["MPG"].max())))
transmission = st.selectbox("Transmission type", df["TRANSMISSION"].unique())
fuel_type = st.selectbox("Fuel type", df["FUEL_TYPE"].unique())

# Filter data based on user's conditions
df_filtered = df[(df["PRICE"].between(*price_range)) & 
                 (df["MPG"].between(*mpg_range)) & 
                 (df["TRANSMISSION"] == transmission) &
                 (df["FUEL_TYPE"] == fuel_type)]

# Display the filtered DataFrame
st.dataframe(df_filtered)

st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

#fruityvice api section
st.header('Fruityvice Fruit Advice!')
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#normalize json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

st.dataframe(fruityvice_normalized)
