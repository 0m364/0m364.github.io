import re

with open('widget.js', 'r') as f:
    content = f.read()

# Update escapeHtml
content = content.replace('function escapeHtml(unsafe) {\n        return unsafe\n', 'function escapeHtml(unsafe) {\n        return String(unsafe)\n')

# Update line 139
content = content.replace('output.innerHTML += `<span style="color: #0f0;">Connection Established. Successful accesses: ${data.count}</span><br>`;', 'output.innerHTML += `<span style="color: #0f0;">Connection Established. Successful accesses: ${escapeHtml(data.count)}</span><br>`;')

with open('widget.js', 'w') as f:
    f.write(content)
