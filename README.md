# zed
An oldskool text editor

Recently an ancient operating system from the 1970s that I used to use quite a bit was brough back to life using the simh machine emulator. This really impressed me. The operating system is called IRIS and it ran on Data General Nova computers. These computers had a very small amount of memory so the tools were kept simple by necessity. I had used the text editor from that operating system for quite some time, so I decided to use that editor as my model for zed.

The IRIS text editor is a lot like a minimal version of TECO, in fact, the commands are quite similar. I've included a PDF showing the commands for the original IRIS text editor. zed is not an exact clone of the IRIS editor. Aside from the fact that it supports a subset of the original functionality the behavior of the supported commands may be slightly different from the original. Searching with regular expressions is one example of different behavior but there are others. The commands supported by zed are listed in the comments at the start of the python file zed.py.

Enjoy!
