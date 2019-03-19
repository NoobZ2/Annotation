import urllib.request
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from tkinterhtml import HtmlFrame

root = tk.Tk()

frame = HtmlFrame(root, horizontal_scrollbar="auto")
frame.grid(sticky=tk.NSEW)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame.set_content("""
<html>
<body>
<h1>Hello world!</h1>
<p>First para</p>
<ul>
    <li>first list item</li>
    <li>second list item</li>
</ul>
</body>
</html>    
""")

frame.set_content(urllib.request.urlopen("http://tkhtml.tcl.tk/").read().decode())

root.mainloop()
