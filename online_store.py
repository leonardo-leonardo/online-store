import streamlit as st
import random
from PIL import Image
import requests
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="🛍️ Online Store", layout="wide")
st.title("🛒 Welcome to the Online Store")

# --- SESSION STATE INITIALIZATION ---
if "cart" not in st.session_state:
    st.session_state.cart = []
if "order_sent" not in st.session_state:
    st.session_state.order_sent = False

# --- ITEM DATA ---
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

# --- SIDEBAR CART UI ---
st.sidebar.header("🛍️ Your Cart")
for c in st.session_state.cart:
    st.sidebar.write(f"• {c['name']} — ${c['price']}")

if st.session_state.cart:
    total = sum([c['price'] for c in st.session_state.cart])
    st.sidebar.subheader(f"Total: ${total}")

    if st.sidebar.button("✔️ Checkout", use_container_width=True):
        st.session_state.order_sent = True
        st.session_state.cart = []
        st.experimental_rerun()

# --- ORDER CONFIRMATION MESSAGE ---
if st.session_state.order_sent:
    st.success("🎉 Your order is sent! Thank you for your shopping.")
    st.info("We appreciate your purchase. Your items will be delivered soon!")

# --- MAIN UI LAYOUT ---
st.write("### ✨ Choose your items below")

cols = st.columns(3)
col_index = 0

for item in items:
    with cols[col_index]:
        try:
            response = requests.get(item["img"])
            img = Image.open(BytesIO(response.content))
            st.image(img, width=180)
        except:
            st.warning("Image unavailable")

        st.write(f"**{item['name']}**")
        st.write(f"💲 Price: ${item['price']}")

        if st.button(f"Add to Cart: {item['name']}", key=item['name']):
            st.session_state.cart.append(item)
            st.toast(f"Added {item['name']} to cart!", icon="🛒")
            st.experimental_rerun()

    col_index = (col_index + 1) % 3

st.write("---")
st.caption("Enhanced UI • Clean Layout • Instant Checkout Messages • v1.2")
