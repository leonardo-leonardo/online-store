# mega_store_single_page.py
import streamlit as st
import random

# ---------------------------
# CONFIG
# ---------------------------
NUM_ITEMS = 500
COLUMNS = 4  # number of cards per row
st.set_page_config(page_title="🛒 Mega Store", layout="wide", page_icon="🛍️")

# ---------------------------
# CSS: modern hover zoom, card styling
# ---------------------------
st.markdown("""
<style>
.product-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 10px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.product-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 12px 24px rgba(0,0,0,0.2);
}
.product-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
}
.price {
  color: #0a84ff;
  font-weight: 700;
  font-size: 18px;
  margin-top: 5px;
}
.category-badge {
  background: #f0f0f0;
  color: #555;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 6px;
  display: inline-block;
  margin-bottom: 4px;
}
.add-button {
  background: #0a84ff;
  color: white;
  border-radius: 8px;
  padding: 6px 12px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  margin-top: 5px;
}
.add-button:hover {
  background: #006fd6;
}
.top-cart-bar {
  position: sticky;
  top: 0;
  background: #ffffff;
  z-index: 100;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# DATA: categories & names
# ---------------------------
CATEGORIES = ["Electronics", "Stationery", "Accessories", "Clothing", "Kitchen", "Sports", "Toys", "Home"]
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
    products=[]
    id_counter=1
    while id_counter<=num_items:
        for cat in CATEGORIES:
            base=random.choice(NAME_POOLS[cat])
            variant=random.choice([""," Pro"," X"," Plus"," Mini"," Max"])
            name=(base+variant).strip()
            price=round(random.uniform(7,399),2)
            img=f"https://picsum.photos/seed/{cat}{id_counter}/400/400"
            products.append({"id":f"item-{id_counter}","name":name,"category":cat,"price":price,"image":img})
            id_counter+=1
            if id_counter>num_items:
                break
    return products

if 'products' not in st.session_state:
    st.session_state['products']=generate_products()
PRODUCTS=st.session_state['products']

# ---------------------------
# CART STATE
# ---------------------------
if 'cart' not in st.session_state: st.session_state['cart']=[]
if 'coupon' not in st.session_state: st.session_state['coupon']=""
if 'pro' not in st.session_state: st.session_state['pro']=False

def add_to_cart(product_id,qty=1):
    prod=next((p for p in PRODUCTS if p['id']==product_id),None)
    if not prod: return
    entry=next((e for e in st.session_state['cart'] if e['id']==product_id),None)
    if entry:
        entry['qty']+=qty
    else:
        st.session_state['cart'].append({"id":prod['id'],"name":prod['name'],"price":prod['price'],"qty":qty})

def summarize_cart():
    subtotal=sum(e['price']*e['qty'] for e in st.session_state['cart'])
    discount=0
    if st.session_state['coupon']=="SAVE10": discount+=subtotal*0.10
    if st.session_state['pro']: discount+=subtotal*0.05
    tax=round((subtotal-discount)*0.05,2)
    shipping=0.0 if subtotal>=100 else 6.99
    total=round(subtotal-discount+tax+shipping,2)
    return {"subtotal":subtotal,"discount":discount,"tax":tax,"shipping":shipping,"total":total}

# ---------------------------
# TOP CART BAR
# ---------------------------
cs=summarize_cart()
st.markdown(f"""
<div class="top-cart-bar">
    <div>🛍️ Mega Store — All Products ({len(PRODUCTS)})</div>
    <div>
        Cart: {len(st.session_state['cart'])} items • Total: ${cs['total']}
        <button onclick="window.scrollTo(0,0)">🛒 View/Checkout</button>
    </div>
</div>
""",unsafe_allow_html=True)

# ---------------------------
# FILTERS
# ---------------------------
st.markdown("### Filters")
search_q=st.text_input("Search product name")
category_filter=st.selectbox("Category",["All"]+CATEGORIES)
min_price,max_price=st.slider("Price range",0.0,500.0,(0.0,500.0))

# ---------------------------
# FILTER PRODUCTS
# ---------------------------
filtered=PRODUCTS
if search_q: filtered=[p for p in filtered if search_q.lower() in p['name'].lower()]
if category_filter!="All": filtered=[p for p in filtered if p['category']==category_filter]
filtered=[p for p in filtered if min_price<=p['price']<=max_price]

# ---------------------------
# GRID DISPLAY
# ---------------------------
columns=st.columns(COLUMNS)
col_idx=0
for prod in filtered:
    with columns[col_idx]:
        st.markdown("<div class='product-card'>",unsafe_allow_html=True)
        st.image(prod['image'],use_column_width=True)
        st.markdown(f"<div class='category-badge'>{prod['category']}</div>",unsafe_allow_html=True)
        st.markdown(f"**{prod['name']}**")
        st.markdown(f"<div class='price'>${prod['price']}</div>",unsafe_allow_html=True)
        qty_key=f"qty_{prod['id']}"
        qty=st.number_input("Qty",min_value=1,value=1,key=qty_key,label_visibility="collapsed")
        if st.button("Add to Cart",key=f"add_{prod['id']}"):
            add_to_cart(prod['id'],qty)
            st.success(f"Added {qty}× {prod['name']} to cart")
        st.markdown("</div>",unsafe_allow_html=True)
    col_idx=(col_idx+1)%COLUMNS
    if col_idx==0: columns=st.columns(COLUMNS)

# ---------------------------
# CART SUMMARY
# ---------------------------
st.markdown("---")
st.markdown("### 🧾 Cart Summary")
cs=summarize_cart()
st.write(f"Items in Cart: {len(st.session_state['cart'])}")
st.write(f"Subtotal: ${cs['subtotal']}")
st.write(f"Discount: -${cs['discount']}")
st.write(f"Tax: ${cs['tax']}")
st.write(f"Shipping: ${cs['shipping']}")
st.markdown(f"**Total: ${cs['total']}**")
if st.button("Checkout ✅"):
    st.success("Order placed successfully!")
    st.session_state['cart']=[]
