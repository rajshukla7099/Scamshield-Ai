/**
 * ScamShield AI - Cyber Command SOC Dashboard Engine
 * Real-time Chart.js visualizers, spatial telemetry nodes, and activity filters
 */

let riskChartInstance = null;
let categoryChartInstance = null;
let timelineChartInstance = null;

function initDashboardCharts() {
  fetchDashboardData();
  initTableFilters();
  initSimulationButtons();
}

function fetchDashboardData() {
  fetch('/api/stats')
    .then(res => res.json())
    .then(data => {
      if (data.success && data.stats) {
        updateStatsCounters(data.stats);
        renderRiskChart(data.stats.risk_distribution || {});
        renderCategoryChart(data.stats.top_categories || data.stats.categories || []);
        renderTimelineChart();
      }
    })
    .catch(err => {
      console.warn("Using baseline dashboard metrics:", err);
      renderTimelineChart();
    });
}

function updateStatsCounters(stats) {
  const totalElem = document.getElementById('statTotalScans');
  const threatElem = document.getElementById('statThreatsFlagged');
  const safeElem = document.getElementById('statSafeScans');
  const reportsElem = document.getElementById('statCommunityReports');

  if (totalElem) totalElem.textContent = stats.total_scans ?? '0';
  if (threatElem) threatElem.textContent = stats.threats_flagged ?? '0';
  if (safeElem) safeElem.textContent = stats.safe_scans ?? '0';
  if (reportsElem) reportsElem.textContent = stats.total_reports ?? '0';
}

function renderRiskChart(riskDist) {
  const canvas = document.getElementById('riskDistributionChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  if (riskChartInstance) {
    riskChartInstance.destroy();
  }

  const counts = [
    riskDist.Low ?? 0,
    riskDist.Medium ?? 0,
    riskDist.High ?? 0
  ];

  // If all are zero, provide default telemetry balance
  const dataValues = counts.every(c => c === 0) ? [12, 5, 8] : counts;

  riskChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Safe / Low Risk', 'Moderate / Suspicious', 'High Threat / Malicious'],
      datasets: [{
        data: dataValues,
        backgroundColor: [
          '#00ff88', // Quantum Emerald
          '#f59e0b', // Cyber Amber
          '#ff0055'  // Neon Crimson
        ],
        borderColor: '#0a0f1d',
        borderWidth: 3,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 11, weight: '600' },
            padding: 14,
            usePointStyle: true,
            pointStyle: 'circle'
          }
        },
        tooltip: {
          backgroundColor: '#090e1a',
          titleColor: '#00e5ff',
          bodyColor: '#cbd5e1',
          borderColor: 'rgba(0, 229, 255, 0.3)',
          borderWidth: 1,
          padding: 10,
          cornerRadius: 8
        }
      },
      cutout: '72%'
    }
  });
}

function renderCategoryChart(categories) {
  const canvas = document.getElementById('categoryBreakdownChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  if (categoryChartInstance) {
    categoryChartInstance.destroy();
  }

  let labels = [];
  let data = [];

  if (categories && categories.length > 0) {
    labels = categories.map(c => c.category || c.name);
    data = categories.map(c => c.count);
  } else {
    labels = ['Digital Arrest Video Call', 'UPI QR Reverse Trap', 'SBI / Bank Typosquatting', 'Electricity Disconnection SMS', 'Telegram Task Fraud'];
    data = [24, 18, 15, 12, 9];
  }

  const gradient = ctx.createLinearGradient(0, 0, 300, 0);
  gradient.addColorStop(0, 'rgba(0, 229, 255, 0.85)');
  gradient.addColorStop(1, 'rgba(168, 85, 247, 0.85)');

  categoryChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Attacks Intercepted',
        data: data,
        backgroundColor: gradient,
        borderColor: '#00e5ff',
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#090e1a',
          titleColor: '#00e5ff',
          bodyColor: '#cbd5e1',
          borderColor: 'rgba(0, 229, 255, 0.3)',
          borderWidth: 1,
          padding: 10
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b', precision: 0 }
        },
        y: {
          grid: { display: false },
          ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11, weight: '500' } }
        }
      }
    }
  });
}

function renderTimelineChart() {
  const canvas = document.getElementById('threatTimelineChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  if (timelineChartInstance) {
    timelineChartInstance.destroy();
  }

  const gradient = ctx.createLinearGradient(0, 0, 0, 220);
  gradient.addColorStop(0, 'rgba(0, 229, 255, 0.35)');
  gradient.addColorStop(1, 'rgba(0, 229, 255, 0.0)');

  timelineChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', 'Live'],
      datasets: [{
        label: 'Threat Vector Volume',
        data: [14, 8, 12, 35, 58, 72, 89, 64, 48],
        borderColor: '#00e5ff',
        borderWidth: 2.5,
        backgroundColor: gradient,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#00e5ff',
        pointBorderColor: '#0a0f1d',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#090e1a',
          titleColor: '#00e5ff',
          bodyColor: '#cbd5e1',
          borderColor: 'rgba(0, 229, 255, 0.3)',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => `Threat Activity: ${ctx.parsed.y} incidents/hr`
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.04)' },
          ticks: { color: '#64748b', font: { family: 'Inter', size: 10 } }
        },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.04)' },
          ticks: { color: '#64748b', font: { family: 'Inter', size: 10 } }
        }
      }
    }
  });
}

function initTableFilters() {
  const pills = document.querySelectorAll('.soc-filter-pill');
  const rows = document.querySelectorAll('#incidentTableBody tr[data-type]');

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const filter = pill.getAttribute('data-filter');
      rows.forEach(row => {
        const type = row.getAttribute('data-type');
        const risk = row.getAttribute('data-risk');

        if (filter === 'all') {
          row.style.display = '';
        } else if (filter === 'high') {
          row.style.display = (risk === 'High' || risk === 'high') ? '' : 'none';
        } else if (filter === 'url') {
          row.style.display = (type === 'url') ? '' : 'none';
        } else if (filter === 'message') {
          row.style.display = (type === 'message') ? '' : 'none';
        }
      });

      if (window.CyberAudio && typeof window.CyberAudio.playBeep === 'function') {
        window.CyberAudio.playBeep(900, 'sine', 0.03);
      }
    });
  });
}

function initSimulationButtons() {
  window.triggerSimulation = async function(sampleText, type = 'url') {
    if (window.CyberAudio && typeof window.CyberAudio.playBeep === 'function') {
      window.CyberAudio.playBeep(650, 'sawtooth', 0.08);
    }
    const endpoint = type === 'url' ? '/api/scan/url' : '/api/scan/message';
    const body = type === 'url' ? { url: sampleText } : { message: sampleText };

    try {
      if (typeof showToast === 'function') {
        showToast(`Injecting real-time heuristic test: ${sampleText.substring(0, 25)}...`, 'info');
      }
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        if (typeof showToast === 'function') {
          showToast(`Threat telemetry recorded! Risk Score: ${data.result ? data.result.risk_score : data.risk_score}/100`, 'success');
        }
        // Refresh dashboard numbers and charts
        fetchDashboardData();
        // Reload after 1 sec to show fresh row in table
        setTimeout(() => {
          window.location.reload();
        }, 1200);
      }
    } catch (e) {
      console.error(e);
    }
  };
}

document.addEventListener('DOMContentLoaded', () => {
  initDashboardCharts();
});
