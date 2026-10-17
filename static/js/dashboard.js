/**
 * ScamShield AI - Dashboard Analytics with Chart.js
 */

let riskChartInstance = null;
let categoryChartInstance = null;

function initDashboardCharts() {
  const riskCtx = document.getElementById('riskDistributionChart');
  const catCtx = document.getElementById('categoryBreakdownChart');

  if (!riskCtx || !catCtx) return;

  // Read data attributes embedded in canvas or fetch via /api/stats
  fetchDashboardData();
}

function fetchDashboardData() {
  fetch('/api/stats')
    .then(res => res.json())
    .then(data => {
      if (data.success && data.stats) {
        updateStatsCounters(data.stats);
        renderRiskChart(data.stats.risk_distribution);
        renderCategoryChart(data.stats.categories);
      }
    })
    .catch(err => {
      console.error("Failed to load dashboard metrics:", err);
    });
}

function updateStatsCounters(stats) {
  const totalElem = document.getElementById('statTotalScans');
  const threatElem = document.getElementById('statThreatsFlagged');
  const safeElem = document.getElementById('statSafeScans');
  const reportsElem = document.getElementById('statCommunityReports');

  if (totalElem) totalElem.textContent = stats.total_scans;
  if (threatElem) threatElem.textContent = stats.threats_flagged;
  if (safeElem) safeElem.textContent = stats.safe_scans;
  if (reportsElem) reportsElem.textContent = stats.total_reports;
}

function renderRiskChart(riskDist) {
  const ctx = document.getElementById('riskDistributionChart').getContext('2d');
  
  if (riskChartInstance) {
    riskChartInstance.destroy();
  }

  const counts = [
    riskDist.Low || 0,
    riskDist.Medium || 0,
    riskDist.High || 0
  ];

  riskChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Low Risk', 'Medium Risk', 'High Risk'],
      datasets: [{
        data: counts,
        backgroundColor: [
          '#10b981', // Low - emerald
          '#f59e0b', // Medium - amber
          '#ef4444'  // High - red
        ],
        borderColor: '#121e36',
        borderWidth: 3,
        hoverOffset: 6
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
            font: { family: 'Inter', size: 12 },
            padding: 15,
            usePointStyle: true
          }
        },
        tooltip: {
          backgroundColor: '#0d1629',
          titleColor: '#fff',
          bodyColor: '#94a3b8',
          borderColor: '#1e2e4f',
          borderWidth: 1
        }
      },
      cutout: '70%'
    }
  });
}

function renderCategoryChart(categories) {
  const ctx = document.getElementById('categoryBreakdownChart').getContext('2d');

  if (categoryChartInstance) {
    categoryChartInstance.destroy();
  }

  const labels = categories.map(c => c.category);
  const data = categories.map(c => c.count);

  categoryChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Scans Flagged',
        data: data,
        backgroundColor: 'rgba(6, 182, 212, 0.65)',
        borderColor: '#06b6d4',
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y', // Horizontal bars
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0d1629',
          titleColor: '#fff',
          bodyColor: '#94a3b8',
          borderColor: '#1e2e4f',
          borderWidth: 1
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b', precision: 0 }
        },
        y: {
          grid: { display: false },
          ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
        }
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initDashboardCharts();
});
