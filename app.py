import streamlit as st

st.set_page_config(page_title="Stock Profit Calculator", layout="centered")

st.title("📈 Stock Profit Calculator")

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
        st.metric("Shares", f"{num_shares:,.2f}")
    with col2:
        st.metric("Buy Value", f"${buy_value:,.2f}")
    with col3:
        st.metric("Sell Value", f"${sell_value:,.2f}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Transaction Cost", f"${total_cost:,.2f}")
    with col2:
        st.metric("Gross Profit", f"${gross_profit:,.2f}")
    
    st.divider()
    
    # Net profit with color
    if net_profit > 0:
        st.success(f"✓ NET PROFIT: ${net_profit:,.2f} ({profit_percent:.2f}%)", icon="✓")
    elif net_profit < 0:
        st.error(f"✗ LOSS: -${abs(net_profit):,.2f} ({profit_percent:.2f}%)", icon="✗")
    else:
        st.info("~ BREAK EVEN", icon="~")
