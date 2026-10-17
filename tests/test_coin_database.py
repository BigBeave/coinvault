"""
Unit tests for Coin Database & Numismatic Knowledge Base
"""

import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

from coin_database import COIN_CATALOG, calculate_melt_value, find_matching_coin, DEFAULT_SPOT_PRICES


def test_catalog_has_major_coins():
    required_coins = [
        "morgan_dollar",
        "peace_dollar",
        "walking_liberty_half",
        "franklin_half",
        "kennedy_half",
        "washington_quarter",
        "mercury_dime",
        "roosevelt_dime",
        "buffalo_nickel",
        "jefferson_nickel",
        "lincoln_wheat_cent",
        "american_silver_eagle",
        "saint_gaudens_double_eagle"
    ]
    for cid in required_coins:
        assert cid in COIN_CATALOG, f"Missing coin {cid} in catalog"
        coin = COIN_CATALOG[cid]
        assert "name" in coin
        assert "composition" in coin
        assert "weight_grams" in coin
        assert "diameter_mm" in coin
        assert "key_dates_and_varieties" in coin
        assert len(coin["key_dates_and_varieties"]) > 0


def test_melt_value_silver_coin():
    # Morgan Dollar contains 0.77344 troy oz silver
    res = calculate_melt_value("morgan_dollar")
    assert res["has_precious_metal"] is True
    assert res["metal"] == "Silver (.999 Fine Equivalent)"
    assert res["net_weight_troy_oz"] == 0.77344
    expected_melt = round(0.77344 * DEFAULT_SPOT_PRICES["silver"], 2)
    assert res["melt_value_usd"] == expected_melt


def test_melt_value_gold_coin():
    # Saint-Gaudens Double Eagle contains 0.9675 troy oz gold
    res = calculate_melt_value("saint_gaudens_double_eagle")
    assert res["has_precious_metal"] is True
    assert "Gold" in res["metal"]
    expected_melt = round(0.9675 * DEFAULT_SPOT_PRICES["gold"], 2)
    assert res["melt_value_usd"] == expected_melt


def test_melt_value_base_coin():
    # Buffalo Nickel is 75% Cu / 25% Ni base metal
    res = calculate_melt_value("buffalo_nickel")
    assert res["has_precious_metal"] is False
    assert res["net_weight_troy_oz"] == 0.0


def test_high_dollar_varieties_exist():
    # Verify famous high-dollar varieties are documented
    wheat_cent = COIN_CATALOG["lincoln_wheat_cent"]
    varieties = [v["date_variety"] for v in wheat_cent["key_dates_and_varieties"]]
    assert any("1955" in v for v in varieties), "1955 DDO should be present"
    assert any("1909-S VDB" in v for v in varieties), "1909-S VDB should be present"
    assert any("1943" in v for v in varieties), "1943 Bronze Cent should be present"

    buffalo = COIN_CATALOG["buffalo_nickel"]
    b_varieties = [v["date_variety"] for v in buffalo["key_dates_and_varieties"]]
    assert any("3-Legged" in v or "3 Leg" in v for v in b_varieties), "3-Legged buffalo should be present"


def test_find_matching_coin():
    assert find_matching_coin("Morgan")["id"] == "morgan_dollar"
    assert find_matching_coin("1921 Peace Dollar")["id"] == "peace_dollar"
    assert find_matching_coin("Buffalo")["id"] == "buffalo_nickel"
    assert find_matching_coin("Wheat Penny")["id"] == "lincoln_wheat_cent"
    assert find_matching_coin("Mercury")["id"] == "mercury_dime"


def test_custom_spot_prices():
    # Test that custom spot prices properly scale the calculated melt value
    res = calculate_melt_value("morgan_dollar", spot_prices={"silver": 40.0, "gold": 2500.0})
    assert res["spot_price_used"] == 40.0
    expected = round(0.77344 * 40.0, 2)
    assert res["melt_value_usd"] == expected


def test_coin_analyzer_defaults():
    from coin_analyzer import generate_coin_report

    # Franklin Half should default to authentic Franklin era (1948-1963), never 1921
    r_franklin = generate_coin_report(coin_hint="franklin_half")
    assert r_franklin["year"] == "1954"
    assert "1954 Franklin Half Dollar" in r_franklin["ebay_listing"]["title"]
    assert "COIN-FRANKL-1954-P" in r_franklin["ebay_listing"]["sku"]

    # Silver Eagle should default to >= 1986, never 1921
    r_eagle = generate_coin_report(coin_hint="american_silver_eagle")
    assert int(r_eagle["year"]) >= 1986
    assert "COIN-AMERIC" in r_eagle["ebay_listing"]["sku"]

    # Kennedy Half should default to >= 1964
    r_kennedy = generate_coin_report(coin_hint="kennedy_half")
    assert int(r_kennedy["year"]) >= 1964

    # Multiplatform listings generated
    assert "mercari_listing" in r_franklin
    assert "whatnot_listing" in r_franklin
    assert "reddit_listing" in r_franklin


def test_ancient_coins_in_catalog():
    ancient_coins = [
        "roman_denarius",
        "roman_aureus",
        "roman_sestertius",
        "athenian_owl_tetradrachm",
        "byzantine_solidus",
        "widows_mite",
        "shekel_of_tyre"
    ]
    for cid in ancient_coins:
        assert cid in COIN_CATALOG, f"Missing ancient coin: {cid}"
        coin = COIN_CATALOG[cid]
        assert "name" in coin
        assert "composition" in coin
        assert "weight_grams" in coin
        assert "key_dates_and_varieties" in coin
        assert len(coin["key_dates_and_varieties"]) >= 3


def test_world_currency_and_bullion_in_catalog():
    world_coins = [
        "british_sovereign",
        "british_britannia",
        "mexican_silver_libertad",
        "mexican_50_pesos_centenario",
        "canadian_silver_maple_leaf",
        "canadian_gold_maple_leaf",
        "south_african_krugerrand",
        "chinese_silver_panda",
        "austrian_philharmonic",
        "australian_kangaroo",
        "world_banknote_currency"
    ]
    for cid in world_coins:
        assert cid in COIN_CATALOG, f"Missing world coin or banknote: {cid}"
        coin = COIN_CATALOG[cid]
        assert "name" in coin
        assert "country" in coin
        assert "key_dates_and_varieties" in coin
        assert len(coin["key_dates_and_varieties"]) >= 3


def test_ancient_and_world_melt_values():
    # Athenian Owl Tetradrachm (0.54 oz pure silver)
    owl_melt = calculate_melt_value("athenian_owl_tetradrachm")
    assert owl_melt["has_precious_metal"] is True
    assert owl_melt["net_weight_troy_oz"] == 0.54
    assert owl_melt["melt_value_usd"] == round(0.54 * DEFAULT_SPOT_PRICES["silver"], 2)

    # British Sovereign (0.2354 oz pure gold)
    sov_melt = calculate_melt_value("british_sovereign")
    assert sov_melt["has_precious_metal"] is True
    assert sov_melt["net_weight_troy_oz"] == 0.2354
    assert sov_melt["melt_value_usd"] == round(0.2354 * DEFAULT_SPOT_PRICES["gold"], 2)

    # Mexican Centenario (1.2057 oz pure gold)
    cent_melt = calculate_melt_value("mexican_50_pesos_centenario")
    assert cent_melt["has_precious_metal"] is True
    assert cent_melt["net_weight_troy_oz"] == 1.2057
    assert cent_melt["melt_value_usd"] == round(1.2057 * DEFAULT_SPOT_PRICES["gold"], 2)

    # Mexican Silver Libertad (1.0 oz pure silver)
    lib_melt = calculate_melt_value("mexican_silver_libertad")
    assert lib_melt["has_precious_metal"] is True
    assert lib_melt["net_weight_troy_oz"] == 1.0

    # South African Krugerrand (1.0 oz pure gold)
    krug_melt = calculate_melt_value("south_african_krugerrand")
    assert krug_melt["has_precious_metal"] is True
    assert krug_melt["net_weight_troy_oz"] == 1.0

    # Biblical Widow's Mite (Ancient bronze - no precious metal melt)
    mite_melt = calculate_melt_value("widows_mite")
    assert mite_melt["has_precious_metal"] is False
    assert mite_melt["net_weight_troy_oz"] == 0.0

    # World Paper Currency (Paper substrate - no bullion melt)
    note_melt = calculate_melt_value("world_banknote_currency")
    assert note_melt["has_precious_metal"] is False
    assert note_melt["melt_value_usd"] == 0.0


def test_find_matching_ancient_and_world():
    assert find_matching_coin("Athenian Owl")["id"] == "athenian_owl_tetradrachm"
    assert find_matching_coin("Julius Caesar Denarius")["id"] == "roman_denarius"
    assert find_matching_coin("Roman Gold Aureus")["id"] == "roman_aureus"
    assert find_matching_coin("Colosseum Sestertius")["id"] == "roman_sestertius"
    assert find_matching_coin("Byzantine Solidus")["id"] == "byzantine_solidus"
    assert find_matching_coin("Widow's Mite")["id"] == "widows_mite"
    assert find_matching_coin("30 pieces of silver Tyre")["id"] == "shekel_of_tyre"
    assert find_matching_coin("British Gold Sovereign")["id"] == "british_sovereign"
    assert find_matching_coin("Mexican Libertad")["id"] == "mexican_silver_libertad"
    assert find_matching_coin("50 Pesos Centenario")["id"] == "mexican_50_pesos_centenario"
    assert find_matching_coin("Gold Maple Leaf")["id"] == "canadian_gold_maple_leaf"
    assert find_matching_coin("Krugerrand")["id"] == "south_african_krugerrand"
    assert find_matching_coin("Silver Panda")["id"] == "chinese_silver_panda"
    assert find_matching_coin("Vienna Philharmonic")["id"] == "austrian_philharmonic"
    assert find_matching_coin("Perth Kangaroo")["id"] == "australian_kangaroo"
    assert find_matching_coin("World Banknote Currency")["id"] == "world_banknote_currency"


def test_ancient_and_world_analyzer_reports():
    from coin_analyzer import generate_coin_report

    # Athenian Owl Tetradrachm report
    owl_rep = generate_coin_report(coin_hint="athenian_owl_tetradrachm")
    assert owl_rep["success"] is True
    assert "Athenian Owl" in owl_rep["coin_name"]
    assert "Ancient Coin" in owl_rep["ebay_listing"]["title"]
    assert owl_rep["melt_value"]["has_precious_metal"] is True
    assert owl_rep["pricing_estimate"]["recommended_buy_it_now"] > 500.0

    # Mexican Libertad report
    lib_rep = generate_coin_report(coin_hint="mexican_silver_libertad")
    assert lib_rep["success"] is True
    assert "World Coin" in lib_rep["ebay_listing"]["title"]
    assert lib_rep["ebay_listing"]["category_id"] == "178078"

    # World Banknote report
    note_rep = generate_coin_report(coin_hint="world_banknote_currency")
    assert note_rep["success"] is True
    assert "Banknote" in note_rep["ebay_listing"]["title"]
    assert note_rep["ebay_listing"]["category_id"] == "3411"


def test_dynamic_report_for_uncataloged_coin():
    """Verify that if vision identifies a coin that is not in the hardcoded series list, it dynamically generates a report for it rather than forcing morgan_dollar."""
    from coin_analyzer import generate_coin_report

    vision_result = {
        "coin_name": "Standing Liberty Quarter",
        "coin_id": "standing_liberty_quarter",
        "denomination": "25 Cents",
        "year": "1917",
        "mint_mark": "D",
        "country": "United States",
        "estimated_grade": "VF-20",
        "strike_type": "Regular Business Strike",
        "composition": "90% Silver 10% Copper",
        "rarity_status": "Key Variety Type 1",
        "high_value_varieties_to_inspect": [
            "1917-D Type 1 Bare Breast vs Type 2 Webbed Mail"
        ],
        "ebay_market_price_estimate": {
            "low": 75.0,
            "average": 110.0,
            "high": 175.0,
            "recommended_buy_it_now": 125.0,
            "starting_bid": 69.99
        }
    }

    report = generate_coin_report(analysis_data=vision_result)
    assert report["success"] is True
    assert report["coin_name"] == "Standing Liberty Quarter"
    assert report["year"] == "1917"
    assert report["mint_mark"] == "D"
    assert report["coin_id"] != "morgan_dollar"
    assert "Standing Liberty Quarter" in report["ebay_listing"]["title"]
    assert "Morgan" not in report["ebay_listing"]["title"]
    assert report["melt_value"]["has_precious_metal"] is True
    assert report["pricing_estimate"]["recommended_buy_it_now"] == 125.0
    assert len(report["high_dollar_varieties"]) > 0
    assert "Bare Breast" in report["high_dollar_varieties"][0]["date_variety"]


def test_uncataloged_gold_and_bronze_coins():
    """Verify uncataloged gold bullion and ancient bronze coins dynamically compute correct metal and category specs."""
    from coin_analyzer import generate_coin_report

    gold_coin = {
        "coin_name": "French 20 Francs Gold Rooster",
        "coin_id": "french_20_francs_gold",
        "denomination": "20 Francs",
        "year": "1907",
        "country": "France",
        "composition": ".900 Gold (0.1867 oz AGW)",
        "estimated_grade": "MS-63"
    }
    gold_rep = generate_coin_report(analysis_data=gold_coin)
    assert gold_rep["success"] is True
    assert "Rooster" in gold_rep["coin_name"]
    assert gold_rep["melt_value"]["has_precious_metal"] is True
    assert gold_rep["melt_value"]["metal"] == "Gold"
    assert gold_rep["ebay_listing"]["category_id"] == "256"  # World Coins

    bronze_coin = {
        "coin_name": "Alexander the Great Bronze Lepton",
        "coin_id": "alexander_bronze_lepton",
        "denomination": "Lepton",
        "year": "-330",
        "country": "Ancient Greece",
        "composition": "Ancient Bronze Alloy",
        "estimated_grade": "VF"
    }
    bronze_rep = generate_coin_report(analysis_data=bronze_coin)
    assert bronze_rep["success"] is True
    assert "330 BC" in bronze_rep["ebay_listing"]["title"]
    assert bronze_rep["ebay_listing"]["category_id"] == "4733"  # Ancient Coins
    assert bronze_rep["melt_value"]["has_precious_metal"] is False


def test_generate_report_without_hint_or_vision_raises_error():
    """Verify that calling generate_coin_report without analysis_data or coin_hint raises ValueError instead of silently defaulting to Morgan Dollar."""
    from coin_analyzer import generate_coin_report
    with pytest.raises(ValueError) as excinfo:
        generate_coin_report(coin_hint="", analysis_data=None)
    assert "Cannot generate coin report without either coin_hint or AI analysis_data" in str(excinfo.value)


def test_default_year_for_unknown_coin_not_1921():
    """Verify get_default_year_for_coin returns Unknown for coins without known years, never defaulting to 1921."""
    from coin_analyzer import get_default_year_for_coin
    meta = {"id": "custom_token", "name": "Custom Token", "years": ""}
    assert get_default_year_for_coin(meta) == "Unknown"



