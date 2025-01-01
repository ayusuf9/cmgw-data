import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# Set page configuration for a better layout
st.set_page_config(
    page_title="Interactive Data Table",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("📊 Interactive Data Table")
st.markdown("""
    Explore your data with this **interactive and visually stunning table**!  
    Features include sorting, filtering, and editing for an exceptional user experience.
""")

# Load data from a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to proceed.")
    st.stop()

# Configure Ag-Grid options for a stunning layout
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(enabled=True, paginationPageSize=10)  # Enable pagination
gb.configure_selection("multiple", use_checkbox=True)  # Multi-row selection with checkboxes
gb.configure_default_column(
    editable=True,  # Allow editing
    filterable=True,  # Enable filtering
    sortable=True,  # Enable sorting
    resizable=True,  # Allow column resizing
    flex=1,  # Flexible column width
    minWidth=100,  # Minimum column width
)
gb.configure_side_bar()  # Add a side bar for filters and columns
grid_options = gb.build()

# Display the Ag-Grid table
st.subheader("Interactive Table")
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    height=400,
    width="100%",
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,  # Return filtered and sorted data
    update_mode=GridUpdateMode.MODEL_CHANGED,  # Update on changes
    fit_columns_on_grid_load=True,  # Fit columns to grid width
    theme="streamlit",  # Use the Streamlit theme (or try "alpine", "balham", etc.)
)

# Display selected rows
st.subheader("Selected Rows")
selected_rows = grid_response["selected_rows"]
if selected_rows:
    st.write(pd.DataFrame(selected_rows))
else:
    st.info("No rows selected. Use the checkboxes to select rows.")

# Add some styling for a polished look
st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stDataFrame {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stAgGrid {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)