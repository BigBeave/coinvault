"""
Unit tests for eBay Listing Service
"""

import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

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
from coin_database import COIN_CATALOG


def test_normalize_mint_mark():
    assert normalize_mint_mark("None (Philadelphia)") == ""
    assert normalize_mint_mark("Philadelphia") == ""
    assert normalize_mint_mark("P") == ""
    assert normalize_mint_mark("D (Denver - 1921 only)") == "D"
    assert normalize_mint_mark("D (Denver)") == "D"
    assert normalize_mint_mark("S (San Francisco)") == "S"
    assert normalize_mint_mark("CC (Carson City)") == "CC"
    assert normalize_mint_mark("O (New Orleans)") == "O"
    assert normalize_mint_mark("W (West Point)") == "W"
    assert normalize_mint_mark("CC") == "CC"
    assert normalize_mint_mark("") == ""


def test_ebay_title_with_descriptive_mint():
    # Should not produce '1921 None (Philadelphia)' or '1921 D (Denver...)'
    title1 = build_ebay_title(
        coin_name="Morgan Silver Dollar",
        year="1921",
        mint_mark="None (Philadelphia)"
    )
    assert "None (Philadelphia)" not in title1
    assert "1921 Morgan Silver Dollar" in title1

    title2 = build_ebay_title(
        coin_name="Morgan Silver Dollar",
        year="1921",
        mint_mark="D (Denver - 1921 only)"
    )
    assert "1921-D Morgan Silver Dollar" in title2
    assert "Denver - 1921" not in title2


def test_ebay_title_length_limit():
    # eBay enforces strict 80 character limit
    title = build_ebay_title(
        coin_name="Morgan Silver Dollar Super Long Extended Title That Exceeds Normal Lengths",
        year="1921",
        mint_mark="S",
        grade_or_condition="MS-65 Gem Uncirculated Full Strike Luster",
        variety_notes="Extremely Rare Variety Double Die",
        metal="90% Silver"
    )
    assert len(title) <= 80, f"Title exceeded 80 chars: length is {len(title)}"
    assert "1921-S" in title
    assert "Morgan" in title


def test_ebay_title_standard():
    title = build_ebay_title(
        coin_name="Morgan Silver Dollar",
        year="1889",
        mint_mark="CC",
        grade_or_condition="AU-50",
        metal="Silver"
    )
    assert len(title) <= 80
    assert "1889-CC" in title
    assert "Morgan Silver Dollar" in title


def test_generate_ebay_html_description():
    coin = COIN_CATALOG["morgan_dollar"]
    html = generate_ebay_html_description(
        title="1889-CC Morgan Silver Dollar AU-50",
        coin_data=coin,
        grade="AU-50",
        condition_notes="Original uncleaned surfaces with slight rim toning.",
        obverse_img_url="https://example.com/front.jpg",
        reverse_img_url="https://example.com/back.jpg"
    )
    assert "<!DOCTYPE html>" in html
    assert "1889-CC Morgan Silver Dollar" in html
    assert "90% Silver, 10% Copper" in html
    assert "26.73 grams" in html
    assert "https://example.com/front.jpg" in html
    assert "https://example.com/back.jpg" in html
    assert "Safe Shipping" in html
    assert "Authenticity Guaranteed" in html


def test_generate_ebay_prelist_url():
    url = generate_ebay_prelist_url("1921 Morgan Silver Dollar", "39464")
    assert "https://www.ebay.com/sl/prelist/suggest" in url
    assert "1921+Morgan+Silver+Dollar" in url or "1921%20Morgan%20Silver%20Dollar" in url
    assert "categoryId=39464" in url


def test_build_ebay_inventory_payload():
    payload = build_ebay_inventory_payload(
        sku="COIN-MORG-1921-P",
        title="1921 Morgan Silver Dollar AU-58",
        description_html="<p>Test</p>",
        image_urls=["https://example.com/front.jpg"],
        condition_enum="USED_EXCELLENT"
    )
    assert payload["condition"] == "USED_EXCELLENT"
    assert payload["product"]["title"] == "1921 Morgan Silver Dollar AU-58"
    assert payload["product"]["description"] == "<p>Test</p>"
    assert payload["product"]["imageUrls"] == ["https://example.com/front.jpg"]
    assert payload["availability"]["shipToLocationAvailability"]["quantity"] == 1


def test_build_ebay_offer_payload():
    payload = build_ebay_offer_payload(
        sku="COIN-MORG-1921-P",
        category_id="39464",
        price=59.99,
        description_html="<p>Test</p>"
    )
    assert payload["sku"] == "COIN-MORG-1921-P"
    assert payload["marketplaceId"] == "EBAY_US"
    assert payload["format"] == "FIXED_PRICE"
    assert payload["categoryId"] == "39464"
    assert payload["pricingSummary"]["price"]["value"] == "59.99"
    assert payload["pricingSummary"]["price"]["currency"] == "USD"
    assert payload["bestOfferTerms"]["bestOfferEnabled"] is True


def test_build_ebay_inventory_payload_filters_data_uris():
    # eBay API rejects data URIs; valid URLs should be preserved and data URIs discarded
    payload = build_ebay_inventory_payload(
        sku="TEST-SKU",
        title="Test Title",
        description_html="<p>Desc</p>",
        image_urls=["data:image/jpeg;base64,/9j/4AAQSkZJRg==", "https://example.com/coin.jpg"]
    )
    assert "https://example.com/coin.jpg" in payload["product"]["imageUrls"]
    assert "data:image/jpeg;base64,/9j/4AAQSkZJRg==" not in payload["product"]["imageUrls"]


def test_multiplatform_generators():
    coin = COIN_CATALOG["morgan_dollar"]
    mercari = generate_mercari_listing(
        title="1921 Morgan Silver Dollar AU-58",
        coin_data=coin,
        grade="AU-58",
        price=55.00
    )
    assert mercari["price"] == 55.00
    assert "1921 Morgan Silver Dollar" in mercari["title"]
    assert "#silver" in mercari["description"]

    whatnot = generate_whatnot_listing(
        title="1921 Morgan Silver Dollar AU-58",
        coin_data=coin,
        grade="AU-58",
        starting_bid=35.00,
        buy_it_now=55.00
    )
    assert whatnot["starting_bid"] == 35.00
    assert whatnot["buy_it_now_price"] == 55.00
    assert "Sudden Death" in whatnot["auction_notes"]

    reddit = generate_reddit_listing(
        title="1921 Morgan Silver Dollar AU-58",
        coin_data=coin,
        grade="AU-58",
        price=55.00
    )
    assert "[WTS]" in reddit
    assert "$55.00" in reddit
    assert "Shipping" in reddit


def test_ancient_and_world_ebay_titles():
    # Ancient Roman Denarius Title
    t_denarius = build_ebay_title(
        coin_name="Roman Empire Silver Denarius",
        year="49 BC",
        grade_or_condition="VF-20",
        metal="90% Silver",
        country="Roman Empire"
    )
    assert len(t_denarius) <= 80
    assert "49 BC" in t_denarius
    assert "Roman Empire Silver Denarius" in t_denarius
    assert "Ancient Coin" in t_denarius
    assert "Old US Coin" not in t_denarius

    # World Coin Libertad Title
    t_libertad = build_ebay_title(
        coin_name="Mexican Silver Libertad 1 oz",
        year="1982",
        mint_mark="M°",
        grade_or_condition="BU",
        metal=".999 Silver",
        country="Mexico"
    )
    assert len(t_libertad) <= 80
    assert "1982" in t_libertad
    assert "Mexican Silver Libertad 1 oz" in t_libertad
    assert "World Coin" in t_libertad
    assert "Old US Coin" not in t_libertad

    # World Banknote Title
    t_banknote = build_ebay_title(
        coin_name="World Paper Currency & Banknotes",
        year="1935",
        grade_or_condition="Gem CU-66",
        metal="Paper",
        country="World"
    )
    assert len(t_banknote) <= 80
    assert "Banknote" in t_banknote
    assert "Old US Coin" not in t_banknote


def test_ancient_and_world_multiplatform_categories():
    # Ancient Coin Whatnot category
    owl = COIN_CATALOG["athenian_owl_tetradrachm"]
    wn_owl = generate_whatnot_listing("Athenian Owl", owl, "VF", 500.0, 950.0)
    assert wn_owl["category"] == "Coins & Money > Ancient Coins"

    # World Coin Whatnot category
    sov = COIN_CATALOG["british_sovereign"]
    wn_sov = generate_whatnot_listing("Gold Sovereign", sov, "AU", 600.0, 750.0)
    assert wn_sov["category"] == "Coins & Money > World Coins"

    # Banknote Whatnot category
    note = COIN_CATALOG["world_banknote_currency"]
    wn_note = generate_whatnot_listing("Silver Certificate", note, "CU", 50.0, 150.0)
    assert wn_note["category"] == "Coins & Money > Paper Money"

    # Ancient Mercari tags
    mer_owl = generate_mercari_listing("Athenian Owl", owl, "VF", 950.0)
    assert "#ancientcoins" in mer_owl["tags"]

    # Banknote Mercari tags
    mer_note = generate_mercari_listing("Banknote", note, "CU", 150.0)
    assert "#papermoney" in mer_note["tags"]


def test_negative_and_bc_year_ebay_titles():
    # Negative year representing BC (e.g., -44 for Julius Caesar)
    t1 = build_ebay_title(
        coin_name="Roman Empire Silver Denarius",
        year="-44",
        grade_or_condition="AU-58",
        metal="90% Silver",
        country="Roman Empire"
    )
    assert len(t1) <= 80
    assert "44 BC" in t1
    assert "-44" not in t1
    assert "Ancient Coin" in t1

    # Ancient coin with descriptive mint mark
    t2 = build_ebay_title(
        coin_name="Roman Empire Silver Denarius",
        year="44 BC",
        mint_mark="Rome",
        grade_or_condition="VF-20",
        country="Roman Empire"
    )
    assert len(t2) <= 80
    assert "44 BC (Rome)" in t2
    assert "Ancient Coin" in t2


