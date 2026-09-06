import re, sys
fp = sys.argv[1]
with open(fp,'r',encoding='utf-8') as f:
    html=f.read()
def extract_div(content, start_marker):
    s = content.find(start_marker)
    idx = s; depth = 0; e = 0
    while idx < len(content):
        if content[idx:idx+5] == '<div ': depth += 1
        elif content[idx:idx+6] == '</div>':
            depth -= 1
            if depth == 0: e = idx+6; break
        idx += 1
    return content[s:e]
ft = extract_div(html, '<div id="fulltext"')
plines = re.findall(r'<div class="pl">(.*?)</div>', ft, re.S)
ft_text = re.sub(r'<[^>]+>', '', ''.join(plines)).strip()
vl = extract_div(html, '<div class="verse-list" id="verseList">')
vlines = re.findall(r'<div class="v-line">(.*?)</div>', vl, re.S)
card_text = re.sub(r'<span class="anno-word"[^>]*>(.*?)</span>', r'\1', ''.join(vlines))
card_text = re.sub(r'<[^>]+>', '', card_text).strip()
print(f"Card: {len(card_text)}, Fulltext: {len(ft_text)}, Match: {card_text == ft_text}")
if card_text != ft_text:
    for i in range(min(len(card_text), len(ft_text))):
        if card_text[i] != ft_text[i]:
            print(f"Diff at {i}: card='{card_text[max(0,i-10):i+10]}' full='{ft_text[max(0,i-10):i+10]}'")
            break
