#!/bin/bash
cd /www/wwwroot/apps
echo '{"apps":[' > _list.json
first=1
# 只处理 *.html 文件，跳过 lib/ 等目录与辅助文件
for f in *.html; do
  [ "$f" = "index.html" ] && continue
  name=$(grep '<title>' "$f" 2>/dev/null | sed 's/.*<title>\([^<]*\)<\/title>.*/\1/' | head -1)
  [ -z "$name" ] && name="${f%.*}"
  [ $first -eq 1 ] && first=0 || echo ',' >> _list.json
  echo "{\"name\":\"$name\",\"path\":\"./$f\"}" >> _list.json
done
echo ']}' >> _list.json
echo "导航页已更新，共 $(grep -o '"name"' _list.json | wc -l) 个应用"