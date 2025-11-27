import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------- Sidebar ----------
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Data Management", "Forecasting", "Print Planning", "Distribution","Reports", "Login"]
)

# ---------- Dashboard ----------
if menu == "Dashboard":
    st.set_page_config(page_title="📊 Dashboard", layout="wide")
    st.title("📊 Dashboard")

    # Top output metrics (4 labels)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Forecast Accuracy", "100%", "+4.2%")
    with col2:
        st.metric("Total Stock on Hand", "1.2M units", "+200k")
    with col3:
        st.metric("Pending Distributions", "3", "+1")
    with col4:
        st.metric("SKUs below Safety Stock", "12", "+10")

    st.markdown("---")

    # Data showcase table
    st.subheader("Recent Data Overview")
    data = pd.DataFrame({
        "Date": ["2025-10-25", "2025-10-26", "2025-10-27", "2025-10-28"],
        "Sales (₹)": [32000, 45000, 41000, 37000],
        "Orders": [15, 18, 16, 14],
        "Clients": [10, 12, 11, 9]
    })
    st.dataframe(data, use_container_width=True)

    st.markdown("---")

    # Bottom section: Quick Actions + Recent Activity
    col_left, col_right = st.columns([1, 2])

    # Quick Actions
    with col_left:
        st.subheader("⚙️ Quick Actions")
        st.button("New Forecast")
        st.button("New Print Plan")
        st.button("New Distribution")

    # Recent Activity Logs
    with col_right:
        st.subheader("🕒 Recent Activity")
        logs = [
            "2025-10-28 10:45 – Forecast model updated",
            "2025-10-27 15:12 – Distribution plan finalized",
            "2025-10-27 09:30 – Data upload completed",
            "2025-10-26 18:02 – User admin logged in"
        ]
        for log in logs:
            st.text(log)

# ---------- Other Pages ----------
# -------------------------------------------------------------------------------------------
elif menu == "Data Management":
    st.title("📁 Data Management")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("SKU Master")
        st.text("Upload the master list of all SKUs, including categories, lead times, and lot sizes.")
        
    with col2:
        st.subheader("Historical Sales")
        st.text("Upload historical sales data. A minimum of 36 months is recommended for accurate forecasting.")
        st.file_uploader(
            label="Historical Sales",
            type=["csv"],
            label_visibility="collapsed"
        )

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Open Purchase Orders")
        st.text("Upload details of all open purchase orders that have not yet been delivered.")
        st.file_uploader(
            label="Open Purchase Orders",
            type=["csv"],
            label_visibility="collapsed"
        )
    with col4:
        st.subheader("Inventory and returns")
        st.text("Upload current warehouse stock levels, returns, and sample data.")
        st.file_uploader(
            label="Inventory and returns",
            type=["csv"],
            label_visibility="collapsed"
        )

    st.markdown("---")
    
    
# -------------------------------------------------------------------------------------------------------------------------
elif menu == "Forecasting":
    # Page config
    st.set_page_config(page_title="Demand Forecasting", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sample data - REPLACE THIS WITH YOUR DATAFRAME
    forecast_df = pd.DataFrame({
        'SKU': ['BK-001', 'BK-002', 'BK-003', 'BK-001', 'BK-004'],
        'Product Name': ['The Alchemist', 'Sapiens', 'Atomic Habits', 'The Alchemist', 'New Release 2024'],
        'Region': ['National', 'National', 'North', 'National', 'National'],
        'Forecast Month': ['Aug 2024', 'Aug 2024', 'Aug 2024', 'Sep 2024', 'Sep 2024'],
        'Forecasted Units': [5200, 3400, 1500, 5500, 8000],
        'Model Used': ['Seasonal Regression', 'Weighted Average', 'Linear Regression', 'Seasonal Regression', 'Delphi Method'],
        'Confidence Interval': ['4900-5500', '3100-3700', '1350-1650', '5200-5800', '7000-9000']
    })

    # Initialize session state
    if 'forecast_data' not in st.session_state:
        st.session_state.forecast_data = forecast_df

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown('<div class="main-header">Demand Forecasting</div>', unsafe_allow_html=True)
    with col2:
        if st.button("▶ Generate Forecast", use_container_width=True):
            st.success("Forecast generated successfully!")
    with col3:
        if st.button("⬇ Export", use_container_width=True):
            st.info("Export functionality")

    # Main layout
    left_col, right_col = st.columns([1, 2])

    # Left column - Forecast Settings
    with left_col:
        st.markdown('<div class="section-header">Forecast Settings</div>', unsafe_allow_html=True)
    
        st.markdown("**Forecast Period**")
        forecast_period = st.text_input("", value="2024-08", label_visibility="collapsed")
    
        st.markdown("**Model Selection**")
        model_selection = st.selectbox(
            "",
            ["Auto-Select Best Model", "Seasonal Regression", "Weighted Average", "Linear Regression", "Delphi Method"],
            label_visibility="collapsed"
        )
    
        apply_growth_cap = st.checkbox("Apply ±5-6% Growth Cap", value=True)

        st.markdown("---")
    
        st.markdown('<div class="section-header">Sales History</div>', unsafe_allow_html=True)
        st.markdown("*Editable past sales data.*")
        st.info("Sales history table placeholder. This would be an editable grid.")

    # Right column - Forecast Results
    with right_col:
        st.markdown('<div class="section-header">Forecast Results</div>', unsafe_allow_html=True)
        st.markdown("View, edit, and analyze the generated forecast data.")
    
        # Export options
        col_export1, col_export2 = st.columns([1, 1])
        with col_export2:
            if st.button("📋 Export (CSV, Excel, PDF)", use_container_width=True):
                csv = st.session_state.forecast_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="forecast_results.csv",
                    mime="text/csv"
                )
    
        # Display forecast table with editable cells
        st.markdown("### Forecast Data")
    
        # Create editable dataframe
        edited_df = st.data_editor(
            st.session_state.forecast_data,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "SKU": st.column_config.TextColumn("SKU", width="small"),
                "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
                "Region": st.column_config.TextColumn("Region", width="small"),
                "Forecast Month": st.column_config.TextColumn("Forecast Month", width="small"),
                "Forecasted Units": st.column_config.NumberColumn(
                    "Forecasted Units",
                    width="small",
                    format="%d"
                ),
                "Model Used": st.column_config.TextColumn("Model Used", width="medium"),
                "Confidence Interval": st.column_config.TextColumn("Confidence Interval", width="medium")
            },
            hide_index=True
        )
    
        # Summary statistics
        st.markdown("### Summary Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Forecasted Units", f"{edited_df['Forecasted Units'].sum():,}")
        with col2:
            st.metric("Average Forecast", f"{edited_df['Forecasted Units'].mean():.0f}")
        with col3:
            st.metric("Total Products", len(edited_df))

    st.subheader("Forecast Visualization")
    st.line_chart(
        data=edited_df,
        x_label="months",
        y_label="integers"
    )

    # Update session state if data was edited
    st.session_state.forecast_data = edited_df
    
# -------------------------------------------------------------------------------------------------------------------------
elif menu == "Print Planning":
    # Page config
    st.set_page_config(page_title="Print Planning", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 0.5rem;
        }
        .section-subtitle {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }   
        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sample data - REPLACE THIS WITH YOUR DATAFRAME
    print_plan_df = pd.DataFrame({
        'SKU': ['BK-001', 'BK-002', 'BK-003', 'BK-005'],
        'Product Name': ['The Alchemist', 'Sapiens', 'Atomic Habits', 'Regional Title A'],
        'Opening Stock': [8000, 7000, 2000, 500],
        'Stock Coverage': ['1.5 months', '2.1 months', '1.3 months', '0.8 months'],
        'Recommended Print Qty': [5000, 0, 2000, 1000],
        'Final Print Lot': [5000, 0, 2000, 1000],
        'Reason': ['Below 2-month coverage', 'Sufficient stock', 'Below 2-month coverage', 'Below 2-month coverage & MOQ']
    })

    # Initialize session state
    if 'print_plan_data' not in st.session_state:
        st.session_state.print_plan_data = print_plan_df
    if 'opening_stock' not in st.session_state:
        st.session_state.opening_stock = 50000
    if 'safety_stock' not in st.session_state:
        st.session_state.safety_stock = 2
    if 'use_rolling_forecast' not in st.session_state:
        st.session_state.use_rolling_forecast = True
    if 'round_lots' not in st.session_state:
        st.session_state.round_lots = True

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown('<div class="main-header">Print Planning</div>', unsafe_allow_html=True)
    with col2:
        if st.button("▶ Calculate Print Plan", use_container_width=True):
            st.success("Print plan calculated successfully!")
    with col3:
        if st.button("⬇ Export Plan", use_container_width=True):
            st.info("Export functionality")

    # Main layout
    left_col, right_col = st.columns([1, 2])

    # Left column - Planning Inputs
    with left_col:
        st.markdown('<div class="section-header">Planning Inputs</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Configure the parameters for the print plan calculation.</div>', unsafe_allow_html=True)
    
        st.markdown("**Opening Stock (Units)**")
        opening_stock = st.number_input(
            "",
            value=st.session_state.opening_stock,
            step=1000,
            placeholder="e.g., 50000",
            label_visibility="collapsed",
            key="opening_stock_input"
        )
        st.session_state.opening_stock = opening_stock
    
        st.markdown("**Safety Stock (Months)**")
        safety_stock = st.number_input(
            "",
            value=st.session_state.safety_stock,
            step=1,
            min_value=1,
            label_visibility="collapsed",
            key="safety_stock_input"
        )
        st.session_state.safety_stock = safety_stock
    
        st.markdown("")
    
        use_rolling = st.checkbox("Use 14-Month Rolling Forecast", value=st.session_state.use_rolling_forecast)
        st.session_state.use_rolling_forecast = use_rolling
    
        round_lots = st.checkbox("Round Lots to nearest 1000", value=st.session_state.round_lots)
        st.session_state.round_lots = round_lots

    # Right column - Print Plan Results
    with right_col:
        st.markdown('<div class="section-header">Print Plan Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Review the recommended print quantities.</div>', unsafe_allow_html=True)
    
        # Export options
        col_export1, col_export2 = st.columns([4, 1])
        with col_export2:
            if st.button("📋 Export Plan", use_container_width=True):
                csv = st.session_state.print_plan_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="print_plan_results.csv",
                    mime="text/csv"
                )
    
        # Display print plan table
        st.markdown("### Print Plan Data")
    
        # Function to apply styling to reason column
        def style_reason(val):
            if 'Sufficient' in str(val):
                return 'background-color: #e3f2fd; color: #0066cc; border-radius: 15px; padding: 5px 10px;'
            else:
                return 'background-color: #bbdefb; color: #0066cc; border-radius: 15px; padding: 5px 10px;'
    
        # Create editable dataframe
        edited_df = st.data_editor(
            st.session_state.print_plan_data,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "SKU": st.column_config.TextColumn("SKU", width="small"),
                "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
                "Opening Stock": st.column_config.NumberColumn(
                    "Opening Stock",
                    width="small",
                    format="%d"
                ),
                "Stock Coverage": st.column_config.TextColumn("Stock Coverage", width="small"),
                "Recommended Print Qty": st.column_config.NumberColumn(
                    "Recommended Print Qty",
                    width="medium",
                    format="%d"
                ),
                "Final Print Lot": st.column_config.NumberColumn(
                    "Final Print Lot",
                    width="small",
                    format="%d"
                ),
                "Reason": st.column_config.TextColumn("Reason", width="large")
            },
            hide_index=True
        )
    
        # Update session state if data was edited
        st.session_state.print_plan_data = edited_df
    
        # Summary statistics
        st.markdown("### Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Print Qty", f"{edited_df['Recommended Print Qty'].sum():,}")
        with col2:
            st.metric("Total Products", len(edited_df))
        with col3:
            items_to_print = len(edited_df[edited_df['Recommended Print Qty'] > 0])
            st.metric("Items to Print", items_to_print)
        with col4:
            avg_print = edited_df[edited_df['Recommended Print Qty'] > 0]['Recommended Print Qty'].mean()
            st.metric("Avg Print Qty", f"{avg_print:,.0f}" if not pd.isna(avg_print) else "0")

# -------------------------------------------------------------------------------------------------------------------------
elif menu == "Distribution":
    # Page config
    st.set_page_config(page_title="Distribution", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 0.5rem;
        }
        .section-subtitle {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
        }
        .info-box {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sample data - REPLACE THIS WITH YOUR DATAFRAME
    distribution_df = pd.DataFrame({
        'SKU': ['BK-001', 'BK-001', 'BK-001', 'BK-003', 'FB-001'],
        'Product Name': ['The Alchemist', 'The Alchemist', 'The Alchemist', 'Atomic Habits', 'Facebook Special'],
        'Total Print Lot': [5000, 5000, 5000, 2000, 10000],
        'From': ['Print Press', 'Print Press', 'Print Press', 'Print Press', 'Print Press'],
        'To (Region WH)': ['North WH', 'South WH', 'East WH', 'North WH', 'North WH'],
        'Distribution Qty': [2000, 1500, 1500, 2000, 10000],
        'Status': ['Planned', 'Planned', 'Planned', 'Planned', 'Planned']
    })

    # Region-Warehouse mapping data
    region_wh_df = pd.DataFrame({
        'Region': ['East', 'South', 'West', 'North', 'All (FB)'],
        'Warehouse': ['East WH', 'South WH', 'North WH', 'North WH', 'North WH']
    })

    # Initialize session state
    if 'distribution_data' not in st.session_state:
        st.session_state.distribution_data = distribution_df
    if 'region_wh_data' not in st.session_state:
        st.session_state.region_wh_data = region_wh_df

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown('<div class="main-header">Distribution Planning</div>', unsafe_allow_html=True)
    with col2:
        if st.button("▶ Calculate Distribution", use_container_width=True):
            st.success("Distribution calculated successfully!")
    with col3:
        if st.button("⬇ Export Plan", use_container_width=True):
            st.info("Export functionality")

    # Main layout
    left_col, right_col = st.columns([1, 2])

    # Left column - Region-Warehouse Logic and Current Stock View
    with left_col:
        st.markdown('<div class="section-header">Region-Warehouse Logic</div>', unsafe_allow_html=True)
    
        # Display region-warehouse mapping table
        st.dataframe(
            st.session_state.region_wh_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Region": st.column_config.TextColumn("Region", width="medium"),
                "Warehouse": st.column_config.TextColumn("Warehouse", width="medium")
            }
        )
    
        st.markdown("---")
    
        st.markdown('<div class="section-header">Current Stock View</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Live stock levels placeholder. This would show current inventory and stock-in-transit (SIT) by warehouse.</div>', unsafe_allow_html=True)

    # Right column - Distribution Plan Results
    with right_col:
        st.markdown('<div class="section-header">Distribution Plan Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Review the recommended stock distribution.</div>', unsafe_allow_html=True)
    
        # Export options
        col_export1, col_export2 = st.columns([4, 1])
        with col_export2:
            if st.button("📋 Export Plan", use_container_width=True):
                csv = st.session_state.distribution_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="distribution_plan_results.csv",
                    mime="text/csv"
                )
    
        # Display distribution plan table
        st.markdown("### Distribution Plan Data")
    
        # Create editable dataframe
        edited_df = st.data_editor(
            st.session_state.distribution_data,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "SKU": st.column_config.TextColumn("SKU", width="small"),
                "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
                "Total Print Lot": st.column_config.NumberColumn(
                    "Total Print Lot",
                    width="small",
                    format="%d"
                ),
                "From": st.column_config.TextColumn("From", width="small"),
                "To (Region WH)": st.column_config.TextColumn("To (Region WH)", width="medium"),
                "Distribution Qty": st.column_config.NumberColumn(
                    "Distribution Qty",
                    width="medium",
                    format="%d"
                ),
                "Status": st.column_config.TextColumn("Status", width="small")
            },
            hide_index=True
        )
    
        # Update session state if data was edited
        st.session_state.distribution_data = edited_df
    
        # Summary statistics
        st.markdown("### Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Distribution Qty", f"{edited_df['Distribution Qty'].sum():,}")
        with col2:
            st.metric("Total Shipments", len(edited_df))
        with col3:
            unique_products = edited_df['SKU'].nunique()
            st.metric("Unique Products", unique_products)
        with col4:
            unique_warehouses = edited_df['To (Region WH)'].nunique()
            st.metric("Warehouses", unique_warehouses)

# -------------------------------------------------------------------------------------------------------------------------
elif menu == "Reports":
    # Page config
    st.set_page_config(page_title="Reports & Analytics", layout="wide")

    # Custom CSS for styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 0.5rem;
        }
        .section-subtitle {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sample data for Forecast vs. Actuals - REPLACE THIS WITH YOUR DATAFRAME
    forecast_actuals_df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        'Forecasted Sales': [4200, 3000, 2200, 2700, 1900, 2500, 3500],
        'Actual Sales': [4300, 2800, 2300, 2600, 2000, 2700, 3400]
    })

    # Initialize session state
    if 'forecast_actuals_data' not in st.session_state:
        st.session_state.forecast_actuals_data = forecast_actuals_df
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None
    if 'selected_report_type' not in st.session_state:
        st.session_state.selected_report_type = None

    # Header
    st.markdown('<div class="main-header">Reports & Analytics</div>', unsafe_allow_html=True)

    # Generate Reports Section
    st.markdown('<div class="section-header">Generate Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Select a module and a report type to generate and view analytics.</div>', unsafe_allow_html=True)

    # Module and Report Type Selection
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.markdown("**Module**")
        module = st.selectbox(
            "",
            ["Select a module", "Demand Forecasting", "Print Planning", "Distribution Planning", "Inventory Management"],
            label_visibility="collapsed",
            key="module_select"
        )
        st.session_state.selected_module = module

    with col2:
        st.markdown("**Report Type**")
        report_type = st.selectbox(
            "",
            ["Select a report type", "Forecast vs. Actuals", "Print Plan Summary", "Distribution Analysis", "Stock Level Report"],
            label_visibility="collapsed",
            key="report_type_select"
        )
        st.session_state.selected_report_type = report_type

    with col3:
        st.markdown("**&nbsp;**")  # Spacer for alignment
        if st.button("Generate Report", use_container_width=True):
            st.success("Report generated successfully!")

    st.markdown("---")

    # Forecast vs. Actuals Section
    st.markdown('<div class="section-header">Forecast vs. Actuals</div>', unsafe_allow_html=True)

    col_title, col_export = st.columns([4, 1])
    with col_title:
        st.markdown('<div class="section-subtitle">Comparison for SKU: BK-001 (National)</div>', unsafe_allow_html=True)
    with col_export:
        if st.button("📋 Export", use_container_width=True):
            csv = st.session_state.forecast_actuals_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="forecast_vs_actuals.csv",
                mime="text/csv"
            )

    # Create the line chart
    fig = go.Figure()

    # Add Forecasted Sales line
    fig.add_trace(go.Scatter(
        x=st.session_state.forecast_actuals_data['Month'],
        y=st.session_state.forecast_actuals_data['Forecasted Sales'],
        mode='lines+markers',
        name='Forecasted Sales',
        line=dict(color='#a8d5ff', width=2, dash='dash'),
        marker=dict(size=8, color='#a8d5ff')
    ))

    # Add Actual Sales line
    fig.add_trace(go.Scatter(
        x=st.session_state.forecast_actuals_data['Month'],
        y=st.session_state.forecast_actuals_data['Actual Sales'],
        mode='lines+markers',
        name='Actual Sales',
        line=dict(color='#333333', width=2, dash='dash'),
        marker=dict(size=8, color='#333333')
    ))

    # Update layout
    fig.update_layout(
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            gridwidth=1,
            title='',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            gridwidth=1,
            title='',
            range=[0, 6000],
            tickfont=dict(size=12)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        margin=dict(l=50, r=50, t=30, b=50)
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Data Table
    st.markdown("### Data Table")
    edited_df = st.data_editor(
        st.session_state.forecast_actuals_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Month": st.column_config.TextColumn("Month", width="small"),
            "Forecasted Sales": st.column_config.NumberColumn(
                "Forecasted Sales",
                width="medium",
                format="%d"
            ),
            "Actual Sales": st.column_config.NumberColumn(
                "Actual Sales",
                width="medium",
                format="%d"
            )
        }
    )

    # Update session state if data was edited
    st.session_state.forecast_actuals_data = edited_df

    # Summary Statistics
    st.markdown("### Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)

    total_forecast = edited_df['Forecasted Sales'].sum()
    total_actual = edited_df['Actual Sales'].sum()
    avg_forecast = edited_df['Forecasted Sales'].mean()
    accuracy = (1 - abs(total_forecast - total_actual) / total_forecast) * 100

    with col1:
        st.metric("Total Forecasted", f"{total_forecast:,.0f}")
    with col2:
        st.metric("Total Actual", f"{total_actual:,.0f}")
    with col3:
        st.metric("Avg Monthly Forecast", f"{avg_forecast:,.0f}")
    with col4:
        st.metric("Forecast Accuracy", f"{accuracy:.1f}%")



# -------------------------------------------------------------------------------------------------------------------------
elif menu == "Login":
    st.title("🔐 Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Login")
    # Authenticate users
    if not st.user.is_logged_in:
      st.login("my_provider")
    f"Hi, {st.user.name}"
    st.logout()

    # Get dictionaries of cookies, headers, locale, and browser data
    st.context.cookies
    st.context.headers
    st.context.ip_address
    st.context.is_embedded
    st.context.locale
    st.context.theme.type
    st.context.timezone
    st.context.timezone_offset
    st.context.url
