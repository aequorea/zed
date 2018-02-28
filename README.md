# zed
Recently an ancient operating system from the 1970s that I used to use quite a bit was brought back to life using the simh machine emulator. This really impressed me. The operating system is called IRIS and it ran on Data General Nova computers. These computers had a very small amount of memory so the tools were kept simple by necessity. I had used the text editor from that operating system for quite some time, so I decided to use that editor as my model for zed.

The IRIS text editor is a lot like a minimal version of TECO, in fact, the commands are quite similar. I've included a PDF showing the commands for the original IRIS text editor. Aside from the fact that zed supports a subset of the original functionality of the IRIS text editor, the behavior of the supported commands may be slightly different from the original IRIS editor. Searching with regular expressions is one example of different behavior but there are others. For example the K, L, and T commands behave more like TECO than the IRIS editor. This is intentional. This way you can upgrade to TECO without being confused by these minor details.

Here are some directions.

```
 Usage
 -----

 zed file

 Commands
 --------

 nCs1/s2/    change first n occurences of s1 to s2 - position at start of
             buffer - if n <= 0 change all (TECO uses FS or FN for this)

 nD          delete n characters from current position

 Ffile/      insert contents of file at current position - position at end of
             file

 H<char>     change input terminator to <char> - you can use escape to be a
             little bit like TECO

 Istr/       insert str at the current position - may be multi-line -
             you can use control-N as a line separator instead of enter
             for multi-line inserts (IRIS uses control-Z for the separator)

 nJ          move to nth line of buffer

 nK          delete n lines from current position

 nL          move n lines from current position

 nM          move n characters from current position (TECO uses C for this)

 nRcommands  repeats commands n times - multi-line inserts must be separated
             with control-N characters - if you don't use the separator
             you don't get an error - just weird results

 nSstr/      search for str n times - position after match -
             you can use python flavored regular expressions

 nT          type n lines - 0TT types current line (like TECO)

 Z           jump to end of buffer


 XEND        exit -- write file (TECO uses EX for this)
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
```
 Enjoy!
