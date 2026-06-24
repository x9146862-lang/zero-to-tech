#!/bin/bash
sed -i '' 's|</div>|<button onclick="window.location.href=\x27https://chat.deepseek.com\x27">去 DeepSeek 聊天</button>\n    </div>|' index.html
