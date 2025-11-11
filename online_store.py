# convenience_store_10_final.py
import streamlit as st

st.set_page_config(page_title="🛒 Convenience Store (10 items)", layout="wide", page_icon="🛍️")
COLUMNS = 4

# ---------------------------
# PRODUCTS (only 10)
# ---------------------------
PRODUCTS = [
    {"id":"c001","name":"Classic Ballpoint Pen","category":"Stationery","price":25,
     "image":"https://th.bing.com/th/id/R.cb4aee1c689dbe892c081f77bed24ab4?rik=Ox67o%2b1d%2f7AQag&pid=ImgRaw&r=0"},
    {"id":"c002","name":"Notebook A5 Ruled","category":"Stationery","price":120,
     "image":"https://th.bing.com/th/id/OIP.Slqd7KcvFd9qNHsZKyLnVQHaGP?o=7&cb=ucfimg2rm=3&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c003","name":"Sticky Note Pack","category":"Stationery","price":60,
     "image":"https://th.bing.com/th/id/OIP.cwm_7SCYy0aBSS97RjAfNgHaFM?o=7&cb=ucfimg2rm=3&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c004","name":"Highlighter Set (4)","category":"Stationery","price":95,
     "image":"https://th.bing.com/th/id/OIP.b_YQ1kPRO4PN4m1iFO5yFAHaHa?o=7&cb=ucfimg2rm=3&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c005","name":"Mechanical Pencil 0.5mm","category":"Stationery","price":85,
     "image":"https://th.bing.com/th/id/OIP.Jq7xQPBZAXqs9xlz-Iw0fAHaHa?o=7&cb=ucfimg2rm=3&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c006","name":"Cozy Knit Socks (3 Pairs)","category":"Clothing","price":150,
     "image":"https://tse1.mm.bing.net/th/id/OIP.zJb_59YSs8dS-yqhsxnSYwHaGT?cb=ucfimg2ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c007","name":"Everyday Cotton T-shirt","category":"Clothing","price":280,
     "image":"https://tse2.mm.bing.net/th/id/OIP.uOktto4M5ejy6b0RIiiNBAHaIc?cb=ucfimg2ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c008","name":"Lightweight Windbreaker","category":"Clothing","price":990,
     "image":"https://tse1.mm.bing.net/th/id/OIP.8W6syRyqiZN2RBwYykI3RwHaIo?cb=ucfimg2ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c009","name":"Classic Baseball Cap","category":"Clothing","price":220,
     "image":"https://tse1.mm.bing.net/th/id/OIP.gS2WiHOUyw5mV5cfU_R8qgHaHa?cb=ucfimg2ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c010","name":"Comfort Flip-flops","category":"Clothing","price":180,
     "image":"https://tse3.mm.bing.net/th/id/OIP.w0bIOKTROYzYouSxxSiuawHaE1?cb=ucfimg2ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
]

# ---------------------------
# SESSION STATE
# ---------------------------
if 'cart' not in st.session_state: st.session_state['cart'] = []

def add_to_cart(prod_id, qty=1):
    prod = next((p for p in PRODUCTS if p['id']==prod_id), None)
    if not prod: return
    found = next((c for c in st.session_state['cart'] if c['id']==prod_id), None)
    if found:
        found['qty'] += qty
    else:
        st.session_state['cart'].append({"id":prod_id,"name":prod['name'],"price":prod['price'],"qty":qty})

# ---------------------------
# DISPLAY
# ---------------------------
st.title("🛒 Convenience Store (10 Items)")

# Cart summary
total_items = sum(c['qty'] for c in st.session_state['cart'])
total_price = sum(c['qty']*c['price'] for c in st.session_state['cart'])
st.sidebar.header(f"🛍️ Cart ({total_items} items) - NT${total_price}")
with st.sidebar.expander("View Cart", expanded=True):
    if st.session_state['cart']:
        for c in st.session_state['cart']:
            st.write(f"{c['name']} x {c['qty']} = NT${c['qty']*c['price']}")
    else:
        st.info("Cart is empty.")

# Filter
search = st.text_input("Search products by name")

# Display products in grid
cols = st.columns(COLUMNS)
for i, p in enumerate(PRODUCTS):
    if search and search.lower() not in p['name'].lower():
        continue
    col = cols[i%COLUMNS]
    with col:
        st.image(p['image'], use_column_width=True)
        st.write(f"**{p['name']}**")
        st.write(f"Category: {p['category']}")
        st.write(f"NT${p['price']}")
        qty = st.number_input("Qty", min_value=1, value=1, key=f"qty_{p['id']}", label_visibility="collapsed")
        if st.button("Add to Cart", key=f"add_{p['id']}"):
            add_to_cart(p['id'], qty)
            st.success(f"Added {qty} x {p['name']} to cart")
