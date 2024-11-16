import streamlit as st
import numpy as np
import pandas as pd
from data_upload import (
    knn_model_data, 
    user_item_matrix, 
    updated_products, 
    cosine_similarities_content, 
    Product_names, 
    suggested_products_basedOnTime
)
import sqlalchemy
import os
from datetime import datetime
import base64
import user_management  # To handle user management

# Database connection
DATABASE_URI = 'mysql+pymysql://root:1234@localhost/product_recommendations'
engine = sqlalchemy.create_engine(DATABASE_URI)

# Function to set background image
def set_background_image():
    current_directory = os.path.dirname(__file__)
    background_image_path = os.path.join(current_directory, 'img7.jpg')
    with open(background_image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()


# Function to display the current date and time
def display_current_datetime():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_time = now.strftime("%H:%M:%S")
    st.sidebar.write(f" Date : {formatted_date}")
    st.sidebar.write(f" Time: {formatted_time}")


# Function to handle logout
def logout():
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']
    if 'username' in st.session_state:
        del st.session_state['username']
    st.success("You have successfully logged out.")
    st.write("Redirecting to login page...")

def main(username=None):
    set_background_image() 

     # If the user is logged in, show "Logout" button
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.sidebar.button("Logout", on_click=logout)
        st.sidebar.write(f"Welcome {st.session_state['username']}")
    else:
        # If not logged in, show the "Menu" (login) button
        st.sidebar.button("Menu", on_click=lambda: st.session_state.update(page='login'))
        st.sidebar.write(f"Welcome {username or 'Guest'}")  


    display_current_datetime()

    st.header('Product Recommender System')

    # Seasonal Picks in the sidebar
    st.sidebar.header("🌟 Seasonal Picks")
    if st.sidebar.button('Show Seasonal Picks'):
        st.write("Showing Seasonal Picks")
        
        if not suggested_products_basedOnTime.empty:
            st.subheader("Seasonal Picks")
            cols = st.columns(5)
            for i, row in suggested_products_basedOnTime.iterrows():
                with cols[i % 5]:
                    st.text(row['Name'])
                    st.image(row['ImageURL'], width=120)
                    st.write(f"Category: {row['Category']}")
        else:
            st.write("No seasonal picks available.")
    
    # Load all products from SQL
    all_products_query = "SELECT * FROM all_products"
    all_products = pd.read_sql(all_products_query, con=engine)

    # Display all products
    def display_all_products():
        cols = st.columns(5)
        for i, row in all_products.iterrows():
            image_url = row['ImageURL'] if row['ImageURL'] else placeholder_image_url
            with cols[i % 5]:
                st.text(row['Name'])
                st.markdown(f'''
                    <div class="product-container">
                        <img src="{image_url}" class="product-image">
                        <div class="product-genres">{row["Brand"]}</div>
                        <div class="product-genres">{row["Category"]}</div>
                    </div>
                ''', unsafe_allow_html=True)
                rating = 4  # Example rating (out of 5)
                display_star_rating(rating)
                if st.button(f'Buy', key=f'buy_all_{i}'):
                    st.success(f"You have selected to buy {row['Name']}!")
    
    # Call the function to display all products
    display_all_products()


# Function to redirect to the login page
def redirect_to_login():
    st.session_state['page'] = 'login'  # Set a session state variable to indicate the current page


# Ensure to call main() when running as a standalone
if __name__ == '__main__':
    if 'page' in st.session_state and st.session_state['page'] == 'login':
        import login  # Import your login module
        login.main()  # Call the main function in login.py
    else:
        main()
