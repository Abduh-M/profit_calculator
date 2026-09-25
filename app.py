
# import streamlit as st
# import math

# st.set_page_config(
#     page_title="Stock Profit Calculator",
#     layout="centered"
# )

# st.title("Stock Profit Calculator")


# # =================================================
# # SESSION STATE
# # =================================================

# if "entry_price" not in st.session_state:
#     st.session_state.entry_price = ""

# if "stop_price" not in st.session_state:
#     st.session_state.stop_price = ""

# if "target_price" not in st.session_state:
#     st.session_state.target_price = ""

# if "cash_budget" not in st.session_state:
#     st.session_state.cash_budget = ""

# if "show_results" not in st.session_state:
#     st.session_state.show_results = False


# # =================================================
# # CLEAR FUNCTION
# # =================================================

# def clear_inputs():
#     st.session_state.entry_price = ""
#     st.session_state.stop_price = ""
#     st.session_state.target_price = ""
#     st.session_state.cash_budget = ""
#     st.session_state.show_results = False


# # =================================================
# # CSS
# # =================================================

# st.markdown("""
# <style>

# /* Number of shares */
# .shares-number {
#     font-size: 30px;
#     font-weight: 700;
#     line-height: 1;
#     margin: 0;
#     padding: 0;
# }

# /* Profit */
# .target-number {
#     color: #00c853;
#     font-size: 30px;
#     font-weight: 700;
#     line-height: 1;
#     margin: 0;
#     padding: 0;
# }

# /* Loss */
# .stop-number {
#     color: #ff4b4b;
#     font-size: 30px;
#     font-weight: 700;
#     line-height: 1;
#     margin: 0;
#     padding: 0;
# }

# /* Titles */
# .main-title,
# .result-title {
#     font-size: 17px;
#     font-weight: 700;
#     margin: 0 0 2px 0;
#     padding: 0;
# }

# /* Sell price */
# .sell-price {
#     font-size: 13px;
#     opacity: 0.7;
#     margin-top: 4px;
# }

# </style>
# """, unsafe_allow_html=True)


# # =================================================
# # FORMATTING
# # =================================================

# def format_currency(value):
#     return f"${value:,.2f}"


# # =================================================
# # BROKER FEES
# # =================================================

# COST_PER_SHARE = 0.005
# MIN_FEE = 1.00


# def transaction_fee(shares):
#     return max(
#         MIN_FEE,
#         shares * COST_PER_SHARE
#     )


# # =================================================
# # INPUTS
# # =================================================

# col1, col2, col3 = st.columns(3)

# # ENTRY
# with col1:
#     st.text_input(
#         "Entry ($)",
#         key="entry_price"
#     )

# # STOP
# with col2:
#     st.text_input(
#         "Stop ($)",
#         key="stop_price"
#     )

# # TARGET
# with col3:
#     st.text_input(
#         "Target ($)",
#         key="target_price"
#     )


# st.text_input(
#     "Total Cash Budget ($)",
#     key="cash_budget",
#     help="Maximum cash you want to use, including the buy fee."
# )


# # =================================================
# # BUTTONS
# # =================================================

# calculate_clicked = st.button(
#     "Calculate Trade",
#     use_container_width=True,
#     type="primary"
# )

# st.button(
#     "Clear Inputs",
#     use_container_width=True,
#     type="secondary",
#     on_click=clear_inputs
# )


# # =================================================
# # CALCULATE
# # =================================================

# if calculate_clicked:

#     # Convert inputs
#     try:

#         entry_price = (
#             float(st.session_state.entry_price)
#             if st.session_state.entry_price
#             else 0.0
#         )

#         stop_price = (
#             float(st.session_state.stop_price)
#             if st.session_state.stop_price
#             else 0.0
#         )

#         target_price = (
#             float(st.session_state.target_price)
#             if st.session_state.target_price
#             else 0.0
#         )

#         cash_budget = (
#             float(st.session_state.cash_budget)
#             if st.session_state.cash_budget
#             else 0.0
#         )

#     except ValueError:
#         st.error("Please enter valid numbers.")
#         st.stop()


#     # =================================================
#     # VALIDATION
#     # =================================================

#     if entry_price <= 0:
#         st.error("Entry price must be greater than 0.")
#         st.stop()

#     if stop_price <= 0:
#         st.error("Stop price must be greater than 0.")
#         st.stop()

#     if target_price <= 0:
#         st.error("Target price must be greater than 0.")
#         st.stop()

#     if cash_budget <= 0:
#         st.error("Cash budget must be greater than 0.")
#         st.stop()


#     # =================================================
#     # NUMBER OF SHARES
#     # =================================================

#     estimated_shares = (
#         cash_budget / entry_price
#     )

#     estimated_fee = transaction_fee(
#         estimated_shares
#     )

#     num_shares = (
#         cash_budget - estimated_fee
#     ) / entry_price

#     # Whole shares only - always round DOWN
#     num_shares = math.floor(num_shares)

#     buy_fee = transaction_fee(
#         num_shares
#     )

#     # Make sure shares + buy fee
#     # never exceed the cash budget
#     while (
#         num_shares > 0
#         and (
#             num_shares * entry_price
#             + buy_fee
#         ) > cash_budget
#     ):
#         num_shares -= 1
#         buy_fee = transaction_fee(num_shares)


#     # =================================================
#     # ENTRY COST
#     # =================================================

#     entry_value = (
#         num_shares * entry_price
#     )

#     total_cash_used = (
#         entry_value + buy_fee
#     )


#     # =================================================
#     # TARGET SCENARIO
#     # =================================================

#     target_sell_value = (
#         num_shares * target_price
#     )

#     target_sell_fee = transaction_fee(
#         num_shares
#     )

#     target_cash_after_sale = (
#         target_sell_value
#         - target_sell_fee
#     )

#     target_net_profit = (
#         target_cash_after_sale
#         - total_cash_used
#     )


#     # =================================================
#     # STOP SCENARIO
#     # =================================================

#     stop_sell_value = (
#         num_shares * stop_price
#     )

#     stop_sell_fee = transaction_fee(
#         num_shares
#     )

#     stop_cash_after_sale = (
#         stop_sell_value
#         - stop_sell_fee
#     )

#     stop_net_result = (
#         stop_cash_after_sale
#         - total_cash_used
#     )


#     # =================================================
#     # SAVE RESULTS
#     # =================================================

#     st.session_state.num_shares = num_shares

#     st.session_state.target_net_profit = (
#         target_net_profit
#     )

#     st.session_state.stop_net_result = (
#         stop_net_result
#     )

#     st.session_state.target_price_result = (
#         target_price
#     )

#     st.session_state.stop_price_result = (
#         stop_price
#     )

#     st.session_state.show_results = True


# # =================================================
# # DISPLAY RESULTS
# # =================================================

# if st.session_state.show_results:

#     num_shares = (
#         st.session_state.num_shares
#     )

#     target_net_profit = (
#         st.session_state.target_net_profit
#     )

#     stop_net_result = (
#         st.session_state.stop_net_result
#     )

#     target_price = (
#         st.session_state.target_price_result
#     )

#     stop_price = (
#         st.session_state.stop_price_result
#     )


#     # =================================================
#     # SHARES
#     # =================================================

#     st.divider()

#     st.markdown(
#         f"""
#         <p class="main-title">Number of Shares</p>
#         <p class="shares-number">{num_shares:,}</p>
#         """,
#         unsafe_allow_html=True
#     )

#     st.divider()


#     # =================================================
#     # TARGET + STOP RESULTS
#     # =================================================

#     col1, col2 = st.columns(2)


#     # TARGET
#     with col1:

#         if target_net_profit >= 0:

#             target_class = "target-number"

#             target_text = (
#                 f"+{format_currency(target_net_profit)}"
#             )

#         else:

#             target_class = "stop-number"

#             target_text = (
#                 f"-{format_currency(abs(target_net_profit))}"
#             )

#         st.markdown(
#             f"""
#             <p class="result-title">Target Hit</p>
#             <p class="{target_class}">{target_text}</p>
#             <p class="sell-price">
#                 Sell at {format_currency(target_price)}
#             </p>
#             """,
#             unsafe_allow_html=True
#         )


#     # STOP
#     with col2:

#         if stop_net_result < 0:

#             stop_class = "stop-number"

#             stop_text = (
#                 f"-{format_currency(abs(stop_net_result))}"
#             )

#         else:

#             stop_class = "target-number"

#             stop_text = (
#                 f"+{format_currency(stop_net_result)}"
#             )

#         st.markdown(
#             f"""
#             <p class="result-title">Stop Hit</p>
#             <p class="{stop_class}">{stop_text}</p>
#             <p class="sell-price">
#                 Sell at {format_currency(stop_price)}
#             </p>
#             """,
#             unsafe_allow_html=True
#         )




#before scrolling change
# import streamlit as st
# import math

# st.set_page_config(
#     page_title="Stock Profit Calculator",
#     layout="centered"
# )

# st.title("Stock Profit Calculator")


# # =================================================
# # SESSION STATE
# # =================================================

# if "entry_price" not in st.session_state:
#     st.session_state.entry_price = None

# if "stop_price" not in st.session_state:
#     st.session_state.stop_price = None

# if "target_price" not in st.session_state:
#     st.session_state.target_price = None

# if "cash_budget" not in st.session_state:
#     st.session_state.cash_budget = None

# if "show_results" not in st.session_state:
#     st.session_state.show_results = False


# # =================================================
# # CLEAR FUNCTION
# # =================================================

# def clear_inputs():
#     st.session_state.entry_price = None
#     st.session_state.stop_price = None
#     st.session_state.target_price = None
#     st.session_state.cash_budget = None
#     st.session_state.show_results = False


# # =================================================
# # CSS
# # =================================================

# st.markdown("""
# <style>

# /* Number of shares */
# .shares-number {
#     font-size: 30px;
#     font-weight: 700;
#     line-height: 1;
#     margin: 0;
#     padding: 0;
# }

# /* Profit */
# .target-number {
#     color: #00c853;
#     font-size: 30px;
#     font-weight: 700;
#     line-height: 1;
#     margin: 0;
#     padding: 0;
# }

# /* Loss */
# .stop-number {
#     color: #ff4b4b;
#     font-size: 30px;
#     font-weight: 700;
#     line-height: 1;
#     margin: 0;
#     padding: 0;
# }

# /* Titles */
# .main-title,
# .result-title {
#     font-size: 17px;
#     font-weight: 700;
#     margin: 0 0 2px 0;
#     padding: 0;
# }

# /* Sell price */
# .sell-price {
#     font-size: 13px;
#     opacity: 0.7;
#     margin-top: 4px;
# }

# </style>
# """, unsafe_allow_html=True)


# # =================================================
# # FORMATTING
# # =================================================

# def format_currency(value):
#     return f"${value:,.2f}"


# # =================================================
# # BROKER FEES
# # =================================================

# COST_PER_SHARE = 0.005
# MIN_FEE = 1.00


# def transaction_fee(shares):
#     return max(
#         MIN_FEE,
#         shares * COST_PER_SHARE
#     )


# # =================================================
# # INPUTS
# # =================================================

# col1, col2, col3 = st.columns(3)


# # ENTRY
# with col1:
#     st.number_input(
#         "Entry ($)",
#         min_value=0.0,
#         value=None,
#         step=0.01,
#         format="%.2f",
#         key="entry_price",
#         placeholder="0.00"
#     )


# # STOP
# with col2:
#     st.number_input(
#         "Stop ($)",
#         min_value=0.0,
#         value=None,
#         step=0.01,
#         format="%.2f",
#         key="stop_price",
#         placeholder="0.00"
#     )


# # TARGET
# with col3:
#     st.number_input(
#         "Target ($)",
#         min_value=0.0,
#         value=None,
#         step=0.01,
#         format="%.2f",
#         key="target_price",
#         placeholder="0.00"
#     )


# # CASH BUDGET
# st.number_input(
#     "Total Cash Budget ($)",
#     min_value=0.0,
#     value=None,
#     step=1.00,
#     format="%.2f",
#     key="cash_budget",
#     placeholder="0.00",
#     help="Maximum cash you want to use, including the buy fee."
# )


# # =================================================
# # BUTTONS
# # =================================================

# calculate_clicked = st.button(
#     "Calculate Trade",
#     use_container_width=True,
#     type="primary"
# )

# st.button(
#     "Clear Inputs",
#     use_container_width=True,
#     type="secondary",
#     on_click=clear_inputs
# )


# # =================================================
# # CALCULATE
# # =================================================

# if calculate_clicked:

#     entry_price = st.session_state.entry_price
#     stop_price = st.session_state.stop_price
#     target_price = st.session_state.target_price
#     cash_budget = st.session_state.cash_budget


#     # =================================================
#     # VALIDATION
#     # =================================================

#     if entry_price is None or entry_price <= 0:
#         st.error("Entry price must be greater than 0.")
#         st.stop()

#     if stop_price is None or stop_price <= 0:
#         st.error("Stop price must be greater than 0.")
#         st.stop()

#     if target_price is None or target_price <= 0:
#         st.error("Target price must be greater than 0.")
#         st.stop()

#     if cash_budget is None or cash_budget <= 0:
#         st.error("Cash budget must be greater than 0.")
#         st.stop()


#     # =================================================
#     # NUMBER OF SHARES
#     # =================================================

#     estimated_shares = (
#         cash_budget / entry_price
#     )

#     estimated_fee = transaction_fee(
#         estimated_shares
#     )

#     num_shares = (
#         cash_budget - estimated_fee
#     ) / entry_price

#     # Whole shares only - always round DOWN
#     num_shares = math.floor(num_shares)

#     buy_fee = transaction_fee(
#         num_shares
#     )

#     # Make sure shares + buy fee
#     # never exceed the cash budget
#     while (
#         num_shares > 0
#         and (
#             num_shares * entry_price
#             + buy_fee
#         ) > cash_budget
#     ):
#         num_shares -= 1
#         buy_fee = transaction_fee(num_shares)


#     # =================================================
#     # ENTRY COST
#     # =================================================

#     entry_value = (
#         num_shares * entry_price
#     )

#     total_cash_used = (
#         entry_value + buy_fee
#     )


#     # =================================================
#     # TARGET SCENARIO
#     # =================================================

#     target_sell_value = (
#         num_shares * target_price
#     )

#     target_sell_fee = transaction_fee(
#         num_shares
#     )

#     target_cash_after_sale = (
#         target_sell_value
#         - target_sell_fee
#     )

#     target_net_profit = (
#         target_cash_after_sale
#         - total_cash_used
#     )


#     # =================================================
#     # STOP SCENARIO
#     # =================================================

#     stop_sell_value = (
#         num_shares * stop_price
#     )

#     stop_sell_fee = transaction_fee(
#         num_shares
#     )

#     stop_cash_after_sale = (
#         stop_sell_value
#         - stop_sell_fee
#     )

#     stop_net_result = (
#         stop_cash_after_sale
#         - total_cash_used
#     )


#     # =================================================
#     # SAVE RESULTS
#     # =================================================

#     st.session_state.num_shares = num_shares

#     st.session_state.target_net_profit = (
#         target_net_profit
#     )

#     st.session_state.stop_net_result = (
#         stop_net_result
#     )

#     st.session_state.target_price_result = (
#         target_price
#     )

#     st.session_state.stop_price_result = (
#         stop_price
#     )

#     st.session_state.show_results = True


# # =================================================
# # DISPLAY RESULTS
# # =================================================

# if st.session_state.show_results:

#     num_shares = (
#         st.session_state.num_shares
#     )

#     target_net_profit = (
#         st.session_state.target_net_profit
#     )

#     stop_net_result = (
#         st.session_state.stop_net_result
#     )

#     target_price = (
#         st.session_state.target_price_result
#     )

#     stop_price = (
#         st.session_state.stop_price_result
#     )


#     # =================================================
#     # SHARES
#     # =================================================

#     st.divider()

#     st.markdown(
#         f"""
#         <p class="main-title">Number of Shares</p>
#         <p class="shares-number">{num_shares:,}</p>
#         """,
#         unsafe_allow_html=True
#     )

#     st.divider()


#     # =================================================
#     # TARGET + STOP RESULTS
#     # =================================================

#     col1, col2 = st.columns(2)


#     # TARGET
#     with col1:

#         if target_net_profit >= 0:

#             target_class = "target-number"

#             target_text = (
#                 f"+{format_currency(target_net_profit)}"
#             )

#         else:

#             target_class = "stop-number"

#             target_text = (
#                 f"-{format_currency(abs(target_net_profit))}"
#             )

#         st.markdown(
#             f"""
#             <p class="result-title">Target Hit</p>
#             <p class="{target_class}">{target_text}</p>
#             <p class="sell-price">
#                 Sell at {format_currency(target_price)}
#             </p>
#             """,
#             unsafe_allow_html=True
#         )


#     # STOP
#     with col2:

#         if stop_net_result < 0:

#             stop_class = "stop-number"

#             stop_text = (
#                 f"-{format_currency(abs(stop_net_result))}"
#             )

#         else:

#             stop_class = "target-number"

#             stop_text = (
#                 f"+{format_currency(stop_net_result)}"
#             )

#         st.markdown(
#             f"""
#             <p class="result-title">Stop Hit</p>
#             <p class="{stop_class}">{stop_text}</p>
#             <p class="sell-price">
#                 Sell at {format_currency(stop_price)}
#             </p>
#             """,
#             unsafe_allow_html=True
#         )




import streamlit as st
import streamlit.components.v1 as components
import math

st.set_page_config(
    page_title="Stock Profit Calculator",
    layout="centered"
)

st.title("Stock Profit Calculator")


# =================================================
# SESSION STATE
# =================================================

if "entry_price" not in st.session_state:
    st.session_state.entry_price = None

if "stop_price" not in st.session_state:
    st.session_state.stop_price = None

if "target_price" not in st.session_state:
    st.session_state.target_price = None

if "cash_budget" not in st.session_state:
    st.session_state.cash_budget = None

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "scroll_to_results" not in st.session_state:
    st.session_state.scroll_to_results = False


# =================================================
# CLEAR FUNCTION
# =================================================

def clear_inputs():
    st.session_state.entry_price = None
    st.session_state.stop_price = None
    st.session_state.target_price = None
    st.session_state.cash_budget = None
    st.session_state.show_results = False
    st.session_state.scroll_to_results = False


# =================================================
# CSS
# =================================================

st.markdown("""
<style>

/* Number of shares */
.shares-number {
    font-size: 30px;
    font-weight: 700;
    line-height: 1;
    margin: 0;
    padding: 0;
}

/* Profit */
.target-number {
    color: #00c853;
    font-size: 30px;
    font-weight: 700;
    line-height: 1;
    margin: 0;
    padding: 0;
}

/* Loss */
.stop-number {
    color: #ff4b4b;
    font-size: 30px;
    font-weight: 700;
    line-height: 1;
    margin: 0;
    padding: 0;
}

/* Titles */
.main-title,
.result-title {
    font-size: 17px;
    font-weight: 700;
    margin: 0 0 2px 0;
    padding: 0;
}

/* Sell price */
.sell-price {
    font-size: 13px;
    opacity: 0.7;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)


# =================================================
# FORMATTING
# =================================================

def format_currency(value):
    return f"${value:,.2f}"


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
# INPUTS
# =================================================

col1, col2, col3 = st.columns(3)


# ENTRY
with col1:
    st.number_input(
        "Entry ($)",
        min_value=0.0,
        value=None,
        step=0.01,
        format="%.2f",
        key="entry_price",
        placeholder="0.00"
    )


# STOP
with col2:
    st.number_input(
        "Stop ($)",
        min_value=0.0,
        value=None,
        step=0.01,
        format="%.2f",
        key="stop_price",
        placeholder="0.00"
    )


# TARGET
with col3:
    st.number_input(
        "Target ($)",
        min_value=0.0,
        value=None,
        step=0.01,
        format="%.2f",
        key="target_price",
        placeholder="0.00"
    )


# CASH BUDGET
st.number_input(
    "Total Cash Budget ($)",
    min_value=0.0,
    value=None,
    step=1.00,
    format="%.2f",
    key="cash_budget",
    placeholder="0.00",
    help="Maximum cash you want to use, including the buy fee."
)


# =================================================
# BUTTONS
# =================================================

calculate_clicked = st.button(
    "Calculate Trade",
    use_container_width=True,
    type="primary"
)

st.button(
    "Clear Inputs",
    use_container_width=True,
    type="secondary",
    on_click=clear_inputs
)


# =================================================
# CALCULATE
# =================================================

if calculate_clicked:

    entry_price = st.session_state.entry_price
    stop_price = st.session_state.stop_price
    target_price = st.session_state.target_price
    cash_budget = st.session_state.cash_budget


    # =================================================
    # VALIDATION
    # =================================================

    if entry_price is None or entry_price <= 0:
        st.error("Entry price must be greater than 0.")
        st.stop()

    if stop_price is None or stop_price <= 0:
        st.error("Stop price must be greater than 0.")
        st.stop()

    if target_price is None or target_price <= 0:
        st.error("Target price must be greater than 0.")
        st.stop()

    if cash_budget is None or cash_budget <= 0:
        st.error("Cash budget must be greater than 0.")
        st.stop()


    # =================================================
    # NUMBER OF SHARES
    # =================================================

    estimated_shares = (
        cash_budget / entry_price
    )

    estimated_fee = transaction_fee(
        estimated_shares
    )

    num_shares = (
        cash_budget - estimated_fee
    ) / entry_price

    # Whole shares only - always round DOWN
    num_shares = math.floor(num_shares)

    buy_fee = transaction_fee(
        num_shares
    )

    # Make sure shares + buy fee
    # never exceed the cash budget
    while (
        num_shares > 0
        and (
            num_shares * entry_price
            + buy_fee
        ) > cash_budget
    ):
        num_shares -= 1
        buy_fee = transaction_fee(num_shares)


    # =================================================
    # ENTRY COST
    # =================================================

    entry_value = (
        num_shares * entry_price
    )

    total_cash_used = (
        entry_value + buy_fee
    )


    # =================================================
    # TARGET SCENARIO
    # =================================================

    target_sell_value = (
        num_shares * target_price
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
    # STOP SCENARIO
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
    # SAVE RESULTS
    # =================================================

    st.session_state.num_shares = num_shares

    st.session_state.target_net_profit = (
        target_net_profit
    )

    st.session_state.stop_net_result = (
        stop_net_result
    )

    st.session_state.target_price_result = (
        target_price
    )

    st.session_state.stop_price_result = (
        stop_price
    )

    st.session_state.show_results = True

    # Tell the app to scroll to results
    st.session_state.scroll_to_results = True


# =================================================
# DISPLAY RESULTS
# =================================================

if st.session_state.show_results:

    num_shares = (
        st.session_state.num_shares
    )

    target_net_profit = (
        st.session_state.target_net_profit
    )

    stop_net_result = (
        st.session_state.stop_net_result
    )

    target_price = (
        st.session_state.target_price_result
    )

    stop_price = (
        st.session_state.stop_price_result
    )


    # =================================================
    # RESULTS ANCHOR
    # =================================================

    st.markdown(
        '<div id="trade-results"></div>',
        unsafe_allow_html=True
    )


    # =================================================
    # SHARES
    # =================================================

    st.divider()

    st.markdown(
        f"""
        <p class="main-title">Number of Shares</p>
        <p class="shares-number">{num_shares:,}</p>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    # =================================================
    # TARGET + STOP RESULTS
    # =================================================

    col1, col2 = st.columns(2)


    # TARGET
    with col1:

        if target_net_profit >= 0:

            target_class = "target-number"

            target_text = (
                f"+{format_currency(target_net_profit)}"
            )

        else:

            target_class = "stop-number"

            target_text = (
                f"-{format_currency(abs(target_net_profit))}"
            )

        st.markdown(
            f"""
            <p class="result-title">Target Hit</p>
            <p class="{target_class}">{target_text}</p>
            <p class="sell-price">
                Sell at {format_currency(target_price)}
            </p>
            """,
            unsafe_allow_html=True
        )


    # STOP
    with col2:

        if stop_net_result < 0:

            stop_class = "stop-number"

            stop_text = (
                f"-{format_currency(abs(stop_net_result))}"
            )

        else:

            stop_class = "target-number"

            stop_text = (
                f"+{format_currency(stop_net_result)}"
            )

        st.markdown(
            f"""
            <p class="result-title">Stop Hit</p>
            <p class="{stop_class}">{stop_text}</p>
            <p class="sell-price">
                Sell at {format_currency(stop_price)}
            </p>
            """,
            unsafe_allow_html=True
        )


    # =================================================
    # AUTO-SCROLL TO RESULTS
    # =================================================

    if st.session_state.scroll_to_results:

        components.html(
            """
            <script>
                setTimeout(function() {
                    const results =
                        window.parent.document.getElementById(
                            "trade-results"
                        );

                    if (results) {
                        results.scrollIntoView({
                            behavior: "smooth",
                            block: "start"
                        });
                    }
                }, 150);
            </script>
            """,
            height=0
        )

        # Prevent scrolling again on unrelated reruns
        st.session_state.scroll_to_results = False
