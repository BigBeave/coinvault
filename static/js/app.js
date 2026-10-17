/**
 * CoinVault iOS App - Core Client Logic
 * Handles camera streaming, photo capture, numismatic analysis,
 * and 1-click eBay listing generation.
 */

// Global State
const state = {
  currentSide: 'obverse', // 'obverse' or 'reverse'
  obverseImage: null,    // base64 data URL
  reverseImage: null,    // base64 data URL
  currentReport: null,
  activeStream: null,
  facingMode: 'environment', // rear camera preferred on iOS
  flashOn: false,
  geminiKey: localStorage.getItem('coinvault_gemini_key') || '',
  ebayToken: localStorage.getItem('coinvault_ebay_token') || '',
  silverSpot: parseFloat(localStorage.getItem('coinvault_silver_spot') || '31.50'),
  operationMode: localStorage.getItem('coinvault_operation_mode') || 'standalone' // 'standalone' (no PC needed) or 'server'
};

// DOM Elements
const video = document.getElementById('cameraVideo');
const shutterBtn = document.getElementById('shutterBtn');
const targetSideBtn = document.getElementById('targetSideBtn');
const targetSideText = document.getElementById('targetSideText');
const targetSideIcon = document.getElementById('targetSideIcon');
const triggerUploadBtn = document.getElementById('triggerUploadBtn');
const fileInput = document.getElementById('fileInput');
const toggleFlashBtn = document.getElementById('toggleFlashBtn');
const switchCameraBtn = document.getElementById('switchCameraBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const photoCanvas = document.getElementById('photoCanvas');
const toastNotice = document.getElementById('toastNotice');
const toastMessage = document.getElementById('toastMessage');
const toastIcon = document.getElementById('toastIcon');

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  initCamera();
  initEventListeners();
  updateModeDisplay();
  loadSampleCoins();
  loadCoinCatalog();
  updateSpotDisplay();
  registerServiceWorker();
});

// Update Mode Display Badge (Standalone vs PC Server)
function updateModeDisplay() {
  const badge = document.getElementById('modeBadge');
  const icon = document.getElementById('modeBadgeIcon');
  const text = document.getElementById('modeBadgeText');
  if (!badge) return;
  if (state.operationMode === 'server') {
    badge.className = 'mode-badge server';
    if (icon) icon.textContent = '🖥️';
    if (text) text.textContent = 'PC Server';
  } else {
    badge.className = 'mode-badge';
    if (icon) icon.textContent = '⚡';
    if (text) text.textContent = 'Standalone';
  }
}

// Register PWA Service Worker
function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js')
      .then(() => console.log('CoinVault Service Worker registered'))
      .catch(err => console.log('Service Worker registration skipped:', err));
  }
}

// Tab Switching
function switchTab(tabId) {
  document.querySelectorAll('.tab-view').forEach(view => {
    view.classList.remove('active');
  });
  document.querySelectorAll('.tab-item').forEach(btn => {
    btn.classList.remove('active');
  });

  const targetView = document.getElementById(tabId);
  if (targetView) targetView.classList.add('active');

  // Highlight tab button
  const indexMap = { tabScan: 0, tabIdentify: 1, tabListing: 2, tabDatabase: 3 };
  const tabBtns = document.querySelectorAll('.tab-item');
  if (tabBtns[indexMap[tabId]]) {
    tabBtns[indexMap[tabId]].classList.add('active');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Camera Management
async function initCamera() {
  const fallbackOverlay = document.getElementById('cameraFallbackOverlay');
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    console.log('getUserMedia not supported, photo upload mode enabled');
    if (fallbackOverlay) fallbackOverlay.classList.remove('hidden');
    return;
  }

  if (state.activeStream) {
    state.activeStream.getTracks().forEach(track => track.stop());
  }

  try {
    const constraints = {
      video: {
        facingMode: state.facingMode,
        width: { ideal: 1280 },
        height: { ideal: 1280 }
      },
      audio: false
    };

    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    state.activeStream = stream;
    video.srcObject = stream;
    await video.play();
    if (fallbackOverlay) fallbackOverlay.classList.add('hidden');
  } catch (err) {
    console.warn('Camera access denied or not available:', err);
    if (fallbackOverlay) fallbackOverlay.classList.remove('hidden');
  }
}

async function toggleFlash() {
  if (!state.activeStream) return;
  const track = state.activeStream.getVideoTracks()[0];
  if (!track) return;

  try {
    const capabilities = track.getCapabilities ? track.getCapabilities() : {};
    if (capabilities.torch) {
      state.flashOn = !state.flashOn;
      await track.applyConstraints({
        advanced: [{ torch: state.flashOn }]
      });
      toggleFlashBtn.style.color = state.flashOn ? '#f59e0b' : '#fff';
      showToast(state.flashOn ? 'Flash turned ON' : 'Flash turned OFF', '⚡');
    } else {
      showToast('Flash/Torch not supported by this device', 'ℹ️');
    }
  } catch (e) {
    showToast('Flashlight unavailable', '⚠️');
  }
}

function switchCamera() {
  state.facingMode = state.facingMode === 'environment' ? 'user' : 'environment';
  initCamera();
  showToast(`Switched to ${state.facingMode === 'environment' ? 'Rear' : 'Front'} Camera`, '🔄');
}

// Capture Photo from Camera Viewfinder or Launch Hardware Camera
function capturePhoto() {
  // If live camera video is not active, trigger native iPhone camera capture
  if (!video.videoWidth || !state.activeStream) {
    const camInput = document.getElementById('cameraInput');
    if (camInput) {
      camInput.click();
      return;
    }
  }

  const ctx = photoCanvas.getContext('2d');
  const size = Math.min(video.videoWidth || 640, video.videoHeight || 640);

  photoCanvas.width = 800;
  photoCanvas.height = 800;

  if (video.videoWidth) {
    // Center crop square to match reticle
    const startX = (video.videoWidth - size) / 2;
    const startY = (video.videoHeight - size) / 2;
    ctx.drawImage(video, startX, startY, size, size, 0, 0, 800, 800);
  }

  const dataUrl = photoCanvas.toDataURL('image/jpeg', 0.85);
  setSidePhoto(state.currentSide, dataUrl);

  // Auto advance side if front captured
  if (state.currentSide === 'obverse' && !state.reverseImage) {
    setTargetSide('reverse');
    showToast('Front captured! Now capture Back (Reverse)', '🦅');
  } else {
    showToast(`${state.currentSide === 'obverse' ? 'Front' : 'Back'} photo captured!`, '📸');
  }
}

// Toggle Target Side (Obverse vs Reverse)
function setTargetSide(side) {
  state.currentSide = side;
  targetSideBtn.dataset.side = side;
  if (side === 'obverse') {
    targetSideText.textContent = 'Front (Obverse)';
    targetSideIcon.textContent = '⚪';
    document.getElementById('reticleLabel').textContent = 'Align Front (Date side)';
  } else {
    targetSideText.textContent = 'Back (Reverse)';
    targetSideIcon.textContent = '🦅';
    document.getElementById('reticleLabel').textContent = 'Align Back (Mintmark)';
  }
}

// Set Photo Data for Side
function setSidePhoto(side, dataUrl) {
  if (side === 'obverse') {
    state.obverseImage = dataUrl;
    document.getElementById('slotObverseEmpty').style.display = 'none';
    document.getElementById('slotObversePreview').style.display = 'block';
    document.getElementById('thumbObverse').src = dataUrl;
    document.getElementById('slotObverse').classList.add('filled');
  } else {
    state.reverseImage = dataUrl;
    document.getElementById('slotReverseEmpty').style.display = 'none';
    document.getElementById('slotReversePreview').style.display = 'block';
    document.getElementById('thumbReverse').src = dataUrl;
    document.getElementById('slotReverse').classList.add('filled');
  }
}

function removeSidePhoto(side) {
  if (side === 'obverse') {
    state.obverseImage = null;
    document.getElementById('slotObverseEmpty').style.display = 'block';
    document.getElementById('slotObversePreview').style.display = 'none';
    document.getElementById('slotObverse').classList.remove('filled');
  } else {
    state.reverseImage = null;
    document.getElementById('slotReverseEmpty').style.display = 'block';
    document.getElementById('slotReversePreview').style.display = 'none';
    document.getElementById('slotReverse').classList.remove('filled');
  }
}

// Handle File Input Upload
function handleFileUpload(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      // Compress and resize
      const maxDim = 1200;
      let width = img.width;
      let height = img.height;
      if (width > maxDim || height > maxDim) {
        if (width > height) {
          height = Math.round((height * maxDim) / width);
          width = maxDim;
        } else {
          width = Math.round((width * maxDim) / height);
          height = maxDim;
        }
      }
      photoCanvas.width = width;
      photoCanvas.height = height;
      const ctx = photoCanvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);
      const compressedDataUrl = photoCanvas.toDataURL('image/jpeg', 0.85);

      setSidePhoto(state.currentSide, compressedDataUrl);
      showToast(`${state.currentSide === 'obverse' ? 'Front' : 'Back'} photo loaded!`, '📁');

      // Auto advance
      if (state.currentSide === 'obverse' && !state.reverseImage) {
        setTargetSide('reverse');
      }
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

// Execute Coin Analysis
async function analyzeCoin(coinHint = '', yearHint = '', mintHint = '') {
  const selectedSeries = document.getElementById('coinSeriesSelect')?.value || '';
  const finalCoinHint = coinHint || selectedSeries;

  if (!state.obverseImage && !state.reverseImage && !finalCoinHint) {
    showToast('Please take or upload a coin photo first!', '⚠️');
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML = `<span>⏳</span> Analyzing Numismatics & Market Data...`;

  // 1. Try PC Server Mode if configured
  if (state.operationMode === 'server') {
    try {
      const payload = {
        obverse_image: state.obverseImage,
        reverse_image: state.reverseImage,
        gemini_api_key: state.geminiKey,
        coin_hint: finalCoinHint,
        year_hint: yearHint,
        mint_hint: mintHint,
        spot_prices: {
          silver: state.silverSpot,
          gold: 2680.00
        }
      };

      const res = await fetch('/api/identify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Analysis request failed');
      const data = await res.json();
      state.currentReport = data;

      renderReport(data);
      switchTab('tabIdentify');
      if (data.ai_identified) {
        showToast(`AI Vision Active: ${data.vision_model || 'Gemini 3.8 Flash'}`, '🎯');
      } else {
        showToast('Identified via Numismatic Catalog Reference!', '📚');
      }
      return;
    } catch (serverErr) {
      console.warn('PC Server endpoint unavailable, falling back to Standalone iOS Engine:', serverErr);
      showToast('PC server unavailable — switched to Standalone Engine ⚡', '🔄');
      state.operationMode = 'standalone';
      localStorage.setItem('coinvault_operation_mode', 'standalone');
      updateModeDisplay();
    }
  }

  // 2. Standalone Client-Side Mode (Runs 100% on iOS without PC)
  try {
    if (!window.CoinVaultEngine) {
      throw new Error('Standalone CoinVaultEngine not loaded');
    }

    let analysisData = null;
    const imagesToAnalyze = [state.obverseImage, state.reverseImage].filter(Boolean);

    // Direct Gemini Vision API call from Safari if API key is provided
    if (imagesToAnalyze.length > 0 && state.geminiKey) {
      analyzeBtn.innerHTML = `<span>🤖</span> Direct Gemini Vision Calling...`;
      try {
        analysisData = await window.CoinVaultEngine.analyzeCoinDirectGemini(imagesToAnalyze, state.geminiKey);
      } catch (geminiErr) {
        console.warn('Direct Gemini Vision call error:', geminiErr);
        showToast('Gemini Vision fallback to on-device catalog', 'ℹ️');
      }
    }

    // Generate comprehensive report with client-side engine
    const report = window.CoinVaultEngine.generateCoinReport({
      analysisData: analysisData,
      coinHint: finalCoinHint,
      yearHint: yearHint,
      mintHint: mintHint,
      obverseUrl: state.obverseImage,
      reverseUrl: state.reverseImage,
      spotPrices: {
        silver: state.silverSpot,
        gold: 2680.00
      }
    });

    state.currentReport = report;
    renderReport(report);
    switchTab('tabIdentify');

    if (report.ai_identified) {
      showToast(`⚡ Direct AI Vision: ${report.vision_model} (No PC needed)`, '🎯');
    } else {
      showToast('⚡ Identified on iOS with Numismatic Engine!', '📚');
    }
  } catch (err) {
    console.error('Error analyzing coin standalone:', err);
    showToast('Error analyzing coin. Please try again.', '❌');
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = `<span>🔍</span> Identify Coin & Check Value`;
  }
}

// Render Coin Analysis Report into Tab 2 and Tab 3
function renderReport(report) {
  document.getElementById('identifyEmpty').style.display = 'none';
  document.getElementById('identifyContent').style.display = 'block';

  // Hero Card
  document.getElementById('heroCoinName').textContent = `${report.year} ${report.coin_name}`;
  document.getElementById('heroSubtitle').textContent = `${report.denomination} • ${report.country}`;
  document.getElementById('heroGrade').textContent = report.estimated_grade;
  document.getElementById('heroMint').textContent = `Mint: ${report.clean_mint || report.mint_mark || 'Philadelphia'}`;
  document.getElementById('heroStrike').textContent = report.strike_type || 'Business Strike';

  // AI Vision Badge
  const aiBadge = document.getElementById('heroAiBadge');
  if (aiBadge) {
    if (report.ai_identified) {
      aiBadge.textContent = `${report.standalone_client_mode ? '⚡ Direct ' : ''}AI Vision: ${report.vision_model || 'Gemini 2.5 Flash'}`;
      aiBadge.className = 'pill pill-green';
    } else {
      aiBadge.textContent = report.standalone_client_mode ? '⚡ Standalone On-Device Catalog' : 'Numismatic Catalog Reference';
      aiBadge.className = 'pill pill-gold';
    }
  }

  // Metrics
  const pricing = report.pricing_estimate || {};
  document.getElementById('metricAvgValue').textContent = `$${(pricing.average || 50).toFixed(2)}`;
  document.getElementById('metricValueRange').textContent = `Range: $${pricing.low || 30} - $${pricing.high || 90}`;

  const melt = report.melt_value || {};
  if (melt.has_precious_metal) {
    document.getElementById('metricMeltValue').textContent = `$${melt.melt_value_usd.toFixed(2)}`;
    document.getElementById('metricMeltDetails').textContent = `${melt.net_weight_troy_oz.toFixed(4)} oz ${melt.metal}`;
  } else {
    document.getElementById('metricMeltValue').textContent = 'Base Metal';
    document.getElementById('metricMeltDetails').textContent = melt.metal;
  }

  // Specifications
  document.getElementById('specComposition').textContent = report.composition;
  document.getElementById('specWeight').textContent = `${report.weight_grams} grams`;
  document.getElementById('specDiameter').textContent = `${report.diameter_mm} mm`;
  document.getElementById('specEdge').textContent = report.edge || 'Reeded';
  document.getElementById('specDesigner').textContent = report.designer || 'US Mint Engraver';

  // High Value Varieties (Crucial Feature)
  const varietiesContainer = document.getElementById('varietiesList');
  varietiesContainer.innerHTML = '';
  const varieties = report.high_dollar_varieties || [];
  if (varieties.length === 0) {
    varietiesContainer.innerHTML = '<p style="color:var(--ios-text-secondary); font-size:12px;">Standard variety. No known ultra-rarities for this specific baseline.</p>';
  } else {
    varieties.forEach(v => {
      const vCard = document.createElement('div');
      vCard.className = 'variety-card';
      vCard.innerHTML = `
        <div class="variety-top">
          <div class="variety-title">${v.date_variety}</div>
          <div class="variety-price">${v.est_value}</div>
        </div>
        <div style="font-size:11px; color:#fbbf24; font-weight:600; margin-bottom:2px;">[${v.rarity_tier}]</div>
        <div class="variety-desc">${v.description}</div>
      `;
      varietiesContainer.appendChild(vCard);
    });
  }

  // Grade Values Table
  const gradeGuide = document.getElementById('gradeGuideContainer');
  gradeGuide.innerHTML = '';
  const grades = report.grade_values_guide || {};
  Object.entries(grades).forEach(([gradeName, valRange]) => {
    const row = document.createElement('div');
    row.style.cssText = 'display:flex; justify-content:space-between; font-size:13px; padding:6px 8px; background:var(--ios-card-sub); border-radius:8px;';
    row.innerHTML = `<span style="font-weight:600;">${gradeName}</span><span style="color:var(--ios-gold); font-weight:700;">${valRange}</span>`;
    gradeGuide.appendChild(row);
  });

  // Collector Advice
  if (report.selling_tips) {
    document.getElementById('collectorAdviceText').textContent = report.selling_tips;
  }

  // Populate Tab 3 Photos Bar
  const obvSlot = document.getElementById('listingThumbObverseSlot');
  const revSlot = document.getElementById('listingThumbReverseSlot');
  if (obvSlot) {
    if (state.obverseImage) {
      obvSlot.innerHTML = `<img src="${state.obverseImage}" alt="Front"><span class="listing-thumb-tag">Front</span>`;
    } else {
      obvSlot.innerHTML = `<span style="font-size:20px;">🪙</span><span class="listing-thumb-tag">Front</span>`;
    }
  }
  if (revSlot) {
    if (state.reverseImage) {
      revSlot.innerHTML = `<img src="${state.reverseImage}" alt="Back"><span class="listing-thumb-tag">Back</span>`;
    } else {
      revSlot.innerHTML = `<span style="font-size:20px;">🦅</span><span class="listing-thumb-tag">Back</span>`;
    }
  }

  // Populate Tab 3: eBay Listing
  const ebay = report.ebay_listing || {};
  const listingTitleInput = document.getElementById('listingTitle');
  listingTitleInput.value = ebay.title || `${report.year} ${report.coin_name} Old US Coin`;
  updateTitleCounter();

  document.getElementById('listingPrice').value = ebay.buy_it_now_price || 49.99;
  document.getElementById('listingBid').value = ebay.starting_bid_price || 29.99;
  document.getElementById('listingCategory').value = ebay.category_name || 'Coins: US';

  const previewBox = document.getElementById('listingHtmlPreview');
  previewBox.innerHTML = ebay.html_description || '';

  // Setup Direct eBay Link
  const ebayLink = document.getElementById('ebayDirectLink');
  ebayLink.href = ebay.prelist_url || `https://www.ebay.com/sl/prelist/suggest?query=${encodeURIComponent(listingTitleInput.value)}`;

  // Populate Mercari
  const mercari = report.mercari_listing || {};
  const mercariTitleInput = document.getElementById('mercariTitle');
  if (mercariTitleInput) mercariTitleInput.value = mercari.title || ebay.title || '';
  const mercariPriceInput = document.getElementById('mercariPrice');
  if (mercariPriceInput) mercariPriceInput.value = mercari.price || ebay.buy_it_now_price || 49.99;
  const mercariDesc = document.getElementById('mercariDescText');
  if (mercariDesc) mercariDesc.value = mercari.description || '';

  // Populate Whatnot
  const whatnot = report.whatnot_listing || {};
  const whatnotTitleInput = document.getElementById('whatnotTitle');
  if (whatnotTitleInput) whatnotTitleInput.value = whatnot.title || ebay.title || '';
  const whatnotBidInput = document.getElementById('whatnotStartingBid');
  if (whatnotBidInput) whatnotBidInput.value = whatnot.starting_bid || ebay.starting_bid_price || 29.99;
  const whatnotBinInput = document.getElementById('whatnotBin');
  if (whatnotBinInput) whatnotBinInput.value = whatnot.buy_it_now_price || ebay.buy_it_now_price || 49.99;
  const whatnotNotes = document.getElementById('whatnotNotes');
  if (whatnotNotes) whatnotNotes.value = whatnot.auction_notes || '';

  // Populate Reddit
  const redditText = document.getElementById('redditPostText');
  if (redditText) redditText.value = report.reddit_listing || '';
}

// Title Character Counter
function updateTitleCounter() {
  const input = document.getElementById('listingTitle');
  const counter = document.getElementById('titleCounter');
  const len = input.value.length;
  counter.textContent = `${len} / 80 characters`;
  counter.style.color = len > 80 ? 'var(--ios-red)' : 'var(--ios-text-secondary)';
}

// Load Pre-configured Sample Coins for 1-Click Testing
async function loadSampleCoins() {
  const container = document.getElementById('samplesContainer');
  if (!container) return;

  let samples = [];
  if (state.operationMode === 'server') {
    try {
      const res = await fetch('/api/sample-coins');
      if (res.ok) {
        const data = await res.json();
        samples = data.samples || [];
      }
    } catch (e) {
      console.log('Server unreachable for sample coins, falling back to local samples');
    }
  }

  if (samples.length === 0 && window.CoinVaultEngine) {
    samples = window.CoinVaultEngine.SAMPLE_COINS;
  }

  container.innerHTML = '';
  samples.forEach(s => {
    const chip = document.createElement('div');
    chip.className = 'sample-chip';
    chip.innerHTML = `
      <div class="sample-icon">🪙</div>
      <div>
        <div class="sample-name">${s.title}</div>
        <div class="sample-val">${s.highlight}</div>
      </div>
    `;
    chip.onclick = () => {
      setSidePhoto('obverse', s.obverse_img);
      setSidePhoto('reverse', s.reverse_img);
      analyzeCoin(s.coin_hint, s.year, s.mint);
    };
    container.appendChild(chip);
  });
}

// Load Coin Encyclopedia Catalog
async function loadCoinCatalog() {
  const container = document.getElementById('catalogList');
  if (!container) return;

  let coins = [];
  if (state.operationMode === 'server') {
    try {
      const res = await fetch('/api/coins');
      if (res.ok) {
        const data = await res.json();
        coins = data.coins || [];
      }
    } catch (e) {
      console.log('Server unreachable for catalog, falling back to local catalog');
    }
  }

  if (coins.length === 0 && window.CoinVaultEngine) {
    const cat = window.CoinVaultEngine.COIN_CATALOG;
    coins = Object.keys(cat).map(cid => {
      const cdata = cat[cid];
      const melt = window.CoinVaultEngine.calculateMeltValue(cid, { silver: state.silverSpot, gold: 2680.00 });
      return {
        id: cid,
        name: cdata.name,
        denomination: cdata.denomination,
        years: cdata.years,
        composition: cdata.composition,
        metal_type: cdata.metal_type,
        melt_value_usd: melt.melt_value_usd || 0.0,
        key_dates_count: (cdata.key_dates_and_varieties || []).length
      };
    });
  }

  container.innerHTML = '';
  coins.forEach(c => {
    const card = document.createElement('div');
    card.className = 'info-card';
    card.style.marginBottom = '8px';
    card.style.cursor = 'pointer';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-weight:700; font-size:15px; color:#fff;">${c.name}</div>
          <div style="font-size:12px; color:var(--ios-text-secondary);">${c.years} &bull; ${c.denomination}</div>
          <div style="font-size:11px; color:var(--ios-gold); margin-top:2px;">Composition: ${c.composition}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:14px; font-weight:800; color:${c.melt_value_usd > 0 ? 'var(--ios-green)' : 'var(--ios-silver)'};">
            ${c.melt_value_usd > 0 ? '$' + c.melt_value_usd.toFixed(2) + ' Melt' : 'Base Metal'}
          </div>
          <div style="font-size:11px; color:var(--ios-blue); font-weight:600; margin-top:4px;">
            ${c.key_dates_count} Key Varieties &rarr;
          </div>
        </div>
      </div>
    `;
    card.onclick = () => {
      analyzeCoin(c.id);
    };
    container.appendChild(card);
  });
}

// Update Spot Display
function updateSpotDisplay() {
  document.getElementById('headerSilverSpot').textContent = `$${state.silverSpot.toFixed(2)}`;
}

// Toast Notification Helper
function showToast(msg, icon = '✅') {
  toastMessage.textContent = msg;
  toastIcon.textContent = icon;
  toastNotice.classList.add('show');
  setTimeout(() => {
    toastNotice.classList.remove('show');
  }, 2800);
}

// Copy to Clipboard Helper
async function copyToClipboard(text, successMsg) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(successMsg, '📋');
  } catch (err) {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast(successMsg, '📋');
  }
}

// Event Listeners Setup
function initEventListeners() {
  // Shutter button
  shutterBtn.addEventListener('click', capturePhoto);

  // Viewfinder standby action buttons
  const vfCaptureBtn = document.getElementById('viewfinderCaptureBtn');
  if (vfCaptureBtn) {
    vfCaptureBtn.addEventListener('click', () => {
      const camInput = document.getElementById('cameraInput');
      if (camInput) camInput.click();
    });
  }

  const vfUploadBtn = document.getElementById('viewfinderUploadBtn');
  if (vfUploadBtn) {
    vfUploadBtn.addEventListener('click', () => fileInput.click());
  }

  // Target side toggle
  targetSideBtn.addEventListener('click', () => {
    setTargetSide(state.currentSide === 'obverse' ? 'reverse' : 'obverse');
  });

  // Camera buttons
  toggleFlashBtn.addEventListener('click', toggleFlash);
  switchCameraBtn.addEventListener('click', switchCamera);

  // Hardware camera input (for iPhone hardware camera)
  const cameraInput = document.getElementById('cameraInput');
  if (cameraInput) {
    cameraInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileUpload(e.target.files[0]);
      }
      cameraInput.value = '';
    });
  }

  // File upload trigger (for Photo Library)
  triggerUploadBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
    fileInput.value = '';
  });

  // Interactive Photo slots
  document.getElementById('slotObverse').addEventListener('click', (e) => {
    if (e.target.closest('#removeObverseBtn')) return;
    setTargetSide('obverse');
    if (!video.videoWidth || !state.activeStream) {
      if (cameraInput) cameraInput.click();
      else fileInput.click();
    } else {
      capturePhoto();
    }
  });

  document.getElementById('slotReverse').addEventListener('click', (e) => {
    if (e.target.closest('#removeReverseBtn')) return;
    setTargetSide('reverse');
    if (!video.videoWidth || !state.activeStream) {
      if (cameraInput) cameraInput.click();
      else fileInput.click();
    } else {
      capturePhoto();
    }
  });

  // Photo slots remove buttons
  document.getElementById('removeObverseBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    removeSidePhoto('obverse');
  });
  document.getElementById('removeReverseBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    removeSidePhoto('reverse');
  });

  // Analyze primary button
  analyzeBtn.addEventListener('click', () => analyzeCoin());

  // Make listing CTA button
  document.getElementById('gotoListingBtn').addEventListener('click', () => {
    switchTab('tabListing');
  });

  // Download Photos for Listing
  const dlPhotosBtn = document.getElementById('downloadPhotosBtn');
  if (dlPhotosBtn) {
    dlPhotosBtn.addEventListener('click', () => {
      const photos = [
        { name: 'obverse.jpg', data: state.obverseImage },
        { name: 'reverse.jpg', data: state.reverseImage }
      ].filter(p => Boolean(p.data));

      if (photos.length === 0) {
        showToast('No photos taken yet to save!', '⚠️');
        return;
      }

      photos.forEach(p => {
        const a = document.createElement('a');
        a.href = p.data;
        a.download = `coinvault_${p.name}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      });
      showToast('Photos saved to your device!', '📥');
    });
  }

  // Multiplatform Segmented Tabs
  document.querySelectorAll('.platform-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.platform-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.platform-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const plat = tab.dataset.platform;
      const targetId = plat === 'ebay' ? 'panelEbay' : plat === 'mercari' ? 'panelMercari' : plat === 'whatnot' ? 'panelWhatnot' : 'panelReddit';
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');
    });
  });

  // Title counter listener
  document.getElementById('listingTitle').addEventListener('input', () => {
    updateTitleCounter();
    const title = document.getElementById('listingTitle').value;
    const cat = state.currentReport?.ebay_listing?.category_id || '';
    document.getElementById('ebayDirectLink').href = `https://www.ebay.com/sl/prelist/suggest?query=${encodeURIComponent(title)}${cat ? '&categoryId=' + cat : ''}`;
  });

  // Copy buttons
  document.getElementById('copyHtmlBtn').addEventListener('click', () => {
    const html = state.currentReport?.ebay_listing?.html_description || document.getElementById('listingHtmlPreview').innerHTML;
    copyToClipboard(html, 'eBay HTML Description Copied!');
  });

  // Mercari Copy Button
  const copyMercariBtn = document.getElementById('copyMercariBtn');
  if (copyMercariBtn) {
    copyMercariBtn.addEventListener('click', () => {
      const title = document.getElementById('mercariTitle').value;
      const price = document.getElementById('mercariPrice').value;
      const desc = document.getElementById('mercariDescText').value;
      const text = `TITLE: ${title}\nPRICE: $${price}\n\nDESCRIPTION:\n${desc}`;
      copyToClipboard(text, 'Mercari Listing Copied!');
    });
  }

  // Whatnot Copy Button
  const copyWhatnotBtn = document.getElementById('copyWhatnotBtn');
  if (copyWhatnotBtn) {
    copyWhatnotBtn.addEventListener('click', () => {
      const title = document.getElementById('whatnotTitle').value;
      const bid = document.getElementById('whatnotStartingBid').value;
      const bin = document.getElementById('whatnotBin').value;
      const notes = document.getElementById('whatnotNotes').value;
      const text = `TITLE: ${title}\nSTARTING BID: $${bid}\nBUY IT NOW: $${bin}\nAUCTION NOTES: ${notes}`;
      copyToClipboard(text, 'Whatnot Auction Card Copied!');
    });
  }

  // Reddit Copy Button
  const copyRedditBtn = document.getElementById('copyRedditBtn');
  if (copyRedditBtn) {
    copyRedditBtn.addEventListener('click', () => {
      const post = document.getElementById('redditPostText').value;
      copyToClipboard(post, 'Reddit Markdown Post Copied!');
    });
  }

  // Direct Publish via eBay API
  document.getElementById('publishEbayApiBtn').addEventListener('click', async () => {
    if (!state.currentReport) {
      showToast('Analyze a coin first', '⚠️');
      return;
    }
    const token = state.ebayToken;
    if (!token) {
      showToast('Please add your eBay User Token in Settings ⚙️ first!', '🔑');
      document.getElementById('settingsModal').classList.add('open');
      return;
    }

    showToast('Creating eBay inventory draft...', '⏳');
    try {
      const res = await fetch('/api/listing/create-draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sku: state.currentReport.ebay_listing.sku,
          title: document.getElementById('listingTitle').value,
          description_html: state.currentReport.ebay_listing.html_description,
          image_urls: [state.obverseImage, state.reverseImage].filter(Boolean),
          category_id: state.currentReport.ebay_listing.category_id || '39464',
          price: parseFloat(document.getElementById('listingPrice').value),
          ebay_token: token
        })
      });
      const result = await res.json();
      if (result.success) {
        showToast('Draft Created in your eBay Inventory!', '🎉');
      } else {
        showToast('eBay API error: ' + (result.error || 'Failed to create'), '❌');
      }
    } catch (e) {
      showToast('No PC/Cloud server connected. Use "Open eBay Web Sell Flow" 1-click button instead!', '📱');
    }
  });

  // Mode Badge Click Listener (Quick Toggle)
  const modeBadge = document.getElementById('modeBadge');
  if (modeBadge) {
    modeBadge.addEventListener('click', () => {
      state.operationMode = state.operationMode === 'standalone' ? 'server' : 'standalone';
      localStorage.setItem('coinvault_operation_mode', state.operationMode);
      updateModeDisplay();
      showToast(state.operationMode === 'standalone' ? 'Switched to Standalone iPhone Mode ⚡ (No PC Needed)' : 'Switched to Local PC Server Mode 🖥️', '🔄');
      loadSampleCoins();
      loadCoinCatalog();
    });
  }

  // Settings Modal Controls
  const settingsModal = document.getElementById('settingsModal');
  document.getElementById('openSettingsBtn').addEventListener('click', () => {
    const opModeSelect = document.getElementById('settingOperationMode');
    if (opModeSelect) opModeSelect.value = state.operationMode;
    document.getElementById('settingGeminiKey').value = state.geminiKey;
    document.getElementById('settingEbayToken').value = state.ebayToken;
    document.getElementById('settingSilverSpot').value = state.silverSpot;
    settingsModal.classList.add('open');
  });

  document.getElementById('closeSettingsBtn').addEventListener('click', () => {
    settingsModal.classList.remove('open');
  });

  document.getElementById('saveSettingsBtn').addEventListener('click', () => {
    const opModeSelect = document.getElementById('settingOperationMode');
    if (opModeSelect) {
      state.operationMode = opModeSelect.value;
      localStorage.setItem('coinvault_operation_mode', state.operationMode);
      updateModeDisplay();
    }
    state.geminiKey = document.getElementById('settingGeminiKey').value.trim();
    state.ebayToken = document.getElementById('settingEbayToken').value.trim();
    state.silverSpot = parseFloat(document.getElementById('settingSilverSpot').value) || 31.50;

    localStorage.setItem('coinvault_gemini_key', state.geminiKey);
    localStorage.setItem('coinvault_ebay_token', state.ebayToken);
    localStorage.setItem('coinvault_silver_spot', state.silverSpot.toString());

    updateSpotDisplay();
    loadSampleCoins();
    loadCoinCatalog();
    settingsModal.classList.remove('open');
    showToast('Settings Saved Successfully!', '⚙️');
  });
}
