import os
os.chdir("/tmp/dog-memorial")

import subprocess
subprocess.run(["curl", "-s", "-o", "index.html", "https://pandongxuhermes.github.io/memorial-xiaohuang/"])
html = open("index.html").read()

# Direct line-by-line approach - just inject after specific markers

# 1. Add userStats after counts declaration
html = html.replace(
    'let counts = { flower: 0, burn: 0, incense: 0 };',
    'let counts = { flower: 0, burn: 0, incense: 0 };\nlet userStats = {};'
)

# 2. Add recordAction after checkName function
html = html.replace(
    'function checkName(action) {',
    'function recordAction(type) { if (!myName) return; if (!userStats[myName]) userStats[myName] = {flower:0,burn:0,pray:0,total:0}; userStats[myName][type]++; userStats[myName].total++; renderLeaderboard(); }\n\nfunction checkName(action) {'
)

# 3. Add renderLeaderboard function before saveState
html = html.replace(
    'function saveState() {',
    'function renderLeaderboard() { var el = document.getElementById("leaderboard"); if (!el) return; var sorted = Object.entries(userStats||{}).sort(function(a,b){return b[1].total-a[1].total}); if (sorted.length===0) { el.innerHTML = \'<div class="lb-empty">还没有人互动，快来献花吧 🌷</div>\'; return; } el.innerHTML = \'<div class="lb-title">🏆 互动榜单</div>\' + sorted.map(function(n,i){var m=i===0?"🥇":i===1?"🥈":i===2?"🥉":(i+1)+"."; return \'<div class="lb-item"><span class="lb-rank">\'+m+\'</span><span class="lb-name">\'+n[0]+\'</span><span class="lb-stats">🌷\'+(n[1].flower||0)+\' 🕯️\'+(n[1].burn||0)+\' 🕊️\'+(n[1].pray||0)+\' · 共\'+n[1].total+\'次</span></div>\'; }).join(""); }\n\nfunction saveState() {'
)

# 4. Save userStats in saveState
html = html.replace(
    "localStorage.setItem('dogMemorial', JSON.stringify({ counts, logs }));",
    "localStorage.setItem('dogMemorial', JSON.stringify({ counts, logs, userStats: userStats || {} }));"
)

# 5. Restore userStats in loadState
html = html.replace(
    "logs = saved.logs || [];",
    "logs = saved.logs || [];\n      userStats = saved.userStats || {};"
)

# 6. Call renderLeaderboard in loadState
html = html.replace(
    "renderLog();\n    }\n  } catch(e) {}",
    "renderLog();\n      renderLeaderboard();\n    }\n  } catch(e) {}"
)

# 7. Call renderLeaderboard on page load
html = html.replace(
    "if (document.getElementById('gbCurrentName')) document.getElementById('gbCurrentName').textContent = myName || '未设置';",
    "if (document.getElementById('gbCurrentName')) document.getElementById('gbCurrentName').textContent = myName || '未设置';\nrenderLeaderboard();"
)

# 8. Add recordAction calls to each interaction
for func, type_name in [('offerFlower','flower'), ('burnPaper','burn'), ('lightIncense','incense')]:
    old = f"function {func}() {{\n  counts.{type_name}++;\n  document.getElementById('{func.replace('offerFlower','flowerCount').replace('burnPaper','burnCount').replace('lightIncense','incenseCount')}').textContent = counts.{type_name};\n  animateFlowers();\n  addLog"
    new = f"function {func}() {{\n  counts.{type_name}++;\n  document.getElementById('{func.replace('offerFlower','flowerCount').replace('burnPaper','burnCount').replace('lightIncense','incenseCount')}').textContent = counts.{type_name};\n  animateFlowers();\n  recordAction('{type_name}');\n  addLog"
    if old in html:
        html = html.replace(old, new)
        print(f"{func}: ✅")
    else:
        print(f"{func}: ❌ - old text not found")
        # try the saveState version
        old2 = f"function {func}() {{\n  counts.{type_name}++;\n  document.getElementById('{func.replace('offerFlower','flowerCount').replace('burnPaper','burnCount').replace('lightIncense','incenseCount')}').textContent = counts.{type_name};\n  animateFlowers();\n  recordAction('{type_name}');\n  addLog"
        if old2 in html:
            print(f"  already has recordAction")

# 9. Add leaderboard HTML
if '<div id="leaderboard"' not in html:
    html = html.replace(
        '<div class="guestbook">',
        '<div id="leaderboard" class="leaderboard"></div>\n  <div class="guestbook">'
    )

# 10. Add leaderboard CSS
lb_css = """
.leaderboard { margin-bottom:20px; text-align:left; }
.lb-title { font-size:15px; font-weight:600; color:#5a4a3a; margin-bottom:12px; text-align:center; }
.lb-item { display:flex; align-items:center; gap:8px; padding:6px 10px; border-bottom:1px solid rgba(232,213,192,0.2); font-size:13px; }
.lb-rank { width:28px; text-align:center; font-size:14px; }
.lb-name { font-weight:600; color:#5a4a3a; flex:1; }
.lb-stats { color:#8a7a6a; font-size:12px; }
.lb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:14px; }"""

if '.lb-title' not in html:
    html = html.replace(
        '.gb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:20px; }',
        lb_css + '\n.gb-empty { text-align:center; color:#b8a48c; font-size:13px; padding:20px; }'
    )

# Quick pray fix - remove duplicate incense counter
# The pray function shouldn't increment incense

open("index.html","w").write(html)

# Verify
for term in ['userStats', 'renderLeaderboard', 'leaderboard', 'recordAction']:
    print(f"{term}: {'✅' if term in html else '❌'} ({html.count(term)})")
