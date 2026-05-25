import os, re
os.chdir("/tmp/dog-memorial")

import subprocess
subprocess.run(["curl", "-s", "-o", "index.html", "https://pandongxuhermes.github.io/memorial-xiaohuang/"])
html = open("index.html").read()

# 1. 在 saveState 中加入 userStats
html = html.replace(
    "localStorage.setItem('dogMemorial', JSON.stringify({ counts, logs }));",
    "localStorage.setItem('dogMemorial', JSON.stringify({ counts, logs, userStats: userStats || {} }));"
)

# 2. 在 loadState 中加入 userStats
html = html.replace(
    """if (saved) {
      counts = saved.counts || counts;
      logs = saved.logs || [];
      document.getElementById('flowerCount').textContent = counts.flower;""",
    """if (saved) {
      counts = saved.counts || counts;
      logs = saved.logs || [];
      userStats = saved.userStats || {};
      document.getElementById('flowerCount').textContent = counts.flower;"""
)

# 3. 在 loadState 结尾加 renderLeaderboard
html = html.replace(
    "renderLog();\n    }\n  } catch(e) {}\n}",
    "renderLog();\n      renderLeaderboard();\n    }\n  } catch(e) {}\n}"
)

# 4. 在 loadGuestbook 后面加上 renderLeaderboard 初始调用
html = html.replace(
    "if (document.getElementById('gbCurrentName')) document.getElementById('gbCurrentName').textContent = myName || '未设置';",
    "if (document.getElementById('gbCurrentName')) document.getElementById('gbCurrentName').textContent = myName || '未设置';\nrenderLeaderboard();"
)

# 5. 在每个互动函数中加入 recordAction + renderLeaderboard
for func_name in ['offerFlower', 'burnPaper', 'lightIncense']:
    # find saveState() in each function and replace with recordAction
    html = html.replace(
        f"function {func_name}() {{\n  counts.{func_name.replace('offerFlower','flower').replace('burnPaper','burn').replace('lightIncense','incense')}++;\n  document.getElementById('{func_name.replace('offerFlower','flowerCount').replace('burnPaper','burnCount').replace('lightIncense','incenseCount')}').textContent = counts.{func_name.replace('offerFlower','flower').replace('burnPaper','burn').replace('lightIncense','incense')};\n  animateFlowers();\n  addLog",
        f"function {func_name}() {{\n  counts.{func_name.replace('offerFlower','flower').replace('burnPaper','burn').replace('lightIncense','incense')}++;\n  document.getElementById('{func_name.replace('offerFlower','flowerCount').replace('burnPaper','burnCount').replace('lightIncense','incenseCount')}').textContent = counts.{func_name.replace('offerFlower','flower').replace('burnPaper','burn').replace('lightIncense','incense')};\n  animateFlowers();\n  if (myName && !userStats[myName]) userStats[myName] = {{flower:0,burn:0,pray:0,total:0}};\n  if (myName) {{ userStats[myName].{func_name.replace('offerFlower','flower').replace('burnPaper','burn').replace('lightIncense','incense')}++; userStats[myName].total++; }}\n  renderLeaderboard();\n  addLog"
    )

# 6. 插入 leaderboard HTML 和 CSS
if '<div id="leaderboard"' not in html:
    html = html.replace(
        '<div class="guestbook">',
        '<div id="leaderboard" class="leaderboard"></div>\n  <div class="guestbook">'
    )

if '.lb-title' not in html:
    lb_css = '''
.leaderboard { margin-bottom:20px; text-align:left; }
.lb-title { font-size:15px; font-weight:600; color:#5a4a3a; margin-bottom:12px; text-align:center; }
.lb-item { display:flex; align-items:center; gap:8px; padding:6px 10px; border-bottom:1px solid rgba(232,213,192,0.2); font-size:13px; }
.lb-rank { width:28px; text-align:center; font-size:14px; }
.lb-name { font-weight:600; color:#5a4a3a; flex:1; }
.lb-stats { color:#8a7a6a; font-size:12px; }
.lb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:14px; }'''
    html = html.replace('.gb-empty { text-align:center;', lb_css + '\n.gb-empty { text-align:center;')

# 7. 加入 renderLeaderboard 和 recordAction 函数
leaderboard_js = """
function renderLeaderboard() {
  const el = document.getElementById('leaderboard');
  if (!el) return;
  const sorted = Object.entries(userStats || {}).sort((a, b) => b[1].total - a[1].total);
  if (sorted.length === 0) {
    el.innerHTML = '<div class="lb-empty">还没有人互动，快来献花吧 🌷</div>';
    return;
  }
  el.innerHTML = '<div class="lb-title">🏆 互动榜单</div>' +
    sorted.map(([name, s], i) => {
      const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i+1) + '.';
      return '<div class="lb-item"><span class="lb-rank">' + medal + '</span><span class="lb-name">' + name + '</span><span class="lb-stats">🌷' + (s.flower||0) + ' 🕯️' + (s.burn||0) + ' 🕊️' + (s.pray||0) + ' · 共' + s.total + '次</span></div>';
    }).join('');
}
"""

if 'function renderLeaderboard' not in html:
    html = html.replace('function saveState()', leaderboard_js + 'function saveState()')

open("index.html","w").write(html)
print("全面修复完成")
print(f"leaderboard: {'✅' if 'leaderboard' in html else '❌'}")
print(f"userStats: {'✅' if 'userStats' in html else '❌'}")
print(f"renderLeaderboard: {'✅' if 'renderLeaderboard' in html else '❌'}")
