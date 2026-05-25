import os, subprocess
os.chdir("/tmp/dog-memorial")
subprocess.run(["curl", "-s", "-o", "index.html", "https://pandongxuhermes.github.io/memorial-xiaohuang/"])
html = open("index.html").read()

# The problem: recordAction() is called but never defined.
# Add the function definition right before checkName

record_action_fn = """function recordAction(type) {
  if (!myName) return;
  if (!userStats[myName]) userStats[myName] = {flower:0,burn:0,pray:0,total:0};
  userStats[myName][type]++;
  userStats[myName].total++;
  saveState();
  renderLeaderboard();
}

function checkName(action) {"""

if "function recordAction" not in html:
    html = html.replace("function checkName(action) {", record_action_fn)
    with open("index.html", "w") as f:
        f.write(html)
    print("✅ recordAction函数已注入")
else:
    print("recordAction已存在")

print(f"recordAction定义: {'✅' if 'function recordAction' in html else '❌'}")
print(f"saveState在recordAction中: {'✅' if 'saveState()' in html[html.find('function recordAction'):html.find('function recordAction')+300] else '❌'}")
