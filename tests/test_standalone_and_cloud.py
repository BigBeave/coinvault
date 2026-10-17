"""
Tests for Standalone Client Mode, Offline PWA assets, and Cloud Deployment Configurations
"""

import pytest
import os
import sys
import json
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))
from main import app
from coin_database import COIN_CATALOG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_standalone_guide_route(client):
    """Verify that COINVAULT_STANDALONE_GUIDE.html is served via Flask endpoint."""
    res = client.get("/COINVAULT_STANDALONE_GUIDE.html")
    assert res.status_code == 200
    assert b"CoinVault Standalone & Cloud Guide" in res.data
    assert b"Zero-PC Architecture" in res.data


def test_general_guide_route(client):
    """Verify that COINVAULT_GUIDE.html is served via Flask endpoint."""
    res = client.get("/COINVAULT_GUIDE.html")
    assert res.status_code == 200
    assert b"Option 1: 100% Standalone iPhone Mode" in res.data


def test_cloud_config_files_exist():
    """Verify all 1-click cloud deployment files exist and are non-empty."""
    expected_files = [
        "requirements.txt",
        "Procfile",
        "render.yaml",
        "vercel.json",
        "railway.json",
        "Dockerfile",
        "COINVAULT_STANDALONE_GUIDE.html",
        "COINVAULT_STANDALONE_GUIDE.txt"
    ]
    for fname in expected_files:
        fpath = os.path.join(BASE_DIR, fname)
        assert os.path.exists(fpath), f"Missing deployment file: {fname}"
        assert os.path.getsize(fpath) > 10, f"File is too small/empty: {fname}"


def test_vercel_and_railway_json_valid():
    """Verify vercel.json and railway.json parse as valid JSON."""
    v_path = os.path.join(BASE_DIR, "vercel.json")
    with open(v_path, "r", encoding="utf-8") as f:
        v_data = json.load(f)
        assert "routes" in v_data
        assert "builds" in v_data

    r_path = os.path.join(BASE_DIR, "railway.json")
    with open(r_path, "r", encoding="utf-8") as f:
        r_data = json.load(f)
        assert "deploy" in r_data


def test_coin_engine_js_exists_and_matches_catalog():
    """Verify static/js/coin-engine.js contains all 14 coin series from the backend catalog."""
    engine_path = os.path.join(BASE_DIR, "static", "js", "coin-engine.js")
    assert os.path.exists(engine_path)
    with open(engine_path, "r", encoding="utf-8") as f:
        content = f.read()

    for cid in COIN_CATALOG.keys():
        assert cid in content, f"Coin series {cid} missing from coin-engine.js"

    # Verify functions are defined
    assert "generateCoinReport" in content
    assert "calculateMeltValue" in content
    assert "analyzeCoinDirectGemini" in content
    assert "buildEbayTitle" in content


def test_coin_engine_evaluates_in_node():
    """Verify static/js/coin-engine.js can be imported and executed without errors in Node.js."""
    script = """
    const engine = require('./static/js/coin-engine.js');
    if (Object.keys(engine.COIN_CATALOG).length < 32) process.exit(1);
    const rep1 = engine.generateCoinReport({ coinHint: 'morgan_dollar' });
    if (!rep1.success || rep1.melt_value.melt_value_usd <= 0) process.exit(2);
    if (!rep1.ebay_listing.title || rep1.ebay_listing.title.length > 80) process.exit(3);
    
    // Test Ancient Athenian Owl
    const rep2 = engine.generateCoinReport({ coinHint: 'athenian_owl_tetradrachm' });
    if (!rep2.success || !rep2.ebay_listing.title.includes('Ancient Coin')) process.exit(4);

    // Test Mexican Libertad World Coin
    const rep3 = engine.generateCoinReport({ coinHint: 'mexican_silver_libertad' });
    if (!rep3.success || !rep3.ebay_listing.title.includes('World Coin')) process.exit(5);

    // Test World Banknote
    const rep4 = engine.generateCoinReport({ coinHint: 'world_banknote_currency' });
    if (!rep4.success || !rep4.ebay_listing.title.includes('Banknote')) process.exit(6);

    console.log('SUCCESS');
    """
    res = subprocess.run(["node", "-e", script], cwd=BASE_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Node.js execution failed: {res.stderr}"
    assert "SUCCESS" in res.stdout


def test_root_and_static_files_synced():
    """Verify root index.html, manifest.json, service-worker.js exist for static hosting."""
    for fname in ["index.html", "manifest.json", "service-worker.js"]:
        root_path = os.path.join(BASE_DIR, fname)
        static_path = os.path.join(BASE_DIR, "static", fname)
        assert os.path.exists(root_path), f"Missing root {fname}"
        assert os.path.exists(static_path), f"Missing static/{fname}"


def test_ios_apple_touch_icon_and_relative_assets():
    """Verify index.html has apple-touch-icon and uses relative asset paths for GitHub Pages subpath compatibility."""
    for path in [os.path.join(BASE_DIR, "index.html"), os.path.join(BASE_DIR, "static", "index.html")]:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        assert 'rel="apple-touch-icon"' in html
        assert 'href="manifest.json"' in html
        assert 'href="/manifest.json"' not in html
        assert 'href="static/css/app.css"' in html
        assert 'href="/static/css/app.css"' not in html


def test_service_worker_relative_registration():
    """Verify app.js registers service-worker.js with relative path."""
    app_js_path = os.path.join(BASE_DIR, "static", "js", "app.js")
    with open(app_js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "navigator.serviceWorker.register('service-worker.js')" in js
    assert "navigator.serviceWorker.register('/service-worker.js')" not in js


def test_coin_engine_robust_edge_cases():
    """Verify static/js/coin-engine.js handles null/undefined inputs safely without unhandled TypeErrors."""
    script = """
    const engine = require('./static/js/coin-engine.js');
    // Test empty opts
    const rep1 = engine.generateCoinReport();
    if (!rep1.success || rep1.coin_name !== 'Morgan Silver Dollar') process.exit(1);

    // Test null coinData in listing generators
    const mercari = engine.generateMercariListing('Title', null, 'AU', 50);
    if (!mercari || mercari.title !== 'Title') process.exit(2);

    const whatnot = engine.generateWhatnotListing('Title', null, 'AU', 20, 50);
    if (!whatnot || whatnot.title !== 'Title') process.exit(3);

    const reddit = engine.generateRedditListing('Title', null, 'AU', 50);
    if (!reddit || !reddit.includes('[WTS] Title')) process.exit(4);

    const html = engine.generateEbayHtmlDescription('Title', null, 'AU', '');
    if (!html || !html.includes('Coin Specifications')) process.exit(5);

    // Test calculateMeltValue on null and unknown
    const meltNull = engine.calculateMeltValue(null);
    if (meltNull.has_precious_metal !== false) process.exit(6);

    const meltUnknown = engine.calculateMeltValue('unknown_xyz');
    if (meltUnknown.has_precious_metal !== false) process.exit(7);

    console.log('EDGE_CASES_PASSED');
    """
    res = subprocess.run(["node", "-e", script], cwd=BASE_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"Edge case testing failed: {res.stderr}"
    assert "EDGE_CASES_PASSED" in res.stdout

