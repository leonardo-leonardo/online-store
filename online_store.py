import streamlit as st
import random

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="🛒 Mega Store NT$", layout="wide", page_icon="🛍️")

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
.product-card {
  background: #fff;
  border-radius: 14px;
  padding: 12px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
  height: 100%;
}
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}
.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}
.price {
  color: #007bff;
  font-weight: bold;
  margin-top: 4px;
}
.add-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
.add-btn:hover {
  background: #005ecb;
}
.top-cart-bar {
  position: sticky;
  top: 0;
  background: white;
  z-index: 100;
  padding: 10px 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# PRODUCT DATA
# ---------------------------
PRODUCTS = [
    # Electronics
    {"name": "Wireless Earbuds", "category": "Electronics", "price": 890, "image": "https://images.pexels.com/photos/373945/pexels-photo-373945.jpeg"},
    {"name": "Smart Watch", "category": "Electronics", "price": 1590, "image": "https://images.pexels.com/photos/190819/pexels-photo-190819.jpeg"},
    {"name": "Laptop", "category": "Electronics", "price": 18990, "image": "https://images.pexels.com/photos/18105/pexels-photo.jpg"},
    {"name": "Bluetooth Speaker", "category": "Electronics", "price": 1290, "image": "https://images.pexels.com/photos/63703/speaker-portable-bluetooth-sound-63703.jpeg"},
    {"name": "Power Bank", "category": "Electronics", "price": 690, "image": "https://images.pexels.com/photos/4386397/pexels-photo-4386397.jpeg"},

    # Stationery
    {"name": "Notebook", "category": "Stationery", "price": 120, "image": "https://images.pexels.com/photos/4144221/pexels-photo-4144221.jpeg"},
    {"name": "Gel Pen", "category": "Stationery", "price": 35, "image": "https://images.pexels.com/photos/3727487/pexels-photo-3727487.jpeg"},
    {"name": "Highlighter Set", "category": "Stationery", "price": 90, "image": "https://images.pexels.com/photos/5699475/pexels-photo-5699475.jpeg"},
    {"name": "Sticky Notes", "category": "Stationery", "price": 60, "image": "https://images.pexels.com/photos/4712407/pexels-photo-4712407.jpeg"},

    # Accessories
    {"name": "Backpack", "category": "Accessories", "price": 890, "image": "https://images.pexels.com/photos/1684075/pexels-photo-1684075.jpeg"},
    {"name": "Wallet", "category": "Accessories", "price": 590, "image": "https://images.pexels.com/photos/1080628/pexels-photo-1080628.jpeg"},
    {"name": "Sunglasses", "category": "Accessories", "price": 350, "image": "https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg"},
    {"name": "Leather Belt", "category": "Accessories", "price": 480, "image": "https://images.pexels.com/photos/165529/pexels-photo-165529.jpeg"},

    # Clothing
    {"name": "T-shirt", "category": "Clothing", "price": 250, "image": "https://images.pexels.com/photos/2983464/pexels-photo-2983464.jpeg"},
    {"name": "Jeans", "category": "Clothing", "price": 780, "image": "https://images.pexels.com/photos/4041682/pexels-photo-4041682.jpeg"},
    {"name": "Sneakers", "category": "Clothing", "price": 1190, "image": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg"},
    {"name": "Socks", "category": "Clothing", "price": 90, "image": "https://images.pexels.com/photos/1859483/pexels-photo-1859483.jpeg"},
    {"name": "Jacket", "category": "Clothing", "price": 990, "image": "https://images.pexels.com/photos/1124465/pexels-photo-1124465.jpeg"},

    # Kitchen
    {"name": "Ceramic Mug", "category": "Kitchen", "price": 180, "image": "https://images.pexels.com/photos/585750/pexels-photo-585750.jpeg"},
    {"name": "Blender", "category": "Kitchen", "price": 1290, "image": "https://images.pexels.com/photos/4040675/pexels-photo-4040675.jpeg"},
    {"name": "Frying Pan", "category": "Kitchen", "price": 590, "image": "https://images.pexels.com/photos/1435895/pexels-photo-1435895.jpeg"},
    {"name": "Cooking Pot", "category": "Kitchen", "price": 820, "image": "https://images.pexels.com/photos/5638215/pexels-photo-5638215.jpeg"},

    # Sports
    {"name": "Running Shoes", "category": "Sports", "price": 1690, "image": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg"},
    {"name": "Yoga Mat", "category": "Sports", "price": 520, "image": "https://images.pexels.com/photos/4056723/pexels-photo-4056723.jpeg"},
    {"name": "Water Bottle", "category": "Sports", "price": 240, "image": "https://images.pexels.com/photos/1546896/pexels-photo-1546896.jpeg"},
    {"name": "Football", "category": "Sports", "price": 450, "image": "https://images.pexels.com/photos/47730/the-ball-stadion-football-the-pitch-47730.jpeg"},

    # Toys
    {"name": "Teddy Bear", "category": "Toys", "price": 390, "image": "https://images.pexels.com/photos/207891/pexels-photo-207891.jpeg"},
    {"name": "Toy Car", "category": "Toys", "price": 160, "image": "https://images.pexels.com/photos/163743/pexels-photo-163743.jpeg"},
    {"name": "Building Blocks", "category": "Toys", "price": 290, "image": "https://images.pexels.com/photos/163743/pexels-photo-163743.jpeg"},
    {"name": "Board Game", "category": "Toys", "price": 450, "image": "https://images.pexels.com/photos/411207/pexels-photo-411207.jpeg"},

    # Home
    {"name": "Table Lamp", "category": "Home", "price": 480, "image": "https://images.pexels.com/photos/1121123/pexels-photo-1121123.jpeg"},
    {"name": "Blanket", "category": "Home", "price": 620, "image": "https://images.pexels.com/photos/1454806/pexels-photo-1454806.jpeg"},
    {"name": "Rug", "category": "Home", "price": 780, "image": "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg"},
    {"name": "Candle Set", "category": "Home", "price": 360, "image": "https://images.pexels.com/photos/695970/pexels-photo-695970.jpeg"},
]

# ---------------------------
# CART SYSTEM
# ---------------------------
if 'cart' not in st.session_state:
    st.session_state['cart'] = []
if 'cart_open' not in st.session_state:
    st.session_state['cart_open'] = False

def add_to_cart(pid, qty=1):
    prod = next((p for p in PRODUCTS if p['name'] == pid), None)
    if not prod:
        return
    existing = next((c for c in st.session_state['cart'] if c['name'] == pid), None)
    if existing:
        existing['qty'] += qty
    else:
        st.session_state['cart'].append({
            "name": prod['name'],
            "price": prod['price'],
            "qty": qty
        })

def summarize_cart():
    subtotal = sum(i['price'] * i['qty'] for i in st.session_state['cart'])
    discount = subtotal * 0.05 if subtotal > 5000 else 0
    tax = (subtotal - discount) * 0.05
    shipping = 0 if subtotal > 3000 else 150
    total = subtotal - discount + tax + shipping
    return {"subtotal": subtotal, "discount": discount, "tax": tax, "shipping": shipping, "total": total}

# ---------------------------
# UI - TOP BAR
# ---------------------------
cs = summarize_cart()
st.markdown(f"""
<div class="top-cart-bar">
  <div><b>🛍️ Mega Store NT$</b> — {len(PRODUCTS)} Items</div>
  <button class="add-btn" onclick="window.location.reload()">🔄 Refresh</button>
  <button class="add-btn">🛒 Cart ({len(st.session_state['cart'])}) — NT${int(cs['total'])}</button>
</div>
""", unsafe_allow_html=True)

if st.button(f"🛒 View Cart ({len(st.session_state['cart'])})"):
    st.session_state['cart_open'] = not st.session_state['cart_open']

if st.session_state['cart_open']:
    with st.expander(f"🛒 Your Cart ({len(st.session_state['cart'])} items)", expanded=True):
        if not st.session_state['cart']:
            st.info("Your cart is empty.")
        else:
            for item in st.session_state['cart']:
                c1, c2, c3 = st.columns([3, 2, 1])
                c1.write(item['name'])
                qty = c2.number_input("Qty", 1, 99, item['qty'], key=f"qty_{item['name']}")
                if qty != item['qty']:
                    item['qty'] = qty
                if c3.button("❌ Remove", key=f"rem_{item['name']}"):
                    st.session_state['cart'] = [x for x in st.session_state['cart'] if x['name'] != item['name']]
                    st.experimental_rerun()
            cs = summarize_cart()
            st.write(f"Subtotal: NT${int(cs['subtotal'])}")
            st.write(f"Discount: -NT${int(cs['discount'])}")
            st.write(f"Tax: NT${int(cs['tax'])}")
            st.write(f"Shipping: NT${int(cs['shipping'])}")
            st.markdown(f"### **Total: NT${int(cs['total'])}**")
            if st.button("✅ Checkout"):
                st.success("Order placed successfully! Thank you!")
                st.session_state['cart'].clear()

# ---------------------------
# FILTERS
# ---------------------------
st.markdown("### 🔍 Filters")
search = st.text_input("Search products")
category = st.selectbox("Category", ["All"] + sorted(list(set(p["category"] for p in PRODUCTS))))
prices = [p['price'] for p in PRODUCTS]
min_price, max_price = st.slider("Price range (NT$)", 0, int(max(prices)), (0, int(max(prices))), step=100)

# Filter logic
filtered = PRODUCTS
if search:
    filtered = [p for p in filtered if search.lower() in p['name'].lower()]
if category != "All":
    filtered = [p for p in filtered if p['category'] == category]
filtered = [p for p in filtered if min_price <= p['price'] <= max_price]

# ---------------------------
# DISPLAY PRODUCTS
# ---------------------------
COLUMNS = 4
cols = st.columns(COLUMNS)
i = 0
for prod in filtered:
    with cols[i]:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(prod['image'], use_column_width=True)
        st.markdown(f"**{prod['name']}**")
        st.caption(prod['category'])
        st.markdown(f"<div class='price'>NT${prod['price']}</div>", unsafe_allow_html=True)
        qty_key = f"q_{prod['name']}"
        qty = st.number_input("Qty", min_value=1, value=1, key=qty_key, label_visibility="collapsed")
        if st.button("Add to Cart", key=f"add_{prod['name']}"):
            add_to_cart(prod['name'], qty)
            st.success(f"Added {qty} × {prod['name']} to cart.")
        st.markdown("</div>", unsafe_allow_html=True)
    i = (i + 1) % COLUMNS
    if i == 0:
        cols = st.columns(COLUMNS)
