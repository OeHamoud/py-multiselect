import sys, tty, termios

# ── Customise here ──────────────────────────────────────────────────────────

CHECKED   = "[*]"          # checked item symbol
UNCHECKED = "[ ]"          # unchecked item symbol
POINTER   = "❯"            # cursor pointer symbol

COLOR_POINTER  = "\033[96m"   # cyan  – active row
COLOR_CHECKED  = "\033[92m"   # green – checked mark
COLOR_HINT     = "\033[2m"    # dim   – footer hint
RESET          = "\033[0m"

KEYS_UP     = {"UP", "k"}
KEYS_DOWN   = {"DOWN", "j"}
KEYS_TOGGLE = {" "}
KEYS_ALL    = {"a"}
KEYS_DONE   = {"\r"}
KEYS_QUIT   = {"q", "\x03"}

# ───────────────────────────────────────────────────────────────────────────

def _read_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.buffer.read(1)
        if ch == b"\x1b":
            nxt = sys.stdin.buffer.read(2)
            return {b"[A": "UP", b"[B": "DOWN"}.get(nxt, "ESC")
        return ch.decode("utf-8", errors="replace")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _draw(items, selected, cursor):
    rows = []
    for i, label in enumerate(items):
        check = COLOR_CHECKED + CHECKED + RESET if i in selected else UNCHECKED
        if i == cursor:
            rows.append(f"{COLOR_POINTER}{POINTER} {check} {label}{RESET}")
        else:
            rows.append(f"  {check} {label}")
    rows.append(COLOR_HINT + "\n  space toggle · a all · enter confirm · q quit" + RESET)

    n = len(rows) + 1
    sys.stdout.write(f"\033[{n}A\r")
    for row in rows:
        sys.stdout.write("\033[2K" + row + "\n")
    sys.stdout.flush()


def multiselect(options, *, preselected=None, max_select=0, groups=None):
    """
    Show an interactive checkbox menu. Returns list of selected strings.

    options      – list of strings to display
    preselected  – list of indices to pre-check  (default: none)
    max_select   – max items allowed; 0 = unlimited
    groups       – list of index lists that are mutually exclusive
                   e.g. [[0, 1]] means picking A deselects B and vice versa
                   e.g. [[0, 1], [2, 3]] for two separate exclusive pairs
    """
    # build a lookup: index -> its exclusive group
    group_map = {}
    for group in (groups or []):
        for idx in group:
            group_map[idx] = group

    def toggle(cursor, selected):
        if cursor in selected:
            selected.discard(cursor)
        else:
            # deselect any sibling in the same exclusive group first
            for sibling in group_map.get(cursor, []):
                selected.discard(sibling)
            if max_select == 0 or len(selected) < max_select:
                selected.add(cursor)

    selected, cursor = set(preselected or []), 0
    sys.stdout.write("\n" * (len(options) + 2))

    _draw(options, selected, cursor)
    while True:
        key = _read_key()
        if   key in KEYS_UP:     cursor = (cursor - 1) % len(options)
        elif key in KEYS_DOWN:   cursor = (cursor + 1) % len(options)
        elif key in KEYS_TOGGLE: toggle(cursor, selected)
        elif key in KEYS_ALL:
            free = {i for i in range(len(options)) if i not in group_map}
            selected = set() if selected >= free else free
        elif key in KEYS_DONE:   break
        elif key in KEYS_QUIT:   return []
        _draw(options, selected, cursor)

    print()
    return [options[i] for i in sorted(selected)]

