import os, re
os.chdir("/tmp/dog-memorial")

import urllib.request
with urllib.request.urlopen("https://pandongxuhermes.github.io/memorial-xiaohuang/") as r:
    html = r.read().decode()

# Replace the old submitMsg that reads from gbName input
old = """function submitMsg() {
  const name = document.getElementById('gbName').value.trim();
  const msg = document.getElementById('gbMsg').value.trim();
  if (!name) { showToast('⚠️ 请留下昵称'); return; }
  if (!msg) { showToast('⚠️ 请输入留言内容'); return; }
  const now = new Date();
  const time = now.toLocaleString('zh-CN', {month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit'});
  guestbook.unshift({ name, msg, time });
  saveGuestbook();
  renderGuestbook();
  document.getElementById('gbName').value = '';
  document.getElementById('gbMsg').value = '';
  showToast('✅ 留言已发布');
}"""

new = """function submitMsg() {
  if (!myName) {
    const n = prompt('请先输入你的昵称：');
    if (n && n.trim()) { myName = n.trim(); localStorage.setItem('dogVisitorName', myName); }
    else { showToast('⚠️ 请填写昵称'); return; }
  }
  const msg = document.getElementById('gbMsg').value.trim();
  if (!msg) { showToast('⚠️ 请输入留言内容'); return; }
  const now = new Date();
  const time = now.toLocaleString('zh-CN', {month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit'});
  guestbook.unshift({ name: myName, msg, time });
  saveGuestbook();
  renderGuestbook();
  document.getElementById('gbMsg').value = '';
  if (document.getElementById('gbCurrentName')) document.getElementById('gbCurrentName').textContent = myName;
  showToast('✅ 留言已发布');
}"""

if old in html:
    html = html.replace(old, new)
    print("替换成功")
    with open("index.html", "w") as f:
        f.write(html)
else:
    print("未完全匹配")
    # try fuzzy match
    idx = html.find("function submitMsg")
    if idx >= 0:
        end = html.find("\n}\n", idx)
        print("Found at", idx, "to", end)
        print(repr(html[idx:end+3]))
