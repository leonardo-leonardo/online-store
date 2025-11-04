import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import random

# -----------------------
# Final Streamlit Online Store — Fixed Version
# -----------------------

st.set_page_config(page_title="🛍️ Better Streamlit Store", layout="wide")
st.title("🛍️ Better Streamlit Store — 100 Named Products")

# -----------------------
# Product Catalog (100 named realistic items)
# -----------------------
CATEGORIES = ["Electronics", "Stationery", "Home", "Kitchen", "Sports", "Accessories", "Toys"]

NAMED_PRODUCTS = [
    ("ElectraKey K1 Wireless Keyboard", "Electronics"),
    ("AeroSound True Wireless Earbuds", "Electronics"),
    ("PulseTrack Fitness Band", "Electronics"),
    ("NovaView 24-Inch Monitor", "Electronics"),
    ("SwiftCharge 30W USB-C Charger", "Electronics"),
    ("LinkMate USB-C Hub 6-in-1", "Electronics"),
    ("ClearCam HD Webcam", "Electronics"),
    ("StreamCast Portable Microphone", "Electronics"),
    ("PowerVault 10000mAh Power Bank", "Electronics"),
    ("ThermaFan Desk USB Fan", "Electronics"),
    ("PixelPen Stylus Pro", "Electronics"),
    ("SonicBoom Bluetooth Speaker", "Electronics"),
    ("Orbit Smart Plug", "Electronics"),
    ("QuietNote Noise-Cancelling Headset", "Electronics"),
    ("BoltData 1TB Portable SSD", "Electronics"),
    ("LinkLight USB-C to HDMI Adapter", "Electronics"),
    ("HomeGuard Motion Sensor", "Electronics"),
    ("VisionLED Desk Lamp", "Electronics"),
    ("EchoPad Tablet Stand", "Electronics"),
    ("ClipCharge Magnetic Cable", "Electronics"),
    ("PaperNest A5 Lined Notebook", "Stationery"),
    ("FineMark Gel Pen Set (10)", "Stationery"),
    ("SketchFlow Drawing Pad", "Stationery"),
    ("ProBinder Ring Binder A4", "Stationery"),
    ("StickyTabs Multi-Color Pack", "Stationery"),
    ("DraftMate Mechanical Pencil", "Stationery"),
    ("HighLight Duo Set", "Stationery"),
    ("Desk Organizer Tray", "Stationery"),
    ("EcoPaper Recycled Notepad", "Stationery"),
    ("LabelPro Printable Labels", "Stationery"),
    ("Calligraphy Starter Kit", "Stationery"),
    ("NoteClip Magnetic Bookmark", "Stationery"),
    ("RollerGrip Eraser Set", "Stationery"),
    ("Precision Ruler Stainless 30cm", "Stationery"),
    ("StickyNote Cube — Pastels", "Stationery"),
    ("CloudCushion Memory Pillow", "Home"),
    ("BreezeAir HEPA Air Purifier", "Home"),
    ("AromaScent Diffuser", "Home"),
    ("FoldAway Laundry Basket", "Home"),
    ("WarmWeave Throw Blanket", "Home"),
    ("SlimShelf Floating Shelf", "Home"),
    ("SmartTherm Programmable Thermostat", "Home"),
    ("GlassGuard Cutting Board", "Home"),
    ("QuietStep Door Mat", "Home"),
    ("Sparkle Cleanup Kit", "Home"),
    ("TidyBox Storage Crate", "Home"),
    ("MellowGlow Night Light", "Home"),
    ("EchoFrame Photo Frame", "Home"),
    ("PlantBuddy Self-Watering Pot", "Home"),
    ("AeroDry Clothes Rack", "Home"),
    ("ChefEdge 8-Inch Chef Knife", "Kitchen"),
    ("AquaBlend Immersion Mixer", "Kitchen"),
    ("ProSip Insulated Bottle 500ml", "Kitchen"),
    ("BrewMaster Pour-Over Set", "Kitchen"),
    ("SilkSpatula Silicone Turner", "Kitchen"),
    ("PanGuard Nonstick Frypan 24cm", "Kitchen"),
    ("MeasureMate Stainless Set", "Kitchen"),
    ("FreshKeep Food Container Set", "Kitchen"),
    ("SteamEasy Vegetable Steamer", "Kitchen"),
    ("GrindMaster Salt & Pepper Mill", "Kitchen"),
    ("ChopAssist Cutting Board with Scale", "Kitchen"),
    ("SavorTray Oven Rack", "Kitchen"),
    ("QuickBoil Electric Kettle", "Kitchen"),
    ("SnackVault Airtight Jar", "Kitchen"),
    ("MiniGrill Portable BBQ", "Kitchen"),
    ("FlexRun Running Belt", "Sports"),
    ("CoreFit Yoga Mat 6mm", "Sports"),
    ("GripPro Resistance Band Set", "Sports"),
    ("AquaStride Swim Goggles", "Sports"),
    ("TrailMate Hydration Pack", "Sports"),
    ("PaceTimer Sports Watch", "Sports"),
    ("PowerRope Jump Rope", "Sports"),
    ("CourtMaster Shuttlecock Pack", "Sports"),
    ("BalancePro Training Disc", "Sports"),
    ("CycloLock Cable U-Lock", "Sports"),
    ("SpeedSock Performance Socks (3)", "Sports"),
    ("GripGlove Workout Gloves", "Sports"),
    ("RecoveryRoll Foam Roller", "Sports"),
    ("UrbanCarry Slim Wallet", "Accessories"),
    ("SolarLite Keychain Flashlight", "Accessories"),
    ("Nomad Luggage Tag", "Accessories"),
    ("WrapBand Headband Pack", "Accessories"),
    ("Mirra Compact Mirror", "Accessories"),
    ("TechSkin Cable Organizer", "Accessories"),
    ("TravelPouch Toiletry Bag", "Accessories"),
    ("ClipStand Phone Holder", "Accessories"),
    ("LoopBand Hair Tie Set", "Accessories"),
    ("WeatherShield Umbrella Compact", "Accessories"),
    ("BuildBox Wooden Blocks (50)", "Toys"),
    ("GlowPuzzle 500-piece", "Toys"),
    ("StoryTime Plush Bear", "Toys"),
    ("RaceTrack Mini Car Set", "Toys"),
    ("LogicMaze Brain Teaser", "Toys"),
    ("CraftBuddy DIY Bracelet Kit", "Toys"),
    ("AeroGlide Foam Glider", "Toys"),
    ("ColorSplash Water Paint Set", "Toys"),
    ("MiniChef Play Kitchen Tools", "Toys"),
    ("EcoPuzzle Wooden Map", "Toys")
]

# Generate products
data = []
random.seed(42)
for i, (name, cat) in enumerate(NAMED_PRODUCTS, 1):
    price = round(random.uniform(5, 120), 2)
    competitor = round(price * random.uniform(0.9, 1.1), 2)
    stock = random.randint(10, 200)
    data.append({"id": f"p{i}", "name": name, "category": cat, "base_price": price, "competitor_price": competitor, "stock": stock})

df = pd.DataFrame(data).set_index("id")

# Discounts & coupons
BULK_DISCOUNTS = [(5, 0.03), (10, 0.07), (25, 0.12)]
COUPONS = {"SAVE5": 0.05, "WELCOME10": 0.10, "SUPER20": 0.20}
PRO_DISCOUNT = 0.05

if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'coupon' not in st.session_state:
    st.session_state.coupon = None
if 'pro' not in st.session_state:
    st.session_state.pro = False

# Functions
def get_bulk_discount(qty):
    return max([d for q, d in BULK_DISCOUNTS if qty >= q] + [0])

def compute_price(pid, qty=1):
    row = df.loc[pid]
    price = row['base_price']
    if row['competitor_price'] < price * 0.99:
        price = row['competitor_price']
    price *= 1 - get_bulk_discount(qty)
    if st.session_state.coupon in COUPONS:
        price *= 1 - COUPONS[st.session_state.coupon]
    if st.session_state.pro:
        price *= 1 - PRO_DISCOUNT
    return round(price, 2)

def summarize_cart():
    subtotal = 0
    saved = 0
    lines = []
    for pid, qty in st.session_state.cart.items():
        row = df.loc[pid]
        unit_price = compute_price(pid, qty)
        subtotal += unit_price * qty
        saved += max(0, (row['base_price'] - unit_price) * qty)
        lines.append((row['name'], qty, unit_price, unit_price * qty))
    tax = round(subtotal * 0.05, 2)
    shipping = 0 if subtotal >= 50 else 4.99
    total = round(subtotal + tax + shipping, 2)
    return lines, subtotal, tax, shipping, total, saved

# Sidebar filters
st.sidebar.header("Filters")
cat = st.sidebar.selectbox("Category", ["All"] + list(df['category'].unique()))
search = st.sidebar.text_input("Search")
price_limit = st.sidebar.slider("Max price", 5.0, 200.0, 200.0)

view = df.copy()
if cat != "All":
    view = view[view['category'] == cat]
if search:
    view = view[view['name'].str.contains(search, case=False)]
view = view[view['base_price'] <= price_limit]

st.subheader("Catalog")
st.dataframe(view[['name','category','base_price','competitor_price','stock']])

pid = st.selectbox("Select product to add", options=view.index, format_func=lambda i: f"{df.loc[i,'name']} (${df.loc[i,'base_price']})")
qty = st.number_input("Quantity", 1, 50, 1)
if st.button("Add to Cart"):
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + qty
    st.success(f"Added {qty} × {df.loc[pid,'name']} to cart")

st.markdown("---")
st.header("🛒 Cart")
if not st.session_state.cart:
    st.info("Your cart is empty.")
else:
    lines, subtotal, tax, shipping, total, saved = summarize_cart()
    for name, qty, unit, line_total in lines:
        st.write(f"{qty} × {name} — ${unit} each — ${line_total}")
    st.markdown(
        f"**Subtotal:** ${subtotal}  \n"
        f"**Tax:** ${tax}  \n"
        f"**Shipping:** ${shipping}  \n"
        f"**Total:** ${total}"
    )
    st.caption(f"You saved ${saved:.2f} from discounts!")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    coupon_in = st.text_input("Coupon code", value=st.session_state.coupon or "")
    if st.button("Apply Coupon"):
        if coupon_in in COUPONS:
            st.session_state.coupon = coupon_in
            st.success(f"Applied {coupon_in}")
        else:
            st.error("Invalid coupon.")
with col2:
    st.session_state.pro = st.checkbox("Pro membership (extra 5% off)", value=st.session_state.pro)

st.caption("All data is in-memory only. Connect a DB/payment gateway for production use.")
