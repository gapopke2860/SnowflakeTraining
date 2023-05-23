import streamlit as st
import pandas as pd
import snowflake.connector as sf

class CarDiner:
    def __init__(self):
        self.current_position = 0
        self.rows_per_page = 10
        self.con = sf.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        self.container = st.empty()

    def fetch_next_rows(self):
        self.current_position += self.rows_per_page
        query = f"SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET LIMIT {self.rows_per_page} OFFSET {self.current_position}"
        df = pd.read_sql_query(query, self.con)
        return df

    def fetch_previous_rows(self):
        self.current_position -= self.rows_per_page
        if self.current_position < 0:
            self.current_position = 0
        query = f"SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET LIMIT {self.rows_per_page} OFFSET {self.current_position}"
        df = pd.read_sql_query(query, self.con)
        return df

    def run(self):
        st.title('My Parents New Healthy Diner')

        st.header('Car Filter Menu')

        # Fetch the initial data, limiting to 50 rows
        query = "SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET LIMIT 50"
        df = pd.read_sql_query(query, self.con)

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

        # Display the number of cars in the current selection
        st.text(f"Number of cars in the selection: {len(df_filtered)}")

        # Display the filtered DataFrame, limited to the specified number of rows per page
        self.container.dataframe(df_filtered.head(self.rows_per_page))

        # Next Page Button
        if st.button("Next Page"):
            df = self.fetch_next_rows()
            self.container.empty()
            self.container.dataframe(df.head(self.rows_per_page))

        # Previous Page Button
        if st.button("Previous Page"):
            df = self.fetch_previous_rows()
            self.container.empty()
            self.container.dataframe(df.head(self.rows_per_page))

if __name__ == "__main__":
    car_diner = CarDiner()
    car_diner.run()
