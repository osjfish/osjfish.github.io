#!/bin/bash
cd /www/wwwroot/apps
echo '{"apps":[' > _list.json
first=1
for f in *; do
  [ "$f" = "_list.json" ] || [ "$f" = "index.html" ] || [ "$f" = "build.sh" ] && continue
  name=$(grep '<title>' "$f" 2>/dev/null | sed 's/.*<title>\([^<]*\)<\/title>.*/\1/' | head -1)
  [ -z "$name" ] && name="${f%.*}"
  [ $first -eq 1 ] && first=0 || echo ',' >> _list.json
  echo "{\"name\":\"$name\",\"path\":\"./$f\"}" >> _list.json
done
echo ']}' >> _list.json
echo "导航页已更新，共 $(grep -o '"name"' _list.json | wc -l) 个应用"