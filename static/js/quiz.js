/**
 * ScamShield AI - Interactive Scam Academy Quiz Engine
 */

let quizData = [];
let currentIndex = 0;
let userScore = 0;
let userStreak = 0;
let answeredQuestions = new Set();

function initQuizEngine(quizzes) {
  quizData = quizzes || [];
  currentIndex = 0;
  userScore = 0;
  userStreak = 0;
  answeredQuestions.clear();

  if (quizData.length === 0) {
    fetch('/api/quizzes')
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          quizData = d.quizzes;
          renderCurrentQuestion();
        }
      });
  } else {
    renderCurrentQuestion();
  }
}

function renderCurrentQuestion() {
  const container = document.getElementById('quizCardContainer');
  if (!container || quizData.length === 0) return;

  const q = quizData[currentIndex];
  const progressPercent = Math.round(((currentIndex) / quizData.length) * 100);

  // Update progress bar & counters
  const progressBar = document.getElementById('quizProgressBar');
  if (progressBar) progressBar.style.width = `${progressPercent}%`;

  const qCountElem = document.getElementById('quizCounter');
  if (qCountElem) qCountElem.textContent = `Scenario ${currentIndex + 1} of ${quizData.length}`;

  const scoreElem = document.getElementById('quizScoreDisplay');
  if (scoreElem) scoreElem.textContent = `Score: ${userScore} pts`;

  container.innerHTML = `
    <div class="cyber-card" style="margin-top: 1rem;">
      <div class="cyber-card-header">
        <div class="card-title-group">
          <span class="badge-risk medium">${escapeHtml(q.source_type)}</span>
          <span class="card-title">${escapeHtml(q.title)}</span>
        </div>
        <span class="badge-risk low">${escapeHtml(q.difficulty)}</span>
      </div>

      <div style="background: var(--bg-input); border: 1px solid var(--border-color); padding: 1.25rem; border-radius: var(--radius-md); font-size: 0.95rem; line-height: 1.6; color: #fff; margin-bottom: 1.5rem;">
        "${escapeHtml(q.scenario_text)}"
      </div>

      <div id="quizActionButtons" style="display: flex; gap: 1rem; margin-bottom: 1.25rem;">
        <button class="btn btn-danger" style="flex: 1;" onclick="submitAnswer(true)">
          🚨 Potential Scam
        </button>
        <button class="btn btn-secondary" style="flex: 1;" onclick="submitAnswer(false)">
          🛡️ Legitimate Message
        </button>
      </div>

      <div id="quizFeedbackArea" style="display: none;"></div>
    </div>
  `;
}

function submitAnswer(userGuess) {
  const q = quizData[currentIndex];
  const isCorrect = (userGuess === q.is_scam);

  if (isCorrect) {
    userScore += 10;
    userStreak += 1;
    showToast("Correct! Excellent detection. (+10 pts)", 'success');
  } else {
    userStreak = 0;
    showToast("Incorrect! Check the red flags below.", 'error');
  }

  // Render Feedback
  const actions = document.getElementById('quizActionButtons');
  if (actions) actions.style.display = 'none';

  const feedback = document.getElementById('quizFeedbackArea');
  if (feedback) {
    feedback.style.display = 'block';

    let flagsHtml = '';
    (q.red_flags || []).forEach(f => {
      flagsHtml += `<li style="display: flex; align-items: flex-start; gap: 0.5rem; font-size: 0.85rem; color: #f1f5f9; margin-bottom: 0.4rem;">
        <span style="color: var(--accent-cyan);">⚠️</span> <span>${escapeHtml(f)}</span>
      </li>`;
    });

    feedback.innerHTML = `
      <div style="background: ${isCorrect ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'}; border: 1px solid ${isCorrect ? 'var(--risk-low)' : 'var(--risk-high)'}; border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 1.25rem;">
        <h4 style="color: ${isCorrect ? 'var(--risk-low)' : 'var(--risk-high)'}; font-size: 1.05rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
          ${isCorrect ? '✅ Well Done! You Spotted It' : '❌ Watch Out! This Was A Threat'}
        </h4>
        <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 0.75rem;">
          ${escapeHtml(q.explanation)}
        </p>
        <ul style="list-style: none; margin-top: 0.5rem;">
          ${flagsHtml}
        </ul>
      </div>

      <div style="display: flex; justify-content: flex-end;">
        <button class="btn btn-primary" onclick="nextQuestion()">
          ${currentIndex + 1 < quizData.length ? 'Next Scenario ➔' : 'Complete Quiz 🏆'}
        </button>
      </div>
    `;
  }
}

function nextQuestion() {
  currentIndex++;
  if (currentIndex < quizData.length) {
    renderCurrentQuestion();
  } else {
    renderQuizSummary();
  }
}

function renderQuizSummary() {
  const container = document.getElementById('quizCardContainer');
  if (!container) return;

  const progressBar = document.getElementById('quizProgressBar');
  if (progressBar) progressBar.style.width = '100%';

  let badgeTitle = "Cyber Apprentice 🛡️";
  let badgeDesc = "Good start! Keep practicing to identify advanced phishing patterns.";
  if (userScore >= 50) {
    badgeTitle = "Master Cyber Guardian ⚔️";
    badgeDesc = "Elite cyber awareness! You successfully detected virtually all deception vectors.";
  } else if (userScore >= 30) {
    badgeTitle = "Phishing Investigator 🕵️";
    badgeDesc = "Solid security instincts! You can easily spot urgent social engineering traps.";
  }

  container.innerHTML = `
    <div class="cyber-card" style="text-align: center; padding: 3rem 1.5rem;">
      <div style="font-size: 4rem; margin-bottom: 1rem;">🏆</div>
      <h2 style="font-size: 1.8rem; color: #fff; margin-bottom: 0.5rem;">Academy Training Completed!</h2>
      <p style="color: var(--text-muted); margin-bottom: 1.5rem;">You scored <strong>${userScore} / ${quizData.length * 10}</strong> points.</p>

      <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid var(--accent-cyan); border-radius: var(--radius-lg); padding: 1.5rem; max-width: 450px; margin: 0 auto 2rem auto;">
        <span style="font-size: 0.75rem; color: var(--accent-cyan); text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Awarded Cyber Badge</span>
        <h3 style="font-size: 1.35rem; color: #fff; margin: 0.4rem 0;">${badgeTitle}</h3>
        <p style="font-size: 0.85rem; color: var(--text-muted);">${badgeDesc}</p>
      </div>

      <button class="btn btn-primary" onclick="initQuizEngine(quizData)">
        🔄 Practice Again
      </button>
    </div>
  `;
}

function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
