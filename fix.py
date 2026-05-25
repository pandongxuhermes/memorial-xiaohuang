import os
os.chdir("/tmp/dog-memorial")

html = open("index.html").read()

# 在 checkName 中设置昵称后同步更新留言板显示
old = "showToast('✅ 昵称已设置：' + myName);\n    action();"
new = "if (document.getElementById('gbCurrentName')) document.getElementById('gbCurrentName').textContent = myName;\n    showToast('✅ 昵称已设置：' + myName);\n    action();"
html = html.replace(old, new)

# 去掉残留的 gbName 引用（会导致JS报错）
html = html.replace("document.getElementById('gbName').value = ''", "// 昵称已统一管理")

open("index.html","w").write(html)
print("已修复")
