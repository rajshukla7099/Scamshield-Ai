/**
 * ScamShield AI - Scam Message Analyzer & Text Highlighter
 */

const SAMPLE_MESSAGES = {
  electricity: "Dear Consumer, Aapka bijli connection aaj raat 9:30 baje kat diya jayega kyunki pichle mahine ka bill update nahi hua. Turant electricity officer Rahul Sharma se 9876543210 par sampark kare.",
  digital_arrest: "CRITICAL NOTICE: You are placed under Digital Arrest by CBI Cyber Crime Cell regarding an illegal FedEx parcel containing narcotics. Join Skype video call immediately and transfer ₹2,50,000 to RBI escrow account for verification.",
  wfh_job: "Congratulations! Work from home part-time job. Ghar baithe daily 2000 se 5000 kamaye just by liking YouTube videos and rating hotels. Join Telegram VIP HR Manager: https://t.me/vip_parttime_jobs",
  upi_fraud: "Buyer: Sir, I have sent payment of ₹4,500. Please scan this PhonePe QR code and enter your UPI PIN to receive money into your bank account immediately.",
  lottery: "Congratulations! Your mobile number won ₹25,00,000 in KBC Lucky Draw 2025. Contact lottery manager to claim prize before deadline tonight.",
  legit_bank: "ICICI Bank Alert: A debit of ₹1,499 was processed on your account. If this was not authorized by you, lock your debit card via iMobile app or call the 24x7 customer care number printed on your physical card. Never share your OTP with anyone."
};

function fillMessageSample(type) {
  const textarea = document.getElementById('messageInput');
  if (textarea && SAMPLE_MESSAGES[type]) {
    textarea.value = SAMPLE_MESSAGES[type];
    showToast(`Loaded sample: ${type.replace('_', ' ').toUpperCase()}`, 'info');
  }
}

function handleMessageScan(e) {
  e.preventDefault();
  const textarea = document.getElementById('messageInput');
  const message = textarea.value.trim();

  if (!message) {
    showToast("Please paste or type a message to analyze", 'error');
    return;
  }

  const submitBtn = document.getElementById('msgScanBtn');
  const spinner = document.getElementById('msgSpinner');
  const resultsCard = document.getElementById('msgResultsCard');

  submitBtn.disabled = true;
  if (spinner) spinner.style.display = 'inline-block';

  fetch('/api/scan/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: message })
  })
  .then(res => res.json())
  .then(data => {
    submitBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';

    if (!data.success) {
      showToast(data.error || "Analysis failed", 'error');
      return;
    }

    renderMessageResults(message, data.result, data.summary, data.scan_id);
    if (resultsCard) {
      resultsCard.style.display = 'block';
      resultsCard.scrollIntoView({ behavior: 'smooth' });
    }
  })
  .catch(err => {
    submitBtn.disabled = false;
    if (spinner) spinner.style.display = 'none';
    showToast("Network error while analyzing message", 'error');
    console.error(err);
  });
}

function renderMessageResults(originalText, result, summary, scanId) {
  const scoreElem = document.getElementById('msgResultScore');
  const levelBadge = document.getElementById('msgResultRiskBadge');
  const catElem = document.getElementById('msgResultCategory');
  const scaleFill = document.getElementById('msgRiskScaleFill');
  const annotatedContainer = document.getElementById('msgAnnotatedText');
  const indicatorsContainer = document.getElementById('msgResultIndicators');
  const recsContainer = document.getElementById('msgResultRecommendations');
  const fullReportLink = document.getElementById('msgViewFullReportBtn');
  const disclaimerElem = document.getElementById('msgResultDisclaimer');

  const riskClass = (result.risk_level || 'low').toLowerCase();

  // Score
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

  // Scale fill
  if (scaleFill) {
    scaleFill.className = `risk-scale-fill ${riskClass}`;
    scaleFill.style.width = `${result.risk_score}%`;
  }

  // Annotated Highlighted Text
  if (annotatedContainer) {
    annotatedContainer.innerHTML = buildHighlightedHtml(originalText, result.highlighted_spans || []);
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

/**
 * Builds HTML with highlighted spans from character offsets
 */
function buildHighlightedHtml(text, spans) {
  if (!spans || spans.length === 0) {
    return escapeHtml(text);
  }

  // Sort spans by start index
  const sorted = [...spans].sort((a, b) => a.start - b.start);

  // Filter overlapping spans
  const nonOverlapping = [];
  let lastEnd = 0;
  for (const s of sorted) {
    if (s.start >= lastEnd) {
      nonOverlapping.push(s);
      lastEnd = s.end;
    }
  }

  let html = '';
  let cursor = 0;

  for (const span of nonOverlapping) {
    if (span.start > cursor) {
      html += escapeHtml(text.substring(cursor, span.start));
    }
    const matchedText = text.substring(span.start, span.end);
    html += `<span class="highlight-threat" title="${escapeHtml(span.category)}: Flagged phrase">${escapeHtml(matchedText)}</span>`;
    cursor = span.end;
  }

  if (cursor < text.length) {
    html += escapeHtml(text.substring(cursor));
  }

  return html;
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('messageScanForm');
  if (form) {
    form.addEventListener('submit', handleMessageScan);
  }
});
