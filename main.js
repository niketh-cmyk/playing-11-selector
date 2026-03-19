const bodyEl  = document.getElementById('body');
const chatEl  = document.getElementById('chat');
const inputEl = document.getElementById('xi-input');
const heroEl  = document.getElementById('hero');
const gridEl  = document.getElementById('grid');
let heroHidden = false;
 
function scrollToBottom() { 
  setTimeout(() => { bodyEl.scrollTop = bodyEl.scrollHeight; }, 50);
}
 
function hideHero() {
  if (!heroHidden) {
    heroEl.style.transition = 'opacity 0.3s, max-height 0.4s, margin 0.4s';
    heroEl.style.opacity    = '0';
    heroEl.style.maxHeight  = '0';
    heroEl.style.overflow   = 'hidden';
    heroEl.style.marginBottom = '0';
 
    gridEl.style.transition = 'opacity 0.3s, max-height 0.4s, margin 0.4s';
    gridEl.style.opacity    = '0';
    gridEl.style.maxHeight  = '0';
    gridEl.style.overflow   = 'hidden';
    gridEl.style.marginBottom = '0';
 
    heroHidden = true;
  }
}
 
function addMessage(text, isUser) {
  hideHero();
 
  const msg = document.createElement('div');
  msg.className = 'msg ' + (isUser ? 'user' : 'bot');
 
  const av = document.createElement('div');
  av.className = 'avatar ' + (isUser ? 'user' : 'bot');
  av.textContent = isUser ? 'U' : '🏏';
 
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
 
  msg.appendChild(av);
  msg.appendChild(bubble);
  chatEl.appendChild(msg);
 
  if (!isUser) {
    const actions = document.createElement('div');
    actions.className = 'msg-actions';
    const safeText = text.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
    actions.innerHTML = `
      <button onclick="copyMsg(this, \`${safeText}\`)">&#8855; Copy</button>
      <button onclick="this.textContent='👍 Thanks!'">👍</button>
      <button onclick="this.textContent='👎 Noted'">👎</button>
    `;
    chatEl.appendChild(actions);
  }
  scrollToBottom();
}
 
function showTyping() {
  hideHero();
  const row = document.createElement('div');
  row.className = 'msg bot';
  row.id = 'typing';
  row.innerHTML = `
    <div class="avatar bot">🏏</div>
    <div class="typing-bubble">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>`;
  chatEl.appendChild(row);
  scrollToBottom();
}
 
function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}
 
function copyMsg(btn, text) {
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = '✓ Copied!';
    setTimeout(() => { btn.textContent = '⊡ Copy'; }, 1800);
  });
}
 
async function quickSelect(type) {
  const labels = {
    bowlers:      'Show me bowler options',
    batsmen:      'Show me batsman options',
    allrounders:  'Suggest all-rounders',
    wicketkeepers:'Best wicket-keepers?'
  };
  addMessage(labels[type], true);
  showTyping();
 
  try {
    const res  = await fetch('/quick', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: type })
    });
    const data = await res.json();
    removeTyping();
    addMessage(data.reply, false);
  } catch (err) {
    removeTyping();
    addMessage('Error connecting to server. Please try again.', false);
  }
}
 
async function sendMessage() {
  const val = inputEl.value.trim();
  if (!val) return;
 
  addMessage(val, true);
  inputEl.value = '';
  showTyping();
 
  try {
    const res  = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: val })
    });
    const data = await res.json();
    removeTyping();
    addMessage(data.reply, false);
  } catch (err) {
    removeTyping();
    addMessage('Error connecting to server. Please try again.', false);
  }
}
 
function handleKey(e) {
  if (e.key === 'Enter') sendMessage();
}
 
function newChat() {
  chatEl.innerHTML   = '';
  heroEl.style.cssText = '';
  gridEl.style.cssText = '';
  heroHidden         = false;
  inputEl.value      = '';
  bodyEl.scrollTop   = 0;
}
 
function shareChat() {
  navigator.clipboard.writeText(window.location.href)
    .then(()  => alert('Link copied!'))
    .catch(()  => alert('Playing XI Selector — share this page!'));
}
 