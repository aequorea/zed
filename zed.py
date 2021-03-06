#!/usr/bin/python3
#
# zed.py -- an oldskool text editor
#           inspired by the IRIS text editor
#
# by John Saeger
#
# 2018-02-27 -- first version
# 2018-02-28 -- (1.01) give an error if bogus command
#               stop executing the current command string on any error
# 2018-02-28 -- (1.02) update command descriptions
#               fix repeat when n <= 0
# 2018-02-28 -- (1.03) consistently
# 2018-03-01 -- (1.04) modify change to use regular expressions
# 2018-03-07 -- (1.05) error if no file specified
# 2018-03-08 -- (1.06) fix bug in change function

"""

 Usage
 -----

 zed file

 Commands
 --------

 nCs1/s2/    change first n occurences of s1 to s2 after current position -
             position doesn't change - you can use python flavored regular
             expressions - if n <= 0 change all after current position

 nD          delete n characters from current position

 Ffile/      insert contents of file at current position - position at end of
             file

 H<char>     change string terminator from / to <char>

 Istr/       insert str at the current position - may be multi-line -
             you can use control-N as a line separator instead of enter
             for multi-line inserts

 nJ          move to nth line of buffer - if n <= 0 go to beginning of buffer

 nK          delete n lines from current position (see below)

 nL          move n lines from current position (see below)

 nM          move n characters from current position

 nRcommands  repeats commands n times - multi-line inserts must be separated
             with control-N characters - if you don't use control-N you don't
             get an error - just weird results - if n <= 0 do it once

 nSstr/      search for str n times after current position - new position after
             match - you can use python flavored regular expressions -
             if n <= 0 search once - there are no backwards searches

 nT          type n lines (see below)

 Z           jump to end of buffer


 XEND        exit -- write file
 XKIL        exit -- abandon edits
 control-C   exit -- abandon edits

 Commands may be in lower case. A number n is optional and defaults to one.
 The number may be positive, negative or zero. A minus sign with no number
 means -1.

 K, T, and L commands use the number n consistently with one another --

     If n < 0, K deletes from the beginning of the nth line previous to the
     current position, T types from the beginning of the nth line previous to
     the current position, and L moves to the beginning of the nth line
     previous.

     If n = 0, K deletes from the beginning of the current line to the current
     position, T types from the beginning of the current line to the current
     position, and L moves to the beginning of the current line.

     If n > 0, K deletes from the current position to the beginning of the nth
     line forward, T types from the current position to the beginning of the
     nth line forward and and L moves to the beginning of nth line forward.

 How to Install
 --------------

 chmod +x zed.py
 sudo cp zed.py /usr/games/zed

 Enjoy!

"""

import sys
import re

terminator = '/'  # string terminator
buf = []          # edit buffer
p = 0             # current position in edit buffer
s = ''            # command buffer
cp = 0            # pointer into command buffer


def readfile(name, buf, p):
    try:
        f = open(name, 'r')
        for ch in f.read():
            buf.insert(p, ch)
            p += 1
        f.close()
    except Exception:       # don't sweat it if nobody is home
        return              # create the file when it's time to write it out


def writefile(name, buf, p):
    f = open(name, 'w')
    string = ''.join(buf)
    f.write(string)
    f.close()


def backscan(n, buf, p):
    n = -n
    while n:
        if p < 0:
            return 0
        p -= 1
        if buf[p] == '\n':
            n -= 1
    return p+1


def do_type(n, buf, p):
    if n <= 0:
        mp = backscan(n-1, buf, p)
        n = 1-n
        while n:
            if mp >= p:
                break
            ch = buf[mp]
            if ch == '\n':
                n -= 1
            print(ch, end='')
            mp += 1
    else:
        while n:
            if p >= len(buf):
                return
            ch = buf[p]
            if ch == '\n':
                n -= 1
            print(ch, end='')
            p += 1


def do_line(n, buf, p):
    if n <= 0:
        p = backscan(n-1, buf, p)
    else:
        while n:
            if p >= len(buf):
                p = len(buf)
                return p
            ch = buf[p]
            if ch == '\n':
                n -= 1
            p += 1
    return p


def do_jump(n, buf, p):
    p = 0
    if n < 0:
        n = 0
    if n != 0:
        n -= 1
    while n:
        if p >= len(buf):
            return p
        if buf[p] == '\n':
            n -= 1
        p += 1
    return p


def do_kill(n, buf, p):
    if n < 0:
        mp = backscan(n-1, buf, p)
        chars = p - mp
        p = mp
        while chars:
            buf.pop(p)
            chars -= 1
    else:
        while n:
            if p >= len(buf):
                return p
            if buf[p] == '\n':
                n -= 1
            buf.pop(p)
    return p


def do_del(n, buf, p):
    if n < 0:
        mp = p + n
        if mp < 0:
            mp = 0
        chars = p - mp
        while chars:
            buf.pop(mp)
            chars -= 1
    else:
        while n:
            if p >= len(buf):
                return p
            buf.pop(p)
            n -= 1
    return p


def do_move(n, buf, p):
    if n < 0:
        p += n
        if p < 0:
            p = 0
    else:
        p += n
        if p >= len(buf):
            p = len(buf)
    return p


def do_input(cp, buf, p):
    global s
    ibuf = []
    while True:
        while cp == len(s):
            s = input('')
            cp = 0
            ibuf += '\n'
        ch = s[cp]
        cp += 1
        if ch == terminator:
            break
        if ch == '\x0E':    # control-N
            ibuf += '\n'
        else:
            ibuf += ch
    for ch in ibuf:
        buf.insert(p, ch)
        p += 1
    return cp, p


def get_short_string(s, cp):
    string = []
    while cp < len(s) and s[cp] != terminator:
        string += s[cp]
        cp += 1
    if cp < len(s):
        cp += 1
        return(''.join(string), s, cp)
    else:
        return('', s, cp)


def do_search(n, s, cp, buf, p):
    editbuf = ''.join(buf)
    searchbuf, s, cp = get_short_string(s, cp)
    if not searchbuf:
        print('? search')
        cp = len(s)     # terminate this command string
        return cp, p
    if n <= 0:
        n = 1
    while n:
        try:
            match = re.search(searchbuf, editbuf[p:])
        except Exception:
            print('? regex')
            cp = len(s)     # terminate this command string
            return cp, p

        if match:
            p += match.end()
        else:
            print('? no match')
            cp = len(s)     # terminate this command string
            return cp, p

        n -= 1
    return cp, p


def do_change(n, s, cp, p):
    global buf
    editbuf = ''.join(buf)
    searchbuf, s, cp = get_short_string(s, cp)
    if not searchbuf:
        print('? change')
        cp = len(s)     # terminate this command string
        return cp, p
    changebuf, s, cp = get_short_string(s, cp)
    if not changebuf:
        print('? change')
        cp = len(s)     # terminate this command string
        return cp, p
    if n <= 0:
        n = 0
    try:
        neweditbuf = re.sub(searchbuf, changebuf, editbuf[p:], n)
    except Exception:
        print('? regex')
        cp = len(s)     # terminate this command string
        return cp, p

    buf = buf[0:p]
    for ch in neweditbuf:
        buf.append(ch)
    p = 0
    return cp, p


def do_file(s, cp, buf, p):
    filename, s, cp = get_short_string(s, cp)
    try:
        f = open(filename, 'r')
        for ch in f.read():
            buf.insert(p, ch)
            p += 1
        f.close()
    except Exception:
        print('? file')
        cp = len(s)     # terminate this command string
    return cp, p


def do_repeat(n, cp, buf, p):
    global s
    sbuf = []
    while cp < len(s):
        sbuf += s[cp]
        cp += 1
    big_s = []
    if n <= 0:
        n = 1
    while n:
        n -= 1
        big_s += sbuf
    s = ''.join(big_s)
    cp = 0
    return cp, p


def do_commands(s, cp, buf, p):
    global terminator

    if s[cp:cp+4].lower() == 'xend':
        writefile(sys.argv[1], buf, p)
        return 0, cp, p
    if s[cp:cp+4].lower() == 'xkil':
        return 0, cp, p

    regex = r"(-?\d{0,10})(\w)"
    match = re.search(regex, s[cp:].lower())
    if not match:
        print("? command")
        cp = len(s)     # terminate this command string
        return 1, cp, p
    if match.group(1):
        if match.group(1) == '-':
            n = -1
        else:
            n = int(match.group(1))
    else:
        n = 1
    cmd = match.group(2)
    cp += match.end()

    if cmd == 't':
        do_type(n, buf, p)
    elif cmd == 'j':
        p = do_jump(n, buf, p)
    elif cmd == 'l':
        p = do_line(n, buf, p)
    elif cmd == 'k':
        p = do_kill(n, buf, p)
    elif cmd == 'm':
        p = do_move(n, buf, p)
    elif cmd == 'd':
        p = do_del(n, buf, p)
    elif cmd == 'c':
        cp, p = do_change(n, s, cp, p)
    elif cmd == 'r':
        cp, p = do_repeat(n, cp, buf, p)
    elif cmd == 's':
        cp, p = do_search(n, s, cp, buf, p)

    elif cmd == 'f':
        cp, p = do_file(s, cp, buf, p)
    elif cmd == 'i':
        cp, p = do_input(cp, buf, p)
    elif cmd == 'z':
        p = len(buf)
    elif cmd == 'h':
        terminator = s[cp]
        cp += 1
    else:
        print('? command')
        cp = len(s)     # terminate this command string

    return 1, cp, p

# read the input file (if it exists) and we're off to the races

try:
    readfile(sys.argv[1], buf, p)
except Exception:
    print('? file')
    exit()

REPL = True
while REPL:
    if cp == len(s):
        s = input('*')
        cp = 0
    REPL, cp, p = do_commands(s, cp, buf, p)
