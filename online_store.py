# convenience_store_50_final.py
import streamlit as st
import re

st.set_page_config(page_title="🛒 Convenience Store (50 items)", layout="wide", page_icon="🛍️")

COLUMNS = 4

# ---------------------------
# UTILITIES
# ---------------------------
def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s

def placeholder_image_for(name: str) -> str:
    slug = slugify(name)
    return f"https://picsum.photos/seed/{slug}/600/400"

# ---------------------------
# PRODUCTS
# ---------------------------
PRODUCTS = [
    {"id":"c001","name":"Classic Ballpoint Pen","category":"Stationery","price":25,
     "image":"https://th.bing.com/th/id/R.cb4aee1c689dbe892c081f77bed24ab4?rik=Ox67o%2b1d%2f7AQag&pid=ImgRaw&r=0"},
    {"id":"c002","name":"Notebook A5 Ruled","category":"Stationery","price":120,
     "image":"https://th.bing.com/th/id/OIP.Slqd7KcvFd9qNHsZKyLnVQHaGP?o=7&cb=ucfimg2rm=3&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
    {"id":"c003","name":"Sticky Note Pack","category":"Stationery","price":60,
     "image":"https://th.bing.com/th/id/OIP.cwm_7SCYy0aBSS97RjAfNgHaFM?o=7&cb=ucfimg2rm=3&ucfimg=1&rs=1&pid=ImgDetMain&o=7&rm=3"},
]

# Add remaining 47 products with placeholder images
names_categories_prices = [
    ("Highlighter Set (4)","Stationery",95),
    ("Mechanical Pencil 0.5mm","Stationery",85),
    ("Cozy Knit Socks (3 Pairs)","Clothing",150),
    ("Everyday Cotton T-shirt","Clothing",280),
    ("Lightweight Windbreaker","Clothing",990),
    ("Classic Baseball Cap","Clothing",220),
    ("Comfort Flip-flops","Clothing",180),
    ("Insulated Travel Mug","Kitchen",420),
    ("Ceramic Coffee Mug","Kitchen",180),
    ("2-slice Toaster","Kitchen",990),
    ("Chef's Spatula Set","Kitchen",240),
    ("Non-stick Frypan 26cm","Kitchen",680),
    ("USB-C Fast Charger","Electronics",390),
    ("Compact Power Bank 10000mAh","Electronics",820),
    ("Wireless Earbuds Basic","Electronics",990),
    ("Portable Bluetooth Speaker","Electronics",1290),
    ("LED Desk Lamp","Electronics",760),
    ("Reusable Water Bottle 500ml","Home",260),
    ("Scented Candle (3-pack)","Home",360),
    ("Microfiber Dish Cloths (5)","Home",140),
    ("Compact Storage Box","Home",320),
    ("Soft Throw Blanket","Home",580),
    ("Everyday Backpack 20L","Accessories",1490),
    ("Slim Card Wallet","Accessories",420),
    ("Travel Umbrella Compact","Accessories",320),
    ("Key Organizer Multi-tool","Accessories",260),
    ("Phone Case Clear Fit","Accessories",290),
    ("Running Shoes Lightweight","Sports",1990),
    ("Yoga Mat Non-slip","Sports",520),
    ("Sports Sweatband","Sports",110),
    ("Tennis Racket Beginner","Sports",1390),
    ("Compact Jump Rope","Sports",210),
    ("Kids Puzzle 100pcs","Toys",260),
    ("Mini Remote Car","Toys",690),
    ("Plush Teddy Bear Medium","Toys",420),
    ("Coloring Crayon Pack","Toys",150),
    ("Stacking Blocks Set","Toys",340),
    ("Face Mask 50pcs","Health",250),
    ("Hand Sanitizer 250ml","Health",180),
    ("First Aid Compact Kit","Health",490),
    ("Vitamin C Chewables","Health",320),
    ("Thermal Reusable Ice Pack","Health",210),
    ("Office Desk Calendar 2026","Stationery",240),
    ("Rechargeable LED Keylight","Electronics",330),
    ("Compact Sewing Kit","Home",140),
    ("Portable Shoe Cleaning Kit","Home",200),
    ("Reusable Grocery Tote (2)","Accessories",160)
]

for i, (name, cat, price) in enumerate(names_categories_prices):
    pid = f"c{4+i:03d}"
    PRODUCTS.append({"id":pid,"name":name,"category":cat,"price":price,"image":placeholder_image_for(name)})

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
st.title("🛒 Convenience Store (50 Items)")

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
