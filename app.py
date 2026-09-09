import streamlit as st
import mysql.connector as MyS
import pandas as pd

Pass = input("Enter your MYSQL password:")

conn = MyS.connect(
    host="localhost",
    user="root",
    password=Pass,
    database="car_dealership"
)

cursor = conn.cursor()

page = st.sidebar.selectbox(
    "Choose an option",
    ["View Cars", "Add Car", "Delete Car"]
)

if page == "View Cars":
    cursor.execute("SELECT * FROM cars")
    data = cursor.fetchall()

    # Get column names from the table
    columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=columns)
    st.title("Car Dealership")
    st.dataframe(df, use_container_width=True)



elif page == "Add Car":
    #Adding car
    st.header("Add Car")

    car_id = st.number_input("Car ID", min_value=1, step=1)
    brand = st.text_input("Brand")
    model = st.text_input("Model")
    year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
    color = st.text_input("Colour")
    fuel_type = st.selectbox("Fuel", ["Petrol", "Diesel"])
    trans = st.selectbox("Transmission",["Manual","Automatic"])
    price = st.number_input("Price", min_value=0, step=1000)
    stock = st.number_input("Stock",min_value=1, step=1)

    if st.button("Add Car"):
        query = """
        INSERT INTO cars
        (car_id, brand, model, year, color, fuel_type, transmission, price, stock)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (car_id, brand, model, year, color, fuel_type, trans, price, stock)
        cursor.execute(query, values)
        conn.commit()

        st.success("Car added successfully!")
        st.rerun()
elif page == "Delete Car":
    #Deleting car
    st.header("Delete Car")

    delete_id = st.number_input(
        "Enter Car ID to delete",
        min_value=1,
        step=1,
        key="delete"
    )

    if st.button("Delete Car"):

        cursor.execute(
            "SELECT * FROM cars WHERE car_id=%s",
            (delete_id,)
        )

        car = cursor.fetchone()

        if car:
            cursor.execute(
                "DELETE FROM cars WHERE car_id=%s",
                (delete_id,)
            )
            conn.commit()
            st.success("Car deleted.")
            st.rerun()
        else:
            st.error("Car ID not found.")
