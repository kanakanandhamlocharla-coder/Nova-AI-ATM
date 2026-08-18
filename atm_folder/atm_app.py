import streamlit as st

st.set_page_config(page_title="ATM Simulator", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    .block-container{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp{
        background-color: #0b132b;
        color: #ffffff;
    }
    div.stButton > button {
            background-color: #1E293B !important;
            border: 2px solid #38BDF8 !important;
            border-radius: 12px !important;
            height: 55px !important;           
            transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button p {
            font-size: 22px !important;         
            font-weight: 800 !important;
            color: #38BDF8 !important;
    }
    div.stButton > button:hover {
            background-color: #38BDF8 !important;
            border-color: #ffffff !important;
    }
    div.stButton > button:hover p {
            color: #0b132b !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "username" not in st.session_state:
    st.session_state.username = "Customer"
if "pin" not in st.session_state:
    st.session_state.pin = 0000
if "account_balance" not in st.session_state:
    st.session_state.account_balance = 100000
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "login"
if "account_type" not in st.session_state:
    st.session_state.account_type = "Savings"
if "transaction" not in st.session_state:
    st.session_state.transaction = "Withdraw"
if "int_amount" not in st.session_state:
    st.session_state.int_amount = 0



def login_screen():
    left_col, center_col, right_col = st.columns([2, 2, 2])

    with center_col:
        st.markdown(
            """
            <div style="text-align: center;
            font-family: sans-serif;
            font-weight: Bold;
            padding: 60px;
            color: #FFFFFF">
            <h1 style="font-size:72px; letter-spacing: 3px"> LOGIN </h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        username = st.text_input("", label_visibility="visible", placeholder="Enter Username", max_chars=15)
        st.session_state.username = username
        pin = st.text_input("", placeholder="Enter 4 digit PIN", max_chars=4, type="password")
        st.session_state.pin = pin
        st.write("###")

        if st.button("Login", use_container_width=True):
            if username != "" and pin != "":
                if not pin.isdigit():
                    st.error("PIN must be numbers")
                elif len(pin) != 4:
                    st.error("PIN must be 4 digits")
                else:
                    st.session_state.pin = int(pin)
                    st.session_state.current_screen = "home"
                    st.rerun()











def home_screen():
    st.markdown("""
        <div style="text-align: center;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        font-family: sans-serif">
        <h1> ATM Simulator </h1>
        </div>
        """,
                unsafe_allow_html=True)

    left_col, center_col, right_col = st.columns([1, 2, 1])

    with left_col:
        st.write("### ")
        if st.button("Check Balance", use_container_width=True):
            st.session_state.current_screen = "balance"
            st.rerun()
        st.write("")
        if st.button("PIN change", use_container_width=True):
            st.session_state.current_screen = "pin_change"
            st.rerun()
        st.write("")
        if st.button("Exit", use_container_width=True):
            st.session_state.current_screen = "exit"
            st.rerun()

    with center_col:
        st.markdown(f"""
        <div style="text-align: center;
        padding: 30px;
        border-radius: 15px;
        ">
        <h2 style="color:#4ADE80;"> Welcome, {st.session_state.username}!</h2>
        <p2 style="font-size:18px;">Please select an option</p>
        </div>
        """,
        unsafe_allow_html=True
        )

    with right_col:
        st.write("### ")
        if st.button("Withdraw", use_container_width=True):
            st.session_state.current_screen = "withdraw"
            st.session_state.transaction = "Withdraw"
            st.rerun()
        st.write("")
        if st.button("Deposit", use_container_width=True):
            st.session_state.current_screen = "deposit"
            st.session_state.transaction = "Deposit"
            st.rerun()
        st.write("")
        if st.button("Mini Statement", use_container_width=True):
            st.session_state.current_screen = "mini_statement"
            st.rerun()


def withdraw():
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with left_col:
        pass
    with right_col:
        st.write("###")
        st.write("###")
        st.write("###")
        if st.button("Savings", use_container_width=True):
            st.session_state.current_screen = "enter_amount"
            st.session_state.account_type = "Savings"
            st.rerun()
        st.write("")
        if st.button("Current", use_container_width=True):
            st.session_state.current_screen = "enter_amount"
            st.session_state.account_type = "Current"
            st.rerun()

def enter_amount():
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with right_col:
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        if st.button("Home", use_container_width=True):
            st.session_state.current_screen = "home"
            st.rerun()
    with center_col:
        st.write("###")
        st.write("###")
        st.markdown("""
                <div style="text-align: center;
                color: #FFFFFF;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
                font-family: sans-serif">
                <h2> Enter Amount </h2>
                <p> Enter  amount  in  100's,  200's,  500's  </p>
                </div>
                """,
                unsafe_allow_html=True
        )
        amount = st.text_input("", key="enter_withdraw_amount")
        if amount == "":
            pass
        elif not amount.isdigit():
            st.error("Enter numbers only.")
        else:
            st.session_state.int_amount = int(amount)

            if st.session_state.int_amount % 100 != 0:
                st.error("Invalid amount entered.")

            elif st.session_state.int_amount > st.session_state.account_balance:
                st.error("Insufficient funds.")

            elif st.session_state.int_amount == 0:
                st.error("Withdrawal amount cannot be zero.")

            else:
                st.success("Amount entered successfully.")
                st.session_state.account_balance -= st.session_state.int_amount
                st.session_state.current_screen = "atm_receipt"
                st.rerun()


def atm_receipt():
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with right_col:
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        if st.button("Home", use_container_width=True):
            st.session_state.current_screen = "home"
            st.rerun()
    with center_col:
        st.markdown(f"""
                        <div style="text-align: center;
                        color: #FFFFFF;
                        font-size: 20px;
                        padding: 15px;
                        border-radius: 10px;
                        font-family: sans-serif">
                        <h1> ___________________ </h1>
                        <h2> ATM Receipt </h2>
                        <p>Transaction&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp; {st.session_state.transaction}</p>
                        <p>Account&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{st.session_state.account_type}</p>
                        <p>Amount&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{st.session_state.int_amount}</p>
                        <p>Balance&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{st.session_state.account_balance}</p>
                        <p>Transaction ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RRN482910583921</p>
                        <p></p>
                        <h3>Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                        &nbsp;&nbsp;&nbsp;&nbsp;SUCCESS✅</h3>
                        <h1> ___________________ </h1>
                        </div>
                        """,
                    unsafe_allow_html=True

                    )


def deposit():
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with center_col:
        st.write("###")
        st.write("###")
        st.markdown("""
                <div style="text-align: center;
                color: #FFFFFF;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
                font-family: sans-serif">
                <h2> Enter Deposit Amount </h2>
                <p> Enter  amount  in  100's,  200's,  500's  </p>
                </div>
                """,
                unsafe_allow_html=True
        )
        amount = st.text_input("", key="enter_deposit_amount")
        if amount == "":
            pass
        elif not amount.isdigit():
            st.error("Enter numbers only.")
        else:
            st.session_state.int_amount = int(amount)

            if st.session_state.int_amount % 100 != 0:
                st.error("Invalid amount entered.")

            elif st.session_state.int_amount == 0:
                st.error("Deposit amount cannot be zero.")

            else:
                st.success("Amount entered successfully.")
                st.session_state.account_balance += st.session_state.int_amount
                st.session_state.current_screen = "atm_receipt"
                st.rerun()

def check_balance():
    st.write("###")
    st.write("###")
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with right_col:
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        st.write("###")
        if st.button("Home", use_container_width=True):
            st.session_state.current_screen = "home"
            st.rerun()

    with center_col:
        st.markdown(f"""
                    <div style="text-align: center;
                    color: #FFFFFF;
                    padding: 15px;
                    border-radius: 10px;
                    font-family: sans-serif">
                    <h1> Account Balance </h1>
                    <p></p>
                    <h1> {st.session_state.account_balance}/- </h1>
                    </div>
                    """,
                    unsafe_allow_html=True)


if st.session_state.current_screen == "login":
    login_screen()

elif st.session_state.current_screen == "home":
    home_screen()

elif st.session_state.current_screen == "withdraw":
    withdraw()

elif st.session_state.current_screen == "enter_amount":
    enter_amount()

elif st.session_state.current_screen == "atm_receipt":
    atm_receipt()

elif st.session_state.current_screen == "deposit":
    deposit()

elif st.session_state.current_screen == "balance":
    check_balance()






