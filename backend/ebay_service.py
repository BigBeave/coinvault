"""
eBay Listing Service
Generates eBay-optimized titles (<= 80 chars), category mappings,
professional HTML listing descriptions, item specifics, quick-list deep links,
and eBay Inventory & Offer API draft payloads.
"""

import re
import urllib.parse
from typing import Dict, Any, List, Optional
import requests

EBAY_SELL_URL = "https://api.ebay.com/sell/inventory/v1"

def normalize_mint_mark(mint_str: str) -> str:
    """
    Normalizes descriptive mint strings like 'None (Philadelphia)', 'D (Denver - 1921 only)',
    'S (San Francisco)', 'CC (Carson City)', 'O (New Orleans)', 'W (West Point)'
    into standard mint marks ('D', 'S', 'CC', 'O', 'W', or '' for Philadelphia / None).
    """
    if not mint_str:
        return ""
    m = mint_str.strip()
    m_lower = m.lower()
    if any(m_lower.startswith(prefix) for prefix in ("none", "p", "phila", "philadelphia", "no mint")):
        return ""
    
    # Check for recognized letter codes at start
    match = re.match(r"^([A-Za-z]{1,2})\b", m)
    if match:
        code = match.group(1).upper()
        if code in ("D", "S", "CC", "O", "W"):
            return code
            
    if m.upper() in ("D", "S", "CC", "O", "W"):
        return m.upper()
    return ""


def build_ebay_title(
    coin_name: str,
    year: str,
    mint_mark: str = "",
    grade_or_condition: str = "Uncirculated",
    variety_notes: str = "",
    metal: str = "",
    country: str = ""
) -> str:
    """
    Constructs an eBay search-optimized title strictly under 80 characters.
    eBay title limit is 80 characters.
    """
    clean_mint = normalize_mint_mark(mint_mark)
    mint_suffix = f"-{clean_mint}" if clean_mint else ""

    # Build primary components
    parts = []
    if year:
        parts.append(f"{year}{mint_suffix}")
    parts.append(coin_name)

    if metal and "silver" in metal.lower() and "silver" not in coin_name.lower():
        parts.append("Silver")
    elif metal and "gold" in metal.lower() and "gold" not in coin_name.lower():
        parts.append("Gold")

    # If grade is long like 'AU-58 (About Uncirculated)', simplify to 'AU-58'
    clean_grade = grade_or_condition
    if "(" in clean_grade:
        clean_grade = clean_grade.split("(")[0].strip()
    if clean_grade:
        parts.append(clean_grade)

    if variety_notes and len(variety_notes) < 25:
        parts.append(variety_notes)

    # Determine accurate closing tag based on coin category/origin
    combined_ctx = f"{coin_name} {country} {metal}".lower()
    if any(k in combined_ctx for k in ("banknote", "paper money", "currency", "bill")):
        parts.append("Banknote")
    elif any(k in combined_ctx for k in ("roman", "greece", "greek", "byzantine", "biblical", "athenian", "ancient", "shekel", "prutah", "widow", "denarius", "aureus", "sestertius")):
        parts.append("Ancient Coin")
    elif any(k in combined_ctx for k in ("mexico", "mexican", "britain", "british", "united kingdom", "uk", "sovereign", "canada", "canadian", "south africa", "krugerrand", "china", "panda", "austria", "philharmonic", "australia", "kangaroo", "kookaburra", "libertad", "centenario")):
        parts.append("World Coin")
    else:
        parts.append("Old US Coin")

    # Truncate while prioritizing retaining the closing tag if possible
    while len(" ".join(parts)) > 80 and len(parts) > 3:
        # Drop the second-to-last item (e.g. variety notes or secondary modifier) before dropping the tag
        parts.pop(-2)

    title = " ".join(parts).strip()
    if len(title) > 80:
        words = title.split()
        while len(" ".join(words)) > 80 and len(words) > 2:
            if len(words) > 3:
                words.pop(-2)
            else:
                words.pop()
        title = " ".join(words)
        if len(title) > 80:
            title = title[:80]

    return title


def generate_ebay_html_description(
    title: str,
    coin_data: Dict[str, Any],
    grade: str = "Collector Grade",
    condition_notes: str = "",
    obverse_img_url: str = "",
    reverse_img_url: str = "",
    seller_name: str = "CoinVault Seller"
) -> str:
    """
    Produces a responsive, clean, professional HTML listing template
    optimized for eBay mobile app and desktop viewing.
    """
    composition = coin_data.get("composition", "N/A")
    weight = coin_data.get("weight_grams", "N/A")
    diameter = coin_data.get("diameter_mm", "N/A")
    edge = coin_data.get("edge", "Reeded")
    melt_val = coin_data.get("melt_value_usd", 0.0)
    has_precious = coin_data.get("has_precious_metal", False)

    images_html = ""
    if obverse_img_url or reverse_img_url:
        images_html = f"""
        <div style="display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin:20px 0;">
            {f'<div style="text-align:center;"><img src="{obverse_img_url}" style="max-width:280px; max-height:280px; border-radius:12px; border:1px solid #ddd; box-shadow:0 4px 10px rgba(0,0,0,0.08); object-fit:contain;"><p style="font-weight:600; color:#555; margin-top:6px;">Obverse (Front)</p></div>' if obverse_img_url else ''}
            {f'<div style="text-align:center;"><img src="{reverse_img_url}" style="max-width:280px; max-height:280px; border-radius:12px; border:1px solid #ddd; box-shadow:0 4px 10px rgba(0,0,0,0.08); object-fit:contain;"><p style="font-weight:600; color:#555; margin-top:6px;">Reverse (Back)</p></div>' if reverse_img_url else ''}
        </div>
        """

    melt_badge = ""
    if has_precious and melt_val > 0:
        melt_badge = f"""
        <div style="background:#fef3c7; border:1px solid #f59e0b; color:#92400e; padding:10px 16px; border-radius:8px; font-weight:600; margin:16px 0; text-align:center;">
            ⚡ Precious Metal Bullion Value: Approx. ${melt_val:.2f} USD minimum intrinsic melt value
        </div>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height:1.6; color:#222; margin:0; padding:12px; background:#f9fafb;">
    <div style="max-width:800px; margin:0 auto; background:#ffffff; border-radius:16px; overflow:hidden; border:1px solid #e5e7eb; box-shadow:0 4px 16px rgba(0,0,0,0.06);">
        <!-- Header Banner -->
        <div style="background:linear-gradient(135deg, #1e3a8a, #3b82f6); color:#ffffff; padding:24px 20px; text-align:center;">
            <h1 style="margin:0; font-size:22px; font-weight:700; letter-spacing:-0.5px;">{title}</h1>
            <p style="margin:6px 0 0; opacity:0.9; font-size:14px;">Authentic Numismatic Specimen &bull; Grade: {grade}</p>
        </div>

        <div style="padding:24px 20px;">
            {images_html}
            {melt_badge}

            <!-- Specifications Table -->
            <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:20px; font-size:17px;">
                🪙 Coin Specifications
            </h3>
            <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:14px;">
                <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; width:40%; border-bottom:1px solid #e2e8f0;">Series / Name</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{coin_data.get('name', 'Coin')}</td></tr>
                <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Denomination</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{coin_data.get('denomination', 'N/A')}</td></tr>
                <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Composition</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{composition}</td></tr>
                <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Weight</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{weight} grams</td></tr>
                <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Diameter</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{diameter} mm</td></tr>
                <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Edge</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{edge}</td></tr>
                <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Country of Origin</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">{coin_data.get('country', 'United States')}</td></tr>
            </table>

            <!-- Item Condition & Description -->
            <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:24px; font-size:17px;">
                🔍 Item Condition & Collector Notes
            </h3>
            <div style="background:#f3f4f6; padding:14px; border-radius:8px; font-size:14px; margin-bottom:20px;">
                <p style="margin:0 0 8px;"><strong>Estimated Grade:</strong> {grade}</p>
                <p style="margin:0 0 8px;">{condition_notes or "Please review all high-resolution photos carefully to determine grade and condition for yourself. The coin shown in the pictures is the exact coin you will receive."}</p>
                <p style="margin:0; font-size:13px; color:#4b5563;"><em>*Numismatic grading is subjective. Photos are taken under neutral lighting without filters. Never cleaned or polished.</em></p>
            </div>

            <!-- Shipping & Packaging Guarantee -->
            <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:24px; font-size:17px;">
                📦 Safe Shipping & Collector Guarantee
            </h3>
            <ul style="padding-left:20px; font-size:14px; color:#374151; margin-bottom:20px;">
                <li><strong>Archival Packaging:</strong> Shipped in a brand new, PVC-free archival coin flip or airtight acrylic capsule.</li>
                <li><strong>Safe Transit:</strong> Packed with cardboard protection inside a secure bubble mailer.</li>
                <li><strong>Fast Tracking:</strong> Ships via USPS First Class / Ground Advantage with full online tracking.</li>
                <li><strong>Authenticity Guaranteed:</strong> 100% authentic genuine coinage guaranteed or your money back.</li>
            </ul>

            <div style="text-align:center; padding:16px; border-top:1px solid #e5e7eb; color:#6b7280; font-size:12px;">
                Thank you for viewing this listing &bull; Feel free to message with any questions before bidding!
            </div>
        </div>
    </div>
</body>
</html>
    """.strip()
    return html


def generate_ebay_prelist_url(title: str, category_id: str = "") -> str:
    """
    Generates a deep link to eBay's web sell flow.
    When clicked on an iPhone or desktop, this immediately opens eBay's Sell flow
    with the title and suggested category pre-filled!
    """
    params = {"query": title}
    if category_id:
        params["categoryId"] = category_id
    query_string = urllib.parse.urlencode(params)
    return f"https://www.ebay.com/sl/prelist/suggest?{query_string}"


def build_ebay_inventory_payload(
    sku: str,
    title: str,
    description_html: str,
    image_urls: List[str],
    condition_enum: str = "USED_EXCELLENT"
) -> Dict[str, Any]:
    """
    Constructs the exact payload needed for eBay Inventory API
    PUT /sell/inventory/v1/inventory_item/{sku}
    """
    # eBay Inventory API requires valid HTTP or HTTPS URLs, data URIs are rejected
    valid_urls = [url for url in image_urls if url and (url.startswith("http://") or url.startswith("https://"))]
    if not valid_urls:
        valid_urls = ["https://via.placeholder.com/600x600.png?text=Coin+Image"]

    return {
        "product": {
            "title": title[:80],
            "description": description_html,
            "imageUrls": valid_urls
        },
        "condition": condition_enum,
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 1
            }
        }
    }


def generate_mercari_listing(
    title: str,
    coin_data: Dict[str, Any],
    grade: str,
    price: float,
    condition_notes: str = ""
) -> Dict[str, Any]:
    """Generates an optimized Mercari coin listing."""
    coin_data = coin_data or {}
    name = coin_data.get("name", "Coin")
    comp = coin_data.get("composition", "Solid Coin")
    country = coin_data.get("country", "")
    melt_val = coin_data.get("melt_value_usd", 0.0)
    has_precious = coin_data.get("has_precious_metal", False)

    tags = "#coins #silver #numismatics #collectibles #bullion"
    combined = f"{name} {country} {comp}".lower()
    if "gold" in comp.lower():
        tags = "#gold #coins #preciousmetals #numismatics #rarecoin"
    elif any(k in combined for k in ("banknote", "paper money", "currency")):
        tags = "#papermoney #banknotes #currency #collectibles #numismatics"
    elif any(k in combined for k in ("roman", "greek", "greece", "byzantine", "ancient", "athenian", "biblical", "shekel", "prutah", "widow", "denarius", "aureus", "sestertius")):
        tags = "#ancientcoins #roman #greek #numismatics #history"
    elif any(k in combined for k in ("mexico", "mexican", "britain", "british", "united kingdom", "uk", "canada", "canadian", "south africa", "china", "austria", "australia", "world", "sovereign", "krugerrand", "libertad", "philharmonic", "centenario", "maple")):
        tags = "#worldcoins #silver #bullion #numismatics #collectibles"

    melt_mention = f"\n• Bullion Melt Value: Approx. ${melt_val:.2f} USD" if has_precious and melt_val > 0 else ""

    desc = f"""FOR SALE: {title}

Coin Details:
• Series: {name}
• Estimated Grade: {grade}
• Composition: {comp}
• Weight: {coin_data.get('weight_grams', 'N/A')}g
• Diameter: {coin_data.get('diameter_mm', 'N/A')}mm{melt_mention}

Condition & Provenance:
{condition_notes or 'Authentic coin with nice original surfaces. Uncleaned and well preserved. Please review all photos for exact condition.'}

Shipping:
Ships safely packaged in a protective PVC-free flip/capsule inside a bubble mailer with USPS tracking within 24 hours of purchase!

{tags}
""".strip()

    return {
        "title": title[:80],
        "price": price,
        "category": "Vintage & Collectibles > Antique Collectibles > Coins & Money",
        "condition": "Good / Like New",
        "description": desc,
        "tags": tags
    }


def generate_whatnot_listing(
    title: str,
    coin_data: Dict[str, Any],
    grade: str,
    starting_bid: float,
    buy_it_now: float
) -> Dict[str, Any]:
    """Generates a Whatnot livestream auction card."""
    coin_data = coin_data or {}
    name = coin_data.get("name", "Coin")
    country = coin_data.get("country", "")
    comp = coin_data.get("composition", "")
    combined = f"{name} {country} {comp}".lower()

    if any(k in combined for k in ("banknote", "paper money", "currency")):
        cat = "Coins & Money > Paper Money"
    elif any(k in combined for k in ("roman", "greek", "greece", "byzantine", "ancient", "athenian", "biblical", "shekel", "prutah", "widow", "denarius", "aureus", "sestertius")):
        cat = "Coins & Money > Ancient Coins"
    elif any(k in combined for k in ("mexico", "mexican", "britain", "british", "united kingdom", "uk", "canada", "canadian", "south africa", "china", "austria", "australia", "world", "sovereign", "krugerrand", "libertad", "philharmonic", "centenario", "maple")):
        cat = "Coins & Money > World Coins"
    else:
        cat = "Coins & Money > US Coins"

    return {
        "title": title[:80],
        "category": cat,
        "starting_bid": starting_bid,
        "buy_it_now_price": buy_it_now,
        "condition": grade,
        "auction_notes": f"{name} • {grade} • {comp} • Sudden Death Auction"
    }


def generate_reddit_listing(
    title: str,
    coin_data: Dict[str, Any],
    grade: str,
    price: float
) -> str:
    """Generates a Reddit r/CoinSales & r/Pmsforsale formatted post."""
    coin_data = coin_data or {}
    melt_val = coin_data.get("melt_value_usd", 0.0)
    has_precious = coin_data.get("has_precious_metal", False)
    melt_str = f" (Melt value: ~${melt_val:.2f})" if has_precious and melt_val > 0 else ""

    return f"""[WTS] {title}

**Item Details:**
- **Coin:** {coin_data.get('name', 'Coin')}
- **Grade / Condition:** {grade}
- **Composition:** {coin_data.get('composition', 'Standard')}
- **Weight / Specs:** {coin_data.get('weight_grams', 'N/A')}g, {coin_data.get('diameter_mm', 'N/A')}mm{melt_str}
- **Asking Price:** **${price:.2f}** (OBO)

**Shipping:**
- $5 Ground Advantage with tracking / $9 Priority Mail
- Ships securely packed in flip with cardboard sandwich

**Payment:** Zelle, Venmo, PayPal F&F, CashApp (no notes please)
""".strip()


def build_ebay_offer_payload(
    sku: str,
    category_id: str,
    price: float,
    description_html: str,
    fulfillment_policy_id: str = "",
    payment_policy_id: str = "",
    return_policy_id: str = ""
) -> Dict[str, Any]:
    """
    Constructs the payload needed for eBay Offer API
    POST /sell/inventory/v1/offer
    """
    lp: Dict[str, Any] = {}
    if fulfillment_policy_id:
        lp["fulfillmentPolicyId"] = fulfillment_policy_id
    if payment_policy_id:
        lp["paymentPolicyId"] = payment_policy_id
    if return_policy_id:
        lp["returnPolicyId"] = return_policy_id

    return {
        "sku": sku,
        "marketplaceId": "EBAY_US",
        "format": "FIXED_PRICE",
        "availableQuantity": 1,
        "categoryId": str(category_id),
        "listingDescription": description_html,
        "pricingSummary": {
            "price": {
                "value": f"{price:.2f}",
                "currency": "USD"
            }
        },
        "listingPolicies": lp,
        "merchantLocationKey": "default",
        "bestOfferTerms": {
            "bestOfferEnabled": True
        }
    }


def create_ebay_live_draft(
    sku: str,
    title: str,
    description_html: str,
    image_urls: List[str],
    category_id: str,
    price: float,
    ebay_token: str
) -> Dict[str, Any]:
    """
    Attempts to create an actual live draft item on eBay using the provided OAuth token.
    """
    if not ebay_token:
        return {"success": False, "error": "No eBay User Token provided"}

    headers = {
        "Authorization": f"Bearer {ebay_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Language": "en-US"
    }

    inv_payload = build_ebay_inventory_payload(sku, title, description_html, image_urls)
    r1 = requests.put(f"{EBAY_SELL_URL}/inventory_item/{sku}", headers=headers, json=inv_payload)
    if r1.status_code not in (200, 201, 204):
        return {
            "success": False,
            "step": "inventory_item",
            "status_code": r1.status_code,
            "response": r1.text
        }

    offer_payload = build_ebay_offer_payload(sku, category_id, price, description_html)
    r2 = requests.post(f"{EBAY_SELL_URL}/offer", headers=headers, json=offer_payload)
    if r2.status_code in (200, 201):
        offer_data = r2.json()
        return {
            "success": True,
            "sku": sku,
            "offerId": offer_data.get("offerId"),
            "status": "DRAFT_CREATED",
            "details": offer_data
        }
    else:
        return {
            "success": False,
            "step": "offer",
            "status_code": r2.status_code,
            "response": r2.text
        }
