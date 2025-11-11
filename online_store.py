# mega_store_matched_photos.py
import streamlit as st
import random

st.set_page_config(page_title="🛒 Mega Store (Matched Photos)", layout="wide", page_icon="🛍️")

# ---------------------------
# STYLE
# ---------------------------
st.markdown("""
<style>
.product-card {
  background: #fff;
  border-radius: 12px;
  padding: 10px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
  transition: transform 0.15s, box-shadow 0.15s;
  text-align: center;
  min-height: 340px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(0,0,0,0.12);
}
.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}
.price { color: #007bff; font-weight: 700; font-size: 18px; }
.top-cart-bar {
  position: sticky; top: 0; z-index: 1000;
  background: #ffffff; padding: 10px 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  display:flex; justify-content:space-between; align-items:center;
}
.small-btn { background:#007bff; color:white; border:none; padding:8px 12px; border-radius:8px; cursor:pointer; }
.small-btn:hover { background:#005ecb; }
.category-badge { font-size:12px; color:#666; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# PRODUCTS — 48 hand-picked items with stable Pexels image URLs (lifestyle)
# Each entry: id, name, category, price (NT$), image (direct URL)
# ---------------------------
PRODUCTS = [
    # Electronics
    {"id":"p001","name":"AeroPods Wireless Earbuds","category":"Electronics","price":1290,"image":"https://images.pexels.com/photos/373945/pexels-photo-373945.jpeg"},
    {"id":"p002","name":"Pulse Bluetooth Speaker","category":"Electronics","price":1490,"image":"https://images.pexels.com/photos/63703/speaker-portable-bluetooth-sound-63703.jpeg"},
    {"id":"p003","name":"ZenScreen 14\" Portable Monitor","category":"Electronics","price":5690,"image":"https://images.pexels.com/photos/277515/pexels-photo-277515.jpeg"},
    {"id":"p004","name":"VoltPro 20000mAh Power Bank","category":"Electronics","price":990,"image":"https://images.pexels.com/photos/4386397/pexels-photo-4386397.jpeg"},
    {"id":"p005","name":"FocusCam Webcam","category":"Electronics","price":1790,"image":"https://images.pexels.com/photos/274973/pexels-photo-274973.jpeg"},

    # Stationery
    {"id":"p006","name":"PaperNest Hardcover Notebook","category":"Stationery","price":220,"image":"https://images.pexels.com/photos/4144221/pexels-photo-4144221.jpeg"},
    {"id":"p007","name":"CloudGel Pen Set (4)","category":"Stationery","price":120,"image":"https://images.pexels.com/photos/3727487/pexels-photo-3727487.jpeg"},
    {"id":"p008","name":"DraftMate Mechanical Pencil","category":"Stationery","price":160,"image":"https://images.pexels.com/photos/210/desk-pen-notes-paper-210.jpg"},
    {"id":"p009","name":"SketchPro A4 Drawing Pad","category":"Stationery","price":290,"image":"https://images.pexels.com/photos/3825583/pexels-photo-3825583.jpeg"},
    {"id":"p010","name":"ProWriter Fountain Pen","category":"Stationery","price":450,"image":"https://images.pexels.com/photos/192553/pexels-photo-192553.jpeg"},

    # Accessories
    {"id":"p011","name":"UrbanFlow Commuter Backpack","category":"Accessories","price":1490,"image":"https://images.pexels.com/photos/1684075/pexels-photo-1684075.jpeg"},
    {"id":"p012","name":"SnapGrip Leather Wallet","category":"Accessories","price":990,"image":"https://images.pexels.com/photos/1080628/pexels-photo-1080628.jpeg"},
    {"id":"p013","name":"SolarTime Minimal Watch","category":"Accessories","price":2690,"image":"https://images.pexels.com/photos/190819/pexels-photo-190819.jpeg"},
    {"id":"p014","name":"PolarShades Sunglasses","category":"Accessories","price":560,"image":"https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg"},
    {"id":"p015","name":"MetroKey Key Organizer","category":"Accessories","price":240,"image":"https://images.pexels.com/photos/728786/pexels-photo-728786.jpeg"},

    # Clothing
    {"id":"p016","name":"AeroFit Performance T-shirt","category":"Clothing","price":350,"image":"https://images.pexels.com/photos/2983464/pexels-photo-2983464.jpeg"},
    {"id":"p017","name":"BreezeJog Active Pants","category":"Clothing","price":680,"image":"https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg"},
    {"id":"p018","name":"ComfyCrew Hoodie","category":"Clothing","price":980,"image":"https://images.pexels.com/photos/1002645/pexels-photo-1002645.jpeg"},
    {"id":"p019","name":"TrailRunner Sneakers","category":"Clothing","price":1890,"image":"https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg"},
    {"id":"p020","name":"CozyCotton Socks — 3 pack","category":"Clothing","price":140,"image":"https://images.pexels.com/photos/1859483/pexels-photo-1859483.jpeg"},

    # Kitchen
    {"id":"p021","name":"PureTaste Ceramic Mug","category":"Kitchen","price":190,"image":"https://images.pexels.com/photos/585750/pexels-photo-585750.jpeg"},
    {"id":"p022","name":"ChefMate 6-pc Knife Set","category":"Kitchen","price":2190,"image":"https://images.pexels.com/photos/357756/pexels-photo-357756.jpeg"},
    {"id":"p023","name":"QuickBlend Hand Blender","category":"Kitchen","price":1290,"image":"https://images.pexels.com/photos/4040675/pexels-photo-4040675.jpeg"},
    {"id":"p024","name":"SmartPan Nonstick Frypan 28cm","category":"Kitchen","price":890,"image":"https://images.pexels.com/photos/1435895/pexels-photo-1435895.jpeg"},
    {"id":"p025","name":"EcoCut Bamboo Cutting Board","category":"Kitchen","price":420,"image":"https://images.pexels.com/photos/318419/pexels-photo-318419.jpeg"},

    # Sports
    {"id":"p026","name":"SwiftRun Running Shoes","category":"Sports","price":1990,"image":"https://images.pexels.com/photos/19090/pexels-photo-19090.jpeg"},
    {"id":"p027","name":"FlexTrack Yoga Mat","category":"Sports","price":520,"image":"https://images.pexels.com/photos/4056723/pexels-photo-4056723.jpeg"},
    {"id":"p028","name":"HydroFlex Insulated Bottle","category":"Sports","price":260,"image":"https://images.pexels.com/photos/1546896/pexels-photo-1546896.jpeg"},
    {"id":"p029","name":"CoreStrength Foam Roller","category":"Sports","price":480,"image":"https://images.pexels.com/photos/416778/pexels-photo-416778.jpeg"},
    {"id":"p030","name":"TurboRacket Badminton Racket","category":"Sports","price":760,"image":"https://images.pexels.com/photos/163403/summer-badminton-sport-163403.jpeg"},

    # Toys
    {"id":"p031","name":"RoboBuddy Programmable Bot","category":"Toys","price":2190,"image":"https://images.pexels.com/photos/1660966/pexels-photo-1660966.jpeg"},
    {"id":"p032","name":"TeddyCuddle Plush Bear","category":"Toys","price":420,"image":"https://images.pexels.com/photos/207891/pexels-photo-207891.jpeg"},
    {"id":"p033","name":"SpeedDrift RC Car","category":"Toys","price":650,"image":"https://images.pexels.com/photos/163743/pexels-photo-163743.jpeg"},
    {"id":"p034","name":"BuildPro Wooden Blocks (50 pcs)","category":"Toys","price":390,"image":"https://images.pexels.com/photos/1660435/pexels-photo-1660435.jpeg"},
    {"id":"p035","name":"PuzzleMaster Brain Teaser","category":"Toys","price":220,"image":"https://images.pexels.com/photos/163742/puzzle-game-education-toy-163742.jpeg"},

    # Home
    {"id":"p036","name":"GlowLite Table Lamp","category":"Home","price":760,"image":"https://images.pexels.com/photos/1121123/pexels-photo-1121123.jpeg"},
    {"id":"p037","name":"DreamWeave Throw Blanket","category":"Home","price":620,"image":"https://images.pexels.com/photos/1454806/pexels-photo-1454806.jpeg"},
    {"id":"p038","name":"PureAir Aroma Diffuser","category":"Home","price":980,"image":"https://images.pexels.com/photos/374870/pexels-photo-374870.jpeg"},
    {"id":"p039","name":"CozyRug Living Room Rug","category":"Home","price":1890,"image":"https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg"},
    {"id":"p040","name":"CandleJoy Scented Set","category":"Home","price":360,"image":"https://images.pexels.com/photos/695970/pexels-photo-695970.jpeg"},

    # Extra realistic picks to reach 48+ items
    {"id":"p041","name":"SlimCharge USB-C Cable","category":"Electronics","price":220,"image":"https://images.pexels.com/photos/450035/pexels-photo-450035.jpeg"},
    {"id":"p042","name":"Notebook Deluxe A5","category":"Stationery","price":260,"image":"https://images.pexels.com/photos/207228/pexels-photo-207228.jpeg"},
    {"id":"p043","name":"Nomad Leather Card Holder","category":"Accessories","price":420,"image":"https://images.pexels.com/photos/289488/pexels-photo-289488.jpeg"},
    {"id":"p044","name":"RainGuard Compact Umbrella","category":"Accessories","price":320,"image":"https://images.pexels.com/photos/3244513/pexels-photo-3244513.jpeg"},
    {"id":"p045","name":"Chef's Silicone Spatula Set","category":"Kitchen","price":210,"image":"https://images.pexels.com/photos/33792/pexels-photo.jpg"},
    {"id":"p046","name":"TrailMate Hydration Pack","category":"Sports","price":1190,"image":"https://images.pexels.com/photos/1229351/pexels-photo-1229351.jpeg"},
    {"id":"p047","name":"ColorSplash Water Paint Set","category":"Toys","price":180,"image":"https://images.pexels.com/photos/239622/pexels-photo-239622.jpeg"},
    {"id":"p048","name":"HavenDecor Photo Frame 8x10","category":"Home","price":240,"image":"https://images.pexels.com/photos/273238/pexels-photo-273238.jpeg"},
]

# ---------------------------
# RANDOMIZE order for variety
# ---------------------------
random.shuffle(PRODUCTS)

# ---------------------------
# CART STATE
# ---------------------------
if 'cart' not in st.session_state:
    st.session_state['cart'] = []            # list of dicts: {id,name,price,qty}
if 'cart_open' not in st.session_state:
    st.session_state['cart_open'] = False

def add_to_cart(prod_id, qty=1):
    prod = next((p for p in PRODUCTS if p["id"] == prod_id), None)
    if not prod:
        return
    entry = next((e for e in st.session_state['cart'] if e['id'] == prod_id), None)
    if entry:
        entry['qty'] += qty
    else:
        st.session_state['cart'].append({"id": prod_id, "name": prod["name"], "price": prod["price"], "qty": qty})

def remove_from_cart(prod_id):
    st.session_state['cart'] = [e for e in st.session_state['cart'] if e['id'] != prod_id]

def update_qty_in_cart(prod_id, qty):
    for e in st.session_state['cart']:
        if e['id'] == prod_id:
            e['qty'] = qty
            break

def summarize_cart():
    subtotal = sum(e['price'] * e['qty'] for e in st.session_state['cart'])
    discount = subtotal * 0.05 if subtotal > 5000 else 0
    tax = round((subtotal - discount) * 0.05)
    shipping = 0 if subtotal > 3000 else 150
    total = int(round(subtotal - discount + tax + shipping))
    return {"subtotal": int(subtotal), "discount": int(discount), "tax": int(tax), "shipping": int(shipping), "total": total}

# ---------------------------
# TOP CART BAR (sticky)
# ---------------------------
cs = summarize_cart()
st.markdown(f"""
<div class="top-cart-bar">
  <div style="font-weight:700">🛍️ Mega Store — Real photos & matched items</div>
  <div>
    <button class="small-btn" onclick="window.location.reload()">🔄 Refresh</button>
    <button class="small-btn" id="cart-toggle">🛒 Cart ({len(st.session_state['cart'])}) — NT${cs['total']}</button>
  </div>
</div>
""", unsafe_allow_html=True)

# cart toggle with a simple button (Streamlit)
if st.button(f"🛒 View Cart ({len(st.session_state['cart'])})"):
    st.session_state['cart_open'] = not st.session_state['cart_open']

# ---------------------------
# CART EXPANDER / PANEL
# ---------------------------
if st.session_state['cart_open']:
    with st.expander(f"🛒 Your Cart ({len(st.session_state['cart'])} items)", expanded=True):
        if not st.session_state['cart']:
            st.info("Your cart is empty — add items from the list below.")
        else:
            for item in st.session_state['cart']:
                c1, c2, c3 = st.columns([4,2,1])
                c1.write(f"**{item['name']}**")
                new_qty = c2.number_input("Qty", min_value=1, value=item['qty'], key=f"cart_qty_{item['id']}")
                if new_qty != item['qty']:
                    update_qty_in_cart(item['id'], new_qty)
                if c3.button("Remove", key=f"remove_{item['id']}"):
                    remove_from_cart(item['id'])
                    st.success(f"Removed {item['name']}")
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
# FILTERS (top)
# ---------------------------
st.markdown("### 🔎 Browse & filter products")
search = st.text_input("Search product name")
category_list = ["All"] + sorted(list({p["category"] for p in PRODUCTS}))
category = st.selectbox("Category", category_list)
prices = [p["price"] for p in PRODUCTS]
min_price_val = 0
max_price_val = int(max(prices)) if prices else 5000
min_price, max_price = st.slider("Price range (NT$)", min_value=min_price_val, max_value=max_price_val,
                                 value=(min_price_val, max_price_val), step=50)

# ---------------------------
# FILTER PRODUCTS
# ---------------------------
filtered = PRODUCTS
if search:
    filtered = [p for p in filtered if search.lower() in p["name"].lower()]
if category != "All":
    filtered = [p for p in filtered if p["category"] == category]
filtered = [p for p in filtered if min_price <= p["price"] <= max_price]

# ---------------------------
# GRID DISPLAY (all items on one page)
# ---------------------------
cols = st.columns(4)
col_i = 0
for prod in filtered:
    with cols[col_i]:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(prod["image"], use_column_width=True)
        st.write(f"**{prod['name']}**")
        st.write(f"<span class='category-badge'>{prod['category']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='price'>NT${prod['price']}</div>", unsafe_allow_html=True)
        qty_key = f"qty_{prod['id']}"
        qty = st.number_input("Qty", min_value=1, value=1, key=qty_key, label_visibility="collapsed")
        if st.button("Add to cart", key=f"add_{prod['id']}"):
            add_to_cart(prod["id"], qty)
            st.success(f"Added {qty} × {prod['name']} to cart.")
        st.markdown("</div>", unsafe_allow_html=True)
    col_i = (col_i + 1) % 4
    if col_i == 0:
        cols = st.columns(4)

# footer summary
st.markdown("---")
cs = summarize_cart()
st.write(f"Cart items: {len(st.session_state['cart'])} • Total: NT${cs['total']}")
