# -*- coding: utf-8 -*-
"""Fix corrupted v5 section in 水调歌头 courseware"""
import re

p = r'D:\App\Apps\yanshi\shuidiaogetou-sushi.html'
with open(p, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the corrupted section: from v4's closing </div> to the 下阕 part-head
# The corrupted section starts after v4's closing and includes the broken v5 fragment
v4_end_marker = '</div>\n        </details>\n      </div>'
v4_pos = html.find('id="v4"')
v4_end = html.find(v4_end_marker, v4_pos) + len(v4_end_marker)

# Find the 下阕 part-head
xiaque_pos = html.find('<div class="part-head"><span class="p-num">下阕</span>')

print(f"v4 end: {v4_end}")
print(f"xiaque: {xiaque_pos}")
print(f"Corrupted section length: {xiaque_pos - v4_end}")
print(f"Corrupted content: {repr(html[v4_end:xiaque_pos][:200])}")

# Correct v5 verse
v5_correct = '''
      <div class="verse" id="v5" data-i="4">
        <div class="v-top"><span class="v-no">5</span><div class="v-line"><span class="anno-word" data-note="移动、转过。此处指月光移动">转</span><span class="anno-word" data-note="朱红色的楼阁。朱，大红色；阁，楼阁">朱阁</span>，<span class="anno-word" data-note="低低地、低垂。此处指月光低照">低</span><span class="anno-word" data-note="（qǐ hù）雕花的窗户。绮，有花纹的丝织品，引申为雕花">绮户</span>，<span class="anno-word" data-note="照射、照耀">照</span><span class="anno-word" data-note="无法入眠的人。眠，睡眠">无眠</span>。</div></div>
        <details class="v-more">
          <summary>译文 · 赏析</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">译　文</b>
              <div class="v-trans">月光转过朱红的楼阁，低低地照进雕花的窗户，照着心事重重、无法入眠的人。</div>
            </div>
            <div class="v-sec"><b class="v-label">赏　析</b>
              <div class="d-body"><p>下阕以写月起笔，“转”“低”“照”三个动词，写出月光的移动轨迹，也暗示时间的流逝。“朱阁”“绮户”，写富贵人家的建筑，与词人“无眠”的清苦形成对照。“照无眠”三字，将月光与人事联系起来——月光本无情，却照着一个因思念而无法入眠的人。此句暗写弟弟苏辙（子由），此时兄弟二人已七年未见，中秋月圆之夜，词人对月怀人，辗转难眠。</p></div>
            </div>
          </div>
        </details>
      </div>
'''

# Replace the corrupted section with correct v5
html = html[:v4_end] + v5_correct + '\n  ' + html[xiaque_pos:]

# Verify verse count
verses = re.findall(r'<div class="verse" id="v\d+"', html)
print(f"\nVerse divs after fix: {len(verses)}")
for v in verses:
    print(f"  {v}")

# Check for any remaining corrupted HTML
corrupted = html.find('class="v\n')
print(f"\nCorrupted 'class=\"v' found: {corrupted}")
corrupted2 = html.find('<<div')
print(f"Corrupted '<<div' found: {corrupted2}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(html)
print("\nDone!")
