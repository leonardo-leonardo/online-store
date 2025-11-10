# streamlit_online_store_final.py
import streamlit as st
import random
import math
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
NUM_ITEMS = 500
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
    .product-card {{
      background: {card_bg};
      color: {text};
      border-radius: 12px;
      padding: 10px;
      box-shadow: 0 6px 18px {shadow};
      transition: transform 0.12s ease, box-shadow 0.12s ease;
      text-align: center;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .product-card:hover {{
      transform: translateY(-6px);
      box-shadow: 0 18px 36px {shadow};
    }}
    .product-image {{
      width: 100%;
      border-radius: 8px;
      object-fit: cover;
      height: 180px;
    }}
    .price {{
      color: {accent};
      font-weight: 700;
      font-size: 18px;
    }}
    .muted {{
      color: {muted};
      font-size: 13px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False
inject_css(st.session_state['dark_mode'])

# ---------------------------
# DATA: categories & names
# ---------------------------
CATEGORIES = [
    "Electronics", "Stationery", "Accessories", "Clothing",
    "Kitchen", "Sports", "Toys", "Home"
]

NAME_POOLS = {
    "Electronics": ["AeroSound Earbuds","VoltPro Power Bank","LumaScreen Monitor","EchoBeam Speaker","NovaCharge Cable","PulseSmart Watch","ByteTab Tablet","ZenBud Earphones"],
    "Stationery": ["CloudPen Gel","TaskMaster Planner","SketchPro Marker","SharpEdge Scissors","Inkwell Fountain Pen","UltraNote Pad","PaperMate Journal","FlexiRuler 30cm"],
    "Accessories": ["UrbanFlow Backpack","SnapGrip Wallet","SolarTime Watch","PureLeather Belt","KeyMate Organizer","ComfyCap Hat","PolarShades Glasses","TrendyCase Cover"],
    "Clothing": ["AeroFit T-shirt","BreezeJog Pants","ComfyCrew Hoodie","StreetWave Jacket","CoolStride Socks","UrbanWalk Shoes","DailyFit Shorts","AquaGuard Raincoat"],
    "Kitchen": ["AquaBlend Mixer","ChefMate Knife Set","SteamEase Kettle","SmartPan Fryer","EcoCut Board","PureTaste Mug","QuickPrep Blender","SpiceJoy Rack"],
    "Sports": ["SwiftRun Shoes","PowerGrip Gloves","HydroFlex Bottle","StaminaPro Rope","FlexTrack Yoga Mat","TurboRacket","WaveRider Surfboard","CoreStrength Dumbbells"],
    "Toys": ["BuildPro Blocks","RoboBuddy Bot","MagicPuzzle Cube","SpeedDrift Car","AeroPlane Toy","GigaBear Plush","DinoQuest Figure","BrainBoost Game"],
    "Home": ["GlowLite Lamp","PureAir Diffuser","ComfyCotton Pillow","DreamWeave Blanket","SmartTemp Fan","AromaCandle Set","CosyMat Rug","BreezeCurtains"]
}

# ---------------------------
# GENERATE PRODUCTS
# ---------------------------
def generate_products(num_items=NUM_ITEMS):
    products = []
    id_counter = 1
    while id_counter <= num_items:
        for cat in CATEGORIES:
            base = random.choice(NAME_POOLS[cat])
            variant = random.choice([""," Pro"," X"," Plus"," Mini"," Max"])
            name = (base + variant).strip()
            price = round(random.uniform(7.0, 399.0),2)
            img = f"https://picsum.photos/seed/{cat}{id_counter}/600/600"
            products.append({"id":f"item-{id_counter}","name":name,"category":cat,"price":price,"image":img})
            id_counter += 1
            if id_counter>num_items:
                break
    return products

if 'products' not in st.session_state:
    st.session_state['products'] = generate_products()

PRODUCTS = st.session_state['products']

# ---------------------------
# CART STATE
# ---------------------------
if 'cart' not in st.session_state:
    st.session_state['cart'] = []
if 'coupon' not in st.session_state:
    st.session_state['coupon'] = ""
if 'pro' not in st.session_state:
    st.session_state['pro'] = False

def add_to_cart(product_id, qty=1):
    prod = next((p for p in PRODUCTS if p['id']==product_id), None)
    if not prod: return
    entry = next((e for e in st.session_state['cart'] if e['id']==product_id), None)
    if entry:
        entry['qty'] += qty
    else:
        st.session_state['cart'].append({"id":prod['id'],"name":prod['name'],"price":prod['price'],"qty":qty})

def remove_from_cart(product_id):
    st.session_state['cart'] = [e for e in st.session_state['cart'] if e['id']!=product_id]

def update_qty(product_id, qty):
    if qty<=0:
        remove_from_cart(product_id)
    else:
        for e in st.session_state['cart']:
            if e['id']==product_id:
                e['qty']=qty

def summarize_cart():
    subtotal = sum(e['price']*e['qty'] for e in st.session_state['cart'])
    discount = 0
    if st.session_state['coupon']=="SAVE10":
        discount += subtotal*0.10
    if st.session_state['pro']:
        discount += subtotal*0.05
    tax = round((subtotal-discount)*0.05,2)
    shipping = 0.0 if subtotal>=100 else 6.99
    total = round(subtotal-discount+tax+shipping,2)
    return {"subtotal":round(subtotal,2),"discount":round(discount,2),"tax":tax,"shipping":round(shipping,2),"total":total}

# ---------------------------
# SIDEBAR: Filters + Cart
# ---------------------------
st.sidebar.markdown("## Filters & Cart")
search_q = st.sidebar.text_input("Search product name")
category_filter = st.sidebar.selectbox("Category", ["All"] + CATEGORIES)
min_price,max_price = st.sidebar.slider("Price range",0.0,500.0,(0.0,500.0))
sort_by = st.sidebar.selectbox("Sort by", ["Relevance","Price ↑","Price ↓","Name"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧾 Cart")
for e in st.session_state['cart']:
    st.sidebar.markdown(f"**{e['qty']}× {e['name']}** - ${e['price']} each")
    new_qty = st.sidebar.number_input("",min_value=0,value=e['qty'],key=f"qty_{e['id']}")
    if st.sidebar.button("Update",key=f"up_{e['id']}"):
        update_qty(e['id'],new_qty)
        st.success(f"Updated {e['name']}")
    if st.sidebar.button("Remove",key=f"rem_{e['id']}"):
        remove_from_cart(e['id'])
        st.success(f"Removed {e['name']}")

cs = summarize_cart()
st.sidebar.markdown(f"**Subtotal:** ${cs['subtotal']}")
st.sidebar.markdown(f"**Discount:** -${cs['discount']}")
st.sidebar.markdown(f"**Tax:** ${cs['tax']}")
st.sidebar.markdown(f"**Shipping:** ${cs['shipping']}")
st.sidebar.markdown(f"### **Total: ${cs['total']}**")

if st.sidebar.button("Checkout"):
    st.sidebar.success("✅ Order placed!")
    st.session_state['cart'] = []

# ---------------------------
# MAIN: Product Grid
# ---------------------------
filtered = PRODUCTS
if search_q: filtered=[p for p in filtered if search_q.lower() in p['name'].lower()]
if category_filter!="All": filtered=[p for p in filtered if p['category']==category_filter]
filtered = [p for p in filtered if min_price<=p['price']<=max_price]

if sort_by=="Price ↑": filtered=sorted(filtered,key=lambda x:x['price'])
elif sort_by=="Price ↓": filtered=sorted(filtered,key=lambda x:-x['price'])
elif sort_by=="Name": filtered=sorted(filtered,key=lambda x:x['name'].lower())

items_per_page = st.selectbox("Items per page",[12,24,36,48],index=1)
total_pages = math.ceil(len(filtered)/items_per_page)
page = st.number_input("Page",1,total_pages,1)
start = (page-1)*items_per_page
end = start+items_per_page
page_items = filtered[start:end]

columns = st.columns(4)
col_idx = 0
for prod in page_items:
    with columns[col_idx]:
        st.markdown(f"<div class='product-card'>",unsafe_allow_html=True)
        st.image(prod['image'], use_column_width=True)
        st.markdown(f"**{prod['name']}**")
        st.markdown(f"<div class='muted'>{prod['category']}</div>",unsafe_allow_html=True)
        st.markdown(f"<div class='price'>${prod['price']}</div>",unsafe_allow_html=True)
        qty_key=f"qty_{prod['id']}"
        qty=st.number_input("Qty",min_value=1,value=1,key=qty_key)
        if st.button("Add to Cart",key=f"add_{prod['id']}"):
            add_to_cart(prod['id'],qty)
            st.success(f"Added {qty}× {prod['name']} to cart")
        st.markdown("</div>",unsafe_allow_html=True)
    col_idx=(col_idx+1)%4
    if col_idx==0:
        columns=st.columns(4)

st.markdown("---")
st.markdown(f"Showing items {start+1}–{min(end,len(filtered))} of {len(filtered)} • Page {page}/{total_pages}")
