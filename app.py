# import streamlit as st

# st.set_page_config(page_title="Stock Profit Calculator", layout="centered")

# st.title("📈 Stock Profit Calculator")

# # Smart formatter - removes .00 but keeps decimals if they exist
# def format_currency(value):
#     return f"${value:,.2f}".rstrip('0').rstrip('.')

# def format_number(value):
#     return f"{value:,.2f}".rstrip('0').rstrip('.')

# # Input fields
# col1, col2 = st.columns(2)

# with col1:
#     purchase_price_input = st.text_input("Buy Price ($)", "")
#     purchase_price = float(purchase_price_input) if purchase_price_input else 0.0
    
# with col2:
#     sell_price_input = st.text_input("Sell Price ($)", "")
#     sell_price = float(sell_price_input) if sell_price_input else 0.0

# investment_input = st.text_input("Investment ($)", "")
# investment_value = float(investment_input) if investment_input else 0.0

# # Fixed cost per share
# cost_per_share = 0.005

# # Calculate
# if st.button("Calculate Profit", use_container_width=True):
#     num_shares = investment_value / purchase_price if purchase_price > 0 else 0
#     buy_value = num_shares * purchase_price
#     sell_value = num_shares * sell_price
    
#     # Transaction cost with $1 minimum
#     calculated_cost = num_shares * cost_per_share
#     total_cost = max(1.0, calculated_cost)
    
#     gross_profit = sell_value - buy_value
#     net_profit = gross_profit - total_cost
#     profit_percent = (net_profit / buy_value * 100) if buy_value > 0 else 0
    
#     # Display results
#     st.divider()
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Shares", format_number(num_shares))
#     with col2:
#         st.metric("Buy Value", format_currency(buy_value))
#     with col3:
#         st.metric("Sell Value", format_currency(sell_value))
    
#     st.divider()
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Transaction Cost", format_currency(total_cost))
#     with col2:
#         st.metric("Gross Profit", format_currency(gross_profit))
    
#     st.divider()
    
#     # Net profit with color
#     if net_profit > 0:
#         st.success(f"✓ NET PROFIT: {format_currency(net_profit)} ({profit_percent:.2f}%)")
#     elif net_profit < 0:
#         st.error(f"✗ LOSS: -{format_currency(abs(net_profit))} ({profit_percent:.2f}%)")
#     else:
#         st.info("~ BREAK EVEN")



# =================================================
# DISPLAY
# =================================================

st.divider()

# ---------------------------------
# MAIN RESULTS
# ---------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "📦 SHARES YOU CAN BUY",
        format_number(num_shares)
    )

with col2:
    if net_profit >= 0:
        st.metric(
            "💰 NET PROFIT",
            format_currency(net_profit),
            f"{profit_percent:.2f}%"
        )
    else:
        st.metric(
            "💰 NET LOSS",
            f"-{format_currency(abs(net_profit))}",
            f"{profit_percent:.2f}%"
        )

st.divider()


# ---------------------------------
# TRADE DETAILS
# ---------------------------------

st.subheader("Trade Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Cash Budget",
        format_currency(cash_budget)
    )

with col2:
    st.metric(
        "Buy Value",
        format_currency(buy_value)
    )

with col3:
    st.metric(
        "Sell Value",
        format_currency(sell_value)
    )


# ---------------------------------
# FEES
# ---------------------------------

st.subheader("Fees")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Buy Fee",
        format_currency(buy_fee)
    )

with col2:
    st.metric(
        "Sell Fee",
        format_currency(sell_fee)
    )

with col3:
    st.metric(
        "Total Fees",
        format_currency(total_fees)
    )


# ---------------------------------
# EXTRA DETAILS
# ---------------------------------

st.subheader("Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Gross Profit",
        format_currency(gross_profit)
    )

with col2:
    st.metric(
        "Cash After Sale",
        format_currency(cash_after_sale)
    )

with col3:
    st.metric(
        "Break Even Price",
        format_currency(break_even_price)
    )
