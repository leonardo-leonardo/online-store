import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="🛒 Common Store", layout="wide")
st.markdown("<h1 style='text-align:center;'>🏪 Common Store</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- DATA SETUP ---
categories = [
    "Electronics", "Stationery", "Accessories", "Clothing",
    "Kitchen", "Sports", "Toys", "Home"
]

# Generate 100 products with unique images
def generate_items():
    items = []
    for i in range(1, 101):
        cat = random.choice(categories)
        name = {
            "Electronics": [
                "AeroSound Earbuds", "VoltPro Power Bank", "ZenScreen Monitor", "EchoBeam Speaker",
                "NovaCharge Cable", "LumaPhone Stand", "PulseSmart Watch", "ByteBook Tablet"
            ],
            "Stationery": [
                "Bamboo Notebook", "CloudPen Gel", "UltraNote Pad", "SketchPro Marker Set",
                "SharpEdge Scissors", "Inkwell Fountain Pen", "TaskMaster Planner", "FlexiRuler 30cm"
            ],
            "Accessories": [
                "UrbanFlow Backpack", "SnapGrip Wallet", "SolarTime Watch", "PureLeather Belt",
                "KeyMate Organizer", "ComfyCap", "PolarShades Glasses", "TrendyCase Phone Cover"
            ],
            "Clothing": [
                "AeroFit T-shirt", "BreezeJog Pants", "ComfyCrew Hoodie", "StreetWave Jacket",
                "CoolStride Socks", "UrbanWalk Shoes", "DailyFit Shorts", "AquaGuard Raincoat"
            ],
            "Kitchen": [
                "AquaBlend Mixer", "ChefMate Knife Set", "SteamEase Kettle", "SmartPan Fryer",
                "EcoCut Chopping Board", "PureTaste Mug", "QuickPrep Blender", "SpiceJoy Rack"
            ],
            "Sports": [
                "SwiftRun Shoes", "PowerGrip Gloves", "HydroFlex Bottle", "StaminaPro Rope",
                "FlexTrack Yoga Mat", "TurboTennis Racket", "WaveRider Surfboard", "CoreStrength Dumbbells"
            ],
            "Toys": [
                "BuildPro Blocks", "RoboBuddy", "MagicPuzzle Cube", "SpeedDrift Car",
                "AeroPlane Set", "GigaBear Plush", "DinoQuest Figure", "BrainBoost Game"
            ],
            "Home": [
                "GlowLite Lamp", "PureAir Diffuser", "ComfyCotton Pillow", "DreamWeave Blanket",
                "SmartTemp Fan", "AromaCandle Set", "CosyMat Rug", "BreezeCurtains"
            ]
        }[cat]
        product_name = random.choice(name)
        price = round(random.uniform(5, 200), 2)
        img_url = f"https://picsum.photos/seed/{i}/400/400"
        items.append({"id": i, "name": product_name, "category": cat, "price": price, "image": img_url})
    return items

items = generate_items()

# --- SAFE SESSION STATE INIT ---
if "cart" not in st.session_state or not isinstance(st.session_state.get("cart"), list):
    st.session_state["cart"] = []
if "coupon" not in st.session_state or not isinstance(st.session_state.get("coupon"), str):
    st.session_state["coupon"] = ""
if "pro" not in st.session_state or not isinstance(st.session_state.get("pro"), bool):
    st.session_state["pro"] = False

# --- FUNCTIONS ---
def add_to_cart(item):
    if "cart" not in st.session_state or not isinstance(st.session_state.get("cart"), list):
        st.session_state["cart"] = []
    st.session_state["cart"].append(item)

def summarize_cart(cart, coupon, pro):
    subtotal = sum(i["price"] for i in cart)
    discount = 0
    if coupon == "SAVE10":
        discount += subtotal * 0.10
    if pro:
        discount += subtotal * 0.05
    tax = (subtotal - discount) * 0.05
    shipping = 0 if subtotal > 100 else 5
    total = subtotal - discount + tax + shipping
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "total": round(total, 2)
    }

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🛍️ Browse", "🧾 Cart", "⚙️ Admin"])

# --- TAB 1: Browse ---
with tab1:
    st.subheader("🛍️ Browse Products")
    selected_category = st.selectbox("Filter by Category", ["All"] + categories, key="category_select")
    search = st.text_input("Search by name", key="search")

    filtered_items = [
        item for item in items
        if (selected_category == "All" or item["category"] == selected_category)
        and (search.lower() in item["name"].lower())
    ]

    # Show items in grid
    cols = st.columns(4)
    col_index = 0

    for item in filtered_items:
        with cols[col_index]:
            st.markdown(
                f"""
                <div style='
                    border-radius: 12px;
                    padding: 10px;
                    background: linear-gradient(145deg, #ffffff, #f0f0f0);
                    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
                    text-align: center;
                    transition: transform 0.2s ease-in-out;
                '>
                    <img src="{item['image']}" width="100%" style="border-radius:10px;">
                    <h5>{item['name']}</h5>
                    <p style='color:gray;font-size:14px;'>{item['category']}</p>
                    <h4 style='color:#0a84ff;'>${item['price']}</h4>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"Add 🛒 {item['id']}", key=f"add_{item['id']}"):
                add_to_cart(item)
        col_index = (col_index + 1) % 4
        if col_index == 0:
            cols = st.columns(4)

# --- TAB 2: Cart ---
with tab2:
    st.subheader("🧾 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty. Add some products from the Browse tab!")
    else:
        for c in st.session_state.cart:
            st.write(f"🛒 {c['name']} — ${c['price']}")
        st.text_input("Enter Coupon (SAVE10 for 10% off)", key="coupon")
        st.checkbox("Pro Member (5% extra off)", key="pro")

        cs = summarize_cart(st.session_state.cart, st.session_state.coupon, st.session_state.pro)
        st.markdown(
            f"**Subtotal:** ${cs['subtotal']}  \n"
            f"**Discount:** -${cs['discount']}  \n"
            f"**Tax:** ${cs['tax']}  \n"
            f"**Shipping:** ${cs['shipping']}  \n"
            f"**Total:** ${cs['total']}"
        )

        if st.button("Checkout ✅"):
            st.success("✅ Order placed successfully! Thank you for shopping.")
            st.session_state.cart = []

# --- TAB 3: Admin ---
with tab3:
    st.subheader("⚙️ Admin Tools")
    st.write("Manage product data or verify price list.")
    if st.checkbox("Show full product list"):
        st.dataframe(items)
