/**
 * ScamShield AI - Master Global App Scripts
 */

// Mobile Navigation Toggle
function initNavigation() {
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const sidebar = document.getElementById('appSidebar');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target) && sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
      }
    });
  }
}

// Toast Notification System
function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  let icon = 'ℹ️';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '⚠️';

  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Copy to Clipboard Helper
function copyToClipboard(text, successMsg = "Copied to clipboard!") {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg, 'success');
    }).catch(() => {
      fallbackCopy(text, successMsg);
    });
  } else {
    fallbackCopy(text, successMsg);
  }
}

function fallbackCopy(text, successMsg) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    showToast(successMsg, 'success');
  } catch (err) {
    showToast("Failed to copy", 'error');
  }
  document.body.removeChild(textArea);
}

// Presentation Modal Controller
function openPresentationModal() {
  const modal = document.getElementById('presentationModal');
  if (modal) modal.classList.add('active');
}

function closePresentationModal() {
  const modal = document.getElementById('presentationModal');
  if (modal) modal.classList.remove('active');
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();

  // Close modals on overlay click
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
      }
    });
  });
});

// =====================================================================
// ShieldBot AI 24/7 Cyber Defense Assistant Controller
// =====================================================================

function toggleShieldChat() {
  const chatWindow = document.getElementById('shieldChatWindow');
  if (!chatWindow) return;

  const isActive = chatWindow.classList.toggle('active');
  if (isActive) {
    const input = document.getElementById('chatInput');
    if (input) input.focus();
    if (window.CyberAudio && typeof window.CyberAudio.playBeep === 'function') {
      window.CyberAudio.playBeep(750, 'sine', 0.05);
    }
  }
}

function sendQuickChat(query) {
  const chatWindow = document.getElementById('shieldChatWindow');
  if (chatWindow && !chatWindow.classList.contains('active')) {
    chatWindow.classList.add('active');
  }
  const input = document.getElementById('chatInput');
  if (input) {
    input.value = query;
    handleSendChat(new Event('submit'));
  }
}

async function handleSendChat(event) {
  if (event && event.preventDefault) event.preventDefault();

  const input = document.getElementById('chatInput');
  const container = document.getElementById('chatMessages');
  if (!input || !container) return;

  const userText = input.value.trim();
  if (!userText) return;

  input.value = '';

  // Append user message
  const userMsgEl = document.createElement('div');
  userMsgEl.className = 'chat-msg user';
  userMsgEl.textContent = userText;
  container.appendChild(userMsgEl);
  container.scrollTop = container.scrollHeight;

  // Append typing indicator
  const typingEl = document.createElement('div');
  typingEl.className = 'chat-msg bot';
  typingEl.id = 'botTyping';
  typingEl.innerHTML = `<span style="font-size: 0.8rem; color: var(--accent-cyan); display: inline-flex; align-items: center; gap: 6px;">
    <span class="pulse-dot" style="width: 6px; height: 6px; background: var(--accent-cyan);"></span>
    Analyzing cyber threat database...
  </span>`;
  container.appendChild(typingEl);
  container.scrollTop = container.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText })
    });
    const data = await res.json();
    typingEl.remove();

    const botMsgEl = document.createElement('div');
    botMsgEl.className = 'chat-msg bot';

    if (data.success && data.response) {
      const resp = data.response;
      let html = '';
      if (resp.title) {
        html += `<div style="font-weight: 700; color: #fff; margin-bottom: 6px; font-size: 0.88rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 4px;">${escapeHtml(resp.title)}</div>`;
      }
      html += `<div>${formatChatMarkdown(resp.reply)}</div>`;

      if (resp.quick_actions && resp.quick_actions.length > 0) {
        html += `<div class="chat-quick-actions" style="margin-top: 10px;">`;
        resp.quick_actions.forEach(action => {
          if (action.url) {
            html += `<a href="${escapeHtml(action.url)}" class="chat-action-btn" style="text-decoration:none; display:inline-flex; align-items:center;">${escapeHtml(action.label)}</a>`;
          } else if (action.query) {
            const safeQuery = action.query.replace(/'/g, "\\'");
            html += `<button type="button" class="chat-action-btn" onclick="sendQuickChat('${safeQuery}')">${escapeHtml(action.label)}</button>`;
          } else if (action.action === 'show_helplines') {
            html += `<button type="button" class="chat-action-btn" onclick="sendQuickChat('national cyber helpline numbers')">${escapeHtml(action.label)}</button>`;
          }
        });
        html += `</div>`;
      }

      botMsgEl.innerHTML = html;
      if (window.CyberAudio && typeof window.CyberAudio.playBeep === 'function') {
        window.CyberAudio.playBeep(880, 'sine', 0.05);
      }
    } else {
      botMsgEl.innerHTML = `<span style="color: var(--accent-red);">Error analyzing query. Emergency? Call 1930 directly.</span>`;
    }

    container.appendChild(botMsgEl);
    container.scrollTop = container.scrollHeight;
  } catch (err) {
    if (typingEl) typingEl.remove();
    const errorMsgEl = document.createElement('div');
    errorMsgEl.className = 'chat-msg bot';
    errorMsgEl.innerHTML = `<span style="color: var(--accent-red);">Network error connecting to defense node. Immediate emergency: Dial <strong>1930</strong> or visit <a href="https://cybercrime.gov.in" target="_blank" style="color:var(--accent-cyan);">cybercrime.gov.in</a>.</span>`;
    container.appendChild(errorMsgEl);
    container.scrollTop = container.scrollHeight;
  }
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatChatMarkdown(text) {
  if (!text) return '';
  // Convert markdown links [Label](url) safely
  let formatted = escapeHtml(text)
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color: var(--accent-cyan); text-decoration: underline;">$1</a>')
    .replace(/\*\*(.*?)\*\*/g, '<strong style="color: #fff;">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/•\s/g, '•&nbsp;')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>');
  return formatted;
}
