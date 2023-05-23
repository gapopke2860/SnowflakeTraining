import streamlit as st
import pandas as pd
import snowflake.connector as sf
import itertools

# Define the paginator function
def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items."""
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    items = list(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: f"Page {i+1}"
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    return itertools.islice(enumerate(items), min_index, max_index)

def filters(df):
    # Let user decide whether to apply filtering conditions
    apply_filters = st.checkbox("Apply Filters")

    if apply_filters:
        # Let user define filtering conditions
        with st.expander("Filter conditions", expanded=True):
            price_active = st.checkbox("Price range")
            price_range = st.slider("Price range", float(df["PRICE"].min()), float(df["PRICE"].max()), (float(df["PRICE"].min()), float(df["PRICE"].max())), key="price_range")

            mpg_active = st.checkbox("MPG range")
            mpg_range = st.slider("MPG range", float(df["MPG"].min()), float(df["MPG"].max()), (float(df["MPG"].min()), float(df["MPG"].max())), key="mpg_range")

            transmission_active = st.checkbox("Transmission type")
            transmission = st.selectbox("Transmission type", [""] + df["TRANSMISSION"].unique(), key="transmission")

            fuel_type_active = st.checkbox("Fuel type")
            fuel_type = st.selectbox("Fuel type", [""] + df["FUEL_TYPE"].unique(), key="fuel_type")

        # Filter data based on user's conditions
        df_filtered = df

        if price_active:
            df_filtered = df_filtered[(df_filtered["PRICE"].between(*price_range))]

        if mpg_active:
            df_filtered = df_filtered[(df_filtered["MPG"].between(*mpg_range))]

        if transmission_active:
            df_filtered = df_filtered[(df_filtered["TRANSMISSION"].isin([transmission, ""]))]

        if fuel_type_active:
            df_filtered = df_filtered[(df_filtered["FUEL_TYPE"].isin([fuel_type, ""]))]

        # Display the number of cars in the current selection
        st.text(f"Number of cars in the selection: {len(df_filtered)}")

    else:
        df_filtered = df

    return df_filtered

def select_cars(df):
    st.header("Select Cars")

    selected_cars = []  # Empty list to store selected car records

    # Paginate the filtered DataFrame based on the selected number of rows and page number
    paginated_df = paginator("Page number", df.iterrows(), items_per_page=10)

    for i, row in paginated_df:
        # Add a checkbox for each record
        selected = st.checkbox("", key=f"car_{i}")
        if selected:
            # Add the selected car to the compare cars list
            selected_cars.append(row)

        # Convert the row into a DataFrame and display
        row_df = pd.DataFrame([row])
        st.dataframe(row_df)

    return selected_cars


def compare_cars(selected_cars):
    st.header("Compare Cars")

    if len(selected_cars) > 1 and len(selected_cars) <= 4:
        # Create a DataFrame from the selected cars list
        comparison_df = pd.DataFrame(selected_cars)
        st.subheader("Comparison Result")
        st.dataframe(comparison_df)

    elif len(selected_cars) > 4:
        st.warning("Please select up to 4 cars for comparison.")

def main():
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

    # Fetch all the data, instead of limiting to 50
    query = "SELECT * FROM DEMO_DB.PUBLIC.CARS_DATASET"
    df = pd.read_sql_query(query, con)

    df_filtered = filters(df)

    selected_cars = select_cars(df_filtered)

    compare_cars(selected_cars)

    st.text('🥑🍞 Avocado Toast')

    st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

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


if __name__ == '__main__':
    main()
