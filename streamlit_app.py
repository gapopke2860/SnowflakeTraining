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

st.header('Breakfast Menu')

query = "SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET LIMIT 50"
df = pd.read_sql_query(query, con)

# Let user select columns
features = df.columns.tolist()
features_selected = st.multiselect("Select car features: ", features, default=features)

# Filter dataframe based on selected columns
df_filtered = df[features_selected]

# Display the DataFrame in the Streamlit app
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
