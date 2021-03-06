## zed
An oldskool text editor.
<p align="center">
  <img src="teletype.jpg" width="500"/>
</p>
Recently an ancient operating system from the 1970s that I used quite a bit was brought back to life using the simh machine emulator. The operating system is called IRIS and it ran on Data General Nova computers. These computers had a very small amount of memory so the tools were simple by necessity. Back in the day, I spent many hours using a very simple text editor on this system, and running it again on the emulator reminded me of some of those happy times. I thought it would be fun to be able to use an editor like that again, except on a more modern computer. Python made this easy.
<br/><br/>
I've included a PDF showing the commands for the original IRIS text editor. I didn't implement all of the features. For example there are no commands related to paging the text file. These days we have lots of memory so we read the whole file in at once. There are other minor differences including the ability to search with regular expressions and some of the commands work a little bit differently than the IRIS editor. Before the IRIS editor I used teco, and although the IRIS editor was clearly inspired by teco, some things were changed. Well, in zed I changed them back. So this is my platonic vision of how the IRIS editor should have been, and it's sort of a minimal subset of a character oriented text editor that is actually useful. Conspicuously absent is any kind of undo command. Trust me, that's part of the fun. And yes, this is the kind of editor one likely would have used when accessing a timeshared computer with a teletype as shown in the picture, although teco was considerably more powerful.
<br/><br/>
Enjoy!
<br/><br/>
Here are some directions.
<br/><br/>

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
 
     Compatibility
     -------------
 
     It has been tested on linux. It might work on a mac, but probably not on windows.
     It might work in the windows linux subsystem.

Image credit for teletype: By ArnoldReinhold - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=31105488
