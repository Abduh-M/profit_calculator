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
import math

st.set_page_config(
    page_title="Stock Profit Calculator",
    layout="centered"
)

st.title("📈 Stock Profit Calculator")


# =================================================
# FORMATTING
# =================================================

def format_currency(value):
    return f"${value:,.2f}"


# =================================================
# INPUTS
# =================================================

col1, col2, col3 = st.columns(3)

with col1:
    purchase_price_input = st.text_input(
        "Buy Price ($)",
        ""
    )

with col2:
    sell_price_input = st.text_input(
        "Target Price ($)",
        ""
    )

with col3:
    stop_price_input = st.text_input(
        "Stop Price ($)",
        ""
    )

investment_input = st.text_input(
    "Total Cash Budget ($)",
    "",
    help="Maximum cash you want to use, including the buy fee."
)


# =================================================
# CONVERT INPUTS
# =================================================

try:
    purchase_price = (
        float(purchase_price_input)
        if purchase_price_input else 0.0
    )

    sell_price = (
        float(sell_price_input)
        if sell_price_input else 0.0
    )

    stop_price = (
        float(stop_price_input)
        if stop_price_input else 0.0
    )

    cash_budget = (
        float(investment_input)
        if investment_input else 0.0
    )

except ValueError:
    st.error("Please enter valid numbers.")
    st.stop()


# =================================================
# BROKER FEES
# =================================================

COST_PER_SHARE = 0.005
MIN_FEE = 1.00


def transaction_fee(shares):
    return max(
        MIN_FEE,
        shares * COST_PER_SHARE
    )


# =================================================
# CALCULATE
# =================================================

if st.button(
    "Calculate Trade",
    use_container_width=True
):

    # Validation

    if purchase_price <= 0:
        st.error("Buy price must be greater than 0.")
        st.stop()

    if sell_price <= 0:
        st.error("Target price must be greater than 0.")
        st.stop()

    if stop_price <= 0:
        st.error("Stop price must be greater than 0.")
        st.stop()

    if cash_budget <= 0:
        st.error("Cash budget must be greater than 0.")
        st.stop()


    # =================================================
    # SHARES
    # =================================================

    estimated_shares = (
        cash_budget / purchase_price
    )

    estimated_fee = transaction_fee(
        estimated_shares
    )

    num_shares = (
        cash_budget - estimated_fee
    ) / purchase_price

    # Whole shares only
    num_shares = math.floor(num_shares)

    buy_fee = transaction_fee(
        num_shares
    )

    # Safety check
    while (
        num_shares > 0
        and
        (
            num_shares * purchase_price
            + buy_fee
        ) > cash_budget
    ):

        num_shares -= 1

        buy_fee = transaction_fee(
            num_shares
        )


    # =================================================
    # BUY
    # =================================================

    buy_value = (
        num_shares * purchase_price
    )

    total_cash_used = (
        buy_value + buy_fee
    )

    cash_remaining = (
        cash_budget - total_cash_used
    )


    # =================================================
    # TARGET
    # =================================================

    target_sell_value = (
        num_shares * sell_price
    )

    target_sell_fee = transaction_fee(
        num_shares
    )

    target_cash_after_sale = (
        target_sell_value
        - target_sell_fee
    )

    target_net_profit = (
        target_cash_after_sale
        - total_cash_used
    )


    # =================================================
    # STOP
    # =================================================

    stop_sell_value = (
        num_shares * stop_price
    )

    stop_sell_fee = transaction_fee(
        num_shares
    )

    stop_cash_after_sale = (
        stop_sell_value
        - stop_sell_fee
    )

    stop_net_result = (
        stop_cash_after_sale
        - total_cash_used
    )


    # =================================================
    # FEES
    # =================================================

    target_total_fees = (
        buy_fee + target_sell_fee
    )

    stop_total_fees = (
        buy_fee + stop_sell_fee
    )


    # =================================================
    # BREAK EVEN
    # =================================================

    break_even_price = (
        (total_cash_used + target_sell_fee)
        / num_shares
        if num_shares > 0
        else 0
    )


    # =================================================
    # MAIN RESULTS
    # =================================================

    st.divider()

    st.metric(
        " SHARES YOU CAN BUY",
        f"{num_shares:,}"
    )

    st.divider()


    # =================================================
    # TARGET + STOP
    # =================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### TARGET HIT")

        if target_net_profit >= 0:

            st.success(
                f" +{format_currency(target_net_profit)}"
            )

        else:

            st.error(
                f" -{format_currency(abs(target_net_profit))}"
            )

        st.caption(
            f"Sell at {format_currency(sell_price)}"
        )


    with col2:

        st.markdown("#### STOP HIT")

        if stop_net_result < 0:

            st.error(
                f" -{format_currency(abs(stop_net_result))}"
            )

        else:

            st.success(
                f" +{format_currency(stop_net_result)}"
            )

        st.caption(
            f"Sell at {format_currency(stop_price)}"
        )


    # =================================================
    # FULL DETAILS
    # =================================================

    st.divider()

    with st.expander(
        "Show Full Trade Details"
    ):

        # BUY

        st.subheader("Buy")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Cash Budget",
                format_currency(cash_budget)
            )

        with col2:
            st.metric(
                "Stock Value",
                format_currency(buy_value)
            )

        with col3:
            st.metric(
                "Buy Fee",
                format_currency(buy_fee)
            )

        st.metric(
            "Unused Cash",
            format_currency(cash_remaining)
        )


        # TARGET

        st.subheader("🎯 Target Scenario")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Target Price",
                format_currency(sell_price)
            )

        with col2:
            st.metric(
                "Sell Value",
                format_currency(target_sell_value)
            )

        with col3:
            st.metric(
                "Total Fees",
                format_currency(target_total_fees)
            )


        # STOP

        st.subheader("🛑 Stop Scenario")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Stop Price",
                format_currency(stop_price)
            )

        with col2:
            st.metric(
                "Sell Value",
                format_currency(stop_sell_value)
            )

        with col3:
            st.metric(
                "Total Fees",
                format_currency(stop_total_fees)
            )


        # OTHER

        st.subheader("Other")

        st.metric(
            "Break Even Price",
            format_currency(break_even_price)
        )
