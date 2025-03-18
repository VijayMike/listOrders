import streamlit as st
import requests
import pandas as pd

PRODUCTS_API_URL = "http://127.0.0.1:8000/products/"
ORDERS_API_URL = "http://127.0.0.1:8000/orders/"

st.set_page_config(page_title="📦 Order Management", layout="wide")

st.title("📦 Order Management System")

@st.cache_data
def fetch_orders():
    response = requests.get(ORDERS_API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Failed to load orders.")
        return pd.DataFrame()

orders_df = fetch_orders()

status_filter = st.selectbox("Filter by Order Status", ["All", "Pending", "Shipped", "Delivered"])
if status_filter != "All":
    orders_df = orders_df[orders_df["status"] == status_filter]

st.write("### 📝 Orders List")
st.dataframe(orders_df, use_container_width=True)

if st.button("Sort by Quantity 📊"):
    orders_df = orders_df.sort_values(by="quantity", ascending=False)
    st.dataframe(orders_df, use_container_width=True)
