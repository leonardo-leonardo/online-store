import streamlit as st

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Online Store", layout="wide")

st.markdown(
    """
    <style>
        .product-card {
            padding: 15px;
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e6e6e6;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            transition: 0.2s;
        }
        .product-card:hover {
            box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
        }
        .cart-box {
            padding: 15px;
            background-color: #eef6ff;
            border-radius: 10px;
            border: 1px solid #bcd9ff;
            margin-bottom: 15px;
        }
        .cart-header {
            font-size: 24px;
            font-weight: bold;
        }
        .checkout-box {
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e1e1e1;
            background: #fafafa;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
        }
        .success-box {
            padding: 20px;
            border-radius: 12px;
            background: #e7ffe7;
            border: 1px solid #9ce79c;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #1b6e1b;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# SESSION STATE
# -------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "checkout" not in st.session_state:
    st.session_state.checkout = False

if "order_complete" not in st.session_state:
    st.session_state.order_complete = False


def add_to_cart(name, price):
    if name in st.session_state.cart:
        st.session_state.cart[name]["qty"] += 1
    else:
        st.session_state.cart[name] = {"price": price, "qty": 1}


def clear_cart():
    st.session_state.cart = {}


# -------------------------
# PRODUCTS (FINAL 10)
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
# CART SUMMARY (BETTER UI)
# -------------------------
total_items = sum(item["qty"] for item in st.session_state.cart.values())
total_price = sum(item["qty"] * item["price"] for item in st.session_state.cart.values())

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
                st.session_state.order_complete = False
                st.rerun()


# -------------------------
# CHECKOUT PAGE
# -------------------------
if st.session_state.checkout:

    st.title("💳 Checkout")

    if total_items == 0:
        st.warning("Your cart is empty!")
        st.stop()

    st.markdown('<div class="checkout-box">', unsafe_allow_html=True)

    st.subheader("🧾 Order Summary")
    for name, info in st.session_state.cart.items():
        st.write(f"• {name} × {info['qty']} — NT${info['qty'] * info['price']}")

    st.write(f"### **Total: NT${total_price}**")

    st.subheader("👤 Customer Info")
    name = st.text_input("Name")
    address = st.text_area("Shipping Address")
    payment = st.selectbox("Payment Method", ["Credit Card", "LINE Pay", "ATM Bank Transfer", "Cash on Delivery"])

    if st.button("✅ Place Order"):
        if not name or not address:
            st.error("Please fill out all fields.")
        else:
            st.session_state.order_complete = True
            clear_cart()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# -------------------------
# SUCCESS MESSAGE PAGE
# -------------------------
if st.session_state.order_complete:

    st.markdown(
        """
        <div class="success-box">
            🎉 Your order is sent!  
            <br>Thank you for your shopping!
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.balloons()

    if st.button("🏬 Back to Store"):
        st.session_state.order_complete = False
        st.rerun()

    st.stop()


# -------------------------
# PRODUCT GRID
# -------------------------
st.subheader("🛒 Products")

cols = st.columns(3)

for i, product in enumerate(products):
    with cols[i % 3]:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        st.image(product["image"], use_column_width=True)
        st.markdown(f"### {product['name']}")
        st.write(f"💲 **NT${product['price']}**")

        if st.button(f"Add to Cart — {product['name']}", key=product["name"]):
            add_to_cart(product["name"], product["price"])
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
