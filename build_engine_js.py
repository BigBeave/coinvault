"""
Builder script to generate static/js/coin-engine.js with full numismatic database,
melt calculations, key varieties, listing generator, and client-side Gemini Vision API logic.
"""
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from coin_database import COIN_CATALOG, DEFAULT_SPOT_PRICES
from coin_analyzer import NUMISMATIC_SYSTEM_PROMPT

SAMPLE_COINS = [
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

catalog_json = json.dumps(COIN_CATALOG, indent=2)
spot_json = json.dumps(DEFAULT_SPOT_PRICES, indent=2)
sample_json = json.dumps(SAMPLE_COINS, indent=2)
system_prompt_escaped = json.dumps(NUMISMATIC_SYSTEM_PROMPT.strip())

js_code = f"""/**
 * CoinVault Standalone Client-Side Numismatic Engine
 * Runs 100% inside iOS Safari / PWA without any PC or local server needed.
 * Includes complete numismatic catalog, melt calculation formulas, high-dollar varieties,
 * direct Gemini Vision API integration, and selling listing generator.
 */

(function(root) {{
  'use strict';

  // 1. Precious Metal Baseline Spot Prices (USD)
  const DEFAULT_SPOT_PRICES = {spot_json};

  // 2. Full Coin Knowledge Base (32 Comprehensive Series)
  const COIN_CATALOG = {catalog_json};

  // 3. Pre-loaded Sample Coins for 1-Tap Offline Testing
  const SAMPLE_COINS = {sample_json};

  // 4. Numismatic AI Vision Prompt
  const NUMISMATIC_SYSTEM_PROMPT = {system_prompt_escaped};

  // 5. Normalizes mint strings to standard single/double letter code
  function normalizeMintMark(mintStr) {{
    if (!mintStr) return '';
    const m = String(mintStr).trim();
    const mLower = m.toLowerCase();

    if (['none', 'no mint', 'philadelphia', 'phila'].some(p => mLower.startsWith(p))) {{
      return '';
    }}
    if (m === 'P' || mLower === 'p (philadelphia)') {{
      return '';
    }}
    if (mLower.includes('perth')) {{
      return 'P';
    }}
    if (mLower.startsWith('m°') || mLower.startsWith('mo')) {{
      return 'M°';
    }}

    const match = m.match(/^([A-Za-z]{{1,2}})\\b/);
    if (match) {{
      const code = match[1].toUpperCase();
      if (['D', 'S', 'CC', 'O', 'W'].includes(code)) return code;
    }}

    const clean = m.split('(')[0].trim();
    if (['philadelphia', 'phila', 'none'].includes(clean.toLowerCase())) {{
      return '';
    }}
    if (clean.length <= 25) {{
      return clean;
    }}
    return '';
  }}

  // 6. Default authentic baseline year for series
  function getDefaultYearForCoin(coinMeta) {{
    if (!coinMeta) return '1921';
    if (coinMeta.default_year) return String(coinMeta.default_year);
    const cid = coinMeta.id || '';
    const knownDefaults = {{
      morgan_dollar: '1921',
      peace_dollar: '1922',
      walking_liberty_half: '1942',
      franklin_half: '1954',
      kennedy_half: '1964',
      washington_quarter: '1964',
      mercury_dime: '1943',
      roosevelt_dime: '1964',
      buffalo_nickel: '1936',
      jefferson_nickel: '1964',
      lincoln_wheat_cent: '1955',
      lincoln_memorial_cent: '1982',
      american_silver_eagle: '2021',
      saint_gaudens_double_eagle: '1924',
      roman_denarius: 'c. 100 AD',
      roman_aureus: 'c. 54 AD',
      roman_sestertius: 'c. 117 AD',
      athenian_owl_tetradrachm: 'c. 440 BC',
      byzantine_solidus: 'c. 527 AD',
      widows_mite: 'c. 103 BC',
      shekel_of_tyre: 'c. 126 BC',
      british_sovereign: '1902',
      british_britannia: '2021',
      mexican_silver_libertad: '1982',
      mexican_50_pesos_centenario: '1947',
      canadian_silver_maple_leaf: '1988',
      canadian_gold_maple_leaf: '1979',
      south_african_krugerrand: '1974',
      chinese_silver_panda: '1989',
      austrian_philharmonic: '2008',
      australian_kangaroo: '1990',
      world_banknote_currency: '1935'
    }};
    if (knownDefaults[cid]) return knownDefaults[cid];
    if (coinMeta.years && coinMeta.years.includes('-')) {{
      return coinMeta.years.split('-')[0].trim();
    }}
    return '1921';
  }}

  // 7. Calculate precious metal melt/bullion value
  function calculateMeltValue(coinId, spotPrices) {{
    const prices = Object.assign({{}}, DEFAULT_SPOT_PRICES, spotPrices || {{}});
    const coin = COIN_CATALOG[coinId];
    if (!coin) {{
      return {{ has_precious_metal: false, melt_value_usd: 0.0, details: 'Unknown coin' }};
    }}

    const metalType = coin.metal_type;
    const netOz = coin.net_pure_metal_oz || 0.0;

    if (metalType === 'paper') {{
      return {{
        has_precious_metal: false,
        metal: 'Banknote Substrate (Cotton/Polymer)',
        net_weight_troy_oz: 0.0,
        melt_value_usd: 0.0,
        details: 'Paper currency (Value is 100% numismatic / collector value)'
      }};
    }}

    if (metalType === 'silver' && netOz > 0) {{
      const melt = Math.round(netOz * prices.silver * 100) / 100;
      return {{
        has_precious_metal: true,
        metal: 'Silver (.999 Fine Equivalent)',
        net_weight_troy_oz: netOz,
        spot_price_used: prices.silver,
        melt_value_usd: melt,
        details: `${{netOz.toFixed(4)}} oz Silver @ $${{prices.silver.toFixed(2)}}/oz = $${{melt.toFixed(2)}}`
      }};
    }} else if (metalType === 'gold' && netOz > 0) {{
      const melt = Math.round(netOz * prices.gold * 100) / 100;
      return {{
        has_precious_metal: true,
        metal: 'Gold',
        net_weight_troy_oz: netOz,
        spot_price_used: prices.gold,
        melt_value_usd: melt,
        details: `${{netOz.toFixed(4)}} oz Gold @ $${{prices.gold.toFixed(2)}}/oz = $${{melt.toFixed(2)}}`
      }};
    }} else if (metalType === 'copper') {{
      const weightLbs = ((coin.weight_grams || 3.11) * 0.95) / 453.592;
      const melt = Math.round(weightLbs * (prices.copper_per_lb || 4.30) * 1000) / 1000;
      return {{
        has_precious_metal: false,
        metal: '95% Pre-1982 Copper',
        net_weight_troy_oz: 0.0,
        melt_value_usd: melt,
        details: `Approx. ~$${{melt.toFixed(3)}} raw copper metal content`
      }};
    }} else if (metalType === 'bronze') {{
      return {{
        has_precious_metal: false,
        metal: 'Ancient Bronze / Orichalcum',
        net_weight_troy_oz: 0.0,
        melt_value_usd: 0.0,
        details: 'Ancient bronze alloy (Value is 100% numismatic / archaeological)'
      }};
    }}

    return {{
      has_precious_metal: false,
      metal: 'Base Metal (Nickel/Zinc/Clad)',
      net_weight_troy_oz: 0.0,
      melt_value_usd: 0.0,
      details: 'No precious metal bullion content (value is numismatic only)'
    }};
  }}

  // 8. Smart lookup in the coin catalog based on text or keywords
  function findMatchingCoin(query) {{
    if (!query) return null;
    const q = String(query).toLowerCase().trim();

    // 1. Exact ID or exact series name match
    for (const [coinId, data] of Object.entries(COIN_CATALOG)) {{
      if (coinId === q || data.name.toLowerCase() === q) return data;
    }}

    // 2. Ancient coin distinctive tokens
    if (q.includes('denarius') || q.includes('caesar')) return COIN_CATALOG.roman_denarius;
    if (q.includes('aureus')) return COIN_CATALOG.roman_aureus;
    if (q.includes('sestertius') || q.includes('sesterce')) return COIN_CATALOG.roman_sestertius;
    if (q.includes('tetradrachm') || q.includes('owl') || q.includes('athenian') || q.includes('athens')) return COIN_CATALOG.athenian_owl_tetradrachm;
    if (q.includes('solidus') || q.includes('byzantine')) return COIN_CATALOG.byzantine_solidus;
    if (q.includes('widow') || q.includes('mite') || q.includes('prutah') || q.includes('lepton')) return COIN_CATALOG.widows_mite;
    if (q.includes('tyre') || q.includes('shekel') || q.includes('30 pieces') || q.includes('thirty pieces')) return COIN_CATALOG.shekel_of_tyre;

    // 3. World coins & bullion distinctive tokens
    if (q.includes('sovereign')) return COIN_CATALOG.british_sovereign;
    if (q.includes('britannia')) return COIN_CATALOG.british_britannia;
    if (q.includes('libertad')) return COIN_CATALOG.mexican_silver_libertad;
    if (q.includes('centenario') || q.includes('50 pesos')) return COIN_CATALOG.mexican_50_pesos_centenario;
    if (q.includes('maple')) {{
      if (q.includes('gold')) return COIN_CATALOG.canadian_gold_maple_leaf;
      return COIN_CATALOG.canadian_silver_maple_leaf;
    }}
    if (q.includes('krugerrand') || q.includes('kruger')) return COIN_CATALOG.south_african_krugerrand;
    if (q.includes('panda')) return COIN_CATALOG.chinese_silver_panda;
    if (q.includes('philharmonic') || q.includes('vienna')) return COIN_CATALOG.austrian_philharmonic;
    if (q.includes('kangaroo') || q.includes('kookaburra') || q.includes('nugget')) return COIN_CATALOG.australian_kangaroo;

    // 4. Banknotes & paper currency
    if (['banknote', 'paper money', 'paper currency', 'bill', 'certificate', 'pmg'].some(k => q.includes(k))) {{
      return COIN_CATALOG.world_banknote_currency;
    }}

    // 5. Classic US series distinctive tokens
    if (q.includes('peace')) return COIN_CATALOG.peace_dollar;
    if (q.includes('morgan')) return COIN_CATALOG.morgan_dollar;
    if (q.includes('walking')) return COIN_CATALOG.walking_liberty_half;
    if (q.includes('franklin')) return COIN_CATALOG.franklin_half;
    if (q.includes('kennedy')) return COIN_CATALOG.kennedy_half;
    if (q.includes('washington')) return COIN_CATALOG.washington_quarter;
    if (q.includes('mercury')) return COIN_CATALOG.mercury_dime;
    if (q.includes('roosevelt')) return COIN_CATALOG.roosevelt_dime;
    if (q.includes('buffalo')) return COIN_CATALOG.buffalo_nickel;
    if (q.includes('jefferson')) return COIN_CATALOG.jefferson_nickel;
    if (q.includes('wheat')) return COIN_CATALOG.lincoln_wheat_cent;
    if (q.includes('memorial')) return COIN_CATALOG.lincoln_memorial_cent;
    if (q.includes('eagle') && q.includes('silver')) return COIN_CATALOG.american_silver_eagle;
    if (q.includes('gaudens') || q.includes('double eagle')) return COIN_CATALOG.saint_gaudens_double_eagle;

    // 6. Substring match on full name
    for (const [coinId, data] of Object.entries(COIN_CATALOG)) {{
      if (q.includes(data.name.toLowerCase())) return data;
    }}

    // 7. Fallback by denomination
    if (q.includes('dollar')) return COIN_CATALOG.morgan_dollar;
    if (q.includes('half')) return COIN_CATALOG.walking_liberty_half;
    if (q.includes('quarter')) return COIN_CATALOG.washington_quarter;
    if (q.includes('dime')) return COIN_CATALOG.mercury_dime;
    if (q.includes('nickel')) return COIN_CATALOG.buffalo_nickel;
    if (q.includes('penny') || q.includes('cent')) return COIN_CATALOG.lincoln_wheat_cent;

    return null;
  }}

  function buildEbayTitle(coinName, year, mintMark, gradeOrCondition, varietyNotes, metal, country) {{
    const cleanMint = normalizeMintMark(mintMark || '');
    let cleanYear = year ? String(year).trim() : '';
    if (cleanYear.startsWith('-') && /^\\d+$/.test(cleanYear.slice(1))) {{
      cleanYear = cleanYear.slice(1) + ' BC';
    }}

    const parts = [];
    if (cleanYear) {{
      if (cleanMint) {{
        if (cleanYear.toLowerCase().includes('bc') || cleanYear.toLowerCase().includes('ad') || cleanYear.includes(' ')) {{
          parts.push(`${{cleanYear}} (${{cleanMint}})`);
        }} else {{
          parts.push(`${{cleanYear}}-${{cleanMint}}`);
        }}
      }} else {{
        parts.push(cleanYear);
      }}
    }}
    parts.push(coinName);

    const metalStr = String(metal || '').toLowerCase();
    const nameStr = String(coinName || '').toLowerCase();
    if (metalStr.includes('silver') && !nameStr.includes('silver')) {{
      parts.push('Silver');
    }} else if (metalStr.includes('gold') && !nameStr.includes('gold')) {{
      parts.push('Gold');
    }}

    // If grade is long like 'AU-58 (About Uncirculated)', simplify to 'AU-58'
    let cleanGrade = gradeOrCondition || '';
    if (cleanGrade.includes('(')) {{
      cleanGrade = cleanGrade.split('(')[0].trim();
    }}
    if (cleanGrade) {{
      parts.push(cleanGrade);
    }}

    if (varietyNotes && varietyNotes.length < 25) {{
      parts.push(varietyNotes);
    }}

    // Determine accurate closing tag based on coin category/origin
    const combinedCtx = `${{coinName}} ${{country || ''}} ${{metal || ''}}`.toLowerCase();
    if (['banknote', 'paper money', 'currency', 'bill'].some(k => combinedCtx.includes(k))) {{
      parts.push('Banknote');
    }} else if (['roman', 'greece', 'greek', 'byzantine', 'biblical', 'athenian', 'ancient', 'shekel', 'prutah', 'widow', 'denarius', 'aureus', 'sestertius'].some(k => combinedCtx.includes(k))) {{
      parts.push('Ancient Coin');
    }} else if (['mexico', 'mexican', 'britain', 'british', 'united kingdom', 'uk', 'sovereign', 'canada', 'canadian', 'south africa', 'krugerrand', 'china', 'panda', 'austria', 'philharmonic', 'australia', 'kangaroo', 'kookaburra', 'libertad', 'centenario'].some(k => combinedCtx.includes(k))) {{
      parts.push('World Coin');
    }} else {{
      parts.push('Old US Coin');
    }}

    // Truncate while prioritizing retaining the closing tag if possible
    while (parts.join(' ').length > 80 && parts.length > 3) {{
      parts.splice(parts.length - 2, 1);
    }}

    let title = parts.join(' ').trim();
    if (title.length > 80) {{
      const words = title.split(' ');
      while (words.join(' ').length > 80 && words.length > 2) {{
        if (words.length > 3) {{
          words.splice(words.length - 2, 1);
        }} else {{
          words.pop();
        }}
      }}
      title = words.join(' ');
      if (title.length > 80) title = title.slice(0, 80);
    }}
    return title;
  }}

  // 10. Generate responsive HTML description
  function generateEbayHtmlDescription(title, coinData, grade, conditionNotes, obverseImgUrl, reverseImgUrl) {{
    coinData = coinData || {{}};
    const composition = coinData.composition || 'N/A';
    const weight = coinData.weight_grams || 'N/A';
    const diameter = coinData.diameter_mm || 'N/A';
    const edge = coinData.edge || 'Reeded';
    const meltVal = coinData.melt_value_usd || 0.0;
    const hasPrecious = coinData.has_precious_metal || false;

    let imagesHtml = '';
    if (obverseImgUrl || reverseImgUrl) {{
      imagesHtml = `
      <div style="display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin:20px 0;">
        ${{obverseImgUrl ? `<div style="text-align:center;"><img src="${{obverseImgUrl}}" style="max-width:280px; max-height:280px; border-radius:12px; border:1px solid #ddd; box-shadow:0 4px 10px rgba(0,0,0,0.08); object-fit:contain;"><p style="font-weight:600; color:#555; margin-top:6px;">Obverse (Front)</p></div>` : ''}}
        ${{reverseImgUrl ? `<div style="text-align:center;"><img src="${{reverseImgUrl}}" style="max-width:280px; max-height:280px; border-radius:12px; border:1px solid #ddd; box-shadow:0 4px 10px rgba(0,0,0,0.08); object-fit:contain;"><p style="font-weight:600; color:#555; margin-top:6px;">Reverse (Back)</p></div>` : ''}}
      </div>`;
    }}

    let meltBadge = '';
    if (hasPrecious && meltVal > 0) {{
      meltBadge = `
      <div style="background:#fef3c7; border:1px solid #f59e0b; color:#92400e; padding:10px 16px; border-radius:8px; font-weight:600; margin:16px 0; text-align:center;">
        ⚡ Precious Metal Bullion Value: Approx. $${{Number(meltVal).toFixed(2)}} USD minimum intrinsic melt value
      </div>`;
    }}

    return `
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height:1.6; color:#222; margin:0; padding:12px; background:#f9fafb;">
  <div style="max-width:800px; margin:0 auto; background:#ffffff; border-radius:16px; overflow:hidden; border:1px solid #e5e7eb; box-shadow:0 4px 16px rgba(0,0,0,0.06);">
    <div style="background:linear-gradient(135deg, #1e3a8a, #3b82f6); color:#ffffff; padding:24px 20px; text-align:center;">
      <h1 style="margin:0; font-size:22px; font-weight:700; letter-spacing:-0.5px;">${{title}}</h1>
      <p style="margin:6px 0 0; opacity:0.9; font-size:14px;">Authentic Numismatic Specimen &bull; Grade: ${{grade || 'Collector Grade'}}</p>
    </div>

    <div style="padding:24px 20px;">
      ${{imagesHtml}}
      ${{meltBadge}}

      <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:20px; font-size:17px;">
        🪙 Coin Specifications
      </h3>
      <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:14px;">
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; width:40%; border-bottom:1px solid #e2e8f0;">Series / Name</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{coinData.name || 'Coin'}}</td></tr>
        <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Denomination</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{coinData.denomination || 'N/A'}}</td></tr>
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Composition</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{composition}}</td></tr>
        <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Weight</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{weight}} grams</td></tr>
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Diameter</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{diameter}} mm</td></tr>
        <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Edge</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{edge}}</td></tr>
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Country of Origin</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${{coinData.country || 'United States'}}</td></tr>
      </table>

      <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:24px; font-size:17px;">
        🔍 Item Condition & Collector Notes
      </h3>
      <div style="background:#f3f4f6; padding:14px; border-radius:8px; font-size:14px; margin-bottom:20px;">
        <p style="margin:0 0 8px;"><strong>Estimated Grade:</strong> ${{grade || 'Collector Grade'}}</p>
        <p style="margin:0 0 8px;">${{conditionNotes || 'Please review all high-resolution photos carefully to determine grade and condition for yourself. The coin shown in the pictures is the exact coin you will receive.'}}</p>
        <p style="margin:0; font-size:13px; color:#4b5563;"><em>*Numismatic grading is subjective. Photos are taken under neutral lighting without filters. Never cleaned or polished.</em></p>
      </div>

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
</html>`.trim();
  }}

  // 11. Deep link to eBay web sell flow
  function generateEbayPrelistUrl(title, categoryId) {{
    const params = new URLSearchParams({{ query: title }});
    if (categoryId) params.set('categoryId', categoryId);
    return `https://www.ebay.com/sl/prelist/suggest?${{params.toString()}}`;
  }}

  // 12. Mercari listing generator
  function generateMercariListing(title, coinData, grade, price, conditionNotes) {{
    coinData = coinData || {{}};
    const name = coinData.name || 'Coin';
    const comp = coinData.composition || 'Solid Coin';
    const country = coinData.country || '';
    const meltVal = coinData.melt_value_usd || 0.0;
    const hasPrecious = coinData.has_precious_metal || false;

    let tags = '#coins #silver #numismatics #collectibles #bullion';
    const combined = `${{name}} ${{country}} ${{comp}}`.toLowerCase();
    if (comp.toLowerCase().includes('gold')) {{
      tags = '#gold #coins #preciousmetals #numismatics #rarecoin';
    }} else if (['banknote', 'paper money', 'currency'].some(k => combined.includes(k))) {{
      tags = '#papermoney #banknotes #currency #collectibles #numismatics';
    }} else if (['roman', 'greek', 'greece', 'byzantine', 'ancient', 'athenian', 'biblical', 'shekel', 'prutah', 'widow', 'denarius', 'aureus', 'sestertius'].some(k => combined.includes(k))) {{
      tags = '#ancientcoins #roman #greek #numismatics #history';
    }} else if (['mexico', 'mexican', 'britain', 'british', 'united kingdom', 'uk', 'canada', 'canadian', 'south africa', 'china', 'austria', 'australia', 'world', 'sovereign', 'krugerrand', 'libertad', 'philharmonic', 'centenario', 'maple'].some(k => combined.includes(k))) {{
      tags = '#worldcoins #silver #bullion #numismatics #collectibles';
    }}

    const meltMention = hasPrecious && meltVal > 0 ? `\\n• Bullion Melt Value: Approx. $${{Number(meltVal).toFixed(2)}} USD` : '';

    const desc = `FOR SALE: ${{title}}

Coin Details:
• Series: ${{name}}
• Estimated Grade: ${{grade}}
• Composition: ${{comp}}
• Weight: ${{coinData.weight_grams || 'N/A'}}g
• Diameter: ${{coinData.diameter_mm || 'N/A'}}mm${{meltMention}}

Condition & Provenance:
${{conditionNotes || 'Authentic coin with nice original surfaces. Uncleaned and well preserved. Please review all photos for exact condition.'}}

Shipping:
Ships safely packaged in a protective PVC-free flip/capsule inside a bubble mailer with USPS tracking within 24 hours of purchase!

${{tags}}`.trim();

    return {{
      title: title.slice(0, 80),
      price: price,
      category: 'Vintage & Collectibles > Antique Collectibles > Coins & Money',
      condition: 'Good / Like New',
      description: desc,
      tags: tags
    }};
  }}

  // 13. Whatnot livestream card generator
  function generateWhatnotListing(title, coinData, grade, startingBid, buyItNow) {{
    coinData = coinData || {{}};
    const name = coinData.name || 'Coin';
    const country = coinData.country || '';
    const comp = coinData.composition || '';
    const combined = `${{name}} ${{country}} ${{comp}}`.toLowerCase();

    let cat = 'Coins & Money > US Coins';
    if (['banknote', 'paper money', 'currency'].some(k => combined.includes(k))) {{
      cat = 'Coins & Money > Paper Money';
    }} else if (['roman', 'greek', 'greece', 'byzantine', 'ancient', 'athenian', 'biblical', 'shekel', 'prutah', 'widow', 'denarius', 'aureus', 'sestertius'].some(k => combined.includes(k))) {{
      cat = 'Coins & Money > Ancient Coins';
    }} else if (['mexico', 'mexican', 'britain', 'british', 'united kingdom', 'uk', 'canada', 'canadian', 'south africa', 'china', 'austria', 'australia', 'world', 'sovereign', 'krugerrand', 'libertad', 'philharmonic', 'centenario', 'maple'].some(k => combined.includes(k))) {{
      cat = 'Coins & Money > World Coins';
    }}

    return {{
      title: title.slice(0, 80),
      category: cat,
      starting_bid: startingBid,
      buy_it_now_price: buyItNow,
      condition: grade,
      auction_notes: `${{name}} • ${{grade}} • ${{comp}} • Sudden Death Auction`
    }};
  }}

  // 14. Reddit [WTS] post generator
  function generateRedditListing(title, coinData, grade, price) {{
    coinData = coinData || {{}};
    const meltVal = coinData.melt_value_usd || 0.0;
    const hasPrecious = coinData.has_precious_metal || false;
    const meltStr = hasPrecious && meltVal > 0 ? ` (Melt value: ~$${{Number(meltVal).toFixed(2)}})` : '';

    return `[WTS] ${{title}}

**Item Details:**
- **Coin:** ${{coinData.name || 'Coin'}}
- **Grade / Condition:** ${{grade}}
- **Composition:** ${{coinData.composition || 'Standard'}}
- **Weight / Specs:** ${{coinData.weight_grams || 'N/A'}}g, ${{coinData.diameter_mm || 'N/A'}}mm${{meltStr}}
- **Asking Price:** **$${{Number(price).toFixed(2)}}** (OBO)

**Shipping:**
- $5 Ground Advantage with tracking / $9 Priority Mail
- Ships securely packed in flip with cardboard sandwich

**Payment:** Zelle, Venmo, PayPal F&F, CashApp (no notes please)`.trim();
  }}

  // 15. Complete coin report builder (runs 100% client side)
  function generateCoinReport(opts) {{
    opts = opts || {{}};
    const analysisData = opts.analysisData || null;
    const coinHint = opts.coinHint || '';
    const yearHint = opts.yearHint || '';
    const mintHint = opts.mintHint || '';
    const obverseUrl = opts.obverseUrl || '';
    const reverseUrl = opts.reverseUrl || '';
    const spotPrices = opts.spotPrices || null;

    let targetId = '';
    if (analysisData && analysisData.coin_id && COIN_CATALOG[analysisData.coin_id]) {{
      targetId = analysisData.coin_id;
    }} else if (coinHint) {{
      const matched = findMatchingCoin(coinHint);
      if (matched) targetId = matched.id;
    }}

    if (!targetId || !COIN_CATALOG[targetId]) {{
      targetId = 'morgan_dollar';
    }}

    const coinMeta = COIN_CATALOG[targetId];
    const defaultYear = getDefaultYearForCoin(coinMeta);
    const year = yearHint || (analysisData && analysisData.year ? String(analysisData.year) : defaultYear);
    const rawMint = mintHint || (analysisData && analysisData.mint_mark ? analysisData.mint_mark : 'None');
    const cleanMint = normalizeMintMark(String(rawMint));
    const mintMark = cleanMint || 'None';
    const estimatedGrade = (analysisData && analysisData.estimated_grade) ? analysisData.estimated_grade : 'AU-58 (About Uncirculated)';
    const strikeType = (analysisData && analysisData.strike_type) ? analysisData.strike_type : 'Regular Business Strike';

    const meltInfo = calculateMeltValue(targetId, spotPrices);

    let pricing;
    if (analysisData && analysisData.ebay_market_price_estimate) {{
      pricing = analysisData.ebay_market_price_estimate;
    }} else {{
      const hasSilver = coinMeta.metal_type === 'silver';
      const hasGold = coinMeta.metal_type === 'gold';
      const isPaper = coinMeta.metal_type === 'paper';
      const isAncientBronze = coinMeta.metal_type === 'bronze';
      const melt = meltInfo.melt_value_usd || 0.0;
      let baseLow, baseAvg, baseHigh;

      if (hasGold && melt > 0) {{
        baseLow = Math.round(melt * 1.03 * 100) / 100;
        baseAvg = Math.round(melt * 1.08 * 100) / 100;
        baseHigh = Math.round(melt * 1.25 * 100) / 100;
      }} else if (hasSilver && melt > 0) {{
        if (['owl', 'shekel', 'denarius', 'ancient'].some(k => (coinMeta.id || '').includes(k))) {{
          baseLow = Math.max(melt * 1.5, ((coinMeta.id || '').includes('owl') || (coinMeta.id || '').includes('shekel')) ? 450.0 : 85.0);
          baseAvg = Math.max(melt * 2.5, ((coinMeta.id || '').includes('owl') || (coinMeta.id || '').includes('shekel')) ? 950.0 : 180.0);
          baseHigh = Math.max(melt * 4.0, ((coinMeta.id || '').includes('owl') || (coinMeta.id || '').includes('shekel')) ? 2200.0 : 450.0);
        }} else {{
          baseLow = Math.max(melt * 1.15, 28.0);
          baseAvg = Math.max(melt * 1.5, 45.0);
          baseHigh = Math.max(melt * 2.2, 85.0);
        }}
      }} else if (isPaper) {{
        baseLow = 35.0;
        baseAvg = 95.0;
        baseHigh = 350.0;
      }} else if (isAncientBronze) {{
        baseLow = (coinMeta.id || '').includes('widow') ? 45.0 : 150.0;
        baseAvg = (coinMeta.id || '').includes('widow') ? 120.0 : 450.0;
        baseHigh = (coinMeta.id || '').includes('widow') ? 350.0 : 1200.0;
      }} else {{
        baseLow = 15.0;
        baseAvg = 25.0;
        baseHigh = 65.0;
      }}

      pricing = {{
        low: Math.round(baseLow * 100) / 100,
        average: Math.round(baseAvg * 100) / 100,
        high: Math.round(baseHigh * 100) / 100,
        recommended_buy_it_now: Math.round(baseAvg * 1.1 * 100) / 100,
        starting_bid: Math.round(baseLow * 0.9 * 100) / 100
      }};
    }}

    const catalogVarieties = coinMeta.key_dates_and_varieties || [];
    const detectedVarieties = (analysisData && analysisData.detected_errors_or_varieties) ? analysisData.detected_errors_or_varieties : [];

    const ebayTitle = buildEbayTitle(
      coinMeta.name,
      String(year),
      cleanMint,
      estimatedGrade,
      'Authentic',
      coinMeta.composition,
      coinMeta.country
    );

    const mergedCoinInfo = Object.assign({{}}, coinMeta, meltInfo);

    const conditionNotes = analysisData && analysisData.numismatic_notes ? analysisData.numismatic_notes : '';
    const htmlDescription = generateEbayHtmlDescription(
      ebayTitle,
      mergedCoinInfo,
      estimatedGrade,
      conditionNotes,
      obverseUrl,
      reverseUrl
    );

    const prelistUrl = generateEbayPrelistUrl(ebayTitle, coinMeta.ebay_category_id || '');
    const skuMint = cleanMint ? cleanMint : 'P';
    let rawYearStr = year ? String(year).trim() : '';
    if (rawYearStr.startsWith('-') && /^\\d+$/.test(rawYearStr.slice(1))) {{
      rawYearStr = rawYearStr.slice(1) + 'BC';
    }}
    const cleanSkuYear = rawYearStr.replace(/[^A-Za-z0-9]/g, '') || 'GEN';
    const sku = `COIN-${{targetId.slice(0, 6).toUpperCase()}}-${{cleanSkuYear}}-${{skuMint}}-${{Math.floor(pricing.recommended_buy_it_now)}}`;

    const mercariListing = generateMercariListing(ebayTitle, mergedCoinInfo, estimatedGrade, pricing.recommended_buy_it_now, conditionNotes);
    const whatnotListing = generateWhatnotListing(ebayTitle, mergedCoinInfo, estimatedGrade, pricing.starting_bid, pricing.recommended_buy_it_now);
    const redditListing = generateRedditListing(ebayTitle, mergedCoinInfo, estimatedGrade, pricing.recommended_buy_it_now);

    return {{
      success: true,
      coin_id: targetId,
      coin_name: coinMeta.name,
      denomination: coinMeta.denomination,
      year: year,
      mint_mark: mintMark,
      clean_mint: cleanMint,
      country: coinMeta.country,
      composition: coinMeta.composition,
      weight_grams: coinMeta.weight_grams,
      diameter_mm: coinMeta.diameter_mm,
      edge: coinMeta.edge,
      designer: coinMeta.designer,
      estimated_grade: estimatedGrade,
      strike_type: strikeType,
      rarity_overview: coinMeta.rarity_overview,
      melt_value: meltInfo,
      grade_values_guide: coinMeta.grade_values || {{}},
      pricing_estimate: pricing,
      high_dollar_varieties: catalogVarieties,
      detected_varieties: detectedVarieties,
      selling_tips: coinMeta.selling_tips || '',
      ai_identified: Boolean(analysisData),
      vision_model: analysisData ? (analysisData.model_used || 'gemini-2.5-flash') : null,
      standalone_client_mode: true,
      ebay_listing: {{
        title: ebayTitle,
        category_id: coinMeta.ebay_category_id || '',
        category_name: coinMeta.ebay_category_name || '',
        sku: sku,
        buy_it_now_price: pricing.recommended_buy_it_now,
        starting_bid_price: pricing.starting_bid,
        html_description: htmlDescription,
        prelist_url: prelistUrl
      }},
      mercari_listing: mercariListing,
      whatnot_listing: whatnotListing,
      reddit_listing: redditListing
    }};
  }}

  // 16. Direct Client-Side Gemini Vision API caller (No local server or PC required)
  async function analyzeCoinDirectGemini(imagesBase64, apiKey) {{
    if (!apiKey) {{
      throw new Error('No Gemini API key provided');
    }}
    if (!imagesBase64 || imagesBase64.length === 0) {{
      throw new Error('No images provided for analysis');
    }}

    const parts = [
      {{ text: 'Analyze this coin photo (obverse/reverse). Provide exact numismatic identification, series name, coin_id, year, mint mark, grade, composition, rarity status, errors or varieties, and valuation. Return strictly a JSON object conforming to the schema.' }}
    ];

    imagesBase64.forEach(dataUri => {{
      if (!dataUri) return;
      let mimeType = 'image/jpeg';
      let rawBase64 = dataUri;
      if (dataUri.includes(';base64,')) {{
        const header = dataUri.split(';base64,')[0];
        rawBase64 = dataUri.split(';base64,')[1];
        if (header.includes('image/png')) mimeType = 'image/png';
        else if (header.includes('image/webp')) mimeType = 'image/webp';
      }}
      parts.push({{
        inlineData: {{
          mimeType: mimeType,
          data: rawBase64
        }}
      }});
    }});

    // Try Gemini 2.5 Flash, fallback to 2.0 Flash
    const models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash'];
    let lastError = null;

    for (const model of models) {{
      const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${{model}}:generateContent?key=${{encodeURIComponent(apiKey)}}`;
      try {{
        const res = await fetch(endpoint, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            systemInstruction: {{
              parts: [{{ text: NUMISMATIC_SYSTEM_PROMPT }}]
            }},
            contents: [{{ parts: parts }}],
            generationConfig: {{
              temperature: 0.2,
              responseMimeType: 'application/json'
            }}
          }})
        }});

        if (!res.ok) {{
          const errText = await res.text();
          console.warn(`Gemini model ${{model}} error:`, errText);
          lastError = new Error(`Gemini API error (${{res.status}}): ${{errText.slice(0, 150)}}`);
          continue;
        }}

        const data = await res.json();
        const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
        if (!candidateText) {{
          throw new Error('Empty response from Gemini Vision API');
        }}

        // Clean json if wrapped in markdown
        let cleaned = candidateText.trim();
        if (cleaned.startsWith('```json')) {{
          cleaned = cleaned.replace(/^```json\\s*/, '').replace(/\\s*```$/, '');
        }} else if (cleaned.startsWith('```')) {{
          cleaned = cleaned.replace(/^```\\s*/, '').replace(/\\s*```$/, '');
        }}

        const parsed = JSON.parse(cleaned);
        parsed.model_used = model;
        return parsed;
      }} catch (err) {{
        console.warn(`Attempt with ${{model}} failed:`, err);
        lastError = err;
      }}
    }}

    throw lastError || new Error('Failed to analyze with Gemini API');
  }}

  // Export to Global namespace
  const CoinVaultEngine = {{
    DEFAULT_SPOT_PRICES,
    COIN_CATALOG,
    SAMPLE_COINS,
    NUMISMATIC_SYSTEM_PROMPT,
    normalizeMintMark,
    getDefaultYearForCoin,
    calculateMeltValue,
    findMatchingCoin,
    buildEbayTitle,
    generateEbayHtmlDescription,
    generateEbayPrelistUrl,
    generateMercariListing,
    generateWhatnotListing,
    generateRedditListing,
    generateCoinReport,
    analyzeCoinDirectGemini
  }};

  if (typeof module !== 'undefined' && module.exports) {{
    module.exports = CoinVaultEngine;
  }} else {{
    root.CoinVaultEngine = CoinVaultEngine;
  }}

}})(typeof window !== 'undefined' ? window : this);
"""

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "js", "coin-engine.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(js_code)

print(f"Successfully generated {out_path} ({len(js_code)} bytes)")
