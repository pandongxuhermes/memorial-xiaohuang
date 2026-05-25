import os
os.chdir("/tmp/dog-memorial")

import subprocess
subprocess.run(["curl", "-s", "-o", "index.html", "https://pandongxuhermes.github.io/memorial-xiaohuang/"])
html = open("index.html").read()

# Replace each interaction function completely
# offerFlower - already has userStats but missing recordAction + renderLeaderboard
html = html.replace(
'''function offerFlower() {
  counts.flower++;
  document.getElementById('flowerCount').textContent = counts.flower;
  animateFlowers();
  if (myName && !userStats[myName]) userStats[myName] = {flower:0,burn:0,pray:0,total:0};
  if (myName) { userStats[myName].flower++; userStats[myName].total++; }
  addLog('🌷 献上了一束花');
  showToast('🌷 愿天堂开满鲜花');
  saveState();
}''',
'''function offerFlower() {
  counts.flower++;
  document.getElementById('flowerCount').textContent = counts.flower;
  animateFlowers();
  recordAction('flower');
  addLog('🌷 献上了一束花');
  showToast('🌷 愿天堂开满鲜花');
}'''
)

# burnPaper - add recordAction + renderLeaderboard
html = html.replace(
'''function burnPaper() {
  counts.burn++;
  document.getElementById('burnCount').textContent = counts.burn;
  animateAshes();
  addLog('🕯️ 烧纸祭奠');
  showToast('🕯️ 纸钱已送达');
  saveState();
}''',
'''function burnPaper() {
  counts.burn++;
  document.getElementById('burnCount').textContent = counts.burn;
  animateAshes();
  recordAction('burn');
  addLog('🕯️ 烧纸祭奠');
  showToast('🕯️ 纸钱已送达');
}'''
)

# lightIncense - already has recordAction, add renderLeaderboard call
html = html.replace(
'''function lightIncense() {
  counts.incense++;
  document.getElementById('incenseCount').textContent = counts.incense;
  addLog('🙏 上香祈福');
  showToast('🙏 一炷清香，愿离苦得乐');
  recordAction('incense');
  saveState();
}''',
'''function lightIncense() {
  counts.incense++;
  document.getElementById('incenseCount').textContent = counts.incense;
  addLog('🙏 上香祈福');
  showToast('🙏 一炷清香，愿离苦得乐');
  recordAction('incense');
}'''
)

open("index.html","w").write(html)
print("互动函数全部更新完成")
