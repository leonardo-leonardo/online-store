# convenience_store_50.py
import streamlit as st
import random
import re
import os

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="🛒 Convenience Store (50 items)", layout="wide", page_icon="🛍️")
COLUMNS = 4
NUM_ITEMS = 50  # fixed to 50 realistic items

# ---------------------------
# UTILS
# ---------------------------
def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s

def local_image_path_for(name: str) -> str:
    """Return local image path (images/{slug}.jpg or .png) if exists, else None"""
    slug = slugify(name)
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = os.path.join("images", slug + ext)
        if os.path.isfile(path):
            return path
    return None

def placeholder_image_for(name: str) -> str:
    """Return a reliable placeholder seeded by slug (picsum)."""
    slug = slugify(name)
    # Use small seedable picsum URL — reliable
    return f"https://picsum.photos/seed/{slug}/600/400"

# ---------------------------
# PRODUCT LIST (50 realistic convenience items)
# ---------------------------
# Realistic names — you can override images by adding images/<slug>.jpg
PRODUCTS = [
    {"id":"c001","name":"Classic Ballpoint Pen","category":"Stationery","price":25},
    {"id":"c002","name":"Notebook A5 Ruled","category":"Stationery","price":120},
    {"id":"c003","name":"Sticky Note Pack","category":"Stationery","price":60},
    {"id":"c004","name":"Highlighter Set (4)","category":"Stationery","price":95},
    {"id":"c005","name":"Mechanical Pencil 0.5mm","category":"Stationery","price":85},

    {"id":"c006","name":"Cozy Knit Socks (3 Pairs)","category":"Clothing","price":150},
    {"id":"c007","name":"Everyday Cotton T-shirt","category":"Clothing","price":280},
    {"id":"c008","name":"Lightweight Windbreaker","category":"Clothing","price":990},
    {"id":"c009","name":"Classic Baseball Cap","category":"Clothing","price":220},
    {"id":"c010","name":"Comfort Flip-flops","category":"Clothing","price":180},

    {"id":"c011","name":"Insulated Travel Mug","category":"Kitchen","price":420},
    {"id":"c012","name":"Ceramic Coffee Mug","category":"Kitchen","price":180},
    {"id":"c013","name":"2-slice Toaster","category":"Kitchen","price":990},
    {"id":"c014","name":"Chef's Spatula Set","category":"Kitchen","price":240},
    {"id":"c015","name":"Non-stick Frypan 26cm","category":"Kitchen","price":680},

    {"id":"c016","name":"USB-C Fast Charger","category":"Electronics","price":390},
    {"id":"c017","name":"Compact Power Bank 10000mAh","category":"Electronics","price":820},
    {"id":"c018","name":"Wireless Earbuds Basic","category":"Electronics","price":990},
    {"id":"c019","name":"Portable Bluetooth Speaker","category":"Electronics","price":1290},
    {"id":"c020","name":"LED Desk Lamp","category":"Electronics","price":760},

    {"id":"c021","name":"Reusable Water Bottle 500ml","category":"Home","price":260},
    {"id":"c022","name":"Scented Candle (3-pack)","category":"Home","price":360},
    {"id":"c023","name":"Microfiber Dish Cloths (5)","category":"Home","price":140},
    {"id":"c024","name":"Compact Storage Box","category":"Home","price":320},
    {"id":"c025","name":"Soft Throw Blanket","category":"Home","price":580},

    {"id":"c026","name":"Everyday Backpack 20L","category":"Accessories","price":1490},
    {"id":"c027","name":"Slim Card Wallet","category":"Accessories","price":420},
    {"id":"c028","name":"Travel Umbrella Compact","category":"Accessories","price":320},
    {"id":"c029","name":"Key Organizer Multi-tool","category":"Accessories","price":260},
    {"id":"c030","name":"Phone Case Clear Fit","category":"Accessories","price":290},

    {"id":"c031","name":"Running Shoes Lightweight","category":"Sports","price":1990},
    {"id":"c032","name":"Yoga Mat Non-slip","category":"Sports","price":520},
    {"id":"c033","name":"Sports Sweatband","category":"Sports","price":110},
    {"id":"c034","name":"Tennis Racket Beginner","category":"Sports","price":1390},
    {"id":"c035","name":"Compact Jump Rope","category":"Sports","price":210},

    {"id":"c036","name":"Kids Puzzle 100pcs","category":"Toys","price":260},
    {"id":"c037","name":"Mini Remote Car","category":"Toys","price":690},
    {"id":"c038","name":"Plush Teddy Bear Medium","category":"Toys","price":420},
    {"id":"c039","name":"Coloring Crayon Pack","category":"Toys","price":150},
    {"id":"c040","name":"Stacking Blocks Set","category":"Toys","price":340},

    {"id":"c041","name":"Face Mask 50pcs","category":"Health","price":250},
    {"id":"c042","name":"Hand Sanitizer 250ml","category":"Health","price":180},
    {"id":"c043","name":"First Aid Compact Kit","category":"Health","price":490},
    {"id":"c044","name":"Vitamin C Chewables","category":"Health","price":320},
    {"id":"c045","name":"Thermal Reusable Ice Pack","category":"Health","price":210},

    {"id":"c046","name":"Office Desk Calendar 2026","category":"Stationery","price":240},
    {"id":"c047","name":"Rechargeable LED Keylight","category":"Electronics","price":330},
    {"id":"c048","name":"Compact Sewing Kit","category":"Home","price":140},
    {"id":"c049","name":"Portable Shoe Cleaning Kit","category":"Home","price":200},
    {"id":"c050","name":"Reusable Grocery Tote (2)", "category":"Accessories","price":160},
]

# ---------------------------
# Attach image path or placeholder image URL to each product
# If you add images into ./images/<slug>.jpg (or .png), the app will use it (priority).
# Otherwise it falls back to a seeded picsum URL so visuals are always present.
# ---------------------------
for p in PRODUCTS:
    local = local_image_path_for(p['name'])
    p['image_local'] = local  # path if found else None
    if local:
        p['image'] = local
    else:
        p['image'] = placeholder_image_for(p['name'])

# ---------------------------
# SESSION STATE SAFE INIT
# ---------------------------
def safe_init():
    if 'cart' not in st.session_state or not isinstance(st.session_state.get('cart'), list):
        st.session_state['cart'] = []
    if 'cart_open' not in st.session_state:
        st.session_state['cart_open'] = False
    if 'coupon' not in st.session_state:
        st.session_state['coupon'] = ""

safe_init()

# ---------------------------
# SHOPPING CART OPERATIONS
# ---------------------------
def add_to_cart(prod_id, qty=1):
    safe_init()
    prod = next((x for x in PRODUCTS if x['id'] == prod_id), None)
    if not prod:
        return
    entry = next((e for e in st.session_state['cart'] if e['id'] == prod_id), None)
    if entry:
        entry['qty'] += qty
    else:
        st.session_state['cart'].append({"id":prod_id, "name":prod['name'], "price":prod['price'], "qty":qty})

def remove_from_cart(prod_id):
    safe_init()
    st.session_state['cart'] = [e for e in st.session_state['cart'] if e['id'] != prod_id]

def update_qty(prod_id, qty):
    safe_init()
    if qty <= 0:
        remove_from_cart(prod_id)
        return
    for e in st.session_state['cart']:
        if e['id'] == prod_id:
            e['qty'] = qty
            break

def summarize_cart():
    safe_init()
    subtotal = sum(e['price']*e['qty'] for e in st.session_state['cart'])
    discount = subtotal * 0.05 if subtotal > 5000 else 0
    tax = int(round((subtotal - discount) * 0.05))
    shipping = 0 if subtotal > 3000 else 120
    total = int(round(subtotal - discount + tax + shipping))
    return {"subtotal":int(subtotal), "discount":int(discount), "tax":tax, "shipping":shipping, "total":total}

# ---------------------------
# PAGE CSS (simple)
# ---------------------------
st.markdown("""
<style>
.product-card { background:#fff; border-radius:10px; padding:10px; box-shadow: 0 6px 18px rgba(0,0,0,0.06); text-align:center; min-height:320px; display:flex; flex-direction:column; justify-content:space-between; }
.product-card:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(0,0,0,0.12); }
.top-bar { position:sticky; top:0; background:#fff; z-index:999; padding:10px 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); display:flex; justify-content:space-between; align-items:center; }
.small-btn { background:#007bff; color:#fff; border:none; padding:8px 12px; border-radius:8px; cursor:pointer; }
.small-btn:hover { background:#005ecb; }
.category-badge { font-size:12px; color:#666; }
.price { color:#007bff; font-weight:700; margin-top:6px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TOP BAR with cart button
# ---------------------------
cart_summary = summarize_cart()
st.markdown(f"<div class='top-bar'><div style='font-weight:700'>🛒 Convenience Store — 50 items</div>"
            f"<div> <button class='small-btn' onclick='window.location.reload()'>🔄 Refresh</button> "
            f"<button class='small-btn'>🛍️ Cart ({len(st.session_state['cart'])}) NT${cart_summary['total']}</button></div></div>", unsafe_allow_html=True)

if st.button(f"🛍️ View Cart ({len(st.session_state['cart'])})"):
    st.session_state['cart_open'] = not st.session_state['cart_open']

# ---------------------------
# CART EXPANDER
# ---------------------------
if st.session_state['cart_open']:
    with st.expander(f"🛍️ Your Cart ({len(st.session_state['cart'])} items)", expanded=True):
        if not st.session_state['cart']:
            st.info("Cart is empty — add items from below.")
        else:
            for entry in st.session_state['cart']:
                c1, c2, c3 = st.columns([4,2,1])
                c1.write(f"**{entry['name']}**")
                new_qty = c2.number_input("Qty", min_value=1, value=entry['qty'], key=f"cart_qty_{entry['id']}")
                if new_qty != entry['qty']:
                    update_qty(entry['id'], new_qty)
                if c3.button("Remove", key=f"rem_{entry['id']}"):
                    remove_from_cart(entry['id'])
                    st.success(f"Removed {entry['name']}")
            cs = summarize_cart()
            st.markdown("---")
            st.write(f"Subtotal: NT${cs['subtotal']}")
            st.write(f"Discount: -NT${cs['discount']}")
            st.write(f"Tax: NT${cs['tax']}")
            st.write(f"Shipping: NT${cs['shipping']}")
            st.markdown(f"### **Total: NT${cs['total']}**")
            if st.button("✅ Checkout"):
                st.success("Order placed — thank you!")
                st.session_state['cart'] = []

# ---------------------------
# FILTERS
# ---------------------------
st.markdown("### 🔎 Browse & filter")
search_q = st.text_input("Search by name")
categories = ["All"] + sorted(list({p['category'] for p in PRODUCTS}))
category = st.selectbox("Category", categories)

prices = [p['price'] for p in PRODUCTS]
min_price_val = 0
max_price_val = int(max(prices)) if prices else 5000

min_price, max_price = st.slider("Price range (NT$)", min_value=min_price_val, max_value=max_price_val,
                                 value=(min_price_val, max_price_val), step=10)

# ---------------------------
# FILTER LOGIC
# ---------------------------
filtered = PRODUCTS
if search_q:
    filtered = [p for p in filtered if search_q.lower() in p['name'].lower()]
if category != "All":
    filtered = [p for p in filtered if p['category'] == category]
filtered = [p for p in filtered if min_price <= p['price'] <= max_price]

# ---------------------------
# GRID (all items)
# ---------------------------
cols = st.columns(COLUMNS)
col_index = 0
for p in filtered:
    with cols[col_index]:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        # image: local file path (if exists) or placeholder url
        try:
            if p.get('image_local'):
                st.image(p['image'], use_column_width=True)
            else:
                # direct external placeholder (picsum) — always viewable
                st.image(p['image'], use_column_width=True)
        except Exception:
            # last resort: display a blank colored block via markdown
            st.markdown("<div style='width:100%;height:200px;background:#f2f2f2;border-radius:8px;'></div>", unsafe_allow_html=True)

        st.write(f"**{p['name']}**")
        st.write(f"<span class='category-badge'>{p['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='price'>NT${p['price']}</div>", unsafe_allow_html=True)

        qty_key = f"qty_{p['id']}"
        qty = st.number_input("Qty", min_value=1, value=1, key=qty_key, label_visibility="collapsed")
        if st.button("Add to cart", key=f"add_{p['id']}"):
            add_to_cart(p['id'], qty)
            st.success(f"Added {qty} × {p['name']} to cart.")
        st.markdown("</div>", unsafe_allow_html=True)
    col_index = (col_index + 1) % COLUMNS
    if col_index == 0:
        cols = st.columns(COLUMNS)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
cs = summarize_cart()
st.write(f"Cart items: {len(st.session_state['cart'])} • Total: NT${cs['total']}")
st.caption("To inject your own images: place files in ./images/<slug>.jpg where slug = product name lowercased, spaces → hyphens (e.g. cozy-knit-socks.jpg).")
