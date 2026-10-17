"""
Integration tests for CoinVault Flask API endpoints
"""

import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["platform"] == "CoinVault iOS"
    assert data["catalog_coins_count"] > 10


def test_list_coins(client):
    response = client.get("/api/coins")
    assert response.status_code == 200
    data = response.get_json()
    assert "coins" in data
    assert len(data["coins"]) >= 10
    names = [c["name"] for c in data["coins"]]
    assert "Morgan Silver Dollar" in names


def test_get_single_coin(client):
    response = client.get("/api/coin/morgan_dollar")
    assert response.status_code == 200
    data = response.get_json()
    assert data["coin"]["name"] == "Morgan Silver Dollar"
    assert "melt_calculation" in data
    assert data["melt_calculation"]["has_precious_metal"] is True


def test_get_invalid_coin(client):
    response = client.get("/api/coin/non_existent_coin_xyz")
    assert response.status_code == 404


def test_sample_coins(client):
    response = client.get("/api/sample-coins")
    assert response.status_code == 200
    data = response.get_json()
    assert "samples" in data
    assert len(data["samples"]) >= 4
    titles = [s["title"] for s in data["samples"]]
    assert any("Morgan" in t for t in titles)
    assert any("Lincoln" in t for t in titles)


def test_spot_prices(client):
    response = client.get("/api/spot-prices")
    assert response.status_code == 200
    data = response.get_json()
    assert "spot_prices" in data
    assert "silver" in data["spot_prices"]


def test_identify_coin_with_hint(client):
    # Identify Morgan Dollar
    payload = {
        "coin_hint": "morgan_dollar",
        "year_hint": "1893",
        "mint_hint": "S"
    }
    response = client.post("/api/identify", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["coin_id"] == "morgan_dollar"
    assert data["year"] == "1893"
    assert data["mint_mark"] == "S"
    assert "melt_value" in data
    assert data["melt_value"]["has_precious_metal"] is True
    assert "high_dollar_varieties" in data
    assert len(data["high_dollar_varieties"]) > 0
    # Check that King 1893-S is highlighted in varieties
    v_dates = [v["date_variety"] for v in data["high_dollar_varieties"]]
    assert "1893-S" in v_dates
    # Check eBay listing generated
    assert "ebay_listing" in data
    assert "1893-S" in data["ebay_listing"]["title"]
    assert "prelist_url" in data["ebay_listing"]


def test_identify_wheat_cent_with_varieties(client):
    payload = {
        "coin_hint": "lincoln_wheat_cent",
        "year_hint": "1955",
        "mint_hint": "None"
    }
    response = client.post("/api/identify", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["coin_id"] == "lincoln_wheat_cent"
    assert "1955" in data["year"]
    assert "high_dollar_varieties" in data
    varieties = [v["date_variety"] for v in data["high_dollar_varieties"]]
    assert any("1955" in v for v in varieties)


def test_create_draft_web_prelist_mode(client):
    payload = {
        "sku": "COIN-TEST-SKU-1",
        "title": "1921 Morgan Silver Dollar BU Uncirculated",
        "description_html": "<p>Test Description</p>",
        "image_urls": ["https://example.com/front.jpg"],
        "category_id": "39464",
        "price": 54.99
    }
    response = client.post("/api/listing/create-draft", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["mode"] == "WEB_PRELIST_READY"
    assert "prelist_url" in data
    assert "https://www.ebay.com/sl/prelist/suggest" in data["prelist_url"]


def test_static_files(client):
    # Root index.html
    r1 = client.get("/")
    assert r1.status_code == 200
    assert "CoinVault" in r1.data.decode("utf-8")

    # Manifest
    r2 = client.get("/manifest.json")
    assert r2.status_code == 200
    assert "CoinVault" in r2.data.decode("utf-8")

    # Service worker
    r3 = client.get("/service-worker.js")
    assert r3.status_code == 200
    assert "caches" in r3.data.decode("utf-8")


def test_upload_photo_base64(client):
    payload = {
        "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
    }
    response = client.post("/api/upload-photo", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "/static/uploads/" in data["url"]


def test_identify_with_custom_spot_prices(client):
    payload = {
        "coin_hint": "morgan_dollar",
        "spot_prices": {
            "silver": 45.0,
            "gold": 2700.0
        }
    }
    response = client.post("/api/identify", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["melt_value"]["spot_price_used"] == 45.0
    expected_melt = round(0.77344 * 45.0, 2)
    assert data["melt_value"]["melt_value_usd"] == expected_melt
    assert "mercari_listing" in data
    assert "whatnot_listing" in data
    assert "reddit_listing" in data
