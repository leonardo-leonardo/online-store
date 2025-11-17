import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- PAGE SETUP ---
st.set_page_config(page_title="🛍️ Online Store", layout="wide")

# --- SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []

if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if "last_added" not in st.session_state:
    st.session_state.last_added = None

if "order_sent" not in st.session_state:
    st.session_state.order_sent = False

# --- ITEMS ---
items = [
    {
        "name": "Classic Ballpoint Pen",
        "price": 39,
        "img": "https://th.bing.com/th/id/R.cb4aee1c689dbe892c081f77bed24ab4?rik=Ox67o%2b1d%2f7AQag&pid=ImgRaw&r=0"
    },
    {
        "name": "Notebook A5 Ruled",
        "price": 89,
        "img": "https://th.bing.com/th/id/OIP.Slqd7KcvFd9qNHsZKyLnVQHaGP?rs=1&pid=ImgDetMain"
    },
    {
        "name": "Sticky Note Pack",
        "price": 59,
        "img": "https://th.bing.com/th/id/OIP.cwm_7SCYy0aBSS97RjAfNgHaFM?rs=1&pid=ImgDetMain"
    },
    {
        "name": "Highlighter Set (4)",
        "price": 79,
        "img": "https://th.bing.com/th/id/OIP.b_YQ1kPRO4PN4m1iFO5yFAHaHa?rs=1&pid=ImgDetMain"
    },
    {
        "name": "Mechanical Pencil 0.5mm",
        "price": 49,
        "img": "https://th.bing.com/th/id/OIP.Jq7xQPBZAXqs9xlz-Iw0fAHaHa?rs=1&pid=ImgDetMain"
    },
]

# --- HEADER ---
st.title("🛒 Super Clean Online Store")

# --- CART BUTTON ---
st.markdown("### 🛍️ Your Shopping Cart")
cart_expander = st.expander(f"🛒 Cart ({len(st.session_state.cart)} items)", expanded=True)

# --- CART UI ---
with cart_expander:
    if st.session_state.cart:
        total = sum(x["price"] for x in st.session_state.cart)

        for c in st.session_state.cart:
            st.write(f"• **{c['name']}** — NT${c['price']}")

        st.markdown(f"### 💰 Total: **NT${total}**")

        payment_method = st.radio(
            "Select your payment method:",
            ["Credit Card", "Apple Pay", "Line Pay", "Bank Transfer", "Cash on Delivery"],
        )

        if st.button("✔️ Checkout", use_container_width=True):
            st.session_state.cart = []
            st.session_state.order_sent = True
            st.success("🎉 Your order is sent. Thank you for your shopping!")
            st.info(f"🧾 Payment Method: **{payment_method}**")
    else:
        st.write("Your cart is empty.")

# --- POPUP MODAL FOR ADD TO CART ---
if st.session_state.show_popup:
    st.info(f"🛒 **{st.session_state.last_added}** has been added to your cart!")

    if st.button("OK", key="popup_ok"):
        st.session_state.show_popup = False
        st.session_state.last_added = None

# --- MAIN STORE DISPLAY ---
st.write("### 🛍️ Choose Your Items")

cols = st.columns(3)
i = 0

for item in items:
    col = cols[i % 3]

    with col:
        try:
            img_data = requests.get(item["img"]).content
            img = Image.open(BytesIO(img_data))
            st.image(img, width=180)
        except:
            st.warning("Image not available")

        st.write(f"**{item['name']}**")
        st.write(f"💲 NT${item['price']}")

        if st.button(f"Add to Cart {item['name']}", key=item["name"]):
            st.session_state.cart.append(item)
            st.session_state.last_added = item["name"]
            st.session_state.show_popup = True

    i += 1

st.write("---")
st.caption("🛒Leonardo online store, V4.0")
