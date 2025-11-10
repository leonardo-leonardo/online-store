import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="🛒 Common Store", layout="wide")
st.markdown("<h1 style='text-align:center;'>🏪 Common Store</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- CATEGORY IMAGE KEYWORDS ---
category_images = {
    "Electronics": "electronics,gadgets,tech",
    "Stationery": "stationery,notebook,pen",
    "Accessories": "wallet,watch,belt",
    "Clothing": "clothing,tshirt,jacket,fashion",
    "Kitchen": "kitchen,utensils,appliances",
    "Sports": "sports,fitness,gear",
    "Toys": "toy,lego,plush",
    "Home": "home,decor,interior"
}

categories = list(category_images.keys())

# --- PRODUCT NAME POOLS ---
product_names = {
    "Electronics": [
        "AeroSound Earbuds", "VoltPro Power Bank", "LumaScreen Monitor", "EchoBeam Speaker",
        "NovaCharge Cable", "PulseSmart Watch", "ByteTab Tablet", "ZenBud Earphones",
        "NeoCharge Adapter", "SkyLink Router", "TrueBass Headset", "VisionPro Projector"
    ],
    "Stationery": [
        "CloudPen Gel", "TaskMaster Planner", "SketchPro Marker Set", "SharpEdge Scissors",
        "Inkwell Fountain Pen", "UltraNote Pad", "PaperMate Journal", "FlexiRuler 30cm",
        "SmoothWrite Pencil Set", "DoodleSketch Pad", "ProWriter Pen", "Notely Binder"
    ],
    "Accessories": [
        "UrbanFlow Backpack", "SnapGrip Wallet", "SolarTime Watch", "PureLeather Belt",
        "KeyMate Organizer", "ComfyCap Hat", "PolarShades Glasses", "TrendyCase Phone Cover",
        "LuxeBag Tote", "SmartStrap Watch", "MetroBuckle Belt", "ZenCase Laptop Sleeve"
    ],
    "Clothing": [
        "AeroFit T-shirt", "BreezeJog Pants", "ComfyCrew Hoodie", "StreetWave Jacket",
        "CoolStride Socks", "UrbanWalk Shoes", "DailyFit Shorts", "AquaGuard Raincoat",
        "PureCotton Tee", "FlexRun Leggings", "HikePro Jacket", "DreamWear Hoodie"
    ],
    "Kitchen": [
        "AquaBlend Mixer", "ChefMate Knife Set", "SteamEase Kettle", "SmartPan Fryer",
        "EcoCut Board", "PureTaste Mug", "QuickPrep Blender", "SpiceJoy Rack",
        "GlassEase Cup Set", "SmoothWhip Mixer", "CrispyBake Tray", "PureChef Pot Set"
    ],
    "Sports": [
        "SwiftRun Shoes", "PowerGrip Gloves", "HydroFlex Bottle", "StaminaPro Rope",
        "FlexTrack Yoga Mat", "TurboTennis Racket", "WaveRider Surfboard", "CoreStrength Dumbbells",
        "FastKick Football", "BalanceStep Board", "RideMax Helmet", "ProPulse Bike Gloves"
    ],
    "Toys": [
        "BuildPro Blocks", "RoboBuddy Bot", "MagicPuzzle Cube", "SpeedDrift Car",
        "AeroPlane Toy", "GigaBear Plush", "DinoQuest Figure", "BrainBoost Game",
        "RocketFun Launcher", "MiniCity Set", "MegaTrain Toy", "ColorSpin Puzzle"
    ],
    "Home": [
        "GlowLite Lamp", "PureAir Diffuser", "ComfyCotton Pillow", "DreamWeave Blanket",
        "SmartTemp Fan", "AromaCandle Set", "CosyMat Rug", "BreezeCurtains",
        "PureWash Towels", "HavenDecor Frame", "FreshMist Diffuser", "WarmGlow Lamp"
    ]
}

# --- GENERATE ITEMS ---
def generate_items():
    items = []
    id_counter = 1
    for cat in categories:
        for name in random.sample(product_names[cat], len(product_names[cat])):
            if id_counter > 100:
                break
            price = round(random.uniform(8, 250), 2)
            img_url = f"https://source.unsplash.com/400x400/?{category_images[cat]}"
            items.append({
                "id": id_counter,
                "name": name,
                "category": cat,
                "price": price,
                "image": img_url
            })
            id_counter += 1
    return items[:100]

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
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    search = st.text_input("Search by name")

    filtered_items = [
        item for item in items
        if (selected_category == "All" or item["category"] == selected_category)
        and (search.lower() in item["name"].lower())
    ]

    cols = st.columns(4)
    idx = 0
    for item in filtered_items:
        with cols[idx]:
            st.markdown(
                f"""
                <div style='
                    border-radius: 12px;
                    padding: 10px;
                    background: linear-gradient(145deg, #ffffff, #f5f5f5);
                    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
                    text-align: center;
                '>
                    <img src="{item['image']}" width="100%" style="border-radius:10px;">
                    <h5>{item['name']}</h5>
                    <p style='color:gray;font-size:14px;'>{item['category']}</p>
                    <h4 style='color:#0a84ff;'>${item['price']}</h4>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"Add 🛒 {item['id']}", key=f"add_{item['id']}"):
                add_to_cart(item)
        idx = (idx + 1) % 4
        if idx == 0:
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
    if st.checkbox("Show full product list"):
        st.dataframe(items)
