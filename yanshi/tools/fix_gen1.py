# -*- coding: utf-8 -*-
"""Fix LQ/RQ concatenation issues in gen script."""
import io

p = r'D:\App\Apps\yanshi\tools\gen_jiuyingfalianjun.py'
h = io.open(p, encoding='utf-8').read()

# Replace all LQ/RQ concatenation patterns with unicode escapes
# Pattern 1: " + LQ + "  ->  \u201c
h = h.replace('" + LQ + "', '\\u201c')
# Pattern 2: " + RQ + "  ->  \u201d
h = h.replace('" + RQ + "', '\\u201d')
# Pattern 3: RQ +  (followed by non-quote) -> \u201d"
# These are the buggy cases where text after RQ + is not quoted
import re
h = re.sub(r'RQ \+ ([^"\n])', r'\\u201d"\1', h)

# Also handle LQ at start of concatenation: " + LQ (already handled above)
# Handle trailing: + LQ + " (already handled)

io.open(p, 'w', encoding='utf-8').write(h)
print('Fixed. LQ remaining:', h.count('LQ'), 'RQ remaining:', h.count('RQ'))
