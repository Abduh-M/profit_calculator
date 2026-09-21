import streamlit as st

st.set_page_config(page_title="Stock Profit Calculator", layout="centered")

st.title("📈 Stock Profit Calculator")

# Smart formatter - removes .00 but keeps decimals if they exist
def format_currency(value):
    return f"${value:,.2f}".rstrip('0').rstrip('.')

def format_number(value):
    return f"{value:,.2f}".rstrip('0').rstrip('.')

# Input fields
col1, col2 = st.columns(2)

with col1:
    purchase_price = st.number_input("Buy Price ($)", value=23.38, step=0.01, min_value=0.0)
    
with col2:
    sell_price = st.number_input("Sell Price ($)", value=23.46, step=0.01, min_value=0.0)

investment_value = st.number_input("Investment ($)", value=3000.0, step=100.0, min_value=0.0)

# Fixed cost per share
cost_per_share = 0.005

# Calculate
if st.button("Calculate Profit", use_container_width=True):
    num_shares = investment_value / purchase_price if purchase_price > 0 else 0
    buy_value = num_shares * purchase_price
    sell_value = num_shares * sell_price
    total_cost = num_shares * cost_per_share
    gross_profit = sell_value - buy_value
    net_profit = gross_profit - total_cost
    profit_percent = (net_profit / buy_value * 100) if buy_value > 0 else 0
    
    # Display results
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Shares", format_number(num_shares))
    with col2:
        st.metric("Buy Value", format_currency(buy_value))
    with col3:
        st.metric("Sell Value", format_currency(sell_value))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Transaction Cost", format_currency(total_cost))
    with col2:
        st.metric("Gross Profit", format_currency(gross_profit))
    
    st.divider()
    
    # Net profit with color
    if net_profit > 0:
        st.success(f"✓ NET PROFIT: {format_currency(net_profit)} ({profit_percent:.2f}%)")
    elif net_profit < 0:
        st.error(f"✗ LOSS: -{format_currency(abs(net_profit))} ({profit_percent:.2f}%)")
    else:
        st.info("~ BREAK EVEN")
