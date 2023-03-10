import os
import sys
import time

def pprint(x, y, text):
     sys.stdout.write(f"\x1b7\x1b[{x};{y}f{text}\x1b8")
     sys.stdout.flush()
# ┌─┐│ │└─┘
ts = os.get_terminal_size()
print(chr(27) + "[2J")
while True:
    time.sleep(1/20)
    # Clear screen on resize
    if ts != os.get_terminal_size():
        ts = os.get_terminal_size()
        print(chr(27) + "[2J")

    # Center text
    texts = [
        'Load Game  ( l )',
        'New Game   ( n )',
        'Settings   ( s )',
        'Help       ( h )',
        'Quit       ( q )'
    ]
    padding = round(ts.lines*(2/3))-len(texts)//2
    for i, text in enumerate(texts):
        pprint(padding+i, ts.columns//2-len(text)//2, text)

    # Sheltero title
    title = (' '*(ts.columns//20)).join('sheltero')
    pprint(ts.lines//5, ts.columns//2-len(title)//2, title)

    # Email
    email = 'hervus.code@gmail.com'
    pprint(ts.lines//3-1, ts.columns-(len(email)+1), email)

    ## BORDERS
    # 1/3 border
    pprint(ts.lines//3, 0, '#'*ts.columns)
    # Top border
    pprint(0, 0, '#'*ts.columns)
    # Bottom border
    pprint(ts.lines, 0, '#'*ts.columns)
    for line in range(ts.lines):
        # Left border
        pprint(line, 0, '#')
        # Right border
        pprint(line, ts.columns, '#')
