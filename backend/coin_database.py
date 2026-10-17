"""
Coin Database & Numismatic Knowledge Base
Provides coin specifications, metal compositions, melt value formulas,
key dates, high-dollar error varieties, and eBay category mappings.
"""

from typing import Dict, Any, List, Optional

# Current baseline spot metal prices (USD / Troy Oz) - updated dynamically if online or fallback
DEFAULT_SPOT_PRICES = {
    "silver": 31.50,
    "gold": 2680.00,
    "platinum": 980.00,
    "copper_per_lb": 4.30
}

COIN_CATALOG: Dict[str, Dict[str, Any]] = {
    "morgan_dollar": {
        "id": "morgan_dollar",
        "name": "Morgan Silver Dollar",
        "denomination": "$1.00 USD",
        "years": "1878 - 1921",
        "country": "United States",
        "composition": "90% Silver, 10% Copper",
        "weight_grams": 26.73,
        "diameter_mm": 38.1,
        "net_pure_metal_oz": 0.77344,  # Troy oz pure silver
        "metal_type": "silver",
        "edge": "Reeded",
        "designer": "George T. Morgan",
        "mint_marks": ["None (Philadelphia)", "D (Denver - 1921 only)", "S (San Francisco)", "O (New Orleans)", "CC (Carson City)"],
        "ebay_category_id": "39464",  # Coins & Paper Money > Coins: US > Dollars > Morgan (1878-1921)
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
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 12.50,
        "diameter_mm": 30.63,
        "net_pure_metal_oz": 0.36169,
        "metal_type": "silver",
        "edge": "Reeded",
        "designer": "Adolph A. Weinman",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 12.50,
        "diameter_mm": 30.63,
        "net_pure_metal_oz": 0.36169,
        "metal_type": "silver",
        "edge": "Reeded",
        "designer": "John R. Sinnock",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 12.50,  # 1964 90%
        "diameter_mm": 30.61,
        "net_pure_metal_oz": 0.36169,  # For 1964 silver
        "metal_type": "silver",
        "edge": "Reeded",
        "designer": "Gilroy Roberts / Frank Gasparro",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 2.50,
        "diameter_mm": 17.9,
        "net_pure_metal_oz": 0.07234,
        "metal_type": "silver",
        "edge": "Reeded",
        "designer": "Adolph A. Weinman",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 2.50,  # Silver
        "diameter_mm": 17.9,
        "net_pure_metal_oz": 0.07234,  # For pre-1965 silver
        "metal_type": "silver",
        "edge": "Reeded",
        "designer": "John R. Sinnock",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)", "P (1980+)"],
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
        "weight_grams": 5.00,
        "diameter_mm": 21.2,
        "net_pure_metal_oz": 0.0,
        "metal_type": "base_metal",
        "edge": "Plain",
        "designer": "James Earle Fraser",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
                "date_variety": "1936-D 3½ Legs",
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
        "weight_grams": 5.00,
        "diameter_mm": 21.2,
        "net_pure_metal_oz": 0.05626,  # For Wartime Silver (1942-1945 with large mintmark above Monticello)
        "metal_type": "silver_or_base",
        "edge": "Plain",
        "designer": "Felix Schlag",
        "mint_marks": ["None / P", "D", "S"],
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
        "weight_grams": 3.11,  # 1943 steel is 2.70g
        "diameter_mm": 19.05,
        "net_pure_metal_oz": 0.0,
        "metal_type": "copper",
        "edge": "Plain",
        "designer": "Victor David Brenner",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 3.11,  # Copper; Zinc is 2.5g
        "diameter_mm": 19.05,
        "net_pure_metal_oz": 0.0,
        "metal_type": "copper_or_zinc",
        "edge": "Plain",
        "designer": "Frank Gasparro",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "mint_marks": ["None (Bullion)", "W (West Point)", "S (San Francisco)", "P (Philadelphia)"],
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
        "net_pure_metal_oz": 0.9675,  # Almost full oz pure gold
        "metal_type": "gold",
        "edge": "Lettered ('E PLURIBUS UNUM' with stars)",
        "designer": "Augustus Saint-Gaudens",
        "mint_marks": ["None (Philadelphia)", "D (Denver)", "S (San Francisco)"],
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
        "weight_grams": 3.90,
        "diameter_mm": 19.0,
        "net_pure_metal_oz": 0.1100,
        "metal_type": "silver",
        "edge": "Plain / Hammered Irregular",
        "designer": "Imperial Roman Mint Masters",
        "mint_marks": ["Rome", "Lugdunum (Lyon)", "Antioch", "Alexandria", "Siscia"],
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
        "weight_grams": 7.30,
        "diameter_mm": 19.5,
        "net_pure_metal_oz": 0.2330,
        "metal_type": "gold",
        "edge": "Plain / Hammered Flanning",
        "designer": "Imperial Mint Masters",
        "mint_marks": ["Rome", "Lugdunum", "Antioch", "Nicomedia"],
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
        "weight_grams": 25.00,
        "diameter_mm": 33.0,
        "net_pure_metal_oz": 0.0,
        "metal_type": "bronze",
        "edge": "Plain / Thick Irregular",
        "designer": "Senate & Imperial Mint Masters (SC - Senatus Consulto)",
        "mint_marks": ["Rome", "Lugdunum"],
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
        "weight_grams": 17.20,
        "diameter_mm": 24.0,
        "net_pure_metal_oz": 0.5400,
        "metal_type": "silver",
        "edge": "Plain / Chunky Hammered Planchet",
        "designer": "Athenian State Mint",
        "mint_marks": ["Athens (ΑΘΕ)"],
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
        "weight_grams": 4.50,
        "diameter_mm": 21.0,
        "net_pure_metal_oz": 0.1420,
        "metal_type": "gold",
        "edge": "Plain / Hammered",
        "designer": "Constantinople Imperial Mint",
        "mint_marks": ["CONOB (Constantinople / Pure Gold)", "Thessalonica", "Ravenna", "Carthage"],
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
        "weight_grams": 1.50,
        "diameter_mm": 14.0,
        "net_pure_metal_oz": 0.0,
        "metal_type": "bronze",
        "edge": "Plain / Crude Irregular",
        "designer": "Jerusalem Mint of Judaea",
        "mint_marks": ["Jerusalem"],
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
        "weight_grams": 14.20,
        "diameter_mm": 27.0,
        "net_pure_metal_oz": 0.4300,
        "metal_type": "silver",
        "edge": "Plain / Thick Planchet",
        "designer": "Tyrian Mint",
        "mint_marks": ["Tyre (Monogram & Club of Melqart)"],
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
        "denomination": "1 Sovereign (£1 GBP)",
        "years": "1817 - Present",
        "country": "United Kingdom",
        "composition": "22 Karat Gold (91.67% Gold, 8.33% Copper)",
        "weight_grams": 7.988,
        "diameter_mm": 22.05,
        "net_pure_metal_oz": 0.2354,
        "metal_type": "gold",
        "edge": "Milled / Reeded",
        "designer": "Benedetto Pistrucci (St. George & Dragon)",
        "mint_marks": ["None (London)", "M (Melbourne)", "S (Sydney)", "P (Perth)", "C (Ottawa)", "SA (Pretoria)", "I (Bombay)"],
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
        "denomination": "£2 GBP (Silver) / £100 GBP (Gold)",
        "years": "1987 - Present",
        "country": "United Kingdom",
        "composition": ".999 Fine Silver / .9999 Pure Gold",
        "weight_grams": 31.21,
        "diameter_mm": 38.61,
        "net_pure_metal_oz": 1.0000,
        "metal_type": "silver",
        "edge": "Reeded / Security Micro-Text",
        "designer": "Philip Nathan / The Royal Mint",
        "mint_marks": ["Royal Mint (Llantrisant, Wales)"],
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
        "net_pure_metal_oz": 1.0000,
        "metal_type": "silver",
        "edge": "Reeded (Edge Lettered 1982-1989 'INDEPENDENCIA Y LIBERTAD')",
        "designer": "Casa de Moneda de México",
        "mint_marks": ["M° (Mexico City Mint - Americas' Oldest Mint)"],
        "ebay_category_id": "178078",
        "ebay_category_name": "Coins & Paper Money > Bullion > Silver > Coins",
        "rarity_overview": "Struck by the oldest operating mint in the Americas (founded 1535). Features the iconic Winged Victory (El Ángel de la Independencia) with volcanoes Popocatépetl and Iztaccíhuatl in the background.",
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
        "mint_marks": ["M° (Mexico City Mint)"],
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
        "net_pure_metal_oz": 1.0000,
        "metal_type": "silver",
        "edge": "Serrated / Radial Lines",
        "designer": "Walter Ott / Royal Canadian Mint",
        "mint_marks": ["RCM (Ottawa Mint)"],
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
        "net_pure_metal_oz": 1.0000,
        "metal_type": "gold",
        "edge": "Reeded",
        "designer": "Walter Ott / Royal Canadian Mint",
        "mint_marks": ["Royal Canadian Mint"],
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
        "net_pure_metal_oz": 1.0000,
        "metal_type": "gold",
        "edge": "Reeded (160 serrations bullion, 220 proof)",
        "designer": "Otto Schultz (Paul Kruger) / Coert Steynberg (Springbok)",
        "mint_marks": ["South African Mint / Rand Refinery"],
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
        "denomination": "10 Yuan (¥10 RMB)",
        "years": "1983 - Present",
        "country": "China",
        "composition": "99.9% Pure Silver (.999 Fine)",
        "weight_grams": 30.00,
        "diameter_mm": 40.0,
        "net_pure_metal_oz": 0.9645,
        "metal_type": "silver",
        "edge": "Slanted / Oblique Reeded",
        "designer": "China Gold Coin Corp / People's Bank of China",
        "mint_marks": ["Beijing", "Shanghai", "Shenyang", "Shenzhen"],
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
        "denomination": "€1.50 EUR (Silver) / €100 EUR (Gold)",
        "years": "1989 - Present (Silver introduced 2008)",
        "country": "Austria",
        "composition": "99.9% Pure Silver (.999 Fine) / 99.99% Pure Gold (.9999 Fine)",
        "weight_grams": 31.103,
        "diameter_mm": 37.0,
        "net_pure_metal_oz": 1.0000,
        "metal_type": "silver",
        "edge": "Smooth / Plain (Silver) / Milled (Gold)",
        "designer": "Thomas Pesendorfer / Austrian Mint",
        "mint_marks": ["Münze Österreich (Vienna Mint)"],
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
        "selling_tips": "Only official sovereign silver bullion denominated in Euros (€1.50). The silver version has an unusual completely smooth edge without reeding."
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
        "net_pure_metal_oz": 1.0000,
        "metal_type": "silver",
        "edge": "Reeded / Radial Micro-Laser Security",
        "designer": "Stuart Devlin / The Perth Mint",
        "mint_marks": ["P (The Perth Mint, Western Australia)"],
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
        "weight_grams": 1.00,
        "diameter_mm": 156.0,
        "net_pure_metal_oz": 0.0,
        "metal_type": "paper",
        "edge": "Clean Trimmed / Security Thread Embedded",
        "designer": "Bureau of Engraving & Printing / World Central Banks",
        "mint_marks": ["Federal Reserve District", "Watermark", "Prefix / Suffix Series", "Signatures"],
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
                "date_variety": "Star Replacement Note (★ Star on Serial)",
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
                "date_variety": "Bank of England White £5 Note (Pre-1956)",
                "rarity_tier": "Classic British Paper Rarity",
                "est_value": "$250 - $2,500+",
                "description": "Large format historic white banknote printed on handmade watermarked paper."
            }
        ],
        "selling_tips": "Never iron, press, or wet clean paper currency; pressing destroys original banknote embossing and cuts value by 70%. Ship in rigid PVC-free top-load currency holders with cardboard reinforcement."
    }
}


def calculate_melt_value(coin_id_or_meta: Union[str, Dict[str, Any]], spot_prices: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Calculate current precious metal melt/bullion value for a coin."""
    prices = spot_prices or DEFAULT_SPOT_PRICES
    if isinstance(coin_id_or_meta, dict):
        coin = coin_id_or_meta
    elif isinstance(coin_id_or_meta, str):
        coin = COIN_CATALOG.get(coin_id_or_meta)
    else:
        coin = None
    if not coin:
        return {"has_precious_metal": False, "melt_value_usd": 0.0, "details": "Unknown coin"}

    metal_type = coin.get("metal_type")
    net_oz = coin.get("net_pure_metal_oz", 0.0)

    if metal_type == "paper":
        return {
            "has_precious_metal": False,
            "metal": "Banknote Substrate (Cotton/Polymer)",
            "net_weight_troy_oz": 0.0,
            "melt_value_usd": 0.0,
            "details": "Paper currency (Value is 100% numismatic / collector value)"
        }

    if metal_type == "silver" and net_oz > 0:
        melt = round(net_oz * prices["silver"], 2)
        return {
            "has_precious_metal": True,
            "metal": "Silver (.999 Fine Equivalent)",
            "net_weight_troy_oz": net_oz,
            "spot_price_used": prices["silver"],
            "melt_value_usd": melt,
            "details": f"{net_oz:.4f} oz Silver @ ${prices['silver']:.2f}/oz = ${melt:.2f}"
        }
    elif metal_type == "gold" and net_oz > 0:
        melt = round(net_oz * prices["gold"], 2)
        return {
            "has_precious_metal": True,
            "metal": "Gold",
            "net_weight_troy_oz": net_oz,
            "spot_price_used": prices["gold"],
            "melt_value_usd": melt,
            "details": f"{net_oz:.4f} oz Gold @ ${prices['gold']:.2f}/oz = ${melt:.2f}"
        }
    elif metal_type == "copper":
        # Base copper melt estimate
        weight_lbs = (coin.get("weight_grams", 3.11) * 0.95) / 453.592
        melt = round(weight_lbs * prices.get("copper_per_lb", 4.30), 3)
        return {
            "has_precious_metal": False,
            "metal": "95% Pre-1982 Copper",
            "net_weight_troy_oz": 0.0,
            "melt_value_usd": melt,
            "details": f"Approx. ~${melt:.3f} raw copper metal content"
        }
    elif metal_type == "bronze":
        return {
            "has_precious_metal": False,
            "metal": "Ancient Bronze / Orichalcum",
            "net_weight_troy_oz": 0.0,
            "melt_value_usd": 0.0,
            "details": "Ancient bronze alloy (Value is 100% numismatic / archaeological)"
        }

    return {
        "has_precious_metal": False,
        "metal": "Base Metal (Nickel/Zinc/Clad)",
        "net_weight_troy_oz": 0.0,
        "melt_value_usd": 0.0,
        "details": "No precious metal bullion content (value is numismatic only)"
    }


def find_matching_coin(query: str) -> Optional[Dict[str, Any]]:
    """Smart lookup in the coin catalog based on text or keywords."""
    if not query:
        return None
    q = query.lower().strip()
    
    # 1. Exact ID or exact series name match
    for coin_id, data in COIN_CATALOG.items():
        if coin_id == q or data["name"].lower() == q:
            return data

    # 2. Ancient coin distinctive tokens
    if "denarius" in q or "caesar" in q:
        return COIN_CATALOG["roman_denarius"]
    if "aureus" in q:
        return COIN_CATALOG["roman_aureus"]
    if "sestertius" in q or "sesterce" in q:
        return COIN_CATALOG["roman_sestertius"]
    if "tetradrachm" in q or "owl" in q or "athenian" in q or "athens" in q:
        return COIN_CATALOG["athenian_owl_tetradrachm"]
    if "solidus" in q or "byzantine" in q:
        return COIN_CATALOG["byzantine_solidus"]
    if "widow" in q or "mite" in q or "prutah" in q or "lepton" in q:
        return COIN_CATALOG["widows_mite"]
    if "tyre" in q or "shekel" in q or "30 pieces" in q or "thirty pieces" in q:
        return COIN_CATALOG["shekel_of_tyre"]

    # 3. World coins & bullion distinctive tokens
    if "sovereign" in q:
        return COIN_CATALOG["british_sovereign"]
    if "britannia" in q:
        return COIN_CATALOG["british_britannia"]
    if "libertad" in q:
        return COIN_CATALOG["mexican_silver_libertad"]
    if "centenario" in q or "50 pesos" in q:
        return COIN_CATALOG["mexican_50_pesos_centenario"]
    if "maple" in q:
        if "gold" in q:
            return COIN_CATALOG["canadian_gold_maple_leaf"]
        return COIN_CATALOG["canadian_silver_maple_leaf"]
    if "krugerrand" in q or "kruger" in q:
        return COIN_CATALOG["south_african_krugerrand"]
    if "panda" in q:
        return COIN_CATALOG["chinese_silver_panda"]
    if "philharmonic" in q or "vienna" in q:
        return COIN_CATALOG["austrian_philharmonic"]
    if "kangaroo" in q or "kookaburra" in q or "nugget" in q:
        return COIN_CATALOG["australian_kangaroo"]

    # 4. Banknotes & paper currency
    if any(k in q for k in ("banknote", "paper money", "paper currency", "bill", "certificate", "pmg")):
        return COIN_CATALOG["world_banknote_currency"]

    # 5. US Coins distinctive tokens
    if "peace" in q:
        return COIN_CATALOG["peace_dollar"]
    if "morgan" in q:
        return COIN_CATALOG["morgan_dollar"]
    if "walking" in q:
        return COIN_CATALOG["walking_liberty_half"]
    if "franklin" in q:
        return COIN_CATALOG["franklin_half"]
    if "kennedy" in q:
        return COIN_CATALOG["kennedy_half"]
    if "washington" in q:
        return COIN_CATALOG["washington_quarter"]
    if "mercury" in q:
        return COIN_CATALOG["mercury_dime"]
    if "roosevelt" in q:
        return COIN_CATALOG["roosevelt_dime"]
    if "buffalo" in q:
        return COIN_CATALOG["buffalo_nickel"]
    if "jefferson" in q:
        return COIN_CATALOG["jefferson_nickel"]
    if "wheat" in q:
        return COIN_CATALOG["lincoln_wheat_cent"]
    if "memorial" in q:
        return COIN_CATALOG["lincoln_memorial_cent"]
    if "eagle" in q and "silver" in q:
        return COIN_CATALOG["american_silver_eagle"]
    if "gaudens" in q or "double eagle" in q:
        return COIN_CATALOG["saint_gaudens_double_eagle"]

    # 6. Substring match on full name
    for coin_id, data in COIN_CATALOG.items():
        if data["name"].lower() in q:
            return data

    return None

