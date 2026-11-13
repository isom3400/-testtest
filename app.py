import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration & Title
st.set_page_config(page_title="Simple Data App", layout="centered")
st.title("📊 Interactive Sales Dashboard")
st.write("Adjust the controls in the sidebar to update the chart and data.")

# 2. Sidebar Inputs
st.sidebar.header("Filter Options ################################")
num_days = st.sidebar.slider("Number of days12343", min_value=7, max_value=90, value=30)
category = st.sidebar.selectbox("Product Category", ["Electronics", 
                                                     "Clothing", 
                                                     "Home Goods",
                                                    "Home Goods 2"])

# 3. Generate Sample Data
np.random.seed(42)
dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days)
sales = np.random.randint(100, 500, size=num_days)
df = pd.DataFrame({"Date": dates, "Sales ($)": sales, "Category": category})

st.write(df)


# 4. Display Key Metrics
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${df['Sales ($)'].sum():,}")
col2.metric("Average Daily Sales", f"${df['Sales ($)'].mean():.2f}")

# 5. Interactive Chart & Data Table
st.subheader(f"{category} Sales Trend")
st.line_chart(df.set_index("Date")["Sales ($)"])

if st.checkbox("Show raw data table"):
    st.dataframe(df, use_container_width=True)
  
