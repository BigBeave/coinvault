"""
Coin Analyzer & Numismatic AI Engine
Integrates Gemini Multimodal Vision with our numismatic database
to detect coin types, dates, mint marks, errors, compositions, values, and listing drafts.
"""

import os
import sys
import json
import base64
import re
from typing import Dict, Any, List, Optional
from PIL import Image
import io

# Ensure current module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from coin_database import COIN_CATALOG, calculate_melt_value, find_matching_coin
    from ebay_service import (
        build_ebay_title,
        normalize_mint_mark,
        generate_ebay_html_description,
        generate_ebay_prelist_url,
        build_ebay_inventory_payload,
        build_ebay_offer_payload,
        generate_mercari_listing,
        generate_whatnot_listing,
        generate_reddit_listing
    )
except ImportError:
    from backend.coin_database import COIN_CATALOG, calculate_melt_value, find_matching_coin
    from backend.ebay_service import (
        build_ebay_title,
        normalize_mint_mark,
        generate_ebay_html_description,
        generate_ebay_prelist_url,
        build_ebay_inventory_payload,
        build_ebay_offer_payload,
        generate_mercari_listing,
        generate_whatnot_listing,
        generate_reddit_listing
    )

def get_default_year_for_coin(coin_meta: Dict[str, Any]) -> str:
    """Returns an authentic baseline year within the coin's mintage period."""
    if "default_year" in coin_meta:
        return str(coin_meta["default_year"])
    cid = coin_meta.get("id", "")
    known_defaults = {
        "morgan_dollar": "1921",
        "peace_dollar": "1922",
        "walking_liberty_half": "1942",
        "franklin_half": "1954",
        "kennedy_half": "1964",
        "washington_quarter": "1964",
        "mercury_dime": "1943",
        "roosevelt_dime": "1964",
        "buffalo_nickel": "1936",
        "jefferson_nickel": "1964",
        "lincoln_wheat_cent": "1955",
        "lincoln_memorial_cent": "1982",
        "american_silver_eagle": "2021",
        "saint_gaudens_double_eagle": "1924",
        "roman_denarius": "c. 100 AD",
        "roman_aureus": "c. 54 AD",
        "roman_sestertius": "c. 117 AD",
        "athenian_owl_tetradrachm": "c. 440 BC",
        "byzantine_solidus": "c. 527 AD",
        "widows_mite": "c. 103 BC",
        "shekel_of_tyre": "c. 126 BC",
        "british_sovereign": "1902",
        "british_britannia": "2021",
        "mexican_silver_libertad": "1982",
        "mexican_50_pesos_centenario": "1947",
        "canadian_silver_maple_leaf": "1988",
        "canadian_gold_maple_leaf": "1979",
        "south_african_krugerrand": "1974",
        "chinese_silver_panda": "1989",
        "austrian_philharmonic": "2008",
        "australian_kangaroo": "1990",
        "world_banknote_currency": "1935"
    }
    if cid in known_defaults:
        return known_defaults[cid]
    years_str = coin_meta.get("years", "")
    if "-" in years_str:
        return years_str.split("-")[0].strip()
    return "1921"

NUMISMATIC_SYSTEM_PROMPT = """
You are an expert World-Class Numismatist and Coin Authenticator (PCGS / NGC Master Grader).
Analyze the provided coin photograph(s) (Obverse and/or Reverse).

Identify the coin or currency item with absolute numismatic precision and return ONLY a valid JSON object with the following schema:
{
  "coin_name": "Full series name, e.g. Morgan Silver Dollar, Athenian Owl Tetradrachm, Roman Empire Silver Denarius, Mexican Silver Libertad, British Full Gold Sovereign, World Paper Currency",
  "coin_id": "One of: morgan_dollar, peace_dollar, walking_liberty_half, franklin_half, kennedy_half, washington_quarter, mercury_dime, roosevelt_dime, buffalo_nickel, jefferson_nickel, lincoln_wheat_cent, lincoln_memorial_cent, american_silver_eagle, saint_gaudens_double_eagle, roman_denarius, roman_aureus, roman_sestertius, athenian_owl_tetradrachm, byzantine_solidus, widows_mite, shekel_of_tyre, british_sovereign, british_britannia, mexican_silver_libertad, mexican_50_pesos_centenario, canadian_silver_maple_leaf, canadian_gold_maple_leaf, south_african_krugerrand, chinese_silver_panda, austrian_philharmonic, australian_kangaroo, world_banknote_currency, or other",
  "denomination": "e.g. $1.00, Tetradrachm, Denarius, Aureus, 1 Sovereign, 1 oz, 50 Pesos, $5 Banknote",
  "year": "Detected year or era, e.g. 1921, 1955, c. 440 BC, c. 100 AD",
  "mint_mark": "e.g. P, D, S, CC, O, W, Athens (ΑΘΕ), Rome, M° (Mexico City), or None",
  "country": "e.g. United States, Roman Empire, Ancient Greece, United Kingdom, Mexico, Canada, South Africa, China, Austria, Australia, World",
  "estimated_grade": "e.g. AU-58, MS-63, VF-20, G-4, Ch VF, Ch AU, Gem CU-66 EPQ",
  "strike_type": "Regular Business Strike / Proof / Hammered Strike / Special Mint Set",
  "composition": "e.g. 90% Silver 10% Copper, 22K Gold, .999 Fine Silver, High-Grade Banknote Paper",
  "rarity_status": "Common / Semi-Key Date / Key Date / Ultra Rare",
  "surface_condition": {
    "cleaned": false,
    "details": "Details on wear, luster, centering, patina, bag marks, strike sharpness, full split bands, crispness, etc."
  },
  "detected_errors_or_varieties": [
    "Any visible die doubling, repunched mint mark, off-center strike, cuds, fancy serials, or note if standard strike"
  ],
  "ebay_market_price_estimate": {
    "low": 35.00,
    "average": 55.00,
    "high": 95.00,
    "recommended_buy_it_now": 64.99,
    "starting_bid": 39.99
  },
  "high_value_varieties_to_inspect": [
    "List of 1-3 specific famous high-value varieties for this year/series the collector should check under magnification"
  ],
  "numismatic_notes": "Expert notes on history, provenance, collectibility, grading advice, and warnings."
}
Do not include any conversational filler or markdown code blocks other than pure json if needed.
"""

def extract_base64_data(data_uri: str) -> bytes:
    """Extract raw image bytes from a data URI or base64 string."""
    if "," in data_uri:
        data_uri = data_uri.split(",", 1)[1]
    return base64.b64decode(data_uri)


def analyze_coin_with_gemini(
    images_base64: List[str],
    api_key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Calls the Gemini API (using google-genai or google.generativeai)
    to perform visual coin identification.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)

        image_parts = []
        for b64 in images_base64:
            raw_bytes = extract_base64_data(b64)
            # Detect mime type or default to image/jpeg
            mime = "image/jpeg"
            if b64.startswith("data:image/png"):
                mime = "image/png"
            elif b64.startswith("data:image/webp"):
                mime = "image/webp"

            image_parts.append(
                types.Part.from_bytes(data=raw_bytes, mime_type=mime)
            )

        prompt_contents = [NUMISMATIC_SYSTEM_PROMPT] + image_parts + [
            "Please analyze these coin image(s) carefully. Detect year, mint mark, variety, errors, and grade."
        ]

        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        resp_text = None
        last_exc = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_contents,
                )
                if response and response.text:
                    resp_text = response.text.strip()
                    break
            except Exception as m_err:
                last_exc = m_err
                continue

        if not resp_text:
            if last_exc:
                print(f"Gemini Vision call note/fallback: {last_exc}")
            return None

        # Clean json formatting
        if resp_text.startswith("```json"):
            resp_text = resp_text[7:]
        if resp_text.startswith("```"):
            resp_text = resp_text[3:]
        if resp_text.endswith("```"):
            resp_text = resp_text[:-3]

        parsed_data = json.loads(resp_text.strip())
        parsed_data["model_used"] = model_name
        return parsed_data
    except Exception as e:
        print(f"Gemini Vision call note/fallback: {e}")
        return None


def create_dynamic_coin_meta(analysis_data: Optional[Dict[str, Any]], coin_hint: str = "") -> Dict[str, Any]:
    """Dynamically construct coin metadata for unrecognized/custom coins identified by AI."""
    raw_name = (analysis_data.get("coin_name") if analysis_data else None) or coin_hint or "Uncataloged Coin"
    raw_denom = (analysis_data.get("denomination") if analysis_data else None) or "Collectible Coin"
    raw_country = (analysis_data.get("country") if analysis_data else None) or "World"
    raw_year = str(analysis_data.get("year")) if (analysis_data and analysis_data.get("year")) else "Unknown"
    raw_comp = (analysis_data.get("composition") if analysis_data else None) or "Standard Coin Metal"
    comp_lower = raw_comp.lower()
    name_lower = raw_name.lower()
    denom_lower = raw_denom.lower()

    metal_type = "base"
    purity = 0.0
    net_oz = 0.0
    weight_grams = 0.0
    diameter_mm = 0.0

    if "gold" in comp_lower or "gold" in name_lower:
        metal_type = "gold"
        purity = 0.999 if ("999" in comp_lower or "24k" in comp_lower) else 0.900
        if "1 oz" in name_lower or "1 oz" in denom_lower or "1 oz" in comp_lower:
            net_oz = 1.0
            weight_grams = 31.1
        elif "1/2 oz" in name_lower or "1/2 oz" in denom_lower:
            net_oz = 0.5
            weight_grams = 15.55
        elif "1/4 oz" in name_lower or "1/4 oz" in denom_lower:
            net_oz = 0.25
            weight_grams = 7.78
        elif "1/10 oz" in name_lower or "1/10 oz" in denom_lower:
            net_oz = 0.1
            weight_grams = 3.11
        else:
            net_oz = 0.25
            weight_grams = 7.78
    elif "silver" in comp_lower or "silver" in name_lower:
        metal_type = "silver"
        if ".999" in comp_lower or "fine silver" in comp_lower or "pure silver" in comp_lower:
            purity = 0.999
            net_oz = 1.0
            weight_grams = 31.1
        elif "90%" in comp_lower or ".900" in comp_lower:
            purity = 0.900
            if "dollar" in denom_lower or "dollar" in name_lower or "$1" in denom_lower:
                net_oz = 0.7734
                weight_grams = 26.73
                diameter_mm = 38.1
            elif "half" in denom_lower or "half" in name_lower or "50" in denom_lower:
                net_oz = 0.3617
                weight_grams = 12.5
                diameter_mm = 30.6
            elif "quarter" in denom_lower or "quarter" in name_lower or "25" in denom_lower:
                net_oz = 0.1808
                weight_grams = 6.25
                diameter_mm = 24.3
            elif "dime" in denom_lower or "dime" in name_lower or "10" in denom_lower:
                net_oz = 0.0723
                weight_grams = 2.5
                diameter_mm = 17.9
            else:
                net_oz = 0.1808
                weight_grams = 6.25
                diameter_mm = 24.3
        elif "40%" in comp_lower or ".400" in comp_lower:
            purity = 0.400
            net_oz = 0.1479
            weight_grams = 11.5
            diameter_mm = 30.6
        else:
            purity = 0.900
            net_oz = 0.1808
            weight_grams = 6.25
            diameter_mm = 24.3
    elif "paper" in comp_lower or "banknote" in comp_lower or "polymer" in comp_lower:
        metal_type = "paper"
    elif "bronze" in comp_lower:
        metal_type = "bronze"
    elif "copper" in comp_lower:
        metal_type = "copper"

    country_lower = raw_country.lower()
    if any(k in country_lower for k in ("united states", "usa", "u.s.")):
        ebay_cat_id = "253"
        ebay_cat_name = "Coins: US"
    elif any(k in country_lower for k in ("rome", "greece", "ancient", "byzantine")):
        ebay_cat_id = "4733"
        ebay_cat_name = "Coins: Ancient"
    elif metal_type == "paper":
        ebay_cat_id = "3411"
        ebay_cat_name = "Paper Money: World"
    else:
        ebay_cat_id = "256"
        ebay_cat_name = "Coins: World"

    dynamic_id = (analysis_data.get("coin_id") if (analysis_data and analysis_data.get("coin_id") and analysis_data.get("coin_id") != "other") else None) or re.sub(r'[^a-z0-9]+', '_', raw_name.lower())[:40]

    varieties = []
    if analysis_data and isinstance(analysis_data.get("high_value_varieties_to_inspect"), list):
        for v in analysis_data["high_value_varieties_to_inspect"]:
            if isinstance(v, str):
                varieties.append({
                    "date_variety": v,
                    "rarity_tier": "Variety to Inspect",
                    "estimated_value": "Market Rate",
                    "description": v
                })
            elif isinstance(v, dict):
                varieties.append(v)

    return {
        "id": dynamic_id,
        "name": raw_name,
        "denomination": raw_denom,
        "country": raw_country,
        "years": raw_year,
        "default_year": raw_year,
        "composition": raw_comp,
        "metal_type": metal_type,
        "purity": purity,
        "net_pure_metal_oz": net_oz,
        "weight_grams": weight_grams,
        "diameter_mm": diameter_mm,
        "edge": "Standard",
        "designer": "Official Mint Engraver",
        "ebay_category_id": ebay_cat_id,
        "ebay_category_name": ebay_cat_name,
        "rarity_overview": (analysis_data.get("rarity_status") if analysis_data else "Numismatic collectibility varies by condition and date."),
        "key_dates_and_varieties": varieties,
        "grade_values": {},
        "selling_tips": "Take sharp close-up photos of both sides and edges under balanced lighting."
    }


def generate_coin_report(
    analysis_data: Optional[Dict[str, Any]] = None,
    coin_hint: str = "",
    year_hint: str = "",
    mint_hint: str = "",
    obverse_url: str = "",
    reverse_url: str = "",
    spot_prices: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Takes AI vision output (or manual selection/hint) and combines it
    with the numismatic database, melt calculations, key dates, and eBay listing tools.
    """
    # 1. Determine base coin catalog entry or dynamic entry
    coin_meta = None
    target_id = ""

    if analysis_data and analysis_data.get("coin_id") in COIN_CATALOG:
        target_id = analysis_data["coin_id"]
        coin_meta = COIN_CATALOG[target_id]
    elif analysis_data and analysis_data.get("coin_id") and analysis_data.get("coin_id") != "other":
        matched = find_matching_coin(analysis_data["coin_id"])
        if matched:
            target_id = matched["id"]
            coin_meta = matched

    if not coin_meta and analysis_data and analysis_data.get("coin_name"):
        matched = find_matching_coin(analysis_data["coin_name"])
        if matched:
            target_id = matched["id"]
            coin_meta = matched

    if not coin_meta and coin_hint:
        matched = find_matching_coin(coin_hint)
        if matched:
            target_id = matched["id"]
            coin_meta = matched

    # If vision identifies a coin that is not in the hardcoded series list,
    # dynamically generate a report for it rather than forcing morgan_dollar.
    if not coin_meta and analysis_data:
        coin_meta = create_dynamic_coin_meta(analysis_data, coin_hint)
        target_id = coin_meta["id"]

    if not coin_meta:
        if coin_hint:
            coin_meta = create_dynamic_coin_meta({"coin_name": coin_hint}, coin_hint)
            target_id = coin_meta["id"]
        else:
            # Baseline demo fallback for empty parameters
            target_id = "morgan_dollar"
            coin_meta = COIN_CATALOG[target_id]

    # Extract detected or provided attributes with authentic series-appropriate defaults
    default_year = get_default_year_for_coin(coin_meta)
    year = year_hint or (str(analysis_data.get("year")) if analysis_data and analysis_data.get("year") else default_year)
    raw_mint = mint_hint or (analysis_data.get("mint_mark") if analysis_data and analysis_data.get("mint_mark") else "None")
    clean_mint = normalize_mint_mark(str(raw_mint))
    mint_mark = clean_mint or "None"
    estimated_grade = (analysis_data.get("estimated_grade") if analysis_data and analysis_data.get("estimated_grade") else "AU-58 (About Uncirculated)")
    strike_type = (analysis_data.get("strike_type") if analysis_data and analysis_data.get("strike_type") else "Regular Business Strike")

    # 2. Melt value calculation using active/custom spot prices if provided
    melt_info = calculate_melt_value(coin_meta, spot_prices=spot_prices)

    # 3. Pricing ranges
    if analysis_data and "ebay_market_price_estimate" in analysis_data:
        pricing = analysis_data["ebay_market_price_estimate"]
    else:
        # Generate realistic pricing based on catalog grade and metal type
        has_silver = coin_meta.get("metal_type") == "silver"
        has_gold = coin_meta.get("metal_type") == "gold"
        is_paper = coin_meta.get("metal_type") == "paper"
        is_ancient_bronze = coin_meta.get("metal_type") == "bronze"
        melt = melt_info.get("melt_value_usd", 0.0)

        if has_gold and melt > 0:
            base_low = round(melt * 1.03, 2)
            base_avg = round(melt * 1.08, 2)
            base_high = round(melt * 1.25, 2)
        elif has_silver and melt > 0:
            # If ancient silver (owl, shekel, denarius), numismatic premium is much higher than melt!
            if any(k in coin_meta.get("id", "") for k in ("owl", "shekel", "denarius", "ancient")):
                base_low = max(melt * 1.5, 450.0 if "owl" in coin_meta["id"] or "shekel" in coin_meta["id"] else 85.0)
                base_avg = max(melt * 2.5, 950.0 if "owl" in coin_meta["id"] or "shekel" in coin_meta["id"] else 180.0)
                base_high = max(melt * 4.0, 2200.0 if "owl" in coin_meta["id"] or "shekel" in coin_meta["id"] else 450.0)
            else:
                base_low = max(melt * 1.15, 28.0)
                base_avg = max(melt * 1.5, 45.0)
                base_high = max(melt * 2.2, 85.0)
        elif is_paper:
            base_low = 35.0
            base_avg = 95.0
            base_high = 350.0
        elif is_ancient_bronze:
            base_low = 45.0 if "widow" in coin_meta.get("id", "") else 150.0
            base_avg = 120.0 if "widow" in coin_meta.get("id", "") else 450.0
            base_high = 350.0 if "widow" in coin_meta.get("id", "") else 1200.0
        else:
            base_low = 15.0
            base_avg = 25.0
            base_high = 65.0

        pricing = {
            "low": round(base_low, 2),
            "average": round(base_avg, 2),
            "high": round(base_high, 2),
            "recommended_buy_it_now": round(base_avg * 1.1, 2),
            "starting_bid": round(base_low * 0.9, 2)
        }

    # 4. Key dates & high dollar varieties
    catalog_varieties = coin_meta.get("key_dates_and_varieties", [])
    detected_varieties = []
    if analysis_data and analysis_data.get("detected_errors_or_varieties"):
        detected_varieties = analysis_data["detected_errors_or_varieties"]

    # 5. Multiplatform listing generation (eBay, Mercari, Whatnot, Reddit)
    ebay_title = build_ebay_title(
        coin_name=coin_meta["name"],
        year=str(year),
        mint_mark=clean_mint,
        grade_or_condition=estimated_grade,
        variety_notes="Authentic",
        metal=coin_meta.get("composition", ""),
        country=coin_meta.get("country", "")
    )

    merged_coin_info = dict(coin_meta)
    merged_coin_info.update(melt_info)

    html_description = generate_ebay_html_description(
        title=ebay_title,
        coin_data=merged_coin_info,
        grade=estimated_grade,
        condition_notes=analysis_data.get("numismatic_notes") if analysis_data else "",
        obverse_img_url=obverse_url,
        reverse_img_url=reverse_url
    )

    prelist_url = generate_ebay_prelist_url(ebay_title, coin_meta.get("ebay_category_id", ""))

    sku_mint = clean_mint if clean_mint else "P"
    raw_year_str = str(year).strip()
    if raw_year_str.startswith("-") and raw_year_str[1:].isdigit():
        raw_year_str = f"{raw_year_str[1:]}BC"
    clean_sku_year = re.sub(r'[^A-Za-z0-9]', '', raw_year_str) or "GEN"
    sku = f"COIN-{target_id[:6].upper()}-{clean_sku_year}-{sku_mint}-{int(pricing['recommended_buy_it_now'])}"

    inventory_payload = build_ebay_inventory_payload(
        sku=sku,
        title=ebay_title,
        description_html=html_description,
        image_urls=[img for img in [obverse_url, reverse_url] if img]
    )

    offer_payload = build_ebay_offer_payload(
        sku=sku,
        category_id=coin_meta.get("ebay_category_id", "39464"),
        price=pricing["recommended_buy_it_now"],
        description_html=html_description
    )

    mercari_listing = generate_mercari_listing(
        title=ebay_title,
        coin_data=merged_coin_info,
        grade=estimated_grade,
        price=pricing["recommended_buy_it_now"],
        condition_notes=analysis_data.get("numismatic_notes") if analysis_data else ""
    )

    whatnot_listing = generate_whatnot_listing(
        title=ebay_title,
        coin_data=merged_coin_info,
        grade=estimated_grade,
        starting_bid=pricing["starting_bid"],
        buy_it_now=pricing["recommended_buy_it_now"]
    )

    reddit_listing = generate_reddit_listing(
        title=ebay_title,
        coin_data=merged_coin_info,
        grade=estimated_grade,
        price=pricing["recommended_buy_it_now"]
    )

    return {
        "success": True,
        "coin_id": target_id,
        "coin_name": coin_meta["name"],
        "denomination": coin_meta["denomination"],
        "year": year,
        "mint_mark": mint_mark,
        "clean_mint": clean_mint,
        "country": coin_meta["country"],
        "composition": coin_meta["composition"],
        "weight_grams": coin_meta["weight_grams"],
        "diameter_mm": coin_meta["diameter_mm"],
        "edge": coin_meta["edge"],
        "designer": coin_meta["designer"],
        "estimated_grade": estimated_grade,
        "strike_type": strike_type,
        "rarity_overview": coin_meta["rarity_overview"],
        "melt_value": melt_info,
        "grade_values_guide": coin_meta.get("grade_values", {}),
        "pricing_estimate": pricing,
        "high_dollar_varieties": catalog_varieties if catalog_varieties else coin_meta.get("key_dates_and_varieties", []),
        "detected_varieties": detected_varieties,
        "selling_tips": coin_meta.get("selling_tips", ""),
        "ai_identified": bool(analysis_data),
        "vision_model": (analysis_data.get("model_used") if analysis_data else None) or ("gemini-2.5-flash" if analysis_data else None),
        "ebay_listing": {
            "title": ebay_title,
            "category_id": coin_meta.get("ebay_category_id", ""),
            "category_name": coin_meta.get("ebay_category_name", ""),
            "sku": sku,
            "buy_it_now_price": pricing["recommended_buy_it_now"],
            "starting_bid_price": pricing["starting_bid"],
            "html_description": html_description,
            "prelist_url": prelist_url,
            "inventory_payload": inventory_payload,
            "offer_payload": offer_payload
        },
        "mercari_listing": mercari_listing,
        "whatnot_listing": whatnot_listing,
        "reddit_listing": reddit_listing
    }
