"""
CoinVault iOS Platform - Web & API Server (Flask)
Serves the iOS mobile web application, coin recognition API,
numismatic database, and eBay listing creator.
"""

import os
import sys
from typing import Dict, Any, List, Optional
from flask import Flask, request, jsonify, send_from_directory, send_file

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coin_database import COIN_CATALOG, calculate_melt_value, DEFAULT_SPOT_PRICES
import uuid
import base64
from coin_analyzer import analyze_coin_with_gemini, generate_coin_report
from ebay_service import create_ebay_live_draft, build_ebay_title, generate_ebay_prelist_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_data_url_as_image(data_url: str, prefix: str = "coin") -> str:
    """Decodes data URL and writes to static/uploads/, returning static URL path."""
    if not data_url or not data_url.startswith("data:image"):
        return data_url
    try:
        header, encoded = data_url.split(",", 1)
        ext = "jpg"
        if "png" in header:
            ext = "png"
        elif "webp" in header:
            ext = "webp"
        raw_bytes = base64.b64decode(encoded)
        filename = f"{prefix}_{uuid.uuid4().hex[:10]}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(raw_bytes)
        return f"/static/uploads/{filename}"
    except Exception as e:
        print(f"Error saving image: {e}")
        return data_url

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
app.config["JSON_SORT_KEYS"] = False


# CORS support
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/")
def index():
    """Serves the iOS platform web app."""
    return send_file(os.path.join(STATIC_DIR, "index.html"))


@app.route("/manifest.json")
def manifest():
    """PWA Manifest for iOS Add to Home Screen."""
    return send_file(os.path.join(STATIC_DIR, "manifest.json"), mimetype="application/manifest+json")


@app.route("/service-worker.js")
def service_worker():
    """PWA Service Worker."""
    return send_file(os.path.join(STATIC_DIR, "service-worker.js"), mimetype="application/javascript")


@app.route("/COINVAULT_STANDALONE_GUIDE.html")
def standalone_guide_html():
    """Serves the Standalone iPhone & Cloud deployment guide."""
    return send_file(os.path.join(BASE_DIR, "COINVAULT_STANDALONE_GUIDE.html"))


@app.route("/COINVAULT_GUIDE.html")
def general_guide_html():
    """Serves the general platform guide."""
    return send_file(os.path.join(BASE_DIR, "COINVAULT_GUIDE.html"))


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "platform": "CoinVault iOS",
        "gemini_api_key_configured": bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")),
        "ebay_token_configured": bool(os.environ.get("EBAY_USER_TOKEN")),
        "catalog_coins_count": len(COIN_CATALOG)
    })


@app.route("/api/coins", methods=["GET"])
def list_coins():
    """Returns all coin series in the knowledge base."""
    result = []
    for cid, cdata in COIN_CATALOG.items():
        melt = calculate_melt_value(cid)
        result.append({
            "id": cid,
            "name": cdata["name"],
            "denomination": cdata["denomination"],
            "years": cdata["years"],
            "composition": cdata["composition"],
            "metal_type": cdata["metal_type"],
            "ebay_category_name": cdata.get("ebay_category_name"),
            "melt_value_usd": melt.get("melt_value_usd", 0.0),
            "key_dates_count": len(cdata.get("key_dates_and_varieties", []))
        })
    return jsonify({"coins": result})


@app.route("/api/coin/<coin_id>", methods=["GET"])
def get_coin(coin_id: str):
    """Retrieve full specifications and high-dollar varieties for a specific coin series."""
    if coin_id not in COIN_CATALOG:
        return jsonify({"error": "Coin series not found"}), 404
    data = COIN_CATALOG[coin_id]
    melt = calculate_melt_value(coin_id)
    return jsonify({"coin": data, "melt_calculation": melt})


@app.route("/api/spot-prices", methods=["GET"])
def get_spot_prices():
    """Returns precious metal spot prices."""
    return jsonify({"spot_prices": DEFAULT_SPOT_PRICES})


@app.route("/api/sample-coins", methods=["GET"])
def sample_coins():
    """Provides sample coin records for instant 1-click demo on iOS."""
    return jsonify({
        "samples": [
            {
                "id": "morgan_1921",
                "title": "1921 Morgan Silver Dollar",
                "coin_hint": "morgan_dollar",
                "year": "1921",
                "mint": "None (Philadelphia)",
                "grade": "AU-58",
                "highlight": "Last year of issue, classic 90% silver dollar",
                "obverse_img": "https://images.unsplash.com/photo-1544377193-33dcf4d68fb5?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "lincoln_1955_ddo",
                "title": "1955 Lincoln Wheat Cent (DDO)",
                "coin_hint": "lincoln_wheat_cent",
                "year": "1955",
                "mint": "None (Philadelphia)",
                "grade": "MS-63 Red-Brown",
                "highlight": "Famous Doubled Die Obverse ($1,000 - $35,000+)",
                "obverse_img": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "buffalo_1937_3leg",
                "title": "1937-D Buffalo Nickel 3-Legged",
                "coin_hint": "buffalo_nickel",
                "year": "1937",
                "mint": "D",
                "grade": "VF-30",
                "highlight": "Famous 3-Legged variety error ($500 - $15,000+)",
                "obverse_img": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "mercury_1916_d",
                "title": "1916-D Mercury Dime",
                "coin_hint": "mercury_dime",
                "year": "1916",
                "mint": "D",
                "grade": "F-12",
                "highlight": "King of Mercury Dimes ($800 - $25,000+)",
                "obverse_img": "https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "kennedy_1964_silver",
                "title": "1964 Kennedy Half Dollar (90% Silver)",
                "coin_hint": "kennedy_half",
                "year": "1964",
                "mint": "D",
                "grade": "MS-64",
                "highlight": "First year 90% solid silver Kennedy half",
                "obverse_img": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "athenian_owl_sample",
                "title": "Ancient Greece Athenian Owl Tetradrachm",
                "coin_hint": "athenian_owl_tetradrachm",
                "year": "c. 440 BC",
                "mint": "Athens (ΑΘΕ)",
                "grade": "Choice VF (NGC Ancients)",
                "highlight": "Iconic Owl of Athena with olive spray (0.54 oz pure silver)",
                "obverse_img": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "roman_denarius_caesar_sample",
                "title": "Roman Empire Silver Denarius (Julius Caesar)",
                "coin_hint": "roman_denarius",
                "year": "49 BC",
                "mint": "Rome",
                "grade": "Ch XF / AU-50",
                "highlight": "Famous Caesar Elephant & Pontifical Implements Denarius",
                "obverse_img": "https://images.unsplash.com/photo-1544377193-33dcf4d68fb5?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "mexican_libertad_sample",
                "title": "Mexican Silver Libertad 1 oz",
                "coin_hint": "mexican_silver_libertad",
                "year": "1982",
                "mint": "M° (Mexico City)",
                "grade": "MS-67 Brilliant Uncirculated",
                "highlight": "Winged Victory over Popocatépetl (1 oz .999 Fine Silver)",
                "obverse_img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "british_sovereign_sample",
                "title": "British Full Gold Sovereign",
                "coin_hint": "british_sovereign",
                "year": "1902",
                "mint": "None (London)",
                "grade": "MS-63 Uncirculated",
                "highlight": "King Edward VII & Pistrucci St George (0.2354 oz Pure Gold)",
                "obverse_img": "https://images.unsplash.com/photo-1610375461246-83df859d849d?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?w=500&auto=format&fit=crop&q=80"
            },
            {
                "id": "world_banknote_sample",
                "title": "1899 $5 Silver Certificate / World Banknote",
                "coin_hint": "world_banknote_currency",
                "year": "1899",
                "mint": "Washington DC",
                "grade": "Gem CU-66 EPQ (PMG Certified)",
                "highlight": "Iconic 'Chief' Oncpapa Vignette & Blue Treasury Seal",
                "obverse_img": "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=500&auto=format&fit=crop&q=80",
                "reverse_img": "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=500&auto=format&fit=crop&q=80"
            }
        ]
    })


@app.route("/api/upload-photo", methods=["POST"])
def upload_photo():
    """Endpoint for uploading coin photos or converting base64 data to static URLs."""
    if "file" in request.files:
        file = request.files["file"]
        if file.filename:
            ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "jpg"
            filename = f"coin_{uuid.uuid4().hex[:10]}.{ext}"
            file.save(os.path.join(UPLOAD_DIR, filename))
            return jsonify({
                "success": True,
                "url": f"/static/uploads/{filename}",
                "filename": filename
            })

    data = request.get_json(force=True, silent=True) or {}
    image_data = data.get("image_data")
    if image_data:
        saved_url = save_data_url_as_image(image_data, prefix="coin")
        return jsonify({
            "success": True,
            "url": saved_url
        })

    return jsonify({"error": "No image file or image_data provided"}), 400


@app.route("/api/identify", methods=["POST"])
def identify_coin():
    """
    Core Numismatic Identification & Valuation Endpoint.
    Analyzes coin images using Gemini Multimodal AI (if available),
    or matches against numismatic reference patterns and provides
    material composition, melt value, rarity, key dates, values, and listing draft.
    """
    data = request.get_json(force=True, silent=True) or {}
    obverse_image = data.get("obverse_image")
    reverse_image = data.get("reverse_image")
    gemini_key = data.get("gemini_api_key")
    coin_hint = data.get("coin_hint")
    year_hint = data.get("year_hint")
    mint_hint = data.get("mint_hint")
    spot_prices = data.get("spot_prices")

    images_to_analyze = []
    if obverse_image:
        images_to_analyze.append(obverse_image)
    if reverse_image:
        images_to_analyze.append(reverse_image)

    analysis_data = None
    if images_to_analyze:
        analysis_data = analyze_coin_with_gemini(
            images_base64=images_to_analyze,
            api_key=gemini_key
        )

    if not analysis_data and not coin_hint:
        return jsonify({
            "success": False,
            "error": "AI Vision requires a Gemini API key or coin series selection. Please enter a Gemini API key in Settings (⚙️) or select your coin series from the dropdown.",
            "needs_api_key": True
        }), 400

    # Save images to local static files to avoid huge payloads and enable clean eBay URLs
    saved_obverse = save_data_url_as_image(obverse_image, prefix="obverse") if obverse_image else ""
    saved_reverse = save_data_url_as_image(reverse_image, prefix="reverse") if reverse_image else ""

    # Combine analysis with numismatic knowledge base & listing engine
    report = generate_coin_report(
        analysis_data=analysis_data,
        coin_hint=coin_hint or "",
        year_hint=year_hint or "",
        mint_hint=mint_hint or "",
        obverse_url=saved_obverse or obverse_image or "",
        reverse_url=saved_reverse or reverse_image or "",
        spot_prices=spot_prices
    )

    return jsonify(report)


@app.route("/api/listing/create-draft", methods=["POST"])
def create_draft():
    """
    Creates an eBay listing draft or returns pre-filled quick listing links.
    If an eBay OAuth user token is passed or configured, it makes the live eBay API calls.
    """
    data = request.get_json(force=True, silent=True) or {}
    sku = data.get("sku", "COIN-DRAFT-1")
    title = data.get("title", "")
    description_html = data.get("description_html", "")
    image_urls = data.get("image_urls", [])
    category_id = str(data.get("category_id", "39464"))
    price = float(data.get("price", 49.99))
    ebay_token = data.get("ebay_token") or os.environ.get("EBAY_USER_TOKEN")

    if ebay_token:
        result = create_ebay_live_draft(
            sku=sku,
            title=title,
            description_html=description_html,
            image_urls=image_urls,
            category_id=category_id,
            price=price,
            ebay_token=ebay_token
        )
        return jsonify(result)

    # Prelist web mode
    prelist = generate_ebay_prelist_url(title, category_id)
    return jsonify({
        "success": True,
        "mode": "WEB_PRELIST_READY",
        "sku": sku,
        "title": title,
        "prelist_url": prelist,
        "note": "Open prelist_url directly on iOS or desktop to complete your eBay listing in 1-click!"
    })


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    print(f"\n========================================================")
    print(f"🪙 CoinVault iOS Platform running at: http://localhost:{port}")
    print(f"📲 On your iPhone (same Wi-Fi), open Safari to: http://<YOUR_LOCAL_IP>:{port}")
    print(f"========================================================\n")
    app.run(host=host, port=port, debug=False)
