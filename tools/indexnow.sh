#!/bin/sh
# Tell IndexNow search engines (Bing, Yandex, Seznam, Naver; Bing feeds DuckDuckGo and ChatGPT search) that pages changed.
# Run after a deploy has finished: tools/indexnow.sh
KEY=$(cat "$(dirname "$0")/indexnow-key")
URLS=$(grep -o '<url><loc>[^<]*</loc>' "$(dirname "$0")/../site/sitemap.xml" | sed -e 's/<url><loc>//' -e 's/<\/loc>//' | sed 's/.*/"&"/' | paste -sd, -)
curl -s -o /dev/null -w "IndexNow %{http_code}\n" -X POST https://api.indexnow.org/indexnow -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"host\":\"davidslv.photography\",\"key\":\"$KEY\",\"keyLocation\":\"https://davidslv.photography/$KEY.txt\",\"urlList\":[$URLS]}"
