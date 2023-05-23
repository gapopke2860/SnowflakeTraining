import streamlit as st
import pandas as pd
import snowflake.connector as sf

# Connect to Snowflake
con = sf.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
)

# Fetch all the data from Snowflake
query = "SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET"
df = pd.read_sql_query(query, con)

# Set the number of cars to display per page
items_per_page = 50

# Get the total number of cars
total_cars = len(df)

# Calculate the total number of pages
total_pages = total_cars // items_per_page + 1

# Get the current page from the user
current_page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

# Calculate the start and end indices for the current page
start_index = (current_page - 1) * items_per_page
end_index = start_index + items_per_page

# Slice the DataFrame to get the cars for the current page
df_page = df.iloc[start_index:end_index]

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

# Get the number of cars to display per page from the user
rows = st.number_input("Number of rows to display", min_value=10, max_value=50, value=10, step=10)

# Display the number of cars in the current selection
st.text(f"Number of cars in the selection: {len(df_filtered)}")

# Display the cars for the current page
with st.beta_expander("Cars"):
    for index, row in df_page.iterrows():
        st.write(f"Car {index}: {row['MAKE']} {row['MODEL']} - Price: ${row['PRICE']}")

# Display pagination controls
if total_pages > 1:
    st.write("Page:", current_page)
    if current_page > 1:
        st.button("Previous")
    if current_page < total_pages:
        st.button("Next")

st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

# Fruityvice API section
st.header('Fruityvice Fruit Advice!')
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Normalize JSON response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

st.dataframe(fruityvice_normalized)
