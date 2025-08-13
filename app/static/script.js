let sessionId = null;

const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('input');
const formEl = document.getElementById('form');
const suggestionsEl = document.getElementById('suggestions');
const resetBtn = document.getElementById('resetBtn');

function addMessage(text, who = 'bot') {
  const div = document.createElement('div');
  div.className = `message ${who}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function renderSuggestions(items) {
  suggestionsEl.innerHTML = '';
  if (!items || !items.length) return;
  items.forEach(txt => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'suggestion';
    b.textContent = txt;
    b.addEventListener('click', () => {
      sendMessage(txt);
    });
    suggestionsEl.appendChild(b);
  });
}

async function sendMessage(msg) {
  if (!msg) return;
  addMessage(msg, 'user');
  inputEl.value = '';

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message: msg })
  });
  const data = await res.json();
  sessionId = data.session_id;
  addMessage(data.reply || '', 'bot');
  renderSuggestions(data.suggestions || []);
}

formEl.addEventListener('submit', (e) => {
  e.preventDefault();
  const msg = inputEl.value.trim();
  if (msg.length === 0) return;
  sendMessage(msg);
});

resetBtn.addEventListener('click', () => {
  sendMessage('Сброс');
});

// Автостарт
sendMessage('/start');