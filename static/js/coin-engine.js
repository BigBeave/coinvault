/**
 * CoinVault Standalone Client-Side Numismatic Engine
 * Runs 100% inside iOS Safari / PWA without any PC or local server needed.
 * Includes complete numismatic catalog, melt calculation formulas, high-dollar varieties,
 * direct Gemini Vision API integration, and selling listing generator.
 */

(function(root) {
  'use strict';

  // 1. Precious Metal Baseline Spot Prices (USD)
  const DEFAULT_SPOT_PRICES = {
  "silver": 31.5,
  "gold": 2680.0,
  "platinum": 980.0,
  "copper_per_lb": 4.3
};

  // 2. Full Coin Knowledge Base (32 Comprehensive Series)
  const COIN_CATALOG = {
  "morgan_dollar": {
    "id": "morgan_dollar",
    "name": "Morgan Silver Dollar",
    "denomination": "$1.00 USD",
    "years": "1878 - 1921",
    "country": "United States",
    "composition": "90% Silver, 10% Copper",
    "weight_grams": 26.73,
    "diameter_mm": 38.1,
    "net_pure_metal_oz": 0.77344,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "George T. Morgan",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver - 1921 only)",
      "S (San Francisco)",
      "O (New Orleans)",
      "CC (Carson City)"
    ],
    "ebay_category_id": "39464",
    "ebay_category_name": "Coins: US > Dollars > Morgan (1878-1921)",
    "rarity_overview": "Carson City (CC) mintages are scarce and highly sought after. 1893-S is the king of regular Morgan keys.",
    "grade_values": {
      "G-4 (Good)": "$32 - $38",
      "VG-8 / F-12 (Fine)": "$36 - $45",
      "VF-20 / EF-40 (Ext. Fine)": "$42 - $55",
      "AU-50 / AU-58 (About Uncirculated)": "$50 - $70",
      "MS-60 to MS-63 (Mint State)": "$65 - $110",
      "MS-65+ (Gem Uncirculated)": "$180 - $450+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1893-S",
        "rarity_tier": "Major Key Date",
        "est_value": "$3,000 - $150,000+",
        "description": "Lowest mintage regular strike Morgan dollar (100,000 minted). Massive collector demand in all grades."
      },
      {
        "date_variety": "1889-CC",
        "rarity_tier": "Carson City Key Date",
        "est_value": "$600 - $35,000+",
        "description": "Carson City rarity with only 350,000 minted. Most were melted under the Pittman Act."
      },
      {
        "date_variety": "1895 (Proof Only)",
        "rarity_tier": "The King of Morgans",
        "est_value": "$40,000 - $250,000+",
        "description": "Only 880 proof coins were struck and no business strikes are known to exist."
      },
      {
        "date_variety": "1878-CC",
        "rarity_tier": "First Year Carson City",
        "est_value": "$150 - $1,500+",
        "description": "Popular first year of issue from the historic Carson City mint."
      },
      {
        "date_variety": "1879-CC Capped Die",
        "rarity_tier": "Major Variety",
        "est_value": "$250 - $8,000+",
        "description": "CC mint mark shows clear evidence of rusted/capped die doubling."
      },
      {
        "date_variety": "1903-O",
        "rarity_tier": "Former Super Rarity",
        "est_value": "$350 - $1,200+",
        "description": "Once considered almost unattainable until Treasury vault bag releases in the 1960s."
      },
      {
        "date_variety": "1921-D",
        "rarity_tier": "Only Denver Morgan",
        "est_value": "$35 - $300+",
        "description": "The only year Morgan dollars were struck at the Denver Mint."
      }
    ],
    "selling_tips": "Do NOT clean or polish! Even light cleaning destroys numismatic premium. Highlight Carson City 'CC' mintmark or full breast feathers on the reverse eagle."
  },
  "peace_dollar": {
    "id": "peace_dollar",
    "name": "Peace Silver Dollar",
    "denomination": "$1.00 USD",
    "years": "1921 - 1935",
    "country": "United States",
    "composition": "90% Silver, 10% Copper",
    "weight_grams": 26.73,
    "diameter_mm": 38.1,
    "net_pure_metal_oz": 0.77344,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "Anthony de Francisci",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39465",
    "ebay_category_name": "Coins: US > Dollars > Peace (1921-1935)",
    "rarity_overview": "Commemorated peace after WWI. 1921 is high relief and a one-year type. 1928 Philadelphia is the key date.",
    "grade_values": {
      "G-4 (Good)": "$28 - $34",
      "VG-8 / F-12 (Fine)": "$32 - $38",
      "VF-20 / EF-40 (Ext. Fine)": "$36 - $45",
      "AU-50 / AU-58 (About Uncirculated)": "$42 - $60",
      "MS-60 to MS-63 (Mint State)": "$60 - $95",
      "MS-65+ (Gem Uncirculated)": "$140 - $350+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1921 High Relief",
        "rarity_tier": "One-Year Type Key",
        "est_value": "$130 - $1,800+",
        "description": "Struck in high relief causing die breakage. Distinctive concave field and sharp strike."
      },
      {
        "date_variety": "1928 (Philadelphia)",
        "rarity_tier": "Key Date",
        "est_value": "$250 - $1,500+",
        "description": "Lowest regular mintage of the series (360,649 struck)."
      },
      {
        "date_variety": "1934-D Doubled Die Obverse",
        "rarity_tier": "Major Variety",
        "est_value": "$150 - $2,500+",
        "description": "Strong doubling visible on 'IN GOD WE TRUST' and the sun rays."
      },
      {
        "date_variety": "1964-D Peace Dollar (Legendary)",
        "rarity_tier": "Ultra Rarity / Government Recall",
        "est_value": "$500,000+ (Illegal to Own)",
        "description": "316,076 struck in 1965 with 1964 date; all ordered melted by the Mint. Rumored survivors exist."
      }
    ],
    "selling_tips": "Check high wear areas on the eagle's wing and hair above the ear. Avoid cleaning."
  },
  "walking_liberty_half": {
    "id": "walking_liberty_half",
    "name": "Walking Liberty Half Dollar",
    "denomination": "$0.50 USD",
    "years": "1916 - 1947",
    "country": "United States",
    "composition": "90% Silver, 10% Copper",
    "weight_grams": 12.5,
    "diameter_mm": 30.63,
    "net_pure_metal_oz": 0.36169,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "Adolph A. Weinman",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "41098",
    "ebay_category_name": "Coins: US > Half Dollars > Walking Liberty (1916-47)",
    "rarity_overview": "Considered by many the most beautiful US silver coin. 1916 and 1921 dates are key rarities.",
    "grade_values": {
      "G-4 (Good)": "$14 - $18",
      "VG-8 / F-12 (Fine)": "$16 - $22",
      "VF-20 / EF-40 (Ext. Fine)": "$20 - $35",
      "AU-50 / AU-58 (About Uncirculated)": "$35 - $65",
      "MS-60 to MS-63 (Mint State)": "$75 - $150",
      "MS-65+ (Gem Uncirculated)": "$200 - $600+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1921-S",
        "rarity_tier": "Major Key Date",
        "est_value": "$150 - $12,000+",
        "description": "Scarce in all conditions with only 542,000 minted. Extremely elusive in Mint State."
      },
      {
        "date_variety": "1921 (Philadelphia)",
        "rarity_tier": "Major Key Date",
        "est_value": "$140 - $7,000+",
        "description": "Very low mintage of 208,000 coins. Heavily circulated."
      },
      {
        "date_variety": "1921-D",
        "rarity_tier": "Major Key Date",
        "est_value": "$180 - $9,000+",
        "description": "Only 208,000 minted in Denver. Tough in mid to high grades."
      },
      {
        "date_variety": "1916-S Obverse Mint Mark",
        "rarity_tier": "Key Variety",
        "est_value": "$120 - $3,500+",
        "description": "Mint mark located on obverse below 'IN GOD WE TRUST' (moved to reverse in mid-1917)."
      },
      {
        "date_variety": "1938-D",
        "rarity_tier": "Late Key Date",
        "est_value": "$60 - $800+",
        "description": "Depression-era low mintage of only 491,600 pieces."
      }
    ],
    "selling_tips": "Examine thumb of Liberty's outstretched hand and eagle feathers on reverse to grade strike sharpness."
  },
  "franklin_half": {
    "id": "franklin_half",
    "name": "Franklin Half Dollar",
    "denomination": "$0.50 USD",
    "years": "1948 - 1963",
    "country": "United States",
    "composition": "90% Silver, 10% Copper",
    "weight_grams": 12.5,
    "diameter_mm": 30.63,
    "net_pure_metal_oz": 0.36169,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "John R. Sinnock",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "41099",
    "ebay_category_name": "Coins: US > Half Dollars > Franklin (1948-63)",
    "rarity_overview": "Popular 90% silver series. Coins exhibiting 'Full Bell Lines' (FBL) on the Liberty Bell command huge premiums.",
    "grade_values": {
      "G-4 (Good)": "$12 - $15",
      "VF-20 / EF-40 (Ext. Fine)": "$14 - $18",
      "AU-50 / AU-58 (About Uncirculated)": "$16 - $24",
      "MS-60 to MS-63 (Mint State)": "$25 - $45",
      "MS-65+ FBL (Full Bell Lines)": "$90 - $1,200+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1949-D (Full Bell Lines)",
        "rarity_tier": "Condition Rarity",
        "est_value": "$40 - $1,500+",
        "description": "Extremely difficult to find with complete unbroken horizontal bell lines."
      },
      {
        "date_variety": "1953-S (Full Bell Lines)",
        "rarity_tier": "Condition Key",
        "est_value": "$60 - $4,000+",
        "description": "Notoriously weak strike; pristine FBL specimens command top dollar at auction."
      },
      {
        "date_variety": "1955 Bugs Bunny Variety",
        "rarity_tier": "Popular Die Clash Variety",
        "est_value": "$35 - $250+",
        "description": "Die clash caused an impression resembling buck teeth on Benjamin Franklin's lip."
      },
      {
        "date_variety": "1961 Proof Doubled Die Reverse",
        "rarity_tier": "Major Proof Variety",
        "est_value": "$80 - $800+",
        "description": "Clear doubling on 'UNITED STATES OF AMERICA' and 'HALF DOLLAR'."
      }
    ],
    "selling_tips": "Photograph the bottom horizontal lines of the Liberty Bell under direct angled light to prove 'Full Bell Lines' (FBL)."
  },
  "kennedy_half": {
    "id": "kennedy_half",
    "name": "Kennedy Half Dollar",
    "denomination": "$0.50 USD",
    "years": "1964 - Present",
    "country": "United States",
    "composition": "1964: 90% Silver; 1965-1970: 40% Silver; 1971+: Copper-Nickel Clad",
    "weight_grams": 12.5,
    "diameter_mm": 30.61,
    "net_pure_metal_oz": 0.36169,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "Gilroy Roberts / Frank Gasparro",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "41100",
    "ebay_category_name": "Coins: US > Half Dollars > Kennedy (1964-Now)",
    "rarity_overview": "1964 is 90% pure silver. 1965-1970 are 40% silver. Several rare accented hair and transitional varieties bring large sums.",
    "grade_values": {
      "Circulated 1964 (90% Silver)": "$12 - $15",
      "Circulated 1965-70 (40% Silver)": "$4.50 - $6.50",
      "1971+ Circulated Clad": "$0.50 - $1.50",
      "MS-65+ High Grade Silver": "$30 - $150+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1964 Proof Accented Hair",
        "rarity_tier": "Famous Proof Variety",
        "est_value": "$45 - $350+",
        "description": "Extra strands of hair above Kennedy's ear; favorite design of Jacqueline Kennedy before revision."
      },
      {
        "date_variety": "1974-D Doubled Die Obverse",
        "rarity_tier": "Major Variety",
        "est_value": "$30 - $350+",
        "description": "Distinct doubling on 'TRUST' and profile."
      },
      {
        "date_variety": "1970-D (40% Silver)",
        "rarity_tier": "Key Date (Mint Set Only)",
        "est_value": "$15 - $90+",
        "description": "Not issued for circulation; only available in 1970 US Mint sets."
      },
      {
        "date_variety": "1998-S Matte Finish",
        "rarity_tier": "Modern Rarity",
        "est_value": "$120 - $350+",
        "description": "Special matte strike issued only with the RFK commemorative coin set."
      }
    ],
    "selling_tips": "Clearly state whether the coin is 1964 (90% Silver) or 1965-1970 (40% Silver) in the title."
  },
  "washington_quarter": {
    "id": "washington_quarter",
    "name": "Washington Quarter (Silver)",
    "denomination": "$0.25 USD",
    "years": "1932 - 1964 (Silver era)",
    "country": "United States",
    "composition": "90% Silver, 10% Copper (Pre-1965)",
    "weight_grams": 6.25,
    "diameter_mm": 24.26,
    "net_pure_metal_oz": 0.18084,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "John Flanagan",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39462",
    "ebay_category_name": "Coins: US > Quarters > Washington (1932-98)",
    "rarity_overview": "All quarters dated 1964 and earlier are 90% solid silver. 1932-D and 1932-S are premier series keys.",
    "grade_values": {
      "G-4 (Good) Common Silver": "$6 - $8",
      "VG-8 / F-12 (Fine)": "$7 - $9",
      "AU-50 / AU-58": "$10 - $18",
      "MS-63 to MS-65": "$25 - $75+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1932-D",
        "rarity_tier": "Key Date",
        "est_value": "$90 - $1,500+",
        "description": "First year issue with only 436,800 minted. High counterfeit rate; inspect mintmark."
      },
      {
        "date_variety": "1932-S",
        "rarity_tier": "Key Date",
        "est_value": "$80 - $1,200+",
        "description": "Only 408,000 minted in San Francisco. Prime collector staple."
      },
      {
        "date_variety": "1937 Doubled Die Obverse",
        "rarity_tier": "Major Variety",
        "est_value": "$100 - $1,800+",
        "description": "Prominent doubling visible in 'IN GOD WE TRUST'."
      },
      {
        "date_variety": "1950-D/S Overmintmark",
        "rarity_tier": "Famous Variety",
        "est_value": "$60 - $700+",
        "description": "D mintmark punched directly over an S mintmark."
      }
    ],
    "selling_tips": "Look at the rim edge: if solid white silver with no copper stripe, it's pre-1965 90% silver!"
  },
  "mercury_dime": {
    "id": "mercury_dime",
    "name": "Mercury Dime (Winged Liberty Head)",
    "denomination": "$0.10 USD",
    "years": "1916 - 1945",
    "country": "United States",
    "composition": "90% Silver, 10% Copper",
    "weight_grams": 2.5,
    "diameter_mm": 17.9,
    "net_pure_metal_oz": 0.07234,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "Adolph A. Weinman",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39459",
    "ebay_category_name": "Coins: US > Dimes > Mercury (1916-45)",
    "rarity_overview": "Beloved 90% silver dime. 1916-D is the holy grail. 'Full Split Bands' (FB) on the fasces bring 5x-20x price jumps.",
    "grade_values": {
      "G-4 (Good) Common Date": "$2.50 - $3.50",
      "VG-8 / F-12 (Fine)": "$3.00 - $4.50",
      "VF-20 / EF-40": "$4.00 - $7.00",
      "AU-50 / AU-58": "$8.00 - $15.00",
      "MS-63 to MS-65": "$25 - $75",
      "MS-65+ Full Split Bands (FB)": "$80 - $500+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1916-D",
        "rarity_tier": "Ultimate Key Date",
        "est_value": "$800 - $25,000+",
        "description": "Only 264,000 minted. Heavily sought after; beware of added 'D' mintmarks."
      },
      {
        "date_variety": "1921 (Philadelphia)",
        "rarity_tier": "Key Date",
        "est_value": "$50 - $1,200+",
        "description": "Post-WWI recession low mintage of 1.23 million."
      },
      {
        "date_variety": "1921-D",
        "rarity_tier": "Key Date",
        "est_value": "$65 - $1,600+",
        "description": "Denver key with only 1.08 million minted."
      },
      {
        "date_variety": "1942/1 Overdate (Philadelphia)",
        "rarity_tier": "Major Variety",
        "est_value": "$400 - $8,000+",
        "description": "Clear 2 over 1 digit visible in the date. Major US coin variety."
      },
      {
        "date_variety": "1942/1-D Overdate (Denver)",
        "rarity_tier": "Major Variety",
        "est_value": "$350 - $7,000+",
        "description": "Denver counterpart to the famous 1942/1 overdate error."
      }
    ],
    "selling_tips": "Photograph the central horizontal bands wrapping around the fasces on reverse. If fully split without merging, advertise as 'Full Bands / FB'!"
  },
  "roosevelt_dime": {
    "id": "roosevelt_dime",
    "name": "Roosevelt Dime",
    "denomination": "$0.10 USD",
    "years": "1946 - Present",
    "country": "United States",
    "composition": "1946-1964: 90% Silver, 10% Copper; 1965+: Copper-Nickel Clad",
    "weight_grams": 2.5,
    "diameter_mm": 17.9,
    "net_pure_metal_oz": 0.07234,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "John R. Sinnock",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)",
      "P (1980+)"
    ],
    "ebay_category_id": "39460",
    "ebay_category_name": "Coins: US > Dimes > Roosevelt (1946-Now)",
    "rarity_overview": "Silver dimes up to 1964 have intrinsic melt value. Several high-dollar modern mint errors exist.",
    "grade_values": {
      "Circulated 1946-1964 Silver": "$2.30 - $3.00",
      "Circulated 1965+ Clad": "$0.10 (Face Value)",
      "MS-65+ Full Torch (FT/FB)": "$20 - $85+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1982 No Mint Mark (No P)",
        "rarity_tier": "Famous Modern Rarity",
        "est_value": "$75 - $350+",
        "description": "Mint worker failed to punch the 'P' mintmark into the working die. Highly sought after."
      },
      {
        "date_variety": "1968 No S Proof",
        "rarity_tier": "Extreme Proof Rarity",
        "est_value": "$15,000 - $30,000+",
        "description": "First of the famous 'No S' proof errors; struck at San Francisco without the S mintmark."
      },
      {
        "date_variety": "1975 No S Proof",
        "rarity_tier": "Ultra Rare Proof Key",
        "est_value": "$350,000 - $500,000+",
        "description": "Only two specimens confirmed to exist. One of the top modern numismatic rarities."
      },
      {
        "date_variety": "1996-W",
        "rarity_tier": "Special Mint Strike",
        "est_value": "$12 - $35+",
        "description": "Struck at West Point to celebrate the 50th anniversary; only included in uncirculated sets."
      }
    ],
    "selling_tips": "Check any 1982 dime without a mintmark above the date. The 'Strong Strike' variety brings over $150 on eBay."
  },
  "buffalo_nickel": {
    "id": "buffalo_nickel",
    "name": "Buffalo Nickel (Indian Head)",
    "denomination": "$0.05 USD",
    "years": "1913 - 1938",
    "country": "United States",
    "composition": "75% Copper, 25% Nickel",
    "weight_grams": 5.0,
    "diameter_mm": 21.2,
    "net_pure_metal_oz": 0.0,
    "metal_type": "base_metal",
    "edge": "Plain",
    "designer": "James Earle Fraser",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39455",
    "ebay_category_name": "Coins: US > Nickels > Buffalo (1913-38)",
    "rarity_overview": "Iconic American coin. Prone to date wear because the date was raised. Famous for 3-legged and overdate varieties.",
    "grade_values": {
      "Dateless / Cull": "$0.75 - $1.25",
      "G-4 (Good with readable date)": "$2.00 - $4.00",
      "VG-8 / F-12 (Fine)": "$4.00 - $8.00",
      "VF-20 / EF-40": "$10.00 - $25.00",
      "MS-60 to MS-63": "$45 - $95",
      "MS-65+": "$150 - $450+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1937-D 3-Legged Buffalo",
        "rarity_tier": "Famous Error Variety",
        "est_value": "$500 - $15,000+",
        "description": "Die over-polishing accidentally erased the buffalo's right front leg while hoof remains visible."
      },
      {
        "date_variety": "1916/16 Doubled Die Obverse",
        "rarity_tier": "Major Variety Key",
        "est_value": "$2,500 - $85,000+",
        "description": "Spectacular doubling on the entire date and feather."
      },
      {
        "date_variety": "1918/7-D Overdate",
        "rarity_tier": "Key Overdate Variety",
        "est_value": "$700 - $25,000+",
        "description": "Working die stamped with 1917 hub, then re-stamped with 1918 hub."
      },
      {
        "date_variety": "1913-S Variety 2",
        "rarity_tier": "Low Mintage Key",
        "est_value": "$250 - $3,500+",
        "description": "Type 2 with buffalo standing on a flat line instead of raised mound. Only 1.2M struck."
      },
      {
        "date_variety": "1936-D 3\u00bd Legs",
        "rarity_tier": "Scarce Error",
        "est_value": "$400 - $4,500+",
        "description": "Die wear and heavy polishing removed half of the foreleg."
      }
    ],
    "selling_tips": "Do NOT acid date (Nic-A-Date) if you want top collector value. Check the front right leg of any 1937-D buffalo immediately!"
  },
  "jefferson_nickel": {
    "id": "jefferson_nickel",
    "name": "Jefferson Nickel",
    "denomination": "$0.05 USD",
    "years": "1938 - Present",
    "country": "United States",
    "composition": "1938-1941, 1946+: 75% Cu, 25% Ni; 1942-1945 Wartime: 56% Copper, 35% Silver, 9% Manganese",
    "weight_grams": 5.0,
    "diameter_mm": 21.2,
    "net_pure_metal_oz": 0.05626,
    "metal_type": "silver_or_base",
    "edge": "Plain",
    "designer": "Felix Schlag",
    "mint_marks": [
      "None / P",
      "D",
      "S"
    ],
    "ebay_category_id": "39456",
    "ebay_category_name": "Coins: US > Nickels > Jefferson (1938-Now)",
    "rarity_overview": "Wartime nickels (1942-1945) contain 35% pure silver with prominent mintmark above dome of Monticello. Full Steps (FS) coins bring large premiums.",
    "grade_values": {
      "Circulated Wartime 35% Silver (1942-45)": "$1.70 - $2.50",
      "Circulated Common Clad": "$0.05 (Face Value)",
      "1950-D MS-65": "$60 - $120+",
      "Full Steps (5FS / 6FS) Gem Uncirculated": "$50 - $800+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1950-D",
        "rarity_tier": "Series Key Date",
        "est_value": "$10 - $120+",
        "description": "Lowest regular mintage in the series (2.63 million). Hoarded in uncirculated rolls."
      },
      {
        "date_variety": "1939 Doubled Die Reverse (Monticello)",
        "rarity_tier": "Major Variety",
        "est_value": "$40 - $1,200+",
        "description": "Clear doubling of 'MONTICELLO' and 'FIVE CENTS' on reverse."
      },
      {
        "date_variety": "1943/2-P Wartime Overdate",
        "rarity_tier": "Major Silver Variety",
        "est_value": "$35 - $600+",
        "description": "The numeral 3 is stamped clearly over a 2 on a 35% silver planchet."
      },
      {
        "date_variety": "1942-D/Horizontal D",
        "rarity_tier": "Famous RPM Variety",
        "est_value": "$50 - $800+",
        "description": "Repunched mintmark where original D was punched sideways."
      }
    ],
    "selling_tips": "Look for a huge P, D, or S above the dome of Monticello. That proves it's a 35% silver war nickel!"
  },
  "lincoln_wheat_cent": {
    "id": "lincoln_wheat_cent",
    "name": "Lincoln Wheat Cent (Penny)",
    "denomination": "$0.01 USD",
    "years": "1909 - 1958",
    "country": "United States",
    "composition": "95% Copper, 5% Tin/Zinc (1943: Zinc-Coated Steel)",
    "weight_grams": 3.11,
    "diameter_mm": 19.05,
    "net_pure_metal_oz": 0.0,
    "metal_type": "copper",
    "edge": "Plain",
    "designer": "Victor David Brenner",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39454",
    "ebay_category_name": "Coins: US > Small Cents > Lincoln, Wheat (1909-1958)",
    "rarity_overview": "One of the most widely collected coins in history. The 1909-S VDB is an American legend. Look out for 1955 Doubled Die Obverse and 1943 Copper transitional errors.",
    "grade_values": {
      "Common Circulated Wheat Cent": "$0.05 - $0.25",
      "G-4 (Good) Semi-Key": "$2.00 - $15.00",
      "EF-40 to AU-50": "$5.00 - $35.00",
      "MS-65 Red (Full Copper Luster)": "$25 - $250+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1909-S VDB",
        "rarity_tier": "Iconic American Key Date",
        "est_value": "$650 - $4,500+",
        "description": "Designer's initials V.D.B. at bottom of reverse with S mintmark. Only 484,000 minted."
      },
      {
        "date_variety": "1955 Doubled Die Obverse (DDO)",
        "rarity_tier": "Famous Mega-Error",
        "est_value": "$1,000 - $35,000+",
        "description": "Massive naked-eye doubling of '1955', 'LIBERTY', and 'IN GOD WE TRUST'."
      },
      {
        "date_variety": "1943 Bronze / Copper Cent (Transitional Error)",
        "rarity_tier": "Six-Figure Trophy Coin",
        "est_value": "$100,000 - $1,700,000+",
        "description": "Accidentally struck on leftover 1942 bronze planchet instead of zinc-coated steel. If it does NOT stick to a magnet, get it certified immediately!"
      },
      {
        "date_variety": "1944 Steel Cent (Transitional Error)",
        "rarity_tier": "Major Error Rarity",
        "est_value": "$30,000 - $100,000+",
        "description": "Struck on leftover 1943 zinc-plated steel planchet. STICKS to a magnet."
      },
      {
        "date_variety": "1914-D",
        "rarity_tier": "Key Date",
        "est_value": "$150 - $4,000+",
        "description": "Low mintage key (1.19 million). Heavily worn in circulation."
      },
      {
        "date_variety": "1922 'No D' (Plain)",
        "rarity_tier": "Famous Die Variety",
        "est_value": "$450 - $15,000+",
        "description": "Die pair #2 where the Denver mint mark was completely polished away."
      },
      {
        "date_variety": "1931-S",
        "rarity_tier": "Key Date",
        "est_value": "$60 - $300+",
        "description": "Second lowest mintage regular wheat cent (866,000 struck)."
      }
    ],
    "selling_tips": "Always test 1943 pennies with a magnet! Regular 1943 cents stick to magnets (steel). If it does NOT stick and weighs ~3.11 grams, you could have a fortune."
  },
  "lincoln_memorial_cent": {
    "id": "lincoln_memorial_cent",
    "name": "Lincoln Memorial Cent",
    "denomination": "$0.01 USD",
    "years": "1959 - 2008",
    "country": "United States",
    "composition": "1959-1982: 95% Copper; 1982+: 97.5% Zinc, 2.5% Copper plating",
    "weight_grams": 3.11,
    "diameter_mm": 19.05,
    "net_pure_metal_oz": 0.0,
    "metal_type": "copper_or_zinc",
    "edge": "Plain",
    "designer": "Frank Gasparro",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39454",
    "ebay_category_name": "Coins: US > Small Cents > Lincoln, Memorial (1959-2008)",
    "rarity_overview": "Common pocket change, but loaded with modern doubled dies and transitional zinc/copper varieties.",
    "grade_values": {
      "Circulated Common": "$0.01 - $0.05",
      "Uncirculated Roll": "$2 - $10",
      "Certified MS-67+ Red": "$25 - $150+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1969-S Doubled Die Obverse",
        "rarity_tier": "Major Modern Rarity",
        "est_value": "$25,000 - $125,000+",
        "description": "Extremely pronounced doubling of the date and obverse lettering. Secret Service originally seized them as counterfeits before validating authenticity."
      },
      {
        "date_variety": "1972 Doubled Die Obverse (FS-101)",
        "rarity_tier": "Famous Variety",
        "est_value": "$250 - $1,200+",
        "description": "Strong doubling across 'LIBERTY', 'IN GOD WE TRUST', and date."
      },
      {
        "date_variety": "1983 Double Die Reverse (DDR)",
        "rarity_tier": "Modern Variety",
        "est_value": "$150 - $600+",
        "description": "Massive doubling on 'ONE CENT' and 'UNITED STATES OF AMERICA'."
      },
      {
        "date_variety": "1992 Close AM (Philadelphia & Denver)",
        "rarity_tier": "Transitional Variety Rarity",
        "est_value": "$3,000 - $20,000+",
        "description": "Letters 'A' and 'M' in 'AMERICA' touch at the bottom (proof reverse die used on business strike)."
      },
      {
        "date_variety": "1982-D Small Date Bronze (Copper)",
        "rarity_tier": "Discovery Rarity",
        "est_value": "$10,000 - $25,000+",
        "description": "Struck in 3.11g solid copper instead of zinc. Only a handful ever discovered."
      }
    ],
    "selling_tips": "Weigh any 1982 penny with a digital scale: 3.1g is copper (worth melt), 2.5g is zinc."
  },
  "american_silver_eagle": {
    "id": "american_silver_eagle",
    "name": "American Silver Eagle (1 oz Bullion)",
    "denomination": "$1.00 USD",
    "years": "1986 - Present",
    "country": "United States",
    "composition": "99.9% Pure Fine Silver",
    "weight_grams": 31.103,
    "diameter_mm": 40.6,
    "net_pure_metal_oz": 1.0,
    "metal_type": "silver",
    "edge": "Reeded",
    "designer": "Adolph A. Weinman / John Mercanti",
    "mint_marks": [
      "None (Bullion)",
      "W (West Point)",
      "S (San Francisco)",
      "P (Philadelphia)"
    ],
    "ebay_category_id": "39489",
    "ebay_category_name": "Bullion > Silver > Coins > US > American Eagle",
    "rarity_overview": "The world's most widely traded silver bullion coin. 1 Troy ounce of .999 fine silver. Proof and burnished keys bring large collector premiums.",
    "grade_values": {
      "Raw Bullion (Common Date)": "$35 - $45",
      "Proof in Original Govt Packaging (OGP)": "$55 - $95",
      "NGC/PCGS MS-70 Perfect": "$65 - $160+",
      "NGC/PCGS PR-70 Deep Cameo": "$85 - $250+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1995-W Proof",
        "rarity_tier": "Series Key Grail",
        "est_value": "$2,800 - $6,500+",
        "description": "Only 30,125 minted; issued exclusively in the 10th Anniversary 5-coin gold proof set."
      },
      {
        "date_variety": "2019-S Enhanced Reverse Proof",
        "rarity_tier": "Modern Proof Key",
        "est_value": "$800 - $2,500+",
        "description": "Lowest mintage regular issue with only 29,910 coins minted with Certificate of Authenticity."
      },
      {
        "date_variety": "2008-W with Reverse of 2007",
        "rarity_tier": "Die Variety",
        "est_value": "$400 - $1,200+",
        "description": "Struck with leftover 2007 reverse die; distinct font difference on the 'U' in 'UNITED'."
      },
      {
        "date_variety": "1986 First Year of Issue",
        "rarity_tier": "Popular First Year",
        "est_value": "$45 - $150+",
        "description": "Inaugural year of the American Silver Eagle program."
      }
    ],
    "selling_tips": "Highlight MS-70 or PR-70 grade if certified, or mention 'Includes original US Mint box and COA'."
  },
  "saint_gaudens_double_eagle": {
    "id": "saint_gaudens_double_eagle",
    "name": "Saint-Gaudens $20 Double Eagle (Gold)",
    "denomination": "$20.00 USD",
    "years": "1907 - 1933",
    "country": "United States",
    "composition": "90% Gold, 10% Copper",
    "weight_grams": 33.436,
    "diameter_mm": 34.0,
    "net_pure_metal_oz": 0.9675,
    "metal_type": "gold",
    "edge": "Lettered ('E PLURIBUS UNUM' with stars)",
    "designer": "Augustus Saint-Gaudens",
    "mint_marks": [
      "None (Philadelphia)",
      "D (Denver)",
      "S (San Francisco)"
    ],
    "ebay_category_id": "39474",
    "ebay_category_name": "Coins: US > Gold > $20, Double Eagle > Saint-Gaudens (1907-33)",
    "rarity_overview": "Widely heralded as America's most stunning coin. Contains 0.9675 troy oz of pure gold. 1933 is the most valuable US coin in history.",
    "grade_values": {
      "VF-20 / EF-40": "$2,650 - $2,750",
      "AU-50 / AU-58": "$2,700 - $2,850",
      "MS-62 to MS-64": "$2,800 - $3,200",
      "MS-65+ Gem": "$3,500 - $6,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1933 Saint-Gaudens",
        "rarity_tier": "World Record Coin",
        "est_value": "$18,900,000 (Last Auction Price)",
        "description": "Never officially released due to the Gold Recall Act of 1933. Only 1 legally owned by private collectors."
      },
      {
        "date_variety": "1907 Ultra High Relief / High Relief Wire Rim",
        "rarity_tier": "Masterpiece Key",
        "est_value": "$12,000 - $150,000+",
        "description": "Roman numerals MCMVII; striking required multiple hydraulic blows."
      },
      {
        "date_variety": "1927-D",
        "rarity_tier": "Supreme Regular Rarity",
        "est_value": "$1,000,000 - $3,000,000+",
        "description": "Virtually the entire mintage of 180,000 was melted; only ~12-15 specimens survive."
      }
    ],
    "selling_tips": "Gold coins should always be shipped with signature confirmation and registered mail insurance."
  },
  "roman_denarius": {
    "id": "roman_denarius",
    "name": "Roman Empire Silver Denarius",
    "denomination": "1 Denarius",
    "years": "c. 211 BC - 240 AD",
    "country": "Roman Empire",
    "composition": "90-95% Silver (High Empire), later debased to 50%",
    "weight_grams": 3.9,
    "diameter_mm": 19.0,
    "net_pure_metal_oz": 0.11,
    "metal_type": "silver",
    "edge": "Plain / Hammered Irregular",
    "designer": "Imperial Roman Mint Masters",
    "mint_marks": [
      "Rome",
      "Lugdunum (Lyon)",
      "Antioch",
      "Alexandria",
      "Siscia"
    ],
    "ebay_category_id": "4733",
    "ebay_category_name": "Coins: Ancient > Roman: Imperial (27 BC-476 AD)",
    "rarity_overview": "The standard silver backbone of the Roman Republic and Empire. Highly collected across the Twelve Caesars, Trajan, Hadrian, and Marcus Aurelius.",
    "grade_values": {
      "VG-8 / F-12 (Fine)": "$65 - $110",
      "VF-20 / VF-30 (Very Fine)": "$125 - $220",
      "EF-40 / XF-45 (Ext. Fine)": "$220 - $450",
      "AU-50 / AU-58 (About Uncirculated)": "$450 - $950",
      "Ch AU / Mint State (NGC Ancients)": "$950 - $3,500+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Julius Caesar Elephant Denarius (49-48 BC)",
        "rarity_tier": "Iconic Historical Key",
        "est_value": "$1,500 - $12,000+",
        "description": "Struck by Caesar during the Civil War showing elephant trampling dragon, reverse pontifical implements."
      },
      {
        "date_variety": "Brutus EID MAR Denarius (42 BC)",
        "rarity_tier": "Supreme Ancient Rarity",
        "est_value": "$500,000 - $3,500,000+",
        "description": "Celebrates the Ides of March assassination of Julius Caesar with daggers and pileus cap of liberty."
      },
      {
        "date_variety": "Tiberius Tribute Penny (14-37 AD)",
        "rarity_tier": "Famous Biblical & Imperial Key",
        "est_value": "$500 - $3,500+",
        "description": "Render unto Caesar coin referenced in Matthew 22:19-21; features seated Livia as Pax."
      },
      {
        "date_variety": "Augustus Capricorn / Pax (27 BC - 14 AD)",
        "rarity_tier": "First Roman Emperor Key",
        "est_value": "$600 - $5,000+",
        "description": "High relief issues struck for the founding emperor of Rome."
      },
      {
        "date_variety": "Marcus Aurelius Philosopher Emperor (161-180 AD)",
        "rarity_tier": "Stoic Emperor Series",
        "est_value": "$120 - $850+",
        "description": "Portrays author of Meditations with distinctive curled beard."
      }
    ],
    "selling_tips": "Never clean ancient silver! Natural dark cabinet toning and horn silver horn patina provide high numismatic premiums. Note strike centering and surface condition (e.g. 5/5 strike, 4/5 surface)."
  },
  "roman_aureus": {
    "id": "roman_aureus",
    "name": "Roman Empire Gold Aureus",
    "denomination": "1 Aureus (25 Denarii)",
    "years": "c. 50 BC - 324 AD",
    "country": "Roman Empire",
    "composition": "98-99% Pure Gold",
    "weight_grams": 7.3,
    "diameter_mm": 19.5,
    "net_pure_metal_oz": 0.233,
    "metal_type": "gold",
    "edge": "Plain / Hammered Flanning",
    "designer": "Imperial Mint Masters",
    "mint_marks": [
      "Rome",
      "Lugdunum",
      "Antioch",
      "Nicomedia"
    ],
    "ebay_category_id": "4733",
    "ebay_category_name": "Coins: Ancient > Roman: Imperial (27 BC-476 AD)",
    "rarity_overview": "The supreme gold denomination of Rome. Aurei were used for military triumphs, high imperial gifts, and state tributes.",
    "grade_values": {
      "Fine / F-12": "$3,000 - $5,500",
      "VF-20 / VF-30": "$5,500 - $10,000",
      "EF-40 / XF-45": "$10,000 - $22,000",
      "AU / Ch AU": "$22,000 - $48,000",
      "Mint State / Gem (NGC Ancients)": "$50,000 - $150,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Nero Gold Aureus - Salus / Jupiter (54-68 AD)",
        "rarity_tier": "Twelve Caesars Key",
        "est_value": "$4,500 - $25,000+",
        "description": "Iconic portrait of Nero struck after the Great Fire of Rome."
      },
      {
        "date_variety": "Augustus Divine Caesar Aureus (27 BC - 14 AD)",
        "rarity_tier": "Imperial Foundation Rarity",
        "est_value": "$10,000 - $65,000+",
        "description": "Depicts deified Julius Caesar and the radiant Comet of 44 BC."
      },
      {
        "date_variety": "Trajan Dacian Triumph Aureus (98-117 AD)",
        "rarity_tier": "Major Historical Key",
        "est_value": "$6,000 - $35,000+",
        "description": "Celebrates conquests funded by the gold and silver spoils of Dacia (Romania)."
      },
      {
        "date_variety": "Hadrian Travel Series / Adventus Aureus (117-138 AD)",
        "rarity_tier": "Architectural & Province Key",
        "est_value": "$8,000 - $45,000+",
        "description": "Features Hadrian visiting Greece, Egypt, and Britannia."
      }
    ],
    "selling_tips": "Gold ancient aurei do not oxidize or tone like silver. Check weight with 0.01g precision to authenticate against modern fakes. Registered and insured shipping mandatory."
  },
  "roman_sestertius": {
    "id": "roman_sestertius",
    "name": "Roman Empire Orichalcum Sestertius",
    "denomination": "1 Sestertius (4 Asses)",
    "years": "c. 211 BC - 280 AD",
    "country": "Roman Empire",
    "composition": "Orichalcum (Golden Brass / Copper-Zinc Alloy)",
    "weight_grams": 25.0,
    "diameter_mm": 33.0,
    "net_pure_metal_oz": 0.0,
    "metal_type": "bronze",
    "edge": "Plain / Thick Irregular",
    "designer": "Senate & Imperial Mint Masters (SC - Senatus Consulto)",
    "mint_marks": [
      "Rome",
      "Lugdunum"
    ],
    "ebay_category_id": "4733",
    "ebay_category_name": "Coins: Ancient > Roman: Imperial (27 BC-476 AD)",
    "rarity_overview": "The largest and most impressive bronze coin of imperial Rome. Famous for lifelike high-relief portraits and architectural masterpieces.",
    "grade_values": {
      "VG-8 / F-12": "$85 - $180",
      "VF-20 / VF-30": "$250 - $650",
      "EF-40 / XF-45": "$750 - $2,200",
      "AU-50 / Ch AU": "$2,500 - $8,500",
      "Choice Tiber Green Patina / Mint State": "$10,000 - $45,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Titus Colosseum Sestertius (80 AD)",
        "rarity_tier": "Architectural Crown Jewel",
        "est_value": "$50,000 - $350,000+",
        "description": "Bird's-eye view of the Flavian Amphitheatre (Colosseum) struck for its grand opening."
      },
      {
        "date_variety": "Nero Port of Ostia Sestertius (64 AD)",
        "rarity_tier": "Major Architectural Rarity",
        "est_value": "$5,000 - $35,000+",
        "description": "Elaborate aerial depiction of Claudius's harbor at Ostia with merchant ships and Neptune."
      },
      {
        "date_variety": "Trajan Danube Bridge / Dacia (105-115 AD)",
        "rarity_tier": "Engineering Masterpiece Key",
        "est_value": "$800 - $6,500+",
        "description": "Celebrates Apollodorus of Damascus's legendary Danube bridge."
      },
      {
        "date_variety": "Hadrian Britannia Sestertius (119-138 AD)",
        "rarity_tier": "First Depiction of Britannia",
        "est_value": "$1,200 - $9,000+",
        "description": "First time the personification of Britannia appeared on a coin."
      }
    ],
    "selling_tips": "Patina is paramount on Roman bronzes. Emerald green 'Tiber patina' or smooth dark chocolate jade surfaces command 3x-10x premiums over stripped or cleaned coins."
  },
  "athenian_owl_tetradrachm": {
    "id": "athenian_owl_tetradrachm",
    "name": "Ancient Greece Athenian Owl Tetradrachm",
    "denomination": "4 Drachms (Tetradrachm)",
    "years": "c. 510 - 38 BC",
    "country": "Ancient Greece (Attica, Athens)",
    "composition": "98% Pure Silver (Laurion Mines)",
    "weight_grams": 17.2,
    "diameter_mm": 24.0,
    "net_pure_metal_oz": 0.54,
    "metal_type": "silver",
    "edge": "Plain / Chunky Hammered Planchet",
    "designer": "Athenian State Mint",
    "mint_marks": [
      "Athens (\u0391\u0398\u0395)"
    ],
    "ebay_category_id": "4738",
    "ebay_category_name": "Coins: Ancient > Greek (450 BC-100 AD)",
    "rarity_overview": "The single most famous ancient coin in the world. Depicts Athena with helmet and crest on obverse, and the iconic owl of wisdom with olive spray and crescent moon on reverse.",
    "grade_values": {
      "Fine / F-12": "$500 - $850",
      "VF-20 / VF-30": "$900 - $1,500",
      "Choice VF (NGC Ancients)": "$1,400 - $2,200",
      "XF / Choice XF (Sharp Crest & Owl)": "$2,000 - $3,500",
      "Ch AU / Mint State (Full Crest, Mint Luster)": "$4,000 - $12,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Classical Mass Owls (c. 440-404 BC)",
        "rarity_tier": "Golden Age of Pericles Key",
        "est_value": "$1,200 - $5,000+",
        "description": "Standard high-demand classical type with complete Athena eye and owl tail feathers."
      },
      {
        "date_variety": "Archaic Owl Tetradrachm (c. 510-480 BC)",
        "rarity_tier": "Pre-Persian War Archaic Key",
        "est_value": "$5,000 - $35,000+",
        "description": "Early archaic style with frontal eye, primitive smile, and crude incuse reverse."
      },
      {
        "date_variety": "Decadrachm of Athens (c. 467 BC)",
        "rarity_tier": "Supreme Numismatic Grail",
        "est_value": "$500,000 - $2,500,000+",
        "description": "Colossal 43-gram masterwork celebrating the Battle of Eurymedon; only ~40 known."
      },
      {
        "date_variety": "New Style Owl with Magistrate Monograms (c. 165-42 BC)",
        "rarity_tier": "Hellenistic Spread-Flan Key",
        "est_value": "$600 - $2,000+",
        "description": "Struck on wider, thinner flan with owl standing upon an amphora surrounded by olive wreath."
      }
    ],
    "selling_tips": "Look for specimens where the crest of Athena's helmet is fully visible on the flan (often off-center on standard strikes). Full crest + full olive spray equals top-dollar realized price."
  },
  "byzantine_solidus": {
    "id": "byzantine_solidus",
    "name": "Byzantine Empire Gold Solidus",
    "denomination": "1 Solidus",
    "years": "c. 312 - 1092 AD",
    "country": "Byzantine Empire",
    "composition": "95-98% Pure Gold (23 Karat)",
    "weight_grams": 4.5,
    "diameter_mm": 21.0,
    "net_pure_metal_oz": 0.142,
    "metal_type": "gold",
    "edge": "Plain / Hammered",
    "designer": "Constantinople Imperial Mint",
    "mint_marks": [
      "CONOB (Constantinople / Pure Gold)",
      "Thessalonica",
      "Ravenna",
      "Carthage"
    ],
    "ebay_category_id": "4740",
    "ebay_category_name": "Coins: Ancient > Byzantine (300-1400 AD)",
    "rarity_overview": "The standard international currency of the medieval Mediterranean world for over 700 years. Famous for front-facing imperial portraits and the first coins to portray Jesus Christ.",
    "grade_values": {
      "Fine / F-12": "$450 - $650",
      "VF-20 / VF-30": "$650 - $950",
      "EF-40 / XF-45": "$950 - $1,500",
      "AU-50 / Ch AU": "$1,400 - $2,500",
      "Mint State (NGC Ancients)": "$2,500 - $6,500+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Justinian I The Great (527-565 AD)",
        "rarity_tier": "Builder of Hagia Sophia Key",
        "est_value": "$700 - $2,200+",
        "description": "Features Justinian holding globus cruciger, reverse angel of Victory."
      },
      {
        "date_variety": "Justinian II Facing Bust of Christ (692-695 AD)",
        "rarity_tier": "First Numismatic Portrait of Christ",
        "est_value": "$2,500 - $12,000+",
        "description": "Historic first coinage featuring the lifelike facing bust of Christ with curly hair."
      },
      {
        "date_variety": "Heraclius & Sons with True Cross (610-641 AD)",
        "rarity_tier": "Major Crusader Precursor Key",
        "est_value": "$650 - $1,800+",
        "description": "Commemorates the recovery of the True Cross from Persian hands."
      },
      {
        "date_variety": "Basil II Slayer of Bulgarians (976-1025 AD)",
        "rarity_tier": "Golden Age of Byzantium Key",
        "est_value": "$1,200 - $4,500+",
        "description": "Shows Basil II and Constantine VIII with large Nimbus Christ Pantokrator."
      }
    ],
    "selling_tips": "Look for sharp face strikes on the Christ bust or emperor's eyes. Byzantine gold was rarely clipped and has consistent high gold purity (CONOB mintmark)."
  },
  "widows_mite": {
    "id": "widows_mite",
    "name": "Biblical Widow's Mite (Bronze Prutah / Lepton)",
    "denomination": "1 Prutah / Lepton",
    "years": "c. 103 BC - 70 AD",
    "country": "Ancient Judaea (Holy Land)",
    "composition": "Bronze",
    "weight_grams": 1.5,
    "diameter_mm": 14.0,
    "net_pure_metal_oz": 0.0,
    "metal_type": "bronze",
    "edge": "Plain / Crude Irregular",
    "designer": "Jerusalem Mint of Judaea",
    "mint_marks": [
      "Jerusalem"
    ],
    "ebay_category_id": "4733",
    "ebay_category_name": "Coins: Ancient > Roman: Provincial",
    "rarity_overview": "The small bronze coin praised by Jesus in the Gospels (Mark 12:41-44). Struck by Maccabean King Alexander Jannaeus and Roman procurators including Pontius Pilate.",
    "grade_values": {
      "Fair / G-4": "$25 - $45",
      "VG-8 / F-12": "$45 - $90",
      "VF-20 / VF-30": "$95 - $220",
      "EF-40 / Choice (Sharp Anchor & Star)": "$220 - $550",
      "NGC Ancients Certified High Grade": "$450 - $1,200+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Alexander Jannaeus Anchor & Star (103-76 BC)",
        "rarity_tier": "True Widow's Mite of the Gospel",
        "est_value": "$45 - $350+",
        "description": "Features eight-ray star inside diadem, reverse inverted anchor with Greek inscription."
      },
      {
        "date_variety": "Pontius Pilate Lituus Prutah (26-36 AD)",
        "rarity_tier": "Crucifixion Procurator Key",
        "est_value": "$150 - $1,200+",
        "description": "Struck under governor Pontius Pilate during Jesus's trial and crucifixion."
      },
      {
        "date_variety": "First Jewish Revolt Year 2 Amphora (67-68 AD)",
        "rarity_tier": "Judean Rebellion Key",
        "est_value": "$120 - $650+",
        "description": "Struck by Jewish defenders in Jerusalem inscribed 'Year Two - Freedom of Zion'."
      },
      {
        "date_variety": "Herod the Great Anchor & Double Cornucopia (37-4 BC)",
        "rarity_tier": "King of Judea Key",
        "est_value": "$85 - $450+",
        "description": "Struck under Herod the Great, ruler at the time of Jesus's nativity."
      }
    ],
    "selling_tips": "Widow's Mites are immensely popular for Christian gifts, Sunday school education, and biblical jewelry. Highlight Gospel citations (Mark 12:42) in eBay and Mercari titles."
  },
  "shekel_of_tyre": {
    "id": "shekel_of_tyre",
    "name": "Biblical Shekel of Tyre (30 Pieces of Silver)",
    "denomination": "1 Shekel (Tetradrachm)",
    "years": "c. 126 BC - 65 AD",
    "country": "Phoenicia, Tyre (Holy Land)",
    "composition": "94% Fine Silver",
    "weight_grams": 14.2,
    "diameter_mm": 27.0,
    "net_pure_metal_oz": 0.43,
    "metal_type": "silver",
    "edge": "Plain / Thick Planchet",
    "designer": "Tyrian Mint",
    "mint_marks": [
      "Tyre (Monogram & Club of Melqart)"
    ],
    "ebay_category_id": "4738",
    "ebay_category_name": "Coins: Ancient > Greek (450 BC-100 AD)",
    "rarity_overview": "The exact coin required by Jewish law for payment of the Temple Tax in Jerusalem. Universally recognized by numismatists and historians as the authentic '30 pieces of silver' paid to Judas Iscariot.",
    "grade_values": {
      "VG-8 / F-12": "$600 - $1,100",
      "VF-20 / VF-30": "$1,200 - $2,200",
      "EF-40 / XF-45": "$2,200 - $4,500",
      "AU-50 / Ch AU (NGC Ancients)": "$4,500 - $9,500",
      "Mint State Gem": "$10,000 - $25,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Ministry of Jesus Era (c. 28-33 AD)",
        "rarity_tier": "Exact 30 Pieces of Silver Date",
        "est_value": "$2,500 - $8,500+",
        "description": "Struck during the exact historical years of Jesus's ministry and passion in Jerusalem."
      },
      {
        "date_variety": "KAP Jerusalem Autonomous Strike (c. 18 BC - 65 AD)",
        "rarity_tier": "Secret Jerusalem Mint Key",
        "est_value": "$1,800 - $6,000+",
        "description": "Identified by numismatists as struck directly in Jerusalem by the Temple priesthood."
      },
      {
        "date_variety": "Half-Shekel of Tyre (Exact Temple Tax Dues)",
        "rarity_tier": "Temple Tax Exact Dues Rarity",
        "est_value": "$1,200 - $5,500+",
        "description": "Much scarcer than full shekels; paid annually by every adult Jewish male."
      },
      {
        "date_variety": "Year 1 of Autonomous Tyre (126/125 BC)",
        "rarity_tier": "First Year of Series Key",
        "est_value": "$1,500 - $4,500+",
        "description": "Inaugural year showing laureate head of Melqart-Hercules."
      }
    ],
    "selling_tips": "Highest demand biblical coin in the world. Emphasize provenance, authentic silver weight (14g+), and clear Tyrian eagle reverse. Always certificate via NGC Ancients for top market value."
  },
  "british_sovereign": {
    "id": "british_sovereign",
    "name": "British Full Gold Sovereign",
    "denomination": "1 Sovereign (\u00a31 GBP)",
    "years": "1817 - Present",
    "country": "United Kingdom",
    "composition": "22 Karat Gold (91.67% Gold, 8.33% Copper)",
    "weight_grams": 7.988,
    "diameter_mm": 22.05,
    "net_pure_metal_oz": 0.2354,
    "metal_type": "gold",
    "edge": "Milled / Reeded",
    "designer": "Benedetto Pistrucci (St. George & Dragon)",
    "mint_marks": [
      "None (London)",
      "M (Melbourne)",
      "S (Sydney)",
      "P (Perth)",
      "C (Ottawa)",
      "SA (Pretoria)",
      "I (Bombay)"
    ],
    "ebay_category_id": "3394",
    "ebay_category_name": "Coins: World > Europe > UK (Great Britain) > Sovereign",
    "rarity_overview": "The chief gold coin of the British Empire. Features the reigning British monarch on the obverse and Benedetto Pistrucci's world-famous St. George slaying the dragon on the reverse.",
    "grade_values": {
      "Bullion / VF": "$630 - $670",
      "EF-40 / AU-50": "$660 - $720",
      "MS-62 / MS-63": "$720 - $890",
      "MS-65+ Gem": "$1,100 - $2,500+",
      "Key Dates / Rarities": "$3,000 - $50,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1819 George III Sovereign",
        "rarity_tier": "British Royal Grail",
        "est_value": "$200,000 - $1,000,000+",
        "description": "Only ~10 specimens known; highest value modern British coin."
      },
      {
        "date_variety": "1917 London Mint Sovereign",
        "rarity_tier": "WWI Wartime Super Key",
        "est_value": "$10,000 - $25,000+",
        "description": "Virtually entire mintage melted down for American war debt payments."
      },
      {
        "date_variety": "1874 Young Head St. George",
        "rarity_tier": "Victorian Type Key",
        "est_value": "$850 - $3,500+",
        "description": "Scarce Queen Victoria first generation St. George reverse."
      },
      {
        "date_variety": "1908-C Ottawa Canada Mint",
        "rarity_tier": "Colonial Branch Mint Key",
        "est_value": "$1,500 - $6,000+",
        "description": "First year Ottawa struck British sovereigns with tiny 'C' mint mark."
      }
    ],
    "selling_tips": "Always check for branch mint letters (S, M, P, C, SA, I) embedded in ground line above date on reverse. Branch mint coins can carry tremendous collector premiums over bullion value."
  },
  "british_britannia": {
    "id": "british_britannia",
    "name": "British Silver & Gold Britannia",
    "denomination": "\u00a32 GBP (Silver) / \u00a3100 GBP (Gold)",
    "years": "1987 - Present",
    "country": "United Kingdom",
    "composition": ".999 Fine Silver / .9999 Pure Gold",
    "weight_grams": 31.21,
    "diameter_mm": 38.61,
    "net_pure_metal_oz": 1.0,
    "metal_type": "silver",
    "edge": "Reeded / Security Micro-Text",
    "designer": "Philip Nathan / The Royal Mint",
    "mint_marks": [
      "Royal Mint (Llantrisant, Wales)"
    ],
    "ebay_category_id": "178078",
    "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
    "rarity_overview": "Flagship official bullion of Great Britain. Recognized worldwide for iconic portrait of Britannia holding trident, shield, and olive branch with high-tech laser hologram security features.",
    "grade_values": {
      "Brilliant Uncirculated": "$35 - $45",
      "MS-69 (NGC / PCGS)": "$45 - $65",
      "MS-70 Perfect": "$75 - $140",
      "Reverse Proof / Proof FDC": "$90 - $220+",
      "Early 1997-2003 Low Mintage Proofs": "$150 - $650+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "2014 Horse Privy Mules Error",
        "rarity_tier": "Major Mint Mule Error",
        "est_value": "$150 - $650+",
        "description": "Obverse struck with Lunar Year of the Horse obverse die missing denticles."
      },
      {
        "date_variety": "1997 First Year Silver Proof Britannia",
        "rarity_tier": "10th Anniversary Silver Key",
        "est_value": "$120 - $450+",
        "description": "Inaugural year for silver proof Britannia denomination."
      },
      {
        "date_variety": "2023 Queen Elizabeth II Memorial Coronation Edition",
        "rarity_tier": "Historic Transition Issue",
        "est_value": "$45 - $150+",
        "description": "Last edition bearing Queen Elizabeth II obverse alongside initial King Charles III releases."
      },
      {
        "date_variety": "2021 Laser Security Padlock Hologram Variety",
        "rarity_tier": "First Laser Security Edition",
        "est_value": "$38 - $85+",
        "description": "Features micro-hologram that flips between a trident and padlock as the coin tilts."
      }
    ],
    "selling_tips": "Highlight the 4 advanced Royal Mint security features in listing descriptions: latent padlock image, animated wave background, micro-text ring, and tincture heraldic lines."
  },
  "mexican_silver_libertad": {
    "id": "mexican_silver_libertad",
    "name": "Mexican Silver Libertad 1 oz",
    "denomination": "1 Onza Plata Pura",
    "years": "1982 - Present",
    "country": "Mexico",
    "composition": "99.9% Pure Silver (.999 Fine)",
    "weight_grams": 31.103,
    "diameter_mm": 40.0,
    "net_pure_metal_oz": 1.0,
    "metal_type": "silver",
    "edge": "Reeded (Edge Lettered 1982-1989 'INDEPENDENCIA Y LIBERTAD')",
    "designer": "Casa de Moneda de M\u00e9xico",
    "mint_marks": [
      "M\u00b0 (Mexico City Mint - Americas' Oldest Mint)"
    ],
    "ebay_category_id": "178078",
    "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
    "rarity_overview": "Struck by the oldest operating mint in the Americas (founded 1535). Features the iconic Winged Victory (El \u00c1ngel de la Independencia) with volcanoes Popocat\u00e9petl and Iztacc\u00edhuatl in the background.",
    "grade_values": {
      "Brilliant Uncirculated": "$38 - $55",
      "MS-69 (NGC / PCGS)": "$60 - $95",
      "MS-70 Perfect": "$120 - $250",
      "Reverse Proof": "$180 - $450+",
      "Ultra Low Mintage Years (1998, 1999)": "$250 - $1,200+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1998 1 oz Libertad (Key Year, Only 67,000 Minted)",
        "rarity_tier": "Supreme Series Key Date",
        "est_value": "$450 - $1,500+",
        "description": "Lowest mintage regular strike Libertad in the entire 1 oz series."
      },
      {
        "date_variety": "1999 1 oz Libertad (Key Year, Only 95,000 Minted)",
        "rarity_tier": "Major Series Key Date",
        "est_value": "$350 - $1,100+",
        "description": "Scarce second key year of the modern Winged Victory redesign."
      },
      {
        "date_variety": "1982 First Year of Issue (Chunkier Planchet)",
        "rarity_tier": "Inaugural Issue Key",
        "est_value": "$45 - $120+",
        "description": "Type 1 thick planchet (36mm) with raised edge lettering."
      },
      {
        "date_variety": "Reverse Proof Libertad",
        "rarity_tier": "Collector Favorite",
        "est_value": "$200 - $600+",
        "description": "Frosted background fields with brilliant mirror relief devices."
      }
    ],
    "selling_tips": "Libertads have much lower mintage figures than American Eagles or Maples, commanding significantly higher premiums. Mention low mintage numbers in titles to maximize sales."
  },
  "mexican_50_pesos_centenario": {
    "id": "mexican_50_pesos_centenario",
    "name": "Mexican 50 Pesos Centenario Gold",
    "denomination": "50 Pesos",
    "years": "1921 - 1947 (Restrikes to 1972)",
    "country": "Mexico",
    "composition": "90% Gold, 10% Copper (21.6 Karat)",
    "weight_grams": 41.67,
    "diameter_mm": 37.0,
    "net_pure_metal_oz": 1.2057,
    "metal_type": "gold",
    "edge": "Lettered: 'INDEPENDENCIA Y LIBERTAD'",
    "designer": "Emilio del Moral",
    "mint_marks": [
      "M\u00b0 (Mexico City Mint)"
    ],
    "ebay_category_id": "39482",
    "ebay_category_name": "Coins & Paper Money > Bullion > Gold > Coins",
    "rarity_overview": "One of the most famous and imposing gold coins in world history. Commemorates the 100th anniversary of Mexican Independence. Weighs 41.67g and contains over 1.2 troy oz pure gold.",
    "grade_values": {
      "Bullion / AU": "$3,250 - $3,450",
      "MS-62 / MS-63": "$3,450 - $3,800",
      "MS-65 Gem Uncirculated": "$3,900 - $4,800+",
      "1921 First Year Key Date": "$4,500 - $12,000+",
      "1931 Rare Date": "$4,200 - $8,500+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1921 First Year Centennial Type",
        "rarity_tier": "Inaugural Centennial Key",
        "est_value": "$4,500 - $12,000+",
        "description": "One-year type showing Winged Victory facing front without '50 PESOS' on obverse."
      },
      {
        "date_variety": "1931 Key Date Centenario",
        "rarity_tier": "Low Mintage Key",
        "est_value": "$4,000 - $8,500+",
        "description": "Only 137,000 minted during the Great Depression."
      },
      {
        "date_variety": "1943 37.5 Gr. Double Obverse Variety",
        "rarity_tier": "Special Wartime Variety",
        "est_value": "$3,600 - $5,500+",
        "description": "Shows '37.5 Gr. ORO PURO' on both sides of Winged Victory."
      },
      {
        "date_variety": "1947 Official Bullion Restrike",
        "rarity_tier": "Classic International Bullion Benchmark",
        "est_value": "$3,250 - $3,450+",
        "description": "Standard high-liquidity bullion issue struck between 1949 and 1972."
      }
    ],
    "selling_tips": "Highlight the 1.2057 oz pure gold content. A heavy favorite among bullion investors and sovereign coin collectors because it is larger and heavier than standard 1 oz coins."
  },
  "canadian_silver_maple_leaf": {
    "id": "canadian_silver_maple_leaf",
    "name": "Canadian Silver Maple Leaf 1 oz",
    "denomination": "$5.00 CAD",
    "years": "1988 - Present",
    "country": "Canada",
    "composition": "99.99% Pure Silver (.9999 Four Nines Fine)",
    "weight_grams": 31.103,
    "diameter_mm": 38.0,
    "net_pure_metal_oz": 1.0,
    "metal_type": "silver",
    "edge": "Serrated / Radial Lines",
    "designer": "Walter Ott / Royal Canadian Mint",
    "mint_marks": [
      "RCM (Ottawa Mint)"
    ],
    "ebay_category_id": "178078",
    "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
    "rarity_overview": "The world's purest official sovereign silver bullion coin at .9999 fine. Produced by the Royal Canadian Mint with proprietary MINTSHIELD milk-spot resistance and micro-engraved laser security.",
    "grade_values": {
      "Brilliant Uncirculated": "$34 - $42",
      "MS-69 (NGC / PCGS)": "$42 - $60",
      "MS-70 Perfect": "$65 - $125",
      "Special Privy Mark Editions": "$55 - $160+",
      "1988 First Year of Issue": "$45 - $95+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1988 First Year of Issue",
        "rarity_tier": "Inaugural Series Key",
        "est_value": "$45 - $110+",
        "description": "First year Canada struck silver bullion Maples."
      },
      {
        "date_variety": "1997 / 1998 Titanic Privy Mark Variety",
        "rarity_tier": "Famous Privy Rarity",
        "est_value": "$85 - $280+",
        "description": "Struck with special Titanic ship privy mark to commemorate the ship discovery."
      },
      {
        "date_variety": "2014 Radial Lines & Bullion DNA Security",
        "rarity_tier": "Security Innovation Key",
        "est_value": "$38 - $75+",
        "description": "First year featuring light-diffracting radial lines and laser-textured maple leaf."
      },
      {
        "date_variety": "Colorized & Hologram Official RCM Issues",
        "rarity_tier": "Collector Specialty",
        "est_value": "$65 - $200+",
        "description": "Government issue proof colorized and hologram variations."
      }
    ],
    "selling_tips": "Emphasize .9999 (Four Nines Fine) purity, which is purer than standard .999 coins. State if coin is 2018 or newer to note MINTSHIELD anti-spotting protection."
  },
  "canadian_gold_maple_leaf": {
    "id": "canadian_gold_maple_leaf",
    "name": "Canadian Gold Maple Leaf 1 oz",
    "denomination": "$50.00 CAD",
    "years": "1979 - Present",
    "country": "Canada",
    "composition": "99.99% Pure Gold (.9999 24 Karat)",
    "weight_grams": 31.103,
    "diameter_mm": 30.0,
    "net_pure_metal_oz": 1.0,
    "metal_type": "gold",
    "edge": "Reeded",
    "designer": "Walter Ott / Royal Canadian Mint",
    "mint_marks": [
      "Royal Canadian Mint"
    ],
    "ebay_category_id": "39482",
    "ebay_category_name": "Coins & Paper Money > Bullion > Gold > Coins",
    "rarity_overview": "The international standard for pure 24-karat gold bullion. Introduced in 1979 as the first real alternative to the Krugerrand, made without alloy metals.",
    "grade_values": {
      "Bullion Spot + Premium": "$2,720 - $2,820",
      "MS-69 (PCGS / NGC)": "$2,800 - $2,950",
      "MS-70 Perfect": "$2,950 - $3,300+",
      "1979 First Year of Issue (.999 Fine)": "$2,750 - $2,950+",
      "Special 5-Nines (.99999) Limited Issues": "$3,200 - $4,500+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1979 First Year of Issue",
        "rarity_tier": "Inaugural Gold Key",
        "est_value": "$2,750 - $3,000+",
        "description": "First year struck; .999 fine before shifting to .9999 standard in 1982."
      },
      {
        "date_variety": "2007 .99999 'Five Nines' Special Issue",
        "rarity_tier": "World Record Purity",
        "est_value": "$3,200 - $4,800+",
        "description": "Struck in 99.999% pure gold, the highest purity coin ever achieved."
      },
      {
        "date_variety": "2013 Bullion DNA Anti-Counterfeit Micro-Leaf",
        "rarity_tier": "Anti-Counterfeit First",
        "est_value": "$2,750 - $2,950+",
        "description": "Contains laser micro-engraving visible only under digital magnification."
      }
    ],
    "selling_tips": "Gold Maple Leafs are soft 24-karat pure gold. Always handle with cotton gloves and store in protective coin capsules to prevent rim dings."
  },
  "south_african_krugerrand": {
    "id": "south_african_krugerrand",
    "name": "South African Gold & Silver Krugerrand",
    "denomination": "1 oz Fine Gold / Silver (No Face Value)",
    "years": "1967 - Present",
    "country": "South Africa",
    "composition": "91.67% Gold, 8.33% Copper (22 Karat durable crown gold)",
    "weight_grams": 33.93,
    "diameter_mm": 32.77,
    "net_pure_metal_oz": 1.0,
    "metal_type": "gold",
    "edge": "Reeded (160 serrations bullion, 220 proof)",
    "designer": "Otto Schultz (Paul Kruger) / Coert Steynberg (Springbok)",
    "mint_marks": [
      "South African Mint / Rand Refinery"
    ],
    "ebay_category_id": "39482",
    "ebay_category_name": "Coins & Paper Money > Bullion > Gold > Coins",
    "rarity_overview": "The pioneer of all modern 1 oz bullion coins. First minted in 1967 and by 1980 accounted for 90% of the world's gold coin market. Contains a full troy ounce of gold in a tough copper-rich alloy.",
    "grade_values": {
      "Bullion Uncirculated": "$2,710 - $2,800",
      "MS-64 / MS-65": "$2,780 - $2,950",
      "Proof Edition (Frosted Devices)": "$2,900 - $3,500+",
      "1967 First Year of Issue (40,000 minted)": "$4,000 - $8,500+",
      "1968-1969 Low Mintage Years": "$2,850 - $3,600+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1967 Inaugural Year Key Date",
        "rarity_tier": "Supreme Modern Bullion Key",
        "est_value": "$4,000 - $8,500+",
        "description": "First year the modern 1 oz gold bullion concept was invented."
      },
      {
        "date_variety": "Proof Krugerrand Variety (220 Serrations)",
        "rarity_tier": "Proof Serration Key",
        "est_value": "$2,900 - $3,800+",
        "description": "Proof strikes feature 220 fine edge serrations compared to 160 on standard bullion."
      },
      {
        "date_variety": "50th Anniversary 2017 Krugerrand (Special Privy)",
        "rarity_tier": "Commemorative Jubilee Key",
        "est_value": "$2,780 - $3,100+",
        "description": "Special 50th jubilee privy mark above the Springbok."
      },
      {
        "date_variety": "2017 First Year Silver Krugerrand (.999 1 oz)",
        "rarity_tier": "First Silver Krugerrand",
        "est_value": "$35 - $65+",
        "description": "First year the Krugerrand was struck in 1 oz pure silver."
      }
    ],
    "selling_tips": "Count edge serrations: 220 edge teeth indicates an expensive proof strike rather than standard 160 teeth bullion. The distinctive reddish gold color is authentic 22k crown gold."
  },
  "chinese_silver_panda": {
    "id": "chinese_silver_panda",
    "name": "Chinese Silver Panda",
    "denomination": "10 Yuan (\u00a510 RMB)",
    "years": "1983 - Present",
    "country": "China",
    "composition": "99.9% Pure Silver (.999 Fine)",
    "weight_grams": 30.0,
    "diameter_mm": 40.0,
    "net_pure_metal_oz": 0.9645,
    "metal_type": "silver",
    "edge": "Slanted / Oblique Reeded",
    "designer": "China Gold Coin Corp / People's Bank of China",
    "mint_marks": [
      "Beijing",
      "Shanghai",
      "Shenyang",
      "Shenzhen"
    ],
    "ebay_category_id": "178078",
    "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
    "rarity_overview": "Famous for annually changing reverse artwork of the beloved Giant Panda. Obverse depicts the iconic Hall of Prayer for Good Harvests in Beijing's Temple of Heaven.",
    "grade_values": {
      "Brilliant Uncirculated": "$38 - $55",
      "MS-69 (PCGS / NGC)": "$55 - $85",
      "MS-70 Perfect": "$95 - $220",
      "Vintage 1980s Proofs / Low Mintages": "$350 - $2,500+",
      "1983 Inaugural Silver Panda Proof": "$1,500 - $4,500+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1983 Inaugural 27g Proof (Key Date, 10,000 minted)",
        "rarity_tier": "Supreme Series Rarity",
        "est_value": "$1,800 - $4,500+",
        "description": "First year of issue struck in 27 grams of .900 silver with only 10,000 minted."
      },
      {
        "date_variety": "1984 & 1985 Early Proof Pandas",
        "rarity_tier": "Early Proof Keys",
        "est_value": "$800 - $2,200+",
        "description": "Early low-mintage proofs coveted by Chinese numismatic specialists."
      },
      {
        "date_variety": "2000 Mirror vs Frosted Ring Variety",
        "rarity_tier": "Major Variety Error",
        "est_value": "$150 - $650+",
        "description": "Frosted outer ring variety commands sharp collector premium."
      },
      {
        "date_variety": "2016 Transition Year (Metric 30 Grams)",
        "rarity_tier": "Metric Standard Key",
        "est_value": "$42 - $85+",
        "description": "Shifted from standard 31.1g 1 troy oz to the metric 30g weight."
      }
    ],
    "selling_tips": "China changed from 31.1 grams (1 troy oz) to 30 grams in 2016. High counterfeiting exists for early Pandas: authentic coins feature distinctive slanted diagonal reeding."
  },
  "austrian_philharmonic": {
    "id": "austrian_philharmonic",
    "name": "Austrian Silver & Gold Philharmonic",
    "denomination": "\u20ac1.50 EUR (Silver) / \u20ac100 EUR (Gold)",
    "years": "1989 - Present (Silver introduced 2008)",
    "country": "Austria",
    "composition": "99.9% Pure Silver (.999 Fine) / 99.99% Pure Gold (.9999 Fine)",
    "weight_grams": 31.103,
    "diameter_mm": 37.0,
    "net_pure_metal_oz": 1.0,
    "metal_type": "silver",
    "edge": "Smooth / Plain (Silver) / Milled (Gold)",
    "designer": "Thomas Pesendorfer / Austrian Mint",
    "mint_marks": [
      "M\u00fcnze \u00d6sterreich (Vienna Mint)"
    ],
    "ebay_category_id": "178078",
    "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
    "rarity_overview": "Europe's most successful and prestigious bullion coin. Depicts the Musikverein Golden Hall pipe organ on obverse and a bouquet of classical orchestral instruments on reverse.",
    "grade_values": {
      "Brilliant Uncirculated": "$34 - $42",
      "MS-69 (NGC / PCGS)": "$44 - $65",
      "MS-70 Perfect": "$70 - $135",
      "2008 First Year of Silver Issue": "$45 - $95+",
      "Gold Philharmonic (1 oz .9999 Pure)": "$2,720 - $2,850+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "2008 First Year Silver Philharmonic Issue",
        "rarity_tier": "Inaugural Silver Key",
        "est_value": "$45 - $95+",
        "description": "First year the Austrian Mint introduced pure 1 oz silver Philharmonics."
      },
      {
        "date_variety": "2009 20th Anniversary Gold '20 Ounce' Special Strike",
        "rarity_tier": "Colossal Gold Rarity",
        "est_value": "$65,000 - $95,000+",
        "description": "Huge 20-troy-ounce gold proof coin struck for the 20th anniversary."
      },
      {
        "date_variety": "2019 30th Anniversary Limited Editions",
        "rarity_tier": "Anniversary Issue",
        "est_value": "$2,850 - $4,000+",
        "description": "Special 30th jubilee editions in platinum, gold, and silver."
      }
    ],
    "selling_tips": "Only official sovereign silver bullion denominated in Euros (\u20ac1.50). The silver version has an unusual completely smooth edge without reeding."
  },
  "australian_kangaroo": {
    "id": "australian_kangaroo",
    "name": "Australian Kangaroo & Kookaburra Bullion",
    "denomination": "$1.00 AUD (Silver) / $100 AUD (Gold)",
    "years": "1986 - Present",
    "country": "Australia",
    "composition": ".9999 Pure Silver / .9999 Pure Gold",
    "weight_grams": 31.103,
    "diameter_mm": 40.6,
    "net_pure_metal_oz": 1.0,
    "metal_type": "silver",
    "edge": "Reeded / Radial Micro-Laser Security",
    "designer": "Stuart Devlin / The Perth Mint",
    "mint_marks": [
      "P (The Perth Mint, Western Australia)"
    ],
    "ebay_category_id": "178078",
    "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
    "rarity_overview": "Struck by Australia's world-renowned Perth Mint. Celebrated for high-relief strikes of the Red Kangaroo and laughing Kookaburra with micro-laser 'A' authentication marks.",
    "grade_values": {
      "Brilliant Uncirculated": "$35 - $45",
      "MS-69 (NGC / PCGS)": "$48 - $70",
      "MS-70 Perfect": "$75 - $150",
      "High Relief Proof Editions": "$95 - $250+",
      "Gold 1 oz Kangaroo / Nugget (.9999 Pure)": "$2,720 - $2,880+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "1990 Inaugural Kookaburra Silver (Square Capsule)",
        "rarity_tier": "Inaugural Australian Silver Key",
        "est_value": "$65 - $160+",
        "description": "First year Perth Mint struck the silver Kookaburra in original square mint capsule."
      },
      {
        "date_variety": "1986 Inaugural Australian Gold Nugget (Welcome Stranger)",
        "rarity_tier": "Original Gold Series Key",
        "est_value": "$2,850 - $3,500+",
        "description": "First gold series before redesigning as the Kangaroo in 1990."
      },
      {
        "date_variety": "Perth Mint Micro-Laser Authenticated 'A' Variety",
        "rarity_tier": "Anti-Counterfeit Laser Security",
        "est_value": "$38 - $85+",
        "description": "Micro-laser engraved letter 'A' inside the title AUSTRALIAN."
      }
    ],
    "selling_tips": "Perth Mint coins come factory-sealed in official acrylic capsules. Unopened capsules retain superior numismatic value. Mention .9999 four nines purity."
  },
  "world_banknote_currency": {
    "id": "world_banknote_currency",
    "name": "World Paper Currency & Banknotes",
    "denomination": "Various Denominations",
    "years": "1861 - Present",
    "country": "World / Global Banknotes",
    "composition": "High-Grade Cotton / Linen Banknote Paper or Polymer Substrate",
    "weight_grams": 1.0,
    "diameter_mm": 156.0,
    "net_pure_metal_oz": 0.0,
    "metal_type": "paper",
    "edge": "Clean Trimmed / Security Thread Embedded",
    "designer": "Bureau of Engraving & Printing / World Central Banks",
    "mint_marks": [
      "Federal Reserve District",
      "Watermark",
      "Prefix / Suffix Series",
      "Signatures"
    ],
    "ebay_category_id": "3411",
    "ebay_category_name": "Coins & Paper Money > Paper Money: World",
    "rarity_overview": "Paper currency and world banknotes valued for historical vignettes, Treasury signatures, Star replacement serials, fancy numbers, PMG EPQ paper quality, and crisp uncirculated preservation.",
    "grade_values": {
      "VG-10 / F-12 (Circulated)": "$15 - $45",
      "VF-20 / VF-30 (Clean Folds)": "$45 - $120",
      "EF-40 / AU-58 (Crisp, Minor Fold)": "$120 - $350",
      "CU-64 to Gem CU-66 EPQ (Crisp Uncirculated)": "$350 - $1,200",
      "Superb Gem CU-67+ EPQ / Rare Errors": "$1,200 - $15,000+"
    },
    "key_dates_and_varieties": [
      {
        "date_variety": "Fancy Serial Number (Solid Digits, Low #1-100, Radar, Ladder)",
        "rarity_tier": "Fancy Serial Number Rarity",
        "est_value": "$150 - $3,500+",
        "description": "Banknotes with palindromic radar numbers (e.g. 12344321), solid 77777777, or low serial under 100."
      },
      {
        "date_variety": "Star Replacement Note (\u2605 Star on Serial)",
        "rarity_tier": "Replacement Note Key",
        "est_value": "$75 - $1,800+",
        "description": "Star replacing suffix letter indicates replacement for sheet damaged during printing."
      },
      {
        "date_variety": "US 1899 $5 'Chief' Silver Certificate",
        "rarity_tier": "Classic Vignette Crown Jewel",
        "est_value": "$850 - $12,500+",
        "description": "Features iconic portrait of Running Antelope (Chief Oncpapa)."
      },
      {
        "date_variety": "US 1901 $10 'Bison' Legal Tender Note",
        "rarity_tier": "Famous American Wildlife Key",
        "est_value": "$1,200 - $18,000+",
        "description": "Features magnificent American bison flanked by Lewis and Clark."
      },
      {
        "date_variety": "PMG EPQ (Exceptional Paper Quality) Certified Specimen",
        "rarity_tier": "Third-Party Certified Gem",
        "est_value": "$150 - $5,000+",
        "description": "Certified by Paper Money Guaranty without pinholes, tears, or chemical washing."
      },
      {
        "date_variety": "Bank of England White \u00a35 Note (Pre-1956)",
        "rarity_tier": "Classic British Paper Rarity",
        "est_value": "$250 - $2,500+",
        "description": "Large format historic white banknote printed on handmade watermarked paper."
      }
    ],
    "selling_tips": "Never iron, press, or wet clean paper currency; pressing destroys original banknote embossing and cuts value by 70%. Ship in rigid PVC-free top-load currency holders with cardboard reinforcement."
  }
};

  // 3. Pre-loaded Sample Coins for 1-Tap Offline Testing
  const SAMPLE_COINS = [
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
    "mint": "Athens (\u0391\u0398\u0395)",
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
    "mint": "M\u00b0 (Mexico City)",
    "grade": "MS-67 Brilliant Uncirculated",
    "highlight": "Winged Victory over Popocat\u00e9petl (1 oz .999 Fine Silver)",
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
];

  // 4. Numismatic AI Vision Prompt
  const NUMISMATIC_SYSTEM_PROMPT = "You are an expert World-Class Numismatist and Coin Authenticator (PCGS / NGC Master Grader).\nAnalyze the provided coin photograph(s) (Obverse and/or Reverse).\n\nIdentify the coin or currency item with absolute numismatic precision and return ONLY a valid JSON object with the following schema:\n{\n  \"coin_name\": \"Full series name, e.g. Morgan Silver Dollar, Athenian Owl Tetradrachm, Roman Empire Silver Denarius, Mexican Silver Libertad, British Full Gold Sovereign, World Paper Currency\",\n  \"coin_id\": \"One of: morgan_dollar, peace_dollar, walking_liberty_half, franklin_half, kennedy_half, washington_quarter, mercury_dime, roosevelt_dime, buffalo_nickel, jefferson_nickel, lincoln_wheat_cent, lincoln_memorial_cent, american_silver_eagle, saint_gaudens_double_eagle, roman_denarius, roman_aureus, roman_sestertius, athenian_owl_tetradrachm, byzantine_solidus, widows_mite, shekel_of_tyre, british_sovereign, british_britannia, mexican_silver_libertad, mexican_50_pesos_centenario, canadian_silver_maple_leaf, canadian_gold_maple_leaf, south_african_krugerrand, chinese_silver_panda, austrian_philharmonic, australian_kangaroo, world_banknote_currency, or other\",\n  \"denomination\": \"e.g. $1.00, Tetradrachm, Denarius, Aureus, 1 Sovereign, 1 oz, 50 Pesos, $5 Banknote\",\n  \"year\": \"Detected year or era, e.g. 1921, 1955, c. 440 BC, c. 100 AD\",\n  \"mint_mark\": \"e.g. P, D, S, CC, O, W, Athens (\u0391\u0398\u0395), Rome, M\u00b0 (Mexico City), or None\",\n  \"country\": \"e.g. United States, Roman Empire, Ancient Greece, United Kingdom, Mexico, Canada, South Africa, China, Austria, Australia, World\",\n  \"estimated_grade\": \"e.g. AU-58, MS-63, VF-20, G-4, Ch VF, Ch AU, Gem CU-66 EPQ\",\n  \"strike_type\": \"Regular Business Strike / Proof / Hammered Strike / Special Mint Set\",\n  \"composition\": \"e.g. 90% Silver 10% Copper, 22K Gold, .999 Fine Silver, High-Grade Banknote Paper\",\n  \"rarity_status\": \"Common / Semi-Key Date / Key Date / Ultra Rare\",\n  \"surface_condition\": {\n    \"cleaned\": false,\n    \"details\": \"Details on wear, luster, centering, patina, bag marks, strike sharpness, full split bands, crispness, etc.\"\n  },\n  \"detected_errors_or_varieties\": [\n    \"Any visible die doubling, repunched mint mark, off-center strike, cuds, fancy serials, or note if standard strike\"\n  ],\n  \"ebay_market_price_estimate\": {\n    \"low\": 35.00,\n    \"average\": 55.00,\n    \"high\": 95.00,\n    \"recommended_buy_it_now\": 64.99,\n    \"starting_bid\": 39.99\n  },\n  \"high_value_varieties_to_inspect\": [\n    \"List of 1-3 specific famous high-value varieties for this year/series the collector should check under magnification\"\n  ],\n  \"numismatic_notes\": \"Expert notes on history, provenance, collectibility, grading advice, and warnings.\"\n}\nDo not include any conversational filler or markdown code blocks other than pure json if needed.";

  // 5. Normalizes mint strings to standard single/double letter code
  function normalizeMintMark(mintStr) {
    if (!mintStr) return '';
    const m = String(mintStr).trim();
    const mLower = m.toLowerCase();

    if (['none', 'no mint', 'philadelphia', 'phila'].some(p => mLower.startsWith(p))) {
      return '';
    }
    if (m === 'P' || mLower === 'p (philadelphia)') {
      return '';
    }
    if (mLower.includes('perth')) {
      return 'P';
    }
    if (mLower.startsWith('m°') || mLower.startsWith('mo')) {
      return 'M°';
    }

    const match = m.match(/^([A-Za-z]{1,2})\b/);
    if (match) {
      const code = match[1].toUpperCase();
      if (['D', 'S', 'CC', 'O', 'W'].includes(code)) return code;
    }

    const clean = m.split('(')[0].trim();
    if (['philadelphia', 'phila', 'none'].includes(clean.toLowerCase())) {
      return '';
    }
    if (clean.length <= 25) {
      return clean;
    }
    return '';
  }

  // 6. Default authentic baseline year for series
  function getDefaultYearForCoin(coinMeta) {
    if (!coinMeta) return 'Unknown';
    if (coinMeta.default_year) return String(coinMeta.default_year);
    const cid = coinMeta.id || '';
    const knownDefaults = {
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
    };
    if (knownDefaults[cid]) return knownDefaults[cid];
    if (coinMeta.years) {
      return coinMeta.years.split('-')[0].trim();
    }
    return 'Unknown';
  }

  // 7. Calculate precious metal melt/bullion value
  function calculateMeltValue(coinId, spotPrices) {
    const prices = Object.assign({}, DEFAULT_SPOT_PRICES, spotPrices || {});
    const coin = (coinId && typeof coinId === 'object') ? coinId : COIN_CATALOG[coinId];
    if (!coin) {
      return { has_precious_metal: false, melt_value_usd: 0.0, details: 'Unknown coin' };
    }

    const metalType = coin.metal_type;
    const netOz = coin.net_pure_metal_oz || 0.0;

    if (metalType === 'paper') {
      return {
        has_precious_metal: false,
        metal: 'Banknote Substrate (Cotton/Polymer)',
        net_weight_troy_oz: 0.0,
        melt_value_usd: 0.0,
        details: 'Paper currency (Value is 100% numismatic / collector value)'
      };
    }

    if (metalType === 'silver' && netOz > 0) {
      const melt = Math.round(netOz * prices.silver * 100) / 100;
      return {
        has_precious_metal: true,
        metal: 'Silver (.999 Fine Equivalent)',
        net_weight_troy_oz: netOz,
        spot_price_used: prices.silver,
        melt_value_usd: melt,
        details: `${netOz.toFixed(4)} oz Silver @ $${prices.silver.toFixed(2)}/oz = $${melt.toFixed(2)}`
      };
    } else if (metalType === 'gold' && netOz > 0) {
      const melt = Math.round(netOz * prices.gold * 100) / 100;
      return {
        has_precious_metal: true,
        metal: 'Gold',
        net_weight_troy_oz: netOz,
        spot_price_used: prices.gold,
        melt_value_usd: melt,
        details: `${netOz.toFixed(4)} oz Gold @ $${prices.gold.toFixed(2)}/oz = $${melt.toFixed(2)}`
      };
    } else if (metalType === 'copper') {
      const weightLbs = ((coin.weight_grams || 3.11) * 0.95) / 453.592;
      const melt = Math.round(weightLbs * (prices.copper_per_lb || 4.30) * 1000) / 1000;
      return {
        has_precious_metal: false,
        metal: '95% Pre-1982 Copper',
        net_weight_troy_oz: 0.0,
        melt_value_usd: melt,
        details: `Approx. ~$${melt.toFixed(3)} raw copper metal content`
      };
    } else if (metalType === 'bronze') {
      return {
        has_precious_metal: false,
        metal: 'Ancient Bronze / Orichalcum',
        net_weight_troy_oz: 0.0,
        melt_value_usd: 0.0,
        details: 'Ancient bronze alloy (Value is 100% numismatic / archaeological)'
      };
    }

    return {
      has_precious_metal: false,
      metal: 'Base Metal (Nickel/Zinc/Clad)',
      net_weight_troy_oz: 0.0,
      melt_value_usd: 0.0,
      details: 'No precious metal bullion content (value is numismatic only)'
    };
  }

  // 8. Smart lookup in the coin catalog based on text or keywords
  function findMatchingCoin(query) {
    if (!query) return null;
    const q = String(query).toLowerCase().trim();

    // 1. Exact ID or exact series name match
    for (const [coinId, data] of Object.entries(COIN_CATALOG)) {
      if (coinId === q || data.name.toLowerCase() === q) return data;
    }

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
    if (q.includes('maple')) {
      if (q.includes('gold')) return COIN_CATALOG.canadian_gold_maple_leaf;
      return COIN_CATALOG.canadian_silver_maple_leaf;
    }
    if (q.includes('krugerrand') || q.includes('kruger')) return COIN_CATALOG.south_african_krugerrand;
    if (q.includes('panda')) return COIN_CATALOG.chinese_silver_panda;
    if (q.includes('philharmonic') || q.includes('vienna')) return COIN_CATALOG.austrian_philharmonic;
    if (q.includes('kangaroo') || q.includes('kookaburra') || q.includes('nugget')) return COIN_CATALOG.australian_kangaroo;

    // 4. Banknotes & paper currency
    if (['banknote', 'paper money', 'paper currency', 'bill', 'certificate', 'pmg'].some(k => q.includes(k))) {
      return COIN_CATALOG.world_banknote_currency;
    }

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
    for (const [coinId, data] of Object.entries(COIN_CATALOG)) {
      if (q.includes(data.name.toLowerCase())) return data;
    }

    return null;
  }

  function buildEbayTitle(coinName, year, mintMark, gradeOrCondition, varietyNotes, metal, country) {
    const cleanMint = normalizeMintMark(mintMark || '');
    let cleanYear = year ? String(year).trim() : '';
    if (cleanYear.startsWith('-') && /^\d+$/.test(cleanYear.slice(1))) {
      cleanYear = cleanYear.slice(1) + ' BC';
    }

    const parts = [];
    if (cleanYear) {
      if (cleanMint) {
        if (cleanYear.toLowerCase().includes('bc') || cleanYear.toLowerCase().includes('ad') || cleanYear.includes(' ')) {
          parts.push(`${cleanYear} (${cleanMint})`);
        } else {
          parts.push(`${cleanYear}-${cleanMint}`);
        }
      } else {
        parts.push(cleanYear);
      }
    }
    parts.push(coinName);

    const metalStr = String(metal || '').toLowerCase();
    const nameStr = String(coinName || '').toLowerCase();
    if (metalStr.includes('silver') && !nameStr.includes('silver')) {
      parts.push('Silver');
    } else if (metalStr.includes('gold') && !nameStr.includes('gold')) {
      parts.push('Gold');
    }

    // If grade is long like 'AU-58 (About Uncirculated)', simplify to 'AU-58'
    let cleanGrade = gradeOrCondition || '';
    if (cleanGrade.includes('(')) {
      cleanGrade = cleanGrade.split('(')[0].trim();
    }
    if (cleanGrade) {
      parts.push(cleanGrade);
    }

    if (varietyNotes && varietyNotes.length < 25) {
      parts.push(varietyNotes);
    }

    // Determine accurate closing tag based on coin category/origin
    const combinedCtx = `${coinName} ${country || ''} ${metal || ''}`.toLowerCase();
    if (['banknote', 'paper money', 'currency', 'bill'].some(k => combinedCtx.includes(k))) {
      parts.push('Banknote');
    } else if (['roman', 'greece', 'greek', 'byzantine', 'biblical', 'athenian', 'ancient', 'shekel', 'prutah', 'widow', 'denarius', 'aureus', 'sestertius'].some(k => combinedCtx.includes(k))) {
      parts.push('Ancient Coin');
    } else if (['mexico', 'mexican', 'britain', 'british', 'united kingdom', 'uk', 'sovereign', 'canada', 'canadian', 'south africa', 'krugerrand', 'china', 'panda', 'austria', 'philharmonic', 'australia', 'kangaroo', 'kookaburra', 'libertad', 'centenario'].some(k => combinedCtx.includes(k))) {
      parts.push('World Coin');
    } else {
      parts.push('Old US Coin');
    }

    // Truncate while prioritizing retaining the closing tag if possible
    while (parts.join(' ').length > 80 && parts.length > 3) {
      parts.splice(parts.length - 2, 1);
    }

    let title = parts.join(' ').trim();
    if (title.length > 80) {
      const words = title.split(' ');
      while (words.join(' ').length > 80 && words.length > 2) {
        if (words.length > 3) {
          words.splice(words.length - 2, 1);
        } else {
          words.pop();
        }
      }
      title = words.join(' ');
      if (title.length > 80) title = title.slice(0, 80);
    }
    return title;
  }

  // 10. Generate responsive HTML description
  function generateEbayHtmlDescription(title, coinData, grade, conditionNotes, obverseImgUrl, reverseImgUrl) {
    coinData = coinData || {};
    const composition = coinData.composition || 'N/A';
    const weight = coinData.weight_grams || 'N/A';
    const diameter = coinData.diameter_mm || 'N/A';
    const edge = coinData.edge || 'Reeded';
    const meltVal = coinData.melt_value_usd || 0.0;
    const hasPrecious = coinData.has_precious_metal || false;

    let imagesHtml = '';
    if (obverseImgUrl || reverseImgUrl) {
      imagesHtml = `
      <div style="display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin:20px 0;">
        ${obverseImgUrl ? `<div style="text-align:center;"><img src="${obverseImgUrl}" style="max-width:280px; max-height:280px; border-radius:12px; border:1px solid #ddd; box-shadow:0 4px 10px rgba(0,0,0,0.08); object-fit:contain;"><p style="font-weight:600; color:#555; margin-top:6px;">Obverse (Front)</p></div>` : ''}
        ${reverseImgUrl ? `<div style="text-align:center;"><img src="${reverseImgUrl}" style="max-width:280px; max-height:280px; border-radius:12px; border:1px solid #ddd; box-shadow:0 4px 10px rgba(0,0,0,0.08); object-fit:contain;"><p style="font-weight:600; color:#555; margin-top:6px;">Reverse (Back)</p></div>` : ''}
      </div>`;
    }

    let meltBadge = '';
    if (hasPrecious && meltVal > 0) {
      meltBadge = `
      <div style="background:#fef3c7; border:1px solid #f59e0b; color:#92400e; padding:10px 16px; border-radius:8px; font-weight:600; margin:16px 0; text-align:center;">
        ⚡ Precious Metal Bullion Value: Approx. $${Number(meltVal).toFixed(2)} USD minimum intrinsic melt value
      </div>`;
    }

    return `
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height:1.6; color:#222; margin:0; padding:12px; background:#f9fafb;">
  <div style="max-width:800px; margin:0 auto; background:#ffffff; border-radius:16px; overflow:hidden; border:1px solid #e5e7eb; box-shadow:0 4px 16px rgba(0,0,0,0.06);">
    <div style="background:linear-gradient(135deg, #1e3a8a, #3b82f6); color:#ffffff; padding:24px 20px; text-align:center;">
      <h1 style="margin:0; font-size:22px; font-weight:700; letter-spacing:-0.5px;">${title}</h1>
      <p style="margin:6px 0 0; opacity:0.9; font-size:14px;">Authentic Numismatic Specimen &bull; Grade: ${grade || 'Collector Grade'}</p>
    </div>

    <div style="padding:24px 20px;">
      ${imagesHtml}
      ${meltBadge}

      <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:20px; font-size:17px;">
        🪙 Coin Specifications
      </h3>
      <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:14px;">
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; width:40%; border-bottom:1px solid #e2e8f0;">Series / Name</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${coinData.name || 'Coin'}</td></tr>
        <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Denomination</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${coinData.denomination || 'N/A'}</td></tr>
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Composition</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${composition}</td></tr>
        <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Weight</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${weight} grams</td></tr>
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Diameter</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${diameter} mm</td></tr>
        <tr><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Edge</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${edge}</td></tr>
        <tr style="background:#f8fafc;"><td style="padding:10px; font-weight:600; border-bottom:1px solid #e2e8f0;">Country of Origin</td><td style="padding:10px; border-bottom:1px solid #e2e8f0;">${coinData.country || 'United States'}</td></tr>
      </table>

      <h3 style="color:#1e3a8a; border-bottom:2px solid #e5e7eb; padding-bottom:8px; margin-top:24px; font-size:17px;">
        🔍 Item Condition & Collector Notes
      </h3>
      <div style="background:#f3f4f6; padding:14px; border-radius:8px; font-size:14px; margin-bottom:20px;">
        <p style="margin:0 0 8px;"><strong>Estimated Grade:</strong> ${grade || 'Collector Grade'}</p>
        <p style="margin:0 0 8px;">${conditionNotes || 'Please review all high-resolution photos carefully to determine grade and condition for yourself. The coin shown in the pictures is the exact coin you will receive.'}</p>
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
  }

  // 11. Deep link to eBay web sell flow
  function generateEbayPrelistUrl(title, categoryId) {
    const params = new URLSearchParams({ query: title });
    if (categoryId) params.set('categoryId', categoryId);
    return `https://www.ebay.com/sl/prelist/suggest?${params.toString()}`;
  }

  // 12. Mercari listing generator
  function generateMercariListing(title, coinData, grade, price, conditionNotes) {
    coinData = coinData || {};
    const name = coinData.name || 'Coin';
    const comp = coinData.composition || 'Solid Coin';
    const country = coinData.country || '';
    const meltVal = coinData.melt_value_usd || 0.0;
    const hasPrecious = coinData.has_precious_metal || false;

    let tags = '#coins #silver #numismatics #collectibles #bullion';
    const combined = `${name} ${country} ${comp}`.toLowerCase();
    if (comp.toLowerCase().includes('gold')) {
      tags = '#gold #coins #preciousmetals #numismatics #rarecoin';
    } else if (['banknote', 'paper money', 'currency'].some(k => combined.includes(k))) {
      tags = '#papermoney #banknotes #currency #collectibles #numismatics';
    } else if (['roman', 'greek', 'greece', 'byzantine', 'ancient', 'athenian', 'biblical', 'shekel', 'prutah', 'widow', 'denarius', 'aureus', 'sestertius'].some(k => combined.includes(k))) {
      tags = '#ancientcoins #roman #greek #numismatics #history';
    } else if (['mexico', 'mexican', 'britain', 'british', 'united kingdom', 'uk', 'canada', 'canadian', 'south africa', 'china', 'austria', 'australia', 'world', 'sovereign', 'krugerrand', 'libertad', 'philharmonic', 'centenario', 'maple'].some(k => combined.includes(k))) {
      tags = '#worldcoins #silver #bullion #numismatics #collectibles';
    }

    const meltMention = hasPrecious && meltVal > 0 ? `\n• Bullion Melt Value: Approx. $${Number(meltVal).toFixed(2)} USD` : '';

    const desc = `FOR SALE: ${title}

Coin Details:
• Series: ${name}
• Estimated Grade: ${grade}
• Composition: ${comp}
• Weight: ${coinData.weight_grams || 'N/A'}g
• Diameter: ${coinData.diameter_mm || 'N/A'}mm${meltMention}

Condition & Provenance:
${conditionNotes || 'Authentic coin with nice original surfaces. Uncleaned and well preserved. Please review all photos for exact condition.'}

Shipping:
Ships safely packaged in a protective PVC-free flip/capsule inside a bubble mailer with USPS tracking within 24 hours of purchase!

${tags}`.trim();

    return {
      title: title.slice(0, 80),
      price: price,
      category: 'Vintage & Collectibles > Antique Collectibles > Coins & Money',
      condition: 'Good / Like New',
      description: desc,
      tags: tags
    };
  }

  // 13. Whatnot livestream card generator
  function generateWhatnotListing(title, coinData, grade, startingBid, buyItNow) {
    coinData = coinData || {};
    const name = coinData.name || 'Coin';
    const country = coinData.country || '';
    const comp = coinData.composition || '';
    const combined = `${name} ${country} ${comp}`.toLowerCase();

    let cat = 'Coins & Money > US Coins';
    if (['banknote', 'paper money', 'currency'].some(k => combined.includes(k))) {
      cat = 'Coins & Money > Paper Money';
    } else if (['roman', 'greek', 'greece', 'byzantine', 'ancient', 'athenian', 'biblical', 'shekel', 'prutah', 'widow', 'denarius', 'aureus', 'sestertius'].some(k => combined.includes(k))) {
      cat = 'Coins & Money > Ancient Coins';
    } else if (['mexico', 'mexican', 'britain', 'british', 'united kingdom', 'uk', 'canada', 'canadian', 'south africa', 'china', 'austria', 'australia', 'world', 'sovereign', 'krugerrand', 'libertad', 'philharmonic', 'centenario', 'maple'].some(k => combined.includes(k))) {
      cat = 'Coins & Money > World Coins';
    }

    return {
      title: title.slice(0, 80),
      category: cat,
      starting_bid: startingBid,
      buy_it_now_price: buyItNow,
      condition: grade,
      auction_notes: `${name} • ${grade} • ${comp} • Sudden Death Auction`
    };
  }

  // 14. Reddit [WTS] post generator
  function generateRedditListing(title, coinData, grade, price) {
    coinData = coinData || {};
    const meltVal = coinData.melt_value_usd || 0.0;
    const hasPrecious = coinData.has_precious_metal || false;
    const meltStr = hasPrecious && meltVal > 0 ? ` (Melt value: ~$${Number(meltVal).toFixed(2)})` : '';

    return `[WTS] ${title}

**Item Details:**
- **Coin:** ${coinData.name || 'Coin'}
- **Grade / Condition:** ${grade}
- **Composition:** ${coinData.composition || 'Standard'}
- **Weight / Specs:** ${coinData.weight_grams || 'N/A'}g, ${coinData.diameter_mm || 'N/A'}mm${meltStr}
- **Asking Price:** **$${Number(price).toFixed(2)}** (OBO)

**Shipping:**
- $5 Ground Advantage with tracking / $9 Priority Mail
- Ships securely packed in flip with cardboard sandwich

**Payment:** Zelle, Venmo, PayPal F&F, CashApp (no notes please)`.trim();
  }

  // 14b. Dynamically construct coin metadata for unrecognized/custom coins identified by AI
  function createDynamicCoinMeta(analysisData, coinHint) {
    const rawName = (analysisData && analysisData.coin_name) || coinHint || 'Uncataloged Coin';
    const rawDenom = (analysisData && analysisData.denomination) || 'Collectible Coin';
    const rawCountry = (analysisData && analysisData.country) || 'World';
    const rawYear = (analysisData && analysisData.year) ? String(analysisData.year) : 'Unknown';
    const rawComp = (analysisData && analysisData.composition) || 'Standard Coin Metal';
    const compLower = rawComp.toLowerCase();
    const nameLower = rawName.toLowerCase();
    const denomLower = rawDenom.toLowerCase();

    let metalType = 'base';
    let purity = 0.0;
    let netOz = 0.0;
    let weightGrams = 0.0;
    let diameterMm = 0.0;

    if (compLower.includes('gold') || nameLower.includes('gold')) {
      metalType = 'gold';
      if (compLower.includes('999') || compLower.includes('24k')) {
        purity = 0.999;
      } else if (compLower.includes('22k') || compLower.includes('91.67')) {
        purity = 0.9167;
      } else {
        purity = 0.900;
      }
      if (nameLower.includes('1 oz') || denomLower.includes('1 oz') || compLower.includes('1 oz')) {
        netOz = 1.0;
        weightGrams = 31.1;
      } else if (nameLower.includes('1/2 oz') || denomLower.includes('1/2 oz')) {
        netOz = 0.5;
        weightGrams = 15.55;
      } else if (nameLower.includes('1/4 oz') || denomLower.includes('1/4 oz')) {
        netOz = 0.25;
        weightGrams = 7.78;
      } else if (nameLower.includes('1/10 oz') || denomLower.includes('1/10 oz')) {
        netOz = 0.1;
        weightGrams = 3.11;
      } else {
        netOz = 0.25;
        weightGrams = 7.78;
      }
    } else if (compLower.includes('silver') || nameLower.includes('silver')) {
      metalType = 'silver';
      if (compLower.includes('.999') || compLower.includes('fine silver') || compLower.includes('pure silver')) {
        purity = 0.999;
        netOz = 1.0;
        weightGrams = 31.1;
      } else if (compLower.includes('90%') || compLower.includes('.900')) {
        purity = 0.900;
        if (denomLower.includes('dollar') || nameLower.includes('dollar') || denomLower.includes('$1')) {
          netOz = 0.7734;
          weightGrams = 26.73;
          diameterMm = 38.1;
        } else if (denomLower.includes('half') || nameLower.includes('half') || denomLower.includes('50')) {
          netOz = 0.3617;
          weightGrams = 12.5;
          diameterMm = 30.6;
        } else if (denomLower.includes('quarter') || nameLower.includes('quarter') || denomLower.includes('25')) {
          netOz = 0.1808;
          weightGrams = 6.25;
          diameterMm = 24.3;
        } else if (denomLower.includes('dime') || nameLower.includes('dime') || denomLower.includes('10')) {
          netOz = 0.0723;
          weightGrams = 2.5;
          diameterMm = 17.9;
        } else {
          netOz = 0.1808;
          weightGrams = 6.25;
          diameterMm = 24.3;
        }
      } else if (compLower.includes('40%') || compLower.includes('.400')) {
        purity = 0.400;
        netOz = 0.1479;
        weightGrams = 11.5;
        diameterMm = 30.6;
      } else {
        purity = 0.900;
        netOz = 0.1808;
        weightGrams = 6.25;
        diameterMm = 24.3;
      }
    } else if (compLower.includes('paper') || compLower.includes('banknote') || compLower.includes('polymer')) {
      metalType = 'paper';
    } else if (compLower.includes('bronze')) {
      metalType = 'bronze';
    } else if (compLower.includes('copper')) {
      metalType = 'copper';
    }

    let ebayCatId = '11116';
    let ebayCatName = 'Coins & Paper Money';
    const cLower = rawCountry.toLowerCase();
    if (cLower.includes('united states') || cLower.includes('usa') || cLower.includes('u.s.')) {
      ebayCatId = '253';
      ebayCatName = 'Coins: US';
    } else if (cLower.includes('rome') || cLower.includes('greece') || cLower.includes('ancient') || cLower.includes('byzantine')) {
      ebayCatId = '4733';
      ebayCatName = 'Coins: Ancient';
    } else if (metalType === 'paper') {
      ebayCatId = '3411';
      ebayCatName = 'Paper Money: World';
    } else {
      ebayCatId = '256';
      ebayCatName = 'Coins: World';
    }

    const dynamicId = (analysisData && analysisData.coin_id && analysisData.coin_id !== 'other')
      ? analysisData.coin_id
      : rawName.toLowerCase().replace(/[^a-z0-9]+/g, '_').slice(0, 40);

    const varieties = [];
    if (analysisData && Array.isArray(analysisData.high_value_varieties_to_inspect)) {
      analysisData.high_value_varieties_to_inspect.forEach(v => {
        if (typeof v === 'string') {
          varieties.push({
            date_variety: v,
            rarity_tier: 'Variety to Inspect',
            estimated_value: 'Market Rate',
            description: v
          });
        } else if (v && typeof v === 'object') {
          varieties.push(v);
        }
      });
    }

    return {
      id: dynamicId,
      name: rawName,
      denomination: rawDenom,
      country: rawCountry,
      years: rawYear,
      default_year: rawYear,
      composition: rawComp,
      metal_type: metalType,
      purity: purity,
      net_pure_metal_oz: netOz,
      weight_grams: weightGrams,
      diameter_mm: diameterMm,
      edge: 'Standard',
      designer: 'Official Mint Engraver',
      ebay_category_id: ebayCatId,
      ebay_category_name: ebayCatName,
      rarity_overview: (analysisData && analysisData.rarity_status) || 'Numismatic collectibility varies by condition and date.',
      key_dates_and_varieties: varieties,
      grade_values: {},
      selling_tips: 'Take sharp close-up photos of both sides and edges under balanced lighting.'
    };
  }

  // 15. Complete coin report builder (runs 100% client side)
  function generateCoinReport(opts) {
    opts = opts || {};
    const analysisData = opts.analysisData || null;
    const coinHint = opts.coinHint || '';
    const yearHint = opts.yearHint || '';
    const mintHint = opts.mintHint || '';
    const obverseUrl = opts.obverseUrl || '';
    const reverseUrl = opts.reverseUrl || '';
    const spotPrices = opts.spotPrices || null;

    let coinMeta = null;
    let targetId = '';

    if (analysisData && analysisData.coin_id && COIN_CATALOG[analysisData.coin_id]) {
      targetId = analysisData.coin_id;
      coinMeta = COIN_CATALOG[targetId];
    } else if (analysisData && analysisData.coin_id && analysisData.coin_id !== 'other') {
      const matched = findMatchingCoin(analysisData.coin_id);
      if (matched) {
        targetId = matched.id;
        coinMeta = matched;
      }
    }

    if (!coinMeta && analysisData && analysisData.coin_name) {
      const matched = findMatchingCoin(analysisData.coin_name);
      if (matched) {
        targetId = matched.id;
        coinMeta = matched;
      }
    }

    if (!coinMeta && coinHint) {
      const matched = findMatchingCoin(coinHint);
      if (matched) {
        targetId = matched.id;
        coinMeta = matched;
      }
    }

    // If analysisData is present but coin is not in the hardcoded series list,
    // dynamically generate a report for it rather than forcing morgan_dollar.
    if (!coinMeta && analysisData) {
      coinMeta = createDynamicCoinMeta(analysisData, coinHint);
      targetId = coinMeta.id;
    }

    // Fallback: If neither analysisData nor matched coinHint was found
    if (!coinMeta) {
      if (coinHint) {
        coinMeta = createDynamicCoinMeta({ coin_name: coinHint }, coinHint);
        targetId = coinMeta.id;
      } else {
        throw new Error('Cannot generate coin report without either coinHint or AI analysisData. Please select a series or configure Gemini Vision.');
      }
    }

    const defaultYear = getDefaultYearForCoin(coinMeta);
    const year = yearHint || (analysisData && analysisData.year ? String(analysisData.year) : defaultYear);
    const rawMint = mintHint || (analysisData && analysisData.mint_mark ? analysisData.mint_mark : 'None');
    const cleanMint = normalizeMintMark(String(rawMint));
    const mintMark = cleanMint || 'None';
    const estimatedGrade = (analysisData && analysisData.estimated_grade) ? analysisData.estimated_grade : 'AU-58 (About Uncirculated)';
    const strikeType = (analysisData && analysisData.strike_type) ? analysisData.strike_type : 'Regular Business Strike';

    const meltInfo = calculateMeltValue(coinMeta, spotPrices);

    let pricing;
    if (analysisData && analysisData.ebay_market_price_estimate && typeof analysisData.ebay_market_price_estimate.average === 'number') {
      pricing = analysisData.ebay_market_price_estimate;
    } else {
      const hasSilver = coinMeta.metal_type === 'silver';
      const hasGold = coinMeta.metal_type === 'gold';
      const isPaper = coinMeta.metal_type === 'paper';
      const isAncientBronze = coinMeta.metal_type === 'bronze';
      const melt = meltInfo.melt_value_usd || 0.0;
      let baseLow, baseAvg, baseHigh;

      if (hasGold && melt > 0) {
        baseLow = Math.round(melt * 1.03 * 100) / 100;
        baseAvg = Math.round(melt * 1.08 * 100) / 100;
        baseHigh = Math.round(melt * 1.25 * 100) / 100;
      } else if (hasSilver && melt > 0) {
        if (['owl', 'shekel', 'denarius', 'ancient'].some(k => (coinMeta.id || '').includes(k))) {
          baseLow = Math.max(melt * 1.5, ((coinMeta.id || '').includes('owl') || (coinMeta.id || '').includes('shekel')) ? 450.0 : 85.0);
          baseAvg = Math.max(melt * 2.5, ((coinMeta.id || '').includes('owl') || (coinMeta.id || '').includes('shekel')) ? 950.0 : 180.0);
          baseHigh = Math.max(melt * 4.0, ((coinMeta.id || '').includes('owl') || (coinMeta.id || '').includes('shekel')) ? 2200.0 : 450.0);
        } else {
          baseLow = Math.max(melt * 1.15, 28.0);
          baseAvg = Math.max(melt * 1.5, 45.0);
          baseHigh = Math.max(melt * 2.2, 85.0);
        }
      } else if (isPaper) {
        baseLow = 35.0;
        baseAvg = 95.0;
        baseHigh = 350.0;
      } else if (isAncientBronze) {
        baseLow = (coinMeta.id || '').includes('widow') ? 45.0 : 150.0;
        baseAvg = (coinMeta.id || '').includes('widow') ? 120.0 : 450.0;
        baseHigh = (coinMeta.id || '').includes('widow') ? 350.0 : 1200.0;
      } else {
        baseLow = 15.0;
        baseAvg = 25.0;
        baseHigh = 65.0;
      }

      pricing = {
        low: Math.round(baseLow * 100) / 100,
        average: Math.round(baseAvg * 100) / 100,
        high: Math.round(baseHigh * 100) / 100,
        recommended_buy_it_now: Math.round(baseAvg * 1.1 * 100) / 100,
        starting_bid: Math.round(baseLow * 0.9 * 100) / 100
      };
    }

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

    const mergedCoinInfo = Object.assign({}, coinMeta, meltInfo);

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
    if (rawYearStr.startsWith('-') && /^\d+$/.test(rawYearStr.slice(1))) {
      rawYearStr = rawYearStr.slice(1) + 'BC';
    }
    const cleanSkuYear = rawYearStr.replace(/[^A-Za-z0-9]/g, '') || 'GEN';
    const sku = `COIN-${targetId.slice(0, 6).toUpperCase()}-${cleanSkuYear}-${skuMint}-${Math.floor(pricing.recommended_buy_it_now)}`;

    const mercariListing = generateMercariListing(ebayTitle, mergedCoinInfo, estimatedGrade, pricing.recommended_buy_it_now, conditionNotes);
    const whatnotListing = generateWhatnotListing(ebayTitle, mergedCoinInfo, estimatedGrade, pricing.starting_bid, pricing.recommended_buy_it_now);
    const redditListing = generateRedditListing(ebayTitle, mergedCoinInfo, estimatedGrade, pricing.recommended_buy_it_now);

    return {
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
      grade_values_guide: coinMeta.grade_values || {},
      pricing_estimate: pricing,
      high_dollar_varieties: (catalogVarieties && catalogVarieties.length > 0)
        ? catalogVarieties
        : ((analysisData && Array.isArray(analysisData.high_value_varieties_to_inspect))
          ? analysisData.high_value_varieties_to_inspect.map(v => (typeof v === 'string' ? { date_variety: v, rarity_tier: 'Variety to Inspect', estimated_value: 'Market Rate', description: v } : v))
          : []),
      detected_varieties: detectedVarieties,
      selling_tips: coinMeta.selling_tips || '',
      ai_identified: Boolean(analysisData),
      vision_model: analysisData ? (analysisData.model_used || 'gemini-2.5-flash') : null,
      standalone_client_mode: true,
      ebay_listing: {
        title: ebayTitle,
        category_id: coinMeta.ebay_category_id || '',
        category_name: coinMeta.ebay_category_name || '',
        sku: sku,
        buy_it_now_price: pricing.recommended_buy_it_now,
        starting_bid_price: pricing.starting_bid,
        html_description: htmlDescription,
        prelist_url: prelistUrl
      },
      mercari_listing: mercariListing,
      whatnot_listing: whatnotListing,
      reddit_listing: redditListing
    };
  }

  // 16. Direct Client-Side Gemini Vision API caller (No local server or PC required)
  async function analyzeCoinDirectGemini(imagesBase64, apiKey) {
    if (!apiKey) {
      throw new Error('No Gemini API key provided');
    }
    if (!imagesBase64 || imagesBase64.length === 0) {
      throw new Error('No images provided for analysis');
    }

    const parts = [
      { text: 'Analyze this coin photo (obverse/reverse). Provide exact numismatic identification, series name, coin_id, year, mint mark, grade, composition, rarity status, errors or varieties, and valuation. Return strictly a JSON object conforming to the schema.' }
    ];

    imagesBase64.forEach(dataUri => {
      if (!dataUri) return;
      let mimeType = 'image/jpeg';
      let rawBase64 = dataUri;
      if (dataUri.includes(';base64,')) {
        const header = dataUri.split(';base64,')[0];
        rawBase64 = dataUri.split(';base64,')[1];
        if (header.includes('image/png')) mimeType = 'image/png';
        else if (header.includes('image/webp')) mimeType = 'image/webp';
      }
      parts.push({
        inlineData: {
          mimeType: mimeType,
          data: rawBase64
        }
      });
    });

    // Try Gemini 2.5 Flash, fallback to 2.0 Flash
    const models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash'];
    let lastError = null;

    for (const model of models) {
      const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(apiKey)}`;
      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            systemInstruction: {
              parts: [{ text: NUMISMATIC_SYSTEM_PROMPT }]
            },
            contents: [{ parts: parts }],
            generationConfig: {
              temperature: 0.2,
              responseMimeType: 'application/json'
            }
          })
        });

        if (!res.ok) {
          const errText = await res.text();
          console.warn(`Gemini model ${model} error:`, errText);
          lastError = new Error(`Gemini API error (${res.status}): ${errText.slice(0, 150)}`);
          continue;
        }

        const data = await res.json();
        const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
        if (!candidateText) {
          throw new Error('Empty response from Gemini Vision API');
        }

        // Clean json if wrapped in markdown
        let cleaned = candidateText.trim();
        if (cleaned.startsWith('```json')) {
          cleaned = cleaned.replace(/^```json\s*/, '').replace(/\s*```$/, '');
        } else if (cleaned.startsWith('```')) {
          cleaned = cleaned.replace(/^```\s*/, '').replace(/\s*```$/, '');
        }

        let parsed;
        try {
          parsed = JSON.parse(cleaned);
        } catch (jsonErr) {
          const firstBrace = cleaned.indexOf('{');
          const lastBrace = cleaned.lastIndexOf('}');
          if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
            parsed = JSON.parse(cleaned.slice(firstBrace, lastBrace + 1));
          } else {
            throw jsonErr;
          }
        }

        parsed.model_used = model;
        return parsed;
      } catch (err) {
        console.warn(`Attempt with ${model} failed:`, err);
        lastError = err;
      }
    }

    throw lastError || new Error('Failed to analyze with Gemini API');
  }

  // Export to Global namespace
  const CoinVaultEngine = {
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
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = CoinVaultEngine;
  } else {
    root.CoinVaultEngine = CoinVaultEngine;
  }

})(typeof window !== 'undefined' ? window : this);
