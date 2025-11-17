import streamlit as st

# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------
st.set_page_config(page_title="Common Store", layout="wide")

st.markdown("""
    <style>
        .product-card {
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 15px;
            background: #ffffff;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .cart-button {
            background-color: #ff9900;
            padding: 10px 18px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 700;
            color: black;
        }
        .checkout-btn {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            width: 100%;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "show_cart" not in st.session_state:
    st.session_state.show_cart = False

if "order_message" not in st.session_state:
    st.session_state.order_message = None


# -------------------------------------------------
# PRODUCTS
# -------------------------------------------------
PRODUCTS = [
    ("Classic Ballpoint Pen", "https://th.bing.com/th/id/R.cb4aee1c689dbe892c081f77bed24ab4?rik=Ox67o%2b1d%2f7AQag&pid=ImgRaw&r=0", 25),
    ("Notebook A5 Ruled", "https://th.bing.com/th/id/OIP.Slqd7KcvFd9qNHsZKyLnVQHaGP?rs=1&pid=ImgDetMain", 55),
    ("Sticky Note Pack", "https://th.bing.com/th/id/OIP.cwm_7SCYy0aBSS97RjAfNgHaFM?rs=1&pid=ImgDetMain", 30),
    ("Highlighter Set (4)", "https://th.bing.com/th/id/OIP.b_YQ1kPRO4PN4m1iFO5yFAHaHa?rs=1&pid=ImgDetMain", 45),
    ("Mechanical Pencil 0.5mm", "https://th.bing.com/th/id/OIP.Jq7xQPBZAXqs9xlz-Iw0fAHaHa?rs=1&pid=ImgDetMain", 40),
    ("Cozy Knit Socks (3 Pairs)", "https://tse1.mm.bing.net/th/id/OIP.zJb_59YSs8dS-yqhsxnSYwHaGT?rs=1&pid=ImgDetMain", 75),
    ("Everyday Cotton T-shirt", "https://tse2.mm.bing.net/th/id/OIP.uOktto4M5ejy6b0RIiiNBAHaIc?rs=1&pid=ImgDetMain", 150),
    ("Lightweight Windbreaker", "https://tse1.mm.bing.net/th/id/OIP.8W6syRyqiZN2RBwYykI3RwHaIo?rs=1&pid=ImgDetMain", 320),
    ("Classic Baseball Cap", "https://tse1.mm.bing.net/th/id/OIP.gS2WiHOUyw5mV5cfU_R8qgHaHa?rs=1&pid=ImgDetMain", 110),
    ("Comfort Flip-flops", "https://tse3.mm.bing.net/th/id/OIP.w0bIOKTROYzYouSxxSiuawHaE1?rs=1&pid=ImgDetMain", 90),
]


# -------------------------------------------------
# NAVIGATION BAR
# -------------------------------------------------
cols = st.columns([6, 1])

with cols[0]:
    st.markdown("## 🏪 **Common Store — Everything You Need**")

with cols[1]:
    if st.button("🛒 Cart", key="cart_btn"):
        st.session_state.show_cart = not st.session_state.show_cart


# -------------------------------------------------
# CHECKOUT SUCCESS MESSAGE
# -------------------------------------------------
if st.session_state.order_message:
    st.success(st.session_state.order_message)


# -------------------------------------------------
# CART PANEL
# -------------------------------------------------
if st.session_state.show_cart:
    st.markdown("### 🛒 Your Cart")
    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item[0]} — NT$ {item[2]}")
            total += item[2]

        st.write(f"### **Total: NT$ {total}**")
        if st.button("✅ Checkout", key="checkout"):
            st.session_state.cart = []
            st.session_state.order_message = "🎉 Your order is sent. Thank you for your shopping!"
            st.session_state.show_cart = False


st.markdown("---")


# -------------------------------------------------
# PRODUCT LIST (single page)
# -------------------------------------------------
st.markdown("### 🛍️ Items Available")

grid_cols = st.columns(3)

index = 0
for name, img, price in PRODUCTS:
    with grid_cols[index % 3]:
        st.markdown(f"""
            <div class='product-card'>
                <img src="{img}" width="180"><br><br>
                <strong>{name}</strong><br>
                <span style='font-size:18px;'>NT$ {price}</span><br><br>
            </div>
        """, unsafe_allow_html=True)

        if st.button(f"Add to cart {name}", key=f"add_{name}"):
            st.session_state.cart.append((name, img, price))

    index += 1
