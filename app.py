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



import streamlit as st

st.set_page_config(page_title="Stock Profit Calculator", layout="centered")

st.title("📈 Stock Profit Calculator")

# -----------------------------
# Formatting
# -----------------------------
def format_currency(value):
    return f"${value:,.2f}"

def format_number(value):
    return f"{value:,.4f}".rstrip("0").rstrip(".")


# -----------------------------
# Inputs
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    purchase_price_input = st.text_input("Buy Price ($)", "")

with col2:
    sell_price_input = st.text_input("Sell Price ($)", "")

investment_input = st.text_input(
    "Total Cash Budget ($)",
    "",
    help="Maximum amount you want to spend, including the BUY fee."
)

try:
    purchase_price = float(purchase_price_input) if purchase_price_input else 0.0
    sell_price = float(sell_price_input) if sell_price_input else 0.0
    cash_budget = float(investment_input) if investment_input else 0.0
except ValueError:
    st.error("Please enter valid numbers.")
    st.stop()


# -----------------------------
# Broker fee settings
# -----------------------------
COST_PER_SHARE = 0.005
MIN_FEE = 1.00


def transaction_fee(shares):
    return max(MIN_FEE, shares * COST_PER_SHARE)


# -----------------------------
# Calculate
# -----------------------------
if st.button("Calculate Profit", use_container_width=True):

    if purchase_price <= 0:
        st.error("Buy price must be greater than 0.")
        st.stop()

    if sell_price <= 0:
        st.error("Sell price must be greater than 0.")
        st.stop()

    if cash_budget <= 0:
        st.error("Cash budget must be greater than 0.")
        st.stop()

    # -------------------------------------------------
    # Determine shares while keeping BUY + fee
    # inside the total cash budget
    # -------------------------------------------------

    # First estimate
    num_shares = cash_budget / purchase_price

    # Calculate estimated buy fee
    buy_fee = transaction_fee(num_shares)

    # Recalculate shares after reserving money for fee
    num_shares = (cash_budget - buy_fee) / purchase_price

    # Recalculate exact fee
    buy_fee = transaction_fee(num_shares)

    # Final shares
    num_shares = (cash_budget - buy_fee) / purchase_price

    # -------------------------------------------------
    # BUY SIDE
    # -------------------------------------------------

    buy_value = num_shares * purchase_price

    total_cash_used = buy_value + buy_fee

    # -------------------------------------------------
    # SELL SIDE
    # -------------------------------------------------

    sell_value = num_shares * sell_price

    sell_fee = transaction_fee(num_shares)

    cash_after_sale = sell_value - sell_fee

    # -------------------------------------------------
    # PROFIT CALCULATIONS
    # -------------------------------------------------

    gross_profit = sell_value - buy_value

    total_fees = buy_fee + sell_fee

    net_profit = cash_after_sale - total_cash_used

    profit_percent = (
        net_profit / total_cash_used * 100
        if total_cash_used > 0
        else 0
    )

    # Break-even sell price
    break_even_price = (
        total_cash_used + sell_fee
    ) / num_shares if num_shares > 0 else 0


    # =================================================
    # DISPLAY
    # =================================================

    st.divider()

    st.subheader("📦 Position")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Shares",
            format_number(num_shares)
        )

    with col2:
        st.metric(
            "Cash Budget",
            format_currency(cash_budget)
        )


    # -----------------------------
    # BUY
    # -----------------------------

    st.divider()

    st.subheader("🟢 BUY")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Stock Value",
            format_currency(buy_value)
        )

    with col2:
        st.metric(
            "Buy Fee",
            format_currency(buy_fee)
        )

    with col3:
        st.metric(
            "Total Cash Used",
            format_currency(total_cash_used)
        )


    # -----------------------------
    # SELL
    # -----------------------------

    st.divider()

    st.subheader("🔴 SELL")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Sell Value",
            format_currency(sell_value)
        )

    with col2:
        st.metric(
            "Sell Fee",
            format_currency(sell_fee)
        )

    with col3:
        st.metric(
            "Cash After Sale",
            format_currency(cash_after_sale)
        )


    # -----------------------------
    # PROFIT
    # -----------------------------

    st.divider()

    st.subheader("💰 Profit Breakdown")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Gross Profit",
            format_currency(gross_profit)
        )

    with col2:
        st.metric(
            "Total Fees",
            format_currency(total_fees)
        )

    with col3:
        st.metric(
            "Break Even",
            format_currency(break_even_price)
        )


    # -----------------------------
    # NET RESULT
    # -----------------------------

    st.divider()

    if net_profit > 0:

        st.success(
            f"✓ NET PROFIT: "
            f"{format_currency(net_profit)} "
            f"({profit_percent:.2f}%)"
        )

    elif net_profit < 0:

        st.error(
            f"✗ NET LOSS: "
            f"{format_currency(abs(net_profit))} "
            f"({profit_percent:.2f}%)"
        )

    else:

        st.info("~ BREAK EVEN")
