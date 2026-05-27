from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# LOAD EXCEL
# -----------------------------

EXCEL_PATH = "data/JCK 2026 Price List.xlsx"

df = pd.read_excel(EXCEL_PATH)

# Clean column names
df.columns = [str(col).strip().replace("\n", " ") for col in df.columns]

# -----------------------------
# SERVE PHOTOS
# -----------------------------

app.mount("/photos", StaticFiles(directory="photos"), name="photos")

# -----------------------------
# HELPERS
# -----------------------------

def clean_value(value):

    if pd.isna(value):
        return None

    return str(value).strip()

def find_image(unique_code):

    extensions = [".png", ".jpg", ".jpeg"]

    for ext in extensions:

        path = f"photos/{unique_code}{ext}"

        if os.path.exists(path):
            return f"/photos/{unique_code}{ext}"

    return None

# -----------------------------
# ROOT
# -----------------------------

@app.get("/")
def root():
    return {"status": "running"}

# -----------------------------
# SEARCH ITEM
# -----------------------------

@app.get("/search/{code}")
def search_item(code: str):

    code = code.upper().strip()

    result = df[
        (df["Unique Code"].astype(str).str.upper() == code)
        |
        (df["Style Code"].astype(str).str.upper() == code)
    ]

    if result.empty:
        return {"error": "Item not found"}

    row = result.iloc[0]

    unique_code = clean_value(row.get("Unique Code"))

    item = {
        "unique_code": unique_code,
        "style_code": clean_value(row.get("Style Code")),
        "design": clean_value(row.get("Design")),
        "collection": clean_value(row.get("Coll'n")),
        "item_size": clean_value(row.get("Item Size")),
        "qty": clean_value(row.get("Qty")),
        "kt_col": clean_value(row.get("KT/Col")),
        "gross_wt": clean_value(row.get("Gross Wt")),
        "net_wt": clean_value(row.get("Net Wt")),
        "today_cost": clean_value(row.get("Today Cost")),
        "inward_value": clean_value(row.get("Inward Value")),
        "sale_price": clean_value(row.get("Sale Price")),
        "round_off": clean_value(row.get("Round Off")),
        "image": find_image(unique_code)
    }

    return item

# -----------------------------
# AUTOCOMPLETE
# -----------------------------

@app.get("/autocomplete")
def autocomplete(query: str):

    query = query.upper().strip()

    results = []

    for _, row in df.iterrows():

        unique_code = str(row.get("Unique Code", ""))
        style_code = str(row.get("Style Code", ""))

        if query in unique_code.upper() or query in style_code.upper():

            results.append({
                "unique_code": unique_code,
                "style_code": style_code,
                "design": row.get("Design")
            })

        if len(results) >= 10:
            break

    return results