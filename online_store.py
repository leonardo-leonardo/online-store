import streamlit as st
import random

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="🛒 Mega Store NT$", layout="wide", page_icon="🛍️")
NUM_ITEMS = 200
COLUMNS = 4

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
.product-card {
  background: #fff;
  border-radius: 12px;
  padding: 10px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
  height: 100%;
}
.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}
.product-image {
  width: 100%;
  height: 180px;
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
# DATA
# ---------------------------
CATEGORIES = ["Electronics", "Stationery", "Accessories", "Clothing", "Kitchen", "Sports", "Toys", "Home"]

IMAGE_URLS = {
    "Electronics": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg",
    "Stationery": "https://images.pexels.com/photos/4144923/pexels-photo-4144923.jpeg",
    "Accessories": "https://images.pexels.com/photos/322207/pexels-photo-322207.jpeg",
    "Clothing": "https://images.pexels.com/photos/2983464/pexels-photo-2983464.jpeg",
    "Kitchen": "https://images.pexels.com/photos/2762247/pexels-photo-2762247.jpeg",
    "Sports": "https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg",
    "Toys": "https://images.pexels.com/photos/3662663/pexels-photo-3662663.jpeg",
    "Home": "https://images.pexels.com/photos/1571459/pexels-photo-1571459.jpeg",
}

NAME_POOLS = {
    "Electronics": ["VoltPro Charger", "EchoBeam Speaker", "NovaScreen Monitor", "PulseSmart Watch", "AeroBuds Earphones", "ByteTab Tablet", "SkyCam Drone", "PowerLink Cable"],
    "Stationery": ["CloudPen Gel", "TaskMaster Planner", "Inkwell Fountain Pen", "UltraNote Pad", "PaperMate Journal", "SketchPro Marker", "SharpEdge Scissors"],
    "Accessories": ["UrbanFlow Backpack", "SnapGrip Wallet", "SolarTime Watch", "PureLeather Belt", "KeyMate Organizer", "ComfyCap Hat", "PolarShades Glasses"],
    "Clothing": ["AeroFit T-shirt", "BreezeJog Pants", "ComfyCrew Hoodie", "StreetWave Jacket", "UrbanWalk Shoes", "DailyFit Shorts"],
    "Kitchen": ["AquaBlend Mixer", "ChefMate Knife Set", "SteamEase Kettle", "SmartPan Fryer", "PureTaste Mug", "SpiceJoy Rack"],
    "Sports": ["SwiftRun Shoes", "PowerGrip Gloves", "HydroFlex Bottle", "StaminaPro Rope", "FlexTrack Yoga Mat", "CoreStrength Dumbbells"],
    "Toys": ["BuildPro Blocks", "RoboBuddy Bot", "MagicPuzzle Cube", "SpeedDrift Car", "AeroPlane Toy", "GigaBear Plush"],
    "Home": ["GlowLite Lamp", "PureAir Diffuser", "ComfyCotton Pillow", "DreamWeave Blanket", "SmartTemp Fan", "AromaCandle Set"]
}

def generate_products(num_items=NUM_ITEMS):
    products = []
    id_counter = 1
    while len(products) < num_items:
        for cat in CATEGORIES:
            base = random.choice(NAME_POOLS[cat])
            variant = random.choice(["", " Mini", " Pro", " X", " Plus"])
            name = base + variant
            price = int(random.uniform(200, 7000) * 0.85)  # cheaper realistic NT$
            img = IMAGE_URLS[cat]
            products.append({
                "id": f"item-{id_counter}",
                "name": name,
                "category": cat,
                "price": price,
                "image": img
            })
            id_counter += 1
            if len(products) >= num_items:
                break
    return products

if 'products' not in st.session_state:
    st.session_state['products'] = generate_products()

PRODUCTS = st.session_state['products']

# ---------------------------
# CART
# ---------------------------
if 'cart' not in st.session_state:
    st.session_state['cart'] = []
if 'cart_open' not in st.session_state:
    st.session_state['cart_open'] = False

def add_to_cart(pid, qty=1):
    prod = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not prod:
        return
    existing = next((c for c in st.session_state['cart'] if c['id'] == pid), None)
    if existing:
        existing['qty'] += qty
    else:
        st.session_state['cart'].append({
            "id": pid,
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
# TOP BAR
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
                qty = c2.number_input("Qty", 1, 99, item['qty'], key=f"qty_{item['id']}")
                if qty != item['qty']:
                    item['qty'] = qty
                if c3.button("❌ Remove", key=f"rem_{item['id']}"):
                    st.session_state['cart'] = [x for x in st.session_state['cart'] if x['id'] != item['id']]
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
category = st.selectbox("Category", ["All"] + CATEGORIES)

# --- Safe Price Slider ---
if PRODUCTS:
    max_price_val = int(max(p['price'] for p in PRODUCTS))
else:
    max_price_val = 5000

min_price, max_price = st.slider(
    "Price range (NT$)",
    min_value=0,
    max_value=max_price_val,
    value=(0, max_price_val),
    step=100
)

# ---------------------------
# FILTER LOGIC
# ---------------------------
filtered = PRODUCTS
if search:
    filtered = [p for p in filtered if search.lower() in p['name'].lower()]
if category != "All":
    filtered = [p for p in filtered if p['category'] == category]
filtered = [p for p in filtered if min_price <= p['price'] <= max_price]

# ---------------------------
# GRID DISPLAY
# ---------------------------
cols = st.columns(COLUMNS)
i = 0
for prod in filtered:
    with cols[i]:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(prod['image'], use_column_width=True)
        st.markdown(f"**{prod['name']}**")
        st.caption(prod['category'])
        st.markdown(f"<div class='price'>NT${prod['price']}</div>", unsafe_allow_html=True)
        qty_key = f"q_{prod['id']}"
        qty = st.number_input("Qty", min_value=1, value=1, key=qty_key, label_visibility="collapsed")
        if st.button("Add to Cart", key=f"add_{prod['id']}"):
            add_to_cart(prod['id'], qty)
            st.success(f"Added {qty} × {prod['name']} to cart.")
        st.markdown("</div>", unsafe_allow_html=True)
    i = (i + 1) % COLUMNS
    if i == 0:
        cols = st.columns(COLUMNS)
