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

"""

 Usage
 -----

 zed file

 Commands
 --------

 nCs1/s2/    change first n occurences of s1 to s2 - position at start of
             buffer - if n <= 0 change all

 nD          delete n characters from current position

 Ffile/      insert contents of file at current position - position at end of
             file

 H<char>     change input terminator to <char> - you can use escape to be a
             little bit like TECO

 Istr/       insert str at the current position - may be multi-line -
             you can use control-N as a line separator instead of enter
             for multi-line inserts

 nJ          move to nth line of buffer

 nK          delete n lines from current position

 nL          move n lines from current position

 nM          move n characters from current position

 nRcommands  repeats commands n times - multi-line inserts must be separated
             with control-N characters - if you don't use the separator
             you don't get an error - just weird results

 nSstr/      search for str n times - position after match -
             you can use python flavored regular expressions

 nT          type n lines

 Z           jump to end of buffer


 XEND        exit -- write file
 XKIL        exit -- abandon edits
 control-C   exit -- abandon edits

 Commands may be in lower case. A number n is optional and defaults to one.
 The number may be positive, negative or zero. A minus sign with no number
 means -1.

 The delimiter for inserts is the forward slash, just like IRIS. You can
 change this with the H command. If you want you can make it the escape key.
 Then it's more like TECO.

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
        neweditbuf = editbuf.replace(searchbuf, changebuf)
    else:
        neweditbuf = editbuf.replace(searchbuf, changebuf, n)
    buf = []
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


readfile(sys.argv[1], buf, p)

REPL = True
while REPL:
    if cp == len(s):
        s = input('*')
        cp = 0
    REPL, cp, p = do_commands(s, cp, buf, p)
