import os, re
os.chdir("/tmp/dog-memorial")

import subprocess
subprocess.run(["curl", "-s", "-o", "index.html", "https://pandongxuhermes.github.io/memorial-xiaohuang/"])
html = open("index.html").read()

# === 1. 替换JS数据模型：加入用户统计 + 榜单 ===

old_js = """const toast = document.getElementById('toast');
let counts = { flower: 0, burn: 0, incense: 0 };
let logs = [];
let myName = localStorage.getItem('dogVisitorName') || '';"""

new_js = """const toast = document.getElementById('toast');
let counts = { flower: 0, burn: 0, incense: 0 };
let logs = [];
let myName = localStorage.getItem('dogVisitorName') || '';
let userStats = {}; // { '昵称': {flower, burn, pray, total} }

function saveState() {
  localStorage.setItem('dogMemorial', JSON.stringify({ counts, logs, userStats }));
}

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem('dogMemorial'));
    if (saved) {
      counts = saved.counts || counts;
      logs = saved.logs || [];
      userStats = saved.userStats || {};
      document.getElementById('flowerCount').textContent = counts.flower;
      document.getElementById('burnCount').textContent = counts.burn;
      document.getElementById('incenseCount').textContent = counts.incense;
      renderLog();
      renderLeaderboard();
    }
  } catch(e) {}
}

function recordAction(type) {
  if (!myName) return;
  if (!userStats[myName]) userStats[myName] = { flower: 0, burn: 0, pray: 0, total: 0 };
  userStats[myName][type]++;
  userStats[myName].total++;
  if (type === 'pray') type = 'pray'; // 祈福
  saveState();
  renderLeaderboard();
}

function renderLeaderboard() {
  const el = document.getElementById('leaderboard');
  if (!el) return;
  const sorted = Object.entries(userStats).sort((a, b) => b[1].total - a[1].total);
  if (sorted.length === 0) {
    el.innerHTML = '<div class="lb-empty">还没有人互动，快来献花吧 🌷</div>';
    return;
  }
  el.innerHTML = '<div class="lb-title">🏆 互动榜单</div>' +
    sorted.map(([name, stats], i) => {
      const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `${i+1}.`;
      return '<div class="lb-item"><span class="lb-rank">' + medal + '</span><span class="lb-name">' + name + '</span><span class="lb-stats">🌷' + stats.flower + ' 🕯️' + stats.burn + ' 🕊️' + stats.pray + ' · 共' + stats.total + '次</span></div>';
    }).join('');
}"""

html = html.replace(old_js, new_js)

# === 2. 修改各互动函数加入recordAction ===
html = html.replace("""function offerFlower() {
  counts.flower++;
  document.getElementById('flowerCount').textContent = counts.flower;
  animateFlowers();
  addLog('🌷 献上了一束花');
  showToast('🌷 愿天堂开满鲜花');
  saveState();
}""", """function offerFlower() {
  counts.flower++;
  document.getElementById('flowerCount').textContent = counts.flower;
  animateFlowers();
  addLog('🌷 献上了一束花');
  showToast('🌷 愿天堂开满鲜花');
  recordAction('flower');
}""")

html = html.replace("""function burnPaper() {
  counts.burn++;
  document.getElementById('burnCount').textContent = counts.burn;
  animateAshes();
  addLog('🕯️ 烧纸祭奠');
  showToast('🕯️ 纸钱已送达');
  saveState();
}""", """function burnPaper() {
  counts.burn++;
  document.getElementById('burnCount').textContent = counts.burn;
  animateAshes();
  addLog('🕯️ 烧纸祭奠');
  showToast('🕯️ 纸钱已送达');
  recordAction('burn');
}""")

html = html.replace("""function lightIncense() {
  counts.incense++;
  document.getElementById('incenseCount').textContent = counts.incense;
  addLog('🙏 上香祈福');
  showToast('🙏 一炷清香，愿离苦得乐');
  saveState();
}""", """function lightIncense() {
  counts.incense++;
  document.getElementById('incenseCount').textContent = counts.incense;
  addLog('🙏 上香祈福');
  showToast('🙏 一炷清香，愿离苦得乐');
  recordAction('incense');
}""")

html = html.replace("""function pray() {
  const prayers = [""", """function pray() {
  const prayers = [""")

# 修改pray函数 - add recordAction + saveState
old_pray_start = """function pray() {"""
old_pray_end = """  showToast(msg);
}"""

new_pray = """function pray() {
  const prayers = [
    '🕊️ 愿你在汪星自由奔跑',
    '🌟 小黄，一路走好',
    '🌈 彩虹桥上有最好的草地',
    '💛 谢谢你带来的快乐时光',
    '🐾 永远活在我们心里',
    '🏍️ 文卓会一直记得你',
    '☀️ 太平山的阳光会替我爱你',
  ];
  const msg = prayers[Math.floor(Math.random() * prayers.length)];
  counts.incense++;
  document.getElementById('incenseCount').textContent = counts.incense;
  addLog(msg);
  showToast(msg);
  recordAction('pray');
}"""

html = html.replace("""  const prayers = [
    '🕊️ 愿你在汪星自由奔跑',
    '🌟 小黄，一路走好',
    '🌈 彩虹桥上有最好的草地',
    '💛 谢谢你带来的快乐时光',
    '🐾 永远活在我们心里',
    '🏍️ 文卓会一直记得你',
    '☀️ 太平山的阳光会替我爱你',
  ];
  const msg = prayers[Math.floor(Math.random() * prayers.length)];
  counts.incense++;
  document.getElementById('incenseCount').textContent = counts.incense;
  addLog(msg);
  showToast(msg);""", """
  const msg = prayers[Math.floor(Math.random() * prayers.length)];
  addLog(msg);
  showToast(msg);""")

# === 3. 在留言板上方加入榜单 ===
old_gb = '<div class="guestbook">'
new_gb = '<div id="leaderboard" class="leaderboard"></div>\n  <div class="guestbook">'
html = html.replace(old_gb, new_gb)

# === 4. 榜单 CSS ===
new_css = """.leaderboard { margin-bottom:20px; text-align:left; }
.lb-title { font-size:15px; font-weight:600; color:#5a4a3a; margin-bottom:12px; text-align:center; }
.lb-item { display:flex; align-items:center; gap:8px; padding:6px 10px; border-bottom:1px solid rgba(232,213,192,0.2); font-size:13px; }
.lb-rank { width:28px; text-align:center; font-size:14px; }
.lb-name { font-weight:600; color:#5a4a3a; flex:1; }
.lb-stats { color:#8a7a6a; font-size:12px; }
.lb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:14px; }"""

html = html.replace('.gb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:20px; }', '.gb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:20px; }\n' + new_css)

open("index.html","w").write(html)
print("全面更新完成")
