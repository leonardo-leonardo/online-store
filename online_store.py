# streamlit_online_store.py
import streamlit as st
import random
import math
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
NUM_ITEMS = 500  # set as high as you want (app paginates)
ITEMS_PER_PAGE_DEFAULT = 24

st.set_page_config(page_title="🛒 Mega Store", layout="wide", page_icon="🛍️")
# ---------------------------
# THEME / CSS
# ---------------------------
def inject_css(dark=False):
    if dark:
        bg = "#0b1221"
        card_bg = "#0f1724"
        text = "#e6eef8"
        muted = "#9aa9bf"
        accent = "#7dd3fc"
        shadow = "rgba(0,0,0,0.6)"
    else:
        bg = "#f6f8fb"
        card_bg = "#ffffff"
        text = "#0b1221"
        muted = "#556080"
        accent = "#0a84ff"
        shadow = "rgba(15,23,42,0.08)"

    css = f"""
    <style>
    :root {{
      --bg: {bg};
      --card-bg: {card_bg};
      --text: {text};
      --muted: {muted};
      --accent: {accent};
      --shadow: {shadow};
    }}
    .stApp > div:first-child {{
      background: linear-gradient(180deg, var(--bg), #ffffff00);
    }}
    .product-card {{
      background: var(--card-bg);
      color: var(--text);
      border-radius: 12px;
      padding: 10px;
      box-shadow: 0 6px 18px var(--shadow);
      transition: transform 0.12s ease, box-shadow 0.12s ease;
      text-align: center;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .product-card:hover {{
      transform: translateY(-6px);
      box-shadow: 0 18px 36px var(--shadow);
    }}
    .product-image {{
      width: 100%;
      border-radius: 8px;
      object-fit: cover;
      height: 180px;
    }}
    .price {{
      color: var(--accent);
      font-weight: 700;
      font-size: 18px;
    }}
    .muted {{
      color: var(--muted);
      font-size: 13px;
    }}
    .qty-input {{
      width: 85px;
      margin-right: 8px;
    }}
    .add-button {{
      background: linear-gradient(90deg,var(--accent), #2bb1ff);
      color: white;
      border-radius: 8px;
      padding: 8px 12px;
      border: none;
      cursor: pointer;
    }}
    .small {{
      font-size: 13px;
      color: var(--muted);
    }}
    /* responsive grid tweak */
    @media (max-width: 800px) {{
      .product-image {{ height: 140px; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# default theme (light)
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False
inject_css(st.session_state['dark_mode'])

# ---------------------------
# DATA: categories & name pools
# ---------------------------
CATEGORY_KEYWORDS = {
    "Electronics": "electronics gadgets tech",
    "Stationery": "notebook pen stationery desk",
    "Accessories": "wallet watch bag accessory",
    "Clothing": "clothing tshirt jacket fashion",
    "Kitchen": "kitchen utensils cooking",
    "Sports": "sports fitness gear",
    "Toys": "toy kids play",
    "Home": "home decor interior"
}
CATEGORIES = list(CATEGORY_KEYWORDS.keys())

NAME_POOLS = {
    "Electronics": [
        "AeroSound Earbuds", "VoltPro Power Bank", "LumaScreen Monitor", "EchoBeam Speaker",
        "NovaCharge Cable", "PulseSmart Watch", "ByteTab Tablet", "ZenBud Earphones",
        "NeoCharge Adapter", "SkyLink Router", "TrueBass Headset", "VisionPro Projector",
        "ClipCharge Magnetic Cable", "BoltData Portable SSD"
    ],
    "Stationery": [
        "CloudPen Gel", "TaskMaster Planner", "SketchPro Marker", "SharpEdge Scissors",
        "Inkwell Fountain Pen", "UltraNote Pad", "PaperMate Journal", "FlexiRuler 30cm",
        "SmoothWrite Pencil Set", "ProWriter Pen"
    ],
    "Accessories": [
        "UrbanFlow Backpack", "SnapGrip Wallet", "SolarTime Watch", "PureLeather Belt",
        "KeyMate Organizer", "ComfyCap Hat", "PolarShades Glasses", "TrendyCase Cover",
        "MetroBuckle Belt"
    ],
    "Clothing": [
        "AeroFit T-shirt", "BreezeJog Pants", "ComfyCrew Hoodie", "StreetWave Jacket",
        "CoolStride Socks", "UrbanWalk Shoes", "DailyFit Shorts", "AquaGuard Raincoat"
    ],
    "Kitchen": [
        "AquaBlend Mixer", "ChefMate Knife Set", "SteamEase Kettle", "SmartPan Fryer",
        "EcoCut Board", "PureTaste Mug", "QuickPrep Blender", "SpiceJoy Rack"
    ],
    "Sports": [
        "SwiftRun Shoes", "PowerGrip Gloves", "HydroFlex Bottle", "StaminaPro Rope",
        "FlexTrack Yoga Mat", "TurboRacket", "WaveRider Surfboard", "CoreStrength Dumbbells"
    ],
    "Toys": [
        "BuildPro Blocks", "RoboBuddy Bot", "MagicPuzzle Cube", "SpeedDrift Car",
        "AeroPlane Toy", "GigaBear Plush", "DinoQuest Figure", "BrainBoost Game"
    ],
    "Home": [
        "GlowLite Lamp", "PureAir Diffuser", "ComfyCotton Pillow", "DreamWeave Blanket",
        "SmartTemp Fan", "AromaCandle Set", "CosyMat Rug", "BreezeCurtains"
    ]
}

# ---------------------------
# GENERATE MANY PRODUCTS
# ---------------------------
def generate_products(num_items=NUM_ITEMS, seed=1234):
    random.seed(seed)
    products = []
    id_counter = 1
    # cycle categories while creating products; create variations to get unique names
    cat_cycle = [c for c in CATEGORIES]
    while id_counter <= num_items:
        for cat in cat_cycle:
            base_names = NAME_POOLS[cat]
            # pick base and append variant if needed
            base = random.choice(base_names)
            variant = random.choice(["", " Pro", " X", " Plus", " Mini", " Max", " S", " 2.0", " Edition"])
            name = (base + variant).strip()
            price = round(random.uniform(7.0, 399.0), 2)
            # picsum seed by category + id ensures visible, varied, and category-coherent images
            img = f"https://picsum.photos/seed/{cat.replace(' ','')}{id_counter}/600/600"
            products.append({
                "id": f"item-{id_counter}",
                "name": name,
                "category": cat,
                "price": price,
                "image": img,
                "sku": f"SKU{100000 + id_counter}"
            })
            id_counter += 1
            if id_counter > num_items:
                break
    return products

if 'products' not in st.session_state:
    st.session_state['products'] = generate_products()

PRODUCTS = st.session_state['products']

# ---------------------------
# SAFE SESSION STATE FOR CART & ORDERS
# ---------------------------
def safe_init_state():
    if 'cart' not in st.session_state or not isinstance(st.session_state.get('cart'), list):
        st.session_state['cart'] = []
    if 'coupon' not in st.session_state or not isinstance(st.session_state.get('coupon'), str):
        st.session_state['coupon'] = ""
    if 'pro' not in st.session_state or not isinstance(st.session_state.get('pro'), bool):
        st.session_state['pro'] = False
    if 'orders' not in st.session_state or not isinstance(st.session_state.get('orders'), list):
        st.session_state['orders'] = []
safe_init_state()

# ---------------------------
# SHOPPING LOGIC
# ---------------------------
def add_to_cart(product_id, qty=1):
    # product_id is item id string
    safe_init_state()
    # store as dict entries for easier operations
    prod = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if prod is None:
        return
    # check if exists in cart
    entry = next((e for e in st.session_state['cart'] if e['id'] == product_id), None)
    if entry:
        entry['qty'] += qty
        entry['updated_at'] = datetime.utcnow().isoformat()
    else:
        st.session_state['cart'].append({
            "id": prod['id'],
            "name": prod['name'],
            "price": prod['price'],
            "qty": qty,
            "image": prod['image'],
            "sku": prod['sku'],
            "added_at": datetime.utcnow().isoformat()
        })

def remove_from_cart(product_id):
    safe_init_state()
    st.session_state['cart'] = [e for e in st.session_state['cart'] if e['id'] != product_id]

def update_qty(product_id, qty):
    safe_init_state()
    if qty <= 0:
        remove_from_cart(product_id)
        return
    for e in st.session_state['cart']:
        if e['id'] == product_id:
            e['qty'] = qty
            e['updated_at'] = datetime.utcnow().isoformat()
            break

def summarize_cart():
    safe_init_state()
    subtotal = sum(e['price'] * e['qty'] for e in st.session_state['cart'])
    discount = 0.0
    if st.session_state['coupon'] == "SAVE10":
        discount += subtotal * 0.10
    if st.session_state['pro']:
        discount += subtotal * 0.05
    tax = round((subtotal - discount) * 0.05, 2)
    shipping = 0.0 if subtotal >= 100.0 else 6.99
    total = round(subtotal - discount + tax + shipping, 2)
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": tax,
        "shipping": round(shipping, 2),
        "total": total
    }

# ---------------------------
# SIDEBAR (filters + cart mini)
# ---------------------------
st.sidebar.markdown("## Filters & Cart")
# theme toggle
if st.sidebar.checkbox("Dark mode", value=st.session_state['dark_mode']):
    st.session_state['dark_mode'] = True
    inject_css(True)
else:
    st.session_state['dark_mode'] = False
    inject_css(False)

# search & filters
search_q = st.sidebar.text_input("Search product name")
category_filter = st.sidebar.selectbox("Category", options=["All"] + CATEGORIES)
min_price, max_price = st.sidebar.slider("Price range", 0.0, 500.0, (0.0, 500.0))
sort_by = st.sidebar.selectbox("Sort by", options=["Relevance", "Price ↑", "Price ↓", "Name"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧾 Cart")
if not st.session_state['cart']:
    st.sidebar.info("Cart is empty")
else:
    for e in st.session_state['cart']:
        st.sidebar.markdown(f"**{e['qty']}× {e['name']}**")
        st.sidebar.caption(f"${e['price']} each — {e['sku']}")
        col1, col2 = st.sidebar.columns([2,1])
        with col1:
            new_qty = col1.number_input("Qty", min_value=0, value=e['qty'], key=f"side_qty_{e['id']}")
        with col2:
            if col2.button("Update", key=f"side_upd_{e['id']}"):
                update_qty(e['id'], int(new_qty))
                st.experimental_rerun()
        if col2.button("Remove", key=f"side_rem_{e['id']}"):
            remove_from_cart(e['id'])
            st.experimental_rerun()
    st.sidebar.markdown("---")
    st.sidebar.text_input("Coupon (SAVE10)", key="coupon_input")
    if st.sidebar.button("Apply Coupon"):
        st.session_state['coupon'] = st.session_state.get('coupon_input', "")
    st.sidebar.checkbox("Pro membership (5% off)", key="pro_sidebar")
    # sync toggles
    st.session_state['pro'] = st.session_state.get('pro_sidebar', st.session_state['pro'])
    cs = summarize_cart()
    st.sidebar.markdown(f"**Subtotal:** ${cs['subtotal']}")
    st.sidebar.markdown(f"**Discount:** -${cs['discount']}")
    st.sidebar.markdown(f"**Tax:** ${cs['tax']}")
    st.sidebar.markdown(f"**Shipping:** ${cs['shipping']}")
    st.sidebar.markdown(f"### **Total: ${cs['total']}**")
    if st.sidebar.button("Checkout"):
        order_id = f"ORD{random.randint(1000,9999)}"
        st.session_state['orders'].append({
            "id": order_id,
            "items": st.session_state['cart'],
            "summary": cs,
            "created": datetime.utcnow().isoformat()
        })
        st.sidebar.success(f"Order placed: {order_id}")
        st.session_state['cart'] = []

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ — demo store")

# ---------------------------
# MAIN: Catalog + Pagination + Grid UI (improved)
# ---------------------------

st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;'>"
            "<div style='font-size:22px;font-weight:700'>🛍️ Mega Store — Browse</div>"
            f"<div style='color:gray'>Products: {len(PRODUCTS)}</div></div>", unsafe_allow_html=True)
st.markdown("##")

# Build filtered list
filtered = PRODUCTS
if search_q:
    sq = search_q.lower().strip()
    filtered = [p for p in filtered if sq in p['name'].lower()]
if category_filter != "All":
    filtered = [p for p in filtered if p['category'] == category_filter]
filtered = [p for p in filtered if p['price'] >= min_price and p['price'] <= max_price]

# sorting
if sort_by == "Price ↑":
    filtered = sorted(filtered, key=lambda x: x['price'])
elif sort_by == "Price ↓":
    filtered = sorted(filtered, key=lambda x: -x['price'])
elif sort_by == "Name":
    filtered = sorted(filtered, key=lambda x: x['name'].lower())

# pagination controls
items_per_page = st.selectbox("Items per page", options=[12, 24, 36, 48], index=1)
total_pages = math.ceil(len(filtered) / items_per_page)
if total_pages == 0:
    total_pages = 1
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

start = (page - 1) * items_per_page
end = start + items_per_page
page_items = filtered[start:end]

# show grid
columns = st.columns(4)
col_idx = 0
for prod in page_items:
    with columns[col_idx]:
        # card html
        st.markdown(
            f"""
            <div class="product-card">
                <img class="product-image" src="{prod['image']}" alt="{prod['name']}">
                <div>
                    <div style="font-weight:600">{prod['name']}</div>
                    <div class="muted">{prod['category']} • {prod['sku']}</div>
                    <div style="margin-top:8px;" class="price">${prod['price']}</div>
                </div>
                <div style="margin-top:10px;">
                    <div style="display:flex;justify-content:center;align-items:center;">
                        <input id="qty_{prod['id']}" type="number" min="1" value="1" style="width:70px;padding:6px;border-radius:6px;border:1px solid #ddd;">
                        <button onclick="document.getElementById('add_{prod['id']}').click()" class="add-button" style="margin-left:8px;">Add to Cart</button>
                    </div>
                    <form style="display:none">
                        <button id="add_{prod['id']}" ></button>
                    </form>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # invisible streamlit button receives JS click; when pressed, read qty widget value via st number_input fallback
        qty_key = f"qty_input_{prod['id']}"
        qty = st.number_input("", min_value=1, value=1, key=qty_key, label_visibility="collapsed")
        if st.button("Add", key=f"st_add_{prod['id']}"):
            add_to_cart(prod['id'], qty)
            st.experimental_rerun()

    col_idx = (col_idx + 1) % 4
    if col_idx == 0:
        columns = st.columns(4)

# footer / pagination summary
st.markdown("---")
st.markdown(f"Showing items {start+1}–{min(end, len(filtered))} of {len(filtered)} • Page {page}/{total_pages}")

# ---------------------------
# ADMIN PANEL (compact)
# ---------------------------
with st.expander("⚙️ Admin — Orders & Adjustments"):
    st.write(f"Orders placed: {len(st.session_state['orders'])}")
    if st.session_state['orders']:
        st.write(st.session_state['orders'][-10:])  # show last 10 orders

    tweak = st.slider("Global price adjust (%)", -50, 50, 0, step=1)
    if st.button("Apply price adjust"):
        factor = 1 + (tweak / 100.0)
        for p in PRODUCTS:
            p['price'] = round(max(0.5, p['price'] * factor), 2)
        st.success(f"Applied {tweak}% to all prices")

st.caption("Demo store — in-memory. Connect a DB and payment gateway for production.")
