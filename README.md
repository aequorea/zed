# zed
Recently an ancient operating system from the 1970s that I used to use quite a bit was brought back to life using the simh machine emulator. The operating system is called IRIS and it ran on Data General Nova computers. These computers had a very small amount of memory so the tools were simple by necessity. Back in the day, I spent many hours using a very simple text editor on this system, and running it again on the emulator reminded me of some of those happy times. I thought it would be fun to be able to use an editor like that again, except on a more modern computer. Python made this easy.

I've included a PDF showing the commands for the original IRIS text editor. I didn't implement all of the features; in particular there are no commands related to paging the text file. These days we have lots of memory and so we read the whole file in at once. This greatly simplifies things. There are also some minor differences in how the K, L, and T commands work, but this is not a big deal. They ended up working like they do in TECO. Oh well. Before IRIS, I used TECO quite a bit. I should probably tell you that control-C works differently too. On IRIS, at least part of your file would get written out before you got dumped out of the editor. With zed you lose everything. This can be especially disappointing if you were thinking that control-C copies something to a clipboard. On the bright side you can search with python flavored regular expressions. We didn't have anything like that on IRIS, but I couldn't resist putting it in. Python made that easy too. 

Here are some directions.

```
 Usage
 -----

 zed file

 Commands
 --------

 nCs1/s2/    change first n occurences of s1 to s2 - new position at start of
             buffer - if n <= 0 change all

 nD          delete n characters from current position

 Ffile/      insert contents of file at current position - new position at end of
             inserted file

 H<char>     change input terminator to <char>

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

 nSstr/      search for str n times - new position after match -
             you can use python flavored regular expressions

 nT          type n lines - 0TT types current line

 Z           jump to end of buffer


 XEND        exit -- write file
 XKIL        exit -- abandon edits
 control-C   exit -- abandon edits

 Commands may be in lower case. A number n is optional and defaults to one.
 The number may be positive, negative or zero. A minus sign with no number
 means -1.

 The delimiter for inserts is the forward slash, just like IRIS. You can
 change this with the H command.

 How to Install
 --------------

 chmod +x zed.py
 sudo cp zed.py /usr/games/zed
 
 I put the file in the games directory because trying to edit a file with an
 editor like this is sort of like a text adventure game.
```
I'm not sure if it was an accident that the editor got the same name as the person responsible for the Learning Python the Hard Way series or not. But I was thinking if you really want to learn Python the hard way, you might try using an editor like this.

Enjoy!
