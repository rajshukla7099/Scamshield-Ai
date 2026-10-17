/**
 * ScamShield AI - Interactive URL Scanner
 */

const SAMPLE_URLS = {
  sbi: "http://sbi-kyc-verification-portal.xyz/login",
  ip: "http://192.168.1.45/paytm-kyc/verify.html",
  tld: "http://indiapost-parcels-track.top/address",
  shortener: "https://bit.ly/free-recharge-bonus-2025",
  legit: "https://onlinesbi.sbi"
};

function fillUrlSample(type) {
  const input = document.getElementById('urlInput');
  if (input && SAMPLE_URLS[type]) {
    input.value = SAMPLE_URLS[type];
    showToast(`Loaded sample URL: ${type.toUpperCase()}`, 'info');
  }
}

function handleUrlScan(e) {
  e.preventDefault();
  const input = document.getElementById('urlInput');
  const url = input.value.trim();

  if (!url) {
    showToast("Please enter a URL to scan", 'error');
    return;
  }

  const submitBtn = document.getElementById('urlScanBtn');
  const spinner = document.getElementById('scanSpinner');
  const resultsCard = document.getElementById('scanResultsCard');

  submitBtn.disabled = true;
  if (spinner) spinner.style.display = 'inline-block';
  if (window.trigger3DLaserSweep) window.trigger3DLaserSweep();

  fetch('/api/scan/url', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url })
  })
  .then(res => res.json())
  .then(data => {
    submitBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';

    if (!data.success) {
      showToast(data.error || "Analysis failed", 'error');
      return;
    }

    if (window.CyberAudio) {
      window.CyberAudio.playAlert(data.result && data.result.risk_level === 'High');
    }

    renderScanResults(data.result, data.summary, data.scan_id);
    if (resultsCard) {
      resultsCard.style.display = 'block';
      resultsCard.scrollIntoView({ behavior: 'smooth' });
    }
  })
  .catch(err => {
    submitBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';
    showToast("Network error while scanning URL", 'error');
    console.error(err);
  });
}

function renderScanResults(result, summary, scanId) {
  const scoreElem = document.getElementById('resultScore');
  const levelBadge = document.getElementById('resultRiskBadge');
  const catElem = document.getElementById('resultCategory');
  const scaleFill = document.getElementById('riskScaleFill');
  const indicatorsContainer = document.getElementById('resultIndicators');
  const recsContainer = document.getElementById('resultRecommendations');
  const fullReportLink = document.getElementById('viewFullReportBtn');
  const disclaimerElem = document.getElementById('resultDisclaimer');

  const riskClass = (result.risk_level || 'low').toLowerCase();

  // Score display
  if (scoreElem) {
    scoreElem.textContent = result.risk_score;
    scoreElem.className = `risk-score-display ${riskClass}`;
  }

  // Level Badge
  if (levelBadge) {
    levelBadge.textContent = `${result.risk_level} Risk`;
    levelBadge.className = `badge-risk ${riskClass}`;
  }

  // Category
  if (catElem) {
    catElem.textContent = result.primary_category;
  }

  // Progress Bar
  if (scaleFill) {
    scaleFill.className = `risk-scale-fill ${riskClass}`;
    scaleFill.style.width = `${result.risk_score}%`;
  }

  // Indicators
  if (indicatorsContainer) {
    indicatorsContainer.innerHTML = '';
    (result.indicators || []).forEach(ind => {
      const sevClass = (ind.severity || 'low').toLowerCase();
      const div = document.createElement('div');
      div.className = `indicator-item ${sevClass}`;
      div.innerHTML = `
        <div class="indicator-item-header">
          <span class="indicator-title">${escapeHtml(ind.title)}</span>
          <span class="badge-risk ${sevClass}">${escapeHtml(ind.severity)}</span>
        </div>
        <p class="indicator-desc">${escapeHtml(ind.desc)}</p>
      `;
      indicatorsContainer.appendChild(div);
    });
  }

  // Recommendations
  if (recsContainer) {
    recsContainer.innerHTML = '';
    (result.recommendations || []).forEach(rec => {
      const li = document.createElement('li');
      li.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>${escapeHtml(rec)}</span>
      `;
      recsContainer.appendChild(li);
    });
  }

  // Disclaimer
  if (disclaimerElem) {
    disclaimerElem.textContent = result.disclaimer;
  }

  // Full Report link
  if (fullReportLink && scanId) {
    fullReportLink.href = `/results/${scanId}`;
    fullReportLink.style.display = 'inline-flex';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('urlScanForm');
  if (form) {
    form.addEventListener('submit', handleUrlScan);
  }
});
