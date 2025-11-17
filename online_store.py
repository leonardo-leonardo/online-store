import streamlit as st

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="Online Store", layout="wide")
st.title("🛍️ Online Store")

# -------------------------
# SESSION STATE (CART)
# -------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

def add_to_cart(name, price):
    if name in st.session_state.cart:
        st.session_state.cart[name]["qty"] += 1
    else:
        st.session_state.cart[name] = {"price": price, "qty": 1}

def clear_cart():
    st.session_state.cart = {}

# -------------------------
# PRODUCT LIST (10 ITEMS)
# -------------------------
products = [
    {
        "name": "Classic Ballpoint Pen",
        "price": 25,
        "image": "https://th.bing.com/th/id/R.cb4aee1c689dbe892c081f77bed24ab4?rik=Ox67o%2b1d%2f7AQag&pid=ImgRaw&r=0",
    },
    {
        "name": "Notebook A5 Ruled",
        "price": 60,
        "image": "https://th.bing.com/th/id/OIP.Slqd7KcvFd9qNHsZKyLnVQHaGP?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Sticky Note Pack",
        "price": 35,
        "image": "https://th.bing.com/th/id/OIP.cwm_7SCYy0aBSS97RjAfNgHaFM?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Highlighter Set (4)",
        "price": 55,
        "image": "https://th.bing.com/th/id/OIP.b_YQ1kPRO4PN4m1iFO5yFAHaHa?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Mechanical Pencil 0.5mm",
        "price": 30,
        "image": "https://th.bing.com/th/id/OIP.Jq7xQPBZAXqs9xlz-Iw0fAHaHa?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Cozy Knit Socks (3 Pairs)",
        "price": 80,
        "image": "https://tse1.mm.bing.net/th/id/OIP.zJb_59YSs8dS-yqhsxnSYwHaGT?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Everyday Cotton T-shirt",
        "price": 120,
        "image": "https://tse2.mm.bing.net/th/id/OIP.uOktto4M5ejy6b0RIiiNBAHaIc?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Lightweight Windbreaker",
        "price": 250,
        "image": "https://tse1.mm.bing.net/th/id/OIP.8W6syRyqiZN2RBwYykI3RwHaIo?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Classic Baseball Cap",
        "price": 90,
        "image": "https://tse1.mm.bing.net/th/id/OIP.gS2WiHOUyw5mV5cfU_R8qgHaHa?rs=1&pid=ImgDetMain",
    },
    {
        "name": "Comfort Flip-flops",
        "price": 70,
        "image": "https://tse3.mm.bing.net/th/id/OIP.w0bIOKTROYzYouSxxSiuawHaE1?rs=1&pid=ImgDetMain",
    },
]

# -------------------------
# CART SUMMARY (IMPROVED UI)
# -------------------------
total_items = sum(item["qty"] for item in st.session_state.cart.values())
total_price = sum(item["qty"] * item["price"] for item in st.session_state.cart.values())

st.markdown(
    """
    <style>
        .cart-box {
            padding: 15px;
            background-color: #f0f7ff;
            border-radius: 10px;
            border: 1px solid #cce0ff;
            margin-bottom: 15px;
        }
        .cart-header {
            font-size: 22px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown(
        f"""
        <div class="cart-box">
            <div class="cart-header">🛒 Cart ({total_items} items) — <b>NT${total_price}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("📦 View Cart", expanded=True):
    if total_items == 0:
        st.write("Your cart is empty.")
    else:
        for name, info in st.session_state.cart.items():
            st.write(f"**{name}** × {info['qty']} — NT${info['qty'] * info['price']}")

        st.markdown("---")

        colA, colB = st.columns(2)

        with colA:
            if st.button("🧹 Clear Cart"):
                clear_cart()
                st.rerun()

        with colB:
            if st.button("💳 Checkout"):
                st.session_state.checkout = True
                st.rerun()

# -------------------------
# CHECKOUT PAGE
# -------------------------
if st.session_state.get("checkout", False):

    st.header("💳 Checkout")

    if total_items == 0:
        st.write("Your cart is empty.")
    else:
        st.subheader("Order Summary")
        for name, info in st.session_state.cart.items():
            st.write(f"{name} × {info['qty']} — NT${info['qty'] * info['price']}")

        st.write(f"### **Total: NT${total_price}**")

        name = st.text_input("Your Name")
        address = st.text_area("Shipping Address")
        payment = st.selectbox("Payment Method", ["Credit Card", "LINE Pay", "ATM Transfer", "Cash on Delivery"])

        if st.button("✅ Confirm Order"):
            st.success("🎉 Order placed successfully! Thank you!")
            clear_cart()
            st.session_state.checkout = False
            st.rerun()

    st.stop()

# -------------------------
# PRODUCT GRID
# -------------------------
st.subheader("🛒 Products")

cols = st.columns(3)

for i, product in enumerate(products):
    with cols[i % 3]:
        st.image(product["image"], use_column_width=True)
        st.markdown(f"### {product['name']}")
        st.write(f"💲 **NT${product['price']}**")

        if st.button(f"Add to Cart — {product['name']}", key=product["name"]):
            add_to_cart(product["name"], product["price"])
            st.rerun()
