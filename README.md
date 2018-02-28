# zed
An oldskool text editor

I was watching this video on learning Python the hard way and it was suggested that I might like to try out the Atom editor. OK. So I did. I put the thing in and launched it. It took something like 10 seconds to load. Wow. That's kind of like a web browser or something. So I looked into it and found that actually it is a web browser. Every time you write a program using the framework that they used to write Atom, you ship a web browser along with the program. So how big is that? Ten megabytes? More. A hundred megabytes? Almost. Welcome to the 21st century! So that's part of the inspiration.

The other part are the Maxwell's equations of software. These guys are writing lisp interpreters in a couple of hundred lines of python code - or less, and I was fairly impressed with what they were doing. I wondered if I could write a text editor in a couple of hundred lines of code. That's another part of the inspiration.

Finally somebody has brought an ancient operating system that I used to do a fair amount of work on back to life using the simh machine emulator. This really impressed me. The operating system is called IRIS and it ran on Data General Nova computers. These computers had a couple of hundred kb of RAM max, so the tools were kept simple by necessity. The text editor that I used for years had almost nothing to it. I decided to use that as my model for a text editor.

Truth be told, the IRIS text editor is a lot like a minimal version of TECO, in fact, the commands are quite similar. So if you decide to fool around with zed which is a subset of the IRIS editor and decide to explore the greater arcana of the grandaddy of them all, you will find that jumping from zed into TECO is not such a big shock. And yes, there is a version of TECO in C that runs on most platforms. The advantage of zed is that it is simple from the get go and it's arguably easier to get started with than TECO. Python programs are easy to run and if you decide to fool around with the code, python programs are easy to modify. With zed, you also get to do searching with regular expressions which is much more familiar to a modern audience than TECO's version of pattern matching.

Maybe that's enough of a sales pitch. The commands are listed in the comments at the start of the python file zed.py.

Enjoy!

P.S. I've decided to include a PDF showing the commands for the original IRIS text editor. zed is not an exact clone. That's why I say it's inspired by the IRIS editor. The commands have the same names but the behavior may be slightly different. Searching with regular expressions is probably the main example of different behavior but there are other subtle differences that you will need to explore to find out exactly what they are.

And BTW, if you want to learn Python the hard way... Start by writing a text editor in Python that is character oriented and has no GUI. Then use it to do the exercises. Cheers!
