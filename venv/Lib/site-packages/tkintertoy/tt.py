# Name:         tkintertoy.py - Mike Callahan - Python 2.7 or 3.4
# Purpose:      Makes it easier to create tk/ttk guis
#
# Author:       Mike Callahan
#
# Created:      03/07/2019
# Copyright:    (c) mike.callahan 2019
# License:      MIT
#
# History:
# 1.00 - initial version
# 1.04 - update comments for autodoc
###################################################################

try:
    import Tkinter as tk                               # support Python 2
    import time, ttk, sys, warnings, tkFont as tkfont
    from tkFileDialog import *
    from tkMessageBox import *
    from tkColorChooser import *
except ImportError:
    import tkinter as tk                               # support Python 3
    import time, tkinter.ttk as ttk, sys, warnings, tkinter.font as tkfont
    from tkinter.filedialog import *
    from tkinter.messagebox import *
    from tkinter.colorchooser import *

class Window(object):
    """ An easy GUI creator intended for early Python programmers, built upon
    Tkinter.

    This will create a Tk window with a contents dictionary. The programmer
    adds "ttwidgets" to the window using the add* methods where the programmer
    assigns a string tag to a widget. Almost all ttk widgets are included
    including some useful combined widgets. I call these ttwidgets because they are
    not really complex enough to be called "megawidgets". Most tk/ttk widgets are
    placed in a frame which can act as a label of the ttwidget to the user. The
    programmer places the ttwidgets using the plot method which is a synonym for
    the tkinter grid geometry manager. Contents of the widget are assigned and
    retrieved by using the tags to the set and get methods. This greatly simplifies
    working with GUIs. Also, all ttwidgets are bundled into the window object so
    individual ttwidgets do not need to be passed to other routines, which simplifies
    interfaces. However, more experienced Python programmers can access the tk/ttk
    widget and frames directly and take advantage of the full power of Tk and ttk.

    In the below methods, not all the possible keyword arguments are listed, only
    the most common ones were selected. The Tk documentation lists all for every
    widget. However, tk control variables should NOT be used since they might
    interfere on how the set and get methods work. Default values are shown in
    brackets [].

    Parameters:
        master (tk.Toplevel): Toplevel window
        extra (bool): True if this is an extra window apart from the main

    Keyword Arguments:
        borderwidth (int): Width of border (pixels)
        height (int): Height of frame (pixels)
        padding (int): Spaces between frame and widgets (pixels)
        relief (str): ['flat'],'raised','sunken','groove', or 'ridge'
        style (ttk.Style): Style used for ttk.Frame or ttk.LabelFrame
        width (int): Width of frame (pixels)
    """

    # basic class methods

    def __init__(self, master=None, extra=False, **tkparms):
        """ Set-up window and create content dictionary

        This creates the window and the content dictionary that all the methods
        use. This is always the first step. This method is called automatically
        for containers.
        """

        if not master:
            if not extra:
                self.master = tk.Tk(**tkparms)                # first window
            else:
                self.master = tk.Toplevel(**tkparms)          # extra window
            topwin = self.master.winfo_toplevel()             # get topwindow info
            if 'destroy' in topwin.protocol(name='WM_DELETE_WINDOW'):  # set close window to cancel
                topwin.protocol(name='WM_DELETE_WINDOW', func=self.cancel)
        else:
            self.master = master
        self.content = dict()                      # create the content dict
        self.style = ttk.Style()                   # access Style database

    def __repr__(self):
        """ Display content dictionary structure, useful for debugging.

        Called using the builtin repr() function.

        Returns:
            String of self.content
        """

        temp = "{{'master':{},\n".format(self.master)
        temp += "'content':{\n"
        for widget in self.content:
            try:
                temp += "  '{}':\n    ".format(widget)
                temp += "{{'frame':{},\n    ".format(self.content[widget]['frame'])
                temp += "'type':{},\n    ".format(self.content[widget]['type'])
                temp += "'widget':{},\n    ".format(self.content[widget]['widget'])
                temp += "'value':{}}}\n".format(self.content[widget]['value'].get())
            except KeyError:
                pass
        return temp+'  }'

    def __len__(self):
        """ Return number of widgets in window.

        Called using the builtin len() function.

        Returns:
            Number of widgets in window
        """

        return len(self.content)

    def __contains__(self, tag):
        """ Checks if widget tag is in window.

        Called using the in operator.

        Returns:
            True if 'tag' is in window
        """

        return (tag in self.content)

    # widget mthods

    def setTitle(self, prompt):
        """ Set the title for a window

        This allows the programmer to set the title of the window. If this method
        is not used, the title will be Tk. This only works with top level windows.

        Parameters:
            prompt (str): The title of the window
        """

        self.master.title(prompt)

    def addLabel(self, tag, prompt='', effects='', **tkpamrs):
        """ Create a ttlabel.

        Labels are used to display simple messages to the user. Due to problems
        with textvariable in nested frames with ttk, the textvariable is not used.
        An effects parameter is included for the simplest font types but this
        will override the font keyword argument.

        Parameters:
            tag (str): Reference to widget
            prompt (str): Text of frame label
            effects (str): 'bold' and/or 'italic'

        Keyword Arguments:
            anchor (str): Position in widget; ['center'], 'w', 'e')
            background (str): Background color
            compound (str): Display both image and text, see ttk docs
            font (tkfont.Font): Font for label
            foreground (str): Text color
            image (tk.PhotoImage): GIF image to display
            justify (str): Justification of text; ['left'], 'right', 'center'
            padding (list): Spacing (left, top, right, bottom) around widget (pixels)
            text (str): The text inside the widget
            width (int): Width of label (chars)
            wraplength (int): Character position to word wrap
        """

        self.content[tag] = {'type': 'label'} # init content to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        label = ttk.Label(frame, **tkpamrs)            # create label
        if effects:
            font = label['font']                       # get the current font
            font = tkfont.Font(family=font)            # break it down
            effects = effects.lower()                  # ignore case
            weight = 'bold' if 'bold' in effects else 'normal'  # set weight
            slant = 'italic' if 'italic' in effects else 'roman'  # set slant
            font.configure(weight=weight, slant=slant)  # change weight, slant
            label['font'] = font                       # use it
        label.grid()                                   # widgets are gridded automatically
        self.content[tag]['frame'] = frame             # allow access to frame
        self.content[tag]['widget'] = label            # allow access to widget

    def addLine(self, tag, **tkparms):
        """ Create a horizontal or vertical ttline across the entire frame.

        Lines are useful for visually separating areas of widgets. They have no
        frame.

        Parameters:
            tag (str): Reference to widget

        Keyword Arguments:
            orient (str): ['horizontal'] or 'vertical'
            style (ttk.Style): Style to use for line
        """

        self.content[tag] = {'type': 'line'}
        line = ttk.Separator(self.master, **tkparms)  # create line
        self.content[tag]['widget'] = line

    def addMessage(self, tag, prompt, **tkparms):
        """ Create a ttmessage which is like multiline label.

        Messages are used to display multiline messages to the user. This is a
        tk widget so the list of options is extensive. Due to problems with
        textvariables in nested ttk windows, they are not used. This widget's
        behavior is a little strange so you might prefer the Text or Label widgets.

        Parameters:
            tag (str): Reference to widget
            prompt (str): Text of frame label

        Keyword Arguments:
            aspect (int): Ratio of width to height
            background (str): Background color
            borderwidth (int): Width of border (pixels)
            font (tkfont.Font): Font for label
            foreground (str): Text color
            justify (str): Justification of text; ['left'], 'right', 'center'
            padx (int): Horizontal spaces to place around widget (pixels)
            pady (int): Vertical spaces to place around widget (pixels)
            relief (str): 'flat','raised','sunken','groove', or 'ridge'
            text (str): The text inside the widget
            width (int): Width of message (pixels)
        """

        self.content[tag] = {'type': 'message'}         # init content to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        message = tk.Message(frame, **tkparms)         # create entry
        message.grid()
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = message

    def addEntry(self, tag, prompt='', **tkparms):
        """ Create an ttentry.

        Entries are the widget to get string input from the user. Due to problems
        with textvariables in nested frames with ttk, they are are used.

        Parameters:
            tag (str): Reference to widget
            prompt (str): Text of frame label

        Keyword Arguments:
            justify (str): Justification of text ('left' [def], 'right', 'center')
            show (str): Char to display instead of actual text
            style (ttk.Style): Style to use for widget
            width (int): Width of label [20] (chars)
        """

        self.content[tag] = {'type':'entry', 'value':tk.StringVar()} # init content to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt) # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        entry = ttk.Entry(frame, **tkparms)            # create entry
        entry.grid()
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = entry

    def addList(self, tag, prompt='', alist=[], **tkparms):
        """ Create a ttlistbox.

        Listboxes allow the user to select a series of options in a vertical list.
        It is best for long titled options but does take up some screen space. This
        implementation avoids the listvariable. Since this is a Tk widget, there
        is no style keyword argument.

        Parameters:
            tag (str): Reference to widget
            prompt (str): Text of frame label
            alist (list): Strings in listbox

        Keyword Arguments:
            background (str): Background color
            font (tkfont.Font): Font for label
            foreground (str): Text color
            height (int): Height of listbox (chars) [10]
            selectmode (str): ['browse'], 'single', 'multiple', or 'extended'
            width (int): Width of label (chars) [20]
        """

        self.content[tag] = {'type': 'list'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt) # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        listbox = tk.Listbox(frame, **tkparms)         # create listbox
        listbox.insert('end', *alist)                  # init content to a list
        vbar = ttk.Scrollbar(frame)                    # create scrollbar
        listbox['yscrollcommand'] = vbar.set           # connect text to scrollbar
        vbar['command'] = listbox.yview                # connect scrollbar to text
        listbox.grid()                                 # grid widget
        vbar.grid(row=0, column=1, sticky='ns')        # grid scrollbar
        for i in range(0, len(alist), 2):
            listbox.itemconfigure(i, background='#f0f0ff')  # color alt backgrounds
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = listbox

    def addCombo(self, tag, values=None, prompt='', **tkparms):
        """ Create a ttcombobox.

        Comboboxes combine features of Entry and Listbox into a single widget. The
        user can select one option out of the list or even type in their own. It is
        better than listboxes for a large number of options. Due to problems with
        textvariable in nested frames with ttk, they are not used.

        Parameters:
            tag (str): Reference to widget
            values (list of str): Values to include in dropdown
            prompt (str): Text of frame label

        Keyword Arguments:
            height (int): Maximum number of rows in dropdown [10]
            justify (str): Justification of text (['left'], 'right', 'center')
            postcommand (callback): Function to call when user clicks on downarrow
            style (ttk.Style): Style to use for widget
            width (int): Width of label (chars) [20]
        """

        self.content[tag] = {'type': 'combo'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        combobox = ttk.Combobox(frame, values=values, **tkparms)  # create combobox
        combobox.grid()
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = combobox

    def addCheck(self, tag, alist, prompt='', orient='horizontal', **tkparms):
        """ Create a ttcheckbutton box.

        Checkboxes are used to collect options from the user, similar to a listbox.
        Checkboxes might be better for short titled options because they don't take
        up as much screen space. The keyword arguments will apply to EVERY checkbutton.

        Parameters:
            tag (str): Reference to widget
            alist (list): Checkbox labels
            prompt (str): Text of frame label
            orient (str): ['horizontal'] or 'vertical'

        Keyword Arguments:
            command (callback): Function to execute when boxes are toggled
            compound (str): Display both image and text, see ttk docs
            image (tk.PhotoImage): GIF image to display
            style (ttk.Style): Style to use for checkboxes
            width (int): Width of max checkbox label (chars), negative sets minimum
        """

        self.content[tag] = {'type': 'check'}          # init content to dict
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        cbuttons = []                                  # list for checkbuttons
        cvalues = []                                   # list for bool varibles
        for n, item in enumerate(alist):               # for every item in the given list
            temp = tk.BooleanVar()                     # create the booleanvar
            cvalues.append(temp)                       # set boolean into content
            checkbutton = ttk.Checkbutton(frame, variable=temp, text=item, **tkparms)  # create checkbutton
            cbuttons.append(checkbutton)               # add checkbutton to list
            if orient == 'horizontal':
                checkbutton.grid(row=0, column=n)      # grid it horizontally
            else:
                checkbutton.grid(row=n, column=0)      # grid it vertically
        self.content[tag]['frame'] = frame
        self.content[tag]['value'] = cvalues
        self.content[tag]['widget'] = cbuttons

    def addRadio(self, tag, alist, prompt='', orient='horizontal', **tkparms):
        """ Create a ttradiobutton box.

        Radiobuttons allow the user to select only one option. If they change options,
        the previous option is unselected. This was the way old car radios worked
        hence its name. They are better for short titled options. The keyword
        arguments will apply to EVERY radiobutton.

        Parameters:
            tag (str): Reference to widget
            alist (list): Radiobutton labels
            prompt (int): Text of frame label
            orient (str): 'horizontal' or 'vertical'

        Keyword Arguments:
            command (callback): Function to execute when boxes are toggled
            compound (str): Display both image and text, see ttk docs
            image (tk.PhotoImage): GIF image to display
            style (ttk.Style): Style to use for checkboxes
            width (int): Width of max label (chars), negative sets minimun
        """

        self.content[tag] = {'type': 'radio', 'value': tk.StringVar()}  # init var to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        rbuttons = []                                  # list for radiobuttons
        for n, item in enumerate(alist):               # for every item in the given list
            radiobutton = ttk.Radiobutton(frame, text=item,
                variable=self.content[tag]['value'], value=item, **tkparms)  # create the radiobutton
            if orient == 'horizontal':
                radiobutton.grid(row=0, column=n)      # grid it horizontally
            else:
                radiobutton.grid(row=n, column=0)      # grid it vertically
            rbuttons.append(radiobutton)               # add it to list
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = rbuttons         # list of radio buttons

    def addOption(self, tag, alist, prompt=''):
        """ Create an ttoptionmenu.

        Option menus allow the user to select one fixed option, similar to
        Radiobutton. However, option menu returns a tk.Menu and is more difficult
        to manipulate. There are no keyword arguments in tk.OptionMenu.

        Parameters:
            tag (str): Reference to widget
            alist (list): Strings in option list
            prompt (str): Text of frame label
        """

        self.content[tag] = {'type': 'option', 'value': tk.StringVar()}  # init var to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        option = tk.OptionMenu(frame, self.content[tag]['value'], *alist)  # create optionmenu
        option.grid()
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = option

    def addScale(self, tag, width, parms, prompt='', **tkparms):
        """ Create a ttscale which is an integer scale with entry box.

        Scale allows the user to enter an integer value using a sliding scale. The
        user can also type in a value directly in the entry box.

        Parameters:
            tag (str): Reference to widget
            width (int): Width of entry widget (chars)
            parms (list): Limits of scale [from, to]
            prompt (str): Text of frame label


        Keyword Arguments:
            command (callback): Function to call when scale changes
            length (int): Length of scale (pixels) [100]
            orient (str): 'horizontal' or 'vertical'
            style (str): Style to use for ttk.Scale
        """

        self.content[tag] = {'type': 'scale', 'value': tk.IntVar()}
        xfrom, to = parms
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt) # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        scale = ttk.Scale(frame, from_=xfrom, to=to, variable=self.content[tag]['value'],
            command=lambda x: self.content[tag]['value'].set(int(float(x))), **tkparms)  # create scale
        # the lambda causes the values to always be integers
        entry = ttk.Entry(frame, width=width, textvariable=self.content[tag]['value'])  # create entry
        scale.grid(row=0, column=0)
        entry.grid(row=0, column=1, padx=3)
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = [scale, entry]

    def addSpin(self, tag, parms, between='', prompt='', **tkparms):
        """ Create a ttspinbox.

        Spinboxes allow the user to enter a series of integers. It is best used
        for items like dates, time, etc. The keyword arguments will apply to EVERY
        spinbox. Since this is a Tk widget, there is no style keyword argument.

        Parameters:
            tag (str): Reference to widget
            parms (list): Parmeters for each spinbox [[width, from, to],...]
            between (str): Label between each box
            prompt (str): Text of frame label

        Keyword Arguments:
            background (str): Background color
            buttonbackground (str): Arrow background color
            command (callback): Function to call when arrows are clicked
            font (tkfont.Font): Text font
            foreground (str): Text color
            justify (str): Text justification; ['left'], 'right', 'center'
            state (str): Widget state; ['normal'], 'disabled', 'readonly'
            wrap (bool): Arrow clicks wrap around
        """

        self.content[tag] = {'type': 'spin', 'value': []} # data is list
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt) # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        col = 0                                        # set col
        spins = []
        for parm in parms:
            width, xfrom, to = parm                    # extract spinbox parms
            self.content[tag]['value'].append(tk.IntVar())  # add tkvar to list
            spin = tk.Spinbox(frame, width=width, from_=xfrom, to=to,
                textvariable=self.content[tag]['value'][col/2], **tkparms)  # create spinbox
            spin.grid(row=0, column=col)               # grid it
            spins.append(spin)                         # add it to list
            label = ttk.Label(frame, text=between)     # add the between str
            label.grid(row=0, column=col+1)            # grid the it
            col += 2
        label.destroy()                                # remove last between str
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = spins
        return spins                                   # list of spinboxes

    def addProgress(self, tag, length, prompt='', orient='horizontal', **tkparms):
        """ Create a ttprogressbar.

        This indicates to the user how an action is progressing. The included method
        supports a determinate mode where the programmer tells the user exactly how
        far they have progressed. Ttk also supports a indeterminate mode where a rectangle
        bounces back a forth. See the ttk documentation.

        Parameters:
            tag (str): Reference to widget
            length (int): Length of widget (pixels)
            prompt (str): Text of frame label
            orient (str): 'horizontal' or 'vertical'
            tkparms (dict): Optional parameters for ttk.Progressbar

        Keyword Arguments:
            maximum (int): Maximum value [100]
            mode (str): ['determinate'] or 'indeterminate'
            style (str): Style to use for ttk.Progressbar
        """

        self.content[tag] = {'type': 'progress', 'value': tk.IntVar()}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        progress = ttk.Progressbar(frame, length=length, orient=orient, variable=self.content[tag]['value'])
        progress.grid()
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = progress

    def addButton(self, tag, cmd=[], space=3, prompt='', orient='horizontal', **tkparms):
        """ Create a ttbuttonbox, defaults to Ok - Cancel.

        This widget is where one would place most of the command buttons for a GUI,
        usually at the bottom of the window. Clicking on a button will execute a
        method usually called a callback. Two basic ones are included; exit and
        cancel. The keyword arguments will apply to EVERY button.

        Parameters:
            tag (str): Reference to widget
            cmd (list): [label:str, callback:function] for each button
            space (int): space (pixels) between buttons
            prompt (str): Text of frame label
            orient (str): ['horizontal'] or 'vertical'

        Keyword Arguments:
            compound (str): Display both image and text, see ttk docs
            image (tk.PhotoImage): GIF image to display
            style (ttk.Style): Style to use for checkboxes
            width (int): Width of label (chars)
        """

        self.content[tag] = {'type': 'buttons'}
        if not cmd:                                    # use default buttons
            cmd = [['Ok', self.breakout], ['Cancel', self.cancel]]
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        buttons = []                                   # list for created buttons
        n = 0                                          # init counter
        for label, callback in cmd:
            button = ttk.Button(frame, width=12, text=label,
              command=callback, **tkparms)             # create button
            if orient == 'horizontal':
                button.grid(row=0, column=n, padx=space)  # grid it horizontally
                n += 1
            else:
                button.grid(row=n, column=0, pady=space)  # grid it vertically
                n += 1
            buttons.append(button)
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = buttons           # list of buttons

    def addText(self, tag, width, height, prompt='', **tkparms):
        """ Create a tttext window.

        The tk.Text widget is an extremely powerful widget that can do many things,
        other than just displaying text. It is almost a mini editor. The default
        method allow the programmer to add and delete text. Be sure to read the
        Tk documentation to discover all the features of this widget. Since this
        is a Tk widget, there is no style keyword argument.

        Parameters:
            tag (str): Reference to widget
            width (int): Width of window (chars)
            height (int): Height of window (chars)
            prompt (str): Text of frame label

        Keyword Arguments:
            background (str): Background color
            font (tkfont.Font): Text font
            foreground (str): Text color
            wrap (str): Wordwrap method; ['char'], 'word', or 'none'
        """

        self.content[tag] = {'type': 'text'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        text = tk.Text(frame, width=width, height=height, **tkparms)  # create text widget
        text.grid(row=0, sticky='wens')                # fill entire frame
        vbar = ttk.Scrollbar(frame)                    # create scrollbar
        text['yscrollcommand'] = vbar.set              # connect text to scrollbar
        vbar['command'] = text.yview                   # connect scrollbar to text
        if 'font' not in tkparms:
            text['font'] = ('Helvetica', '10')         # default font
        vbar.grid(row=0, column=1, sticky='ns')        # grid scrollbar
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = text

    def addCanvas(self, tag, width, height, prompt='', **tkparms):
        """ Create a ttcanvas window.

        The tk.Canvas is another extremely powerful widget that displays graphics.
        Again, read the Tkinter documentation to discover all the features of this
        widget.

        Parameters:
            tag (str): Reference to widget
            width (int): Width of window (pixels)
            height (int): Height of window (pixels)
            prompt (str): Text of frame label

        Keyword Arguments:
            background (str): Background color
            closeenough (float): Mouse threshold
            confine (bool): Canvas cannot be scrolled ourside scrolling region
            cursor (str): Mouse cursor
            scrollregion (list of int): w, n, e, s bondaries of scrolling region
        """

        self.content[tag] = {'type': 'canvas'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt) # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        text = tk.Canvas(frame, width=width, height=height, **tkparms)  # create text widget
        text.grid(row=0, sticky='wens')                # fill entire frame
        vbar = ttk.Scrollbar(frame)                    # create scrollbar
        text['yscrollcommand'] = vbar.set              # connect text to scrollbar
        vbar['command'] = text.yview                   # connect scrollbar to text
        vbar.grid(row=0, column=1, sticky='ns')        # grid scrollbar
        hbar = ttk.Scrollbar(frame, orient='horizontal')  # create scrollbar
        text['xscrollcommand'] = hbar.set              # connect text to scrollbar
        hbar['command'] = text.xview                   # connect scrollbar to text
        hbar.grid(row=1, column=0, sticky='we')        # grid scrollbar
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = text

    # file/directory dialogs

    def addOpen(self, tag, width=20, prompt='', **tkparms):
        """ Create a ttopen box which is a file entry and a browse button.

        This has all the widgets needed to open a file. When the user clicks on
        the Browse button, a standard Open dialog box pops up. There are many
        tkparms that are useful for limiting choices, see the Tk documentation.

        Parameters:
            tag (str): Reference to widget
            width (int): Width of entry widget (chars)
            prompt (str): Text of frame label

        Keyword Arguments:
            defaultextension (str): extention added to filename (must strat with .)
            filetypes (list of str): entrys in file listing [[label1, pattern1], [...]]
            initialdir (str): Initial directory (space, ' ' remembers last directory)
            initialfile (str): Default filename
            title (str): Pop-up window's title
        """

        self.content[tag] = {'type': 'open', 'value': tk.StringVar()}  # init var to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        entry = ttk.Entry(frame, textvariable=self.content[tag]['value'], width=width)  # create entry
        entry.grid(padx=3, pady=3)                     # grid entry in frame
        command = (lambda: self._openDialog(tag, **tkparms))
        #photo = tk.PhotoImage(file='openfolder.gif')  # optional folder icon
        #button = ttk.Button(frame, image=photo, command=command)
        button = ttk.Button(frame, width=7, text='Browse', command=command)  # create button
        button.grid(row=0, column=1, padx=3)           # grid button in frame
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = [entry, button]  # list of entry and button

    def _openDialog(self, tag, **tkparms):
        """ Create the file browsing window, do not call directly.
        """

        fn = askopenfilename(**tkparms)                # create the file dialog
        if fn:                                         # user selected file?
            self.set(tag, fn)                          # store it in content

    def addSaveAs(self, tag, width=20, prompt='', **tkparms):
        """ Create an ttsaveas box which is a file entry with a browse button.

        This has all the widgets needed to save a file. When the user clicks on
        the Browse button, a standard SaveAs dialog box pops up. If the user
        selects an existing file, it will pop up a overwrite confirmation box.
        There are many tkparms that are useful for limiting choices, see the Tk
        documentation.

        Parameters:
            tag (str): Reference to widget
            width (int): Width of entry widget
            prompt (str): Text of frame label

        Keyword Arguments:
            defaultextension (str): extention added to filename (must strat with .)
            filetypes (list of str): entrys in file listing [[label1, pattern1], [...]]
            initialdir (str): Initial directory (space, ' ' remembers last directory)
            initialfile (str): Default filename
            title (str): Pop-up window's title
        """

        self.content[tag] = {'type': 'saveas', 'value': tk.StringVar()}  # very similar to addOpen
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        entry = ttk.Entry(frame, textvariable=self.content[tag]['value'], width=width)
        button = ttk.Button(frame, width=7, text='Browse',
            command=(lambda: self._saveDialog(tag, **tkparms)))
        entry.grid(padx=3, pady=3)
        button.grid(row=0, column=1, padx=3, pady=3)
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = [entry, button]   # list of entry and button

    def _saveDialog(self, tag, **tkparms):
        """ Create the file browsing window, do not call directly.
        """

        fn = asksaveasfilename(**tkparms)                # similar to _openDialog
        if fn:
            self.set(tag, fn)

    def addChooseDir(self, tag, width=20, prompt='', **tkparms):
        """ Create a ttchoosedir box which is a directory entry with a browse button.

        This has all the widgets needed to select a directory. When the user clicks
        on the Browse button, a standard Choose Directory dialog box pops up. There
        are many tkparms that are useful for limiting choices, see the Tk
        documentation.

        Parameters:
            tag (str): Reference to widget
            width (int): Width of entry widget
            prompt (str): Text of frame label

        Keyword Arguments:
            initialdir (str): Initial directory (space, ' ' remembers last directory)
            title (str): Pop-up window's title
        """

        self.content[tag] = {'type': 'choosedir', 'value': tk.StringVar()}  # init var to tk var
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        entry = ttk.Entry(frame, textvariable=self.content[tag]['value'], width=width)  # create entry
        entry.grid(padx=3, pady=3)                     # grid entry in frame
        command = (lambda: self._chooseDialog(tag, **tkparms))
        button = ttk.Button(frame, width=7, text='Browse', command=command)  # create button
        button.grid(row=0, column=1, padx=3)           # grid button in frame
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = [entry, button]  # list of entry and button

    def _chooseDialog(self, tag, **tkparms):
        """ Create the directory choose browsing window, do not call directly.
        """

        dirn = askdirectory(**tkparms)                 # similar to _openDialog
        if dirn:
            self.set(tag, dirn)

    # treeview based widgets

    def addLedger(self, tag, height, columns, prompt='', **tkparms):
        """ Create a ttledger which is based on a treeview that displays a simple
        list with column headers.

        This widget allows a nice display of data in columns. It is a simplified
        version of the Collector widget. Due to a bug in ttk, sideways scrolling
        does not work correctly. If you need sideways scrolling use the Text widget.

        Parameters:
            tag (str): Reference to widget
            height (int): Height of widget
            columns (list): Column headers and width (pixels)
            prompt (str): Text of frame label

        Keyword Arguments:
            padding (int): Spaces around values
            selectmode (str): ['browse'] or 'extended'
            style (ttk:Style): Style used for ttk.Treeview
        """

        self.content[tag] = {'type': 'ledger'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        titles = [item[0] for item in columns]         # create the column titles
        tree = ttk.Treeview(frame, columns=titles, show='headings',
            height=height, **tkparms) # create treeview
        yscroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree['yscrollcommand'] = yscroll.set           # create scrollbar
        for title, width in columns:                   # init column headers
            tree.heading(title, text=title, anchor='w')  # set the title
            tree.column(title, width=width, stretch=False)  # set the width
        tree.grid(row=0, column=0, pady=3)             # grid the tree
        yscroll.grid(row=0, column=1, sticky='ns')     # grid scrollbar
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = tree

    def addCollector(self, tag, height, columns, widgets, prompt='', **tkparms):
        """ Create a ttcollector which is based on a treeview that collects contents
        of other widgets.

        This collection of widgets allows the programmer to collect the contents
        of other widgets into a row. The user can add or delete rows as they
        wish using the included buttons.

        Parameters:
            tag (str): Reference to widget
            height (int): Height of widget
            columns (list): column headers and width (pixels)
            widgets (list): (Tags) for simple or (window, tag) for embedded widgets
            prompt (str): Text of frame label

        Keyword Arguments:
            padding (int): Spaces around values
            style (ttk.Style): Style used for ttk.Treeview
        """

        self.content[tag] = {'type': 'collector'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt)  # create titled frame
        else:
            frame = ttk.Frame(self.master)             # no title
        titles = [item[0] for item in columns]         # create the column titles
        tree = ttk.Treeview(frame, columns=titles, show='headings',
            selectmode='browse', height=height, **tkparms)  # create treeview
        yscroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree['yscrollcommand'] = yscroll.set           # create scrollbar
        for title, width in columns:                   # init column headers
            tree.heading(title, text=title, anchor='w')  # set the title
            tree.column(title, width=width, stretch=False)  # set the width
        tree.grid(row=0, column=0, pady=3)             # grid the tree
        yscroll.grid(row=0, column=1, sticky='ns')     # grid scrollbar
        buttonFrame = ttk.Frame(frame)                 # create the add/delete frame
        buttonFrame.grid(row=0, column=2, padx=3)      # grid the frame
        addbutton = ttk.Button(buttonFrame, width=6, text='Add',
            command=(lambda: self._addrow(tag, widgets)))  # create add button
        subbutton = ttk.Button(buttonFrame, width=6, text='Delete',
            command=(lambda: self._delrow(tag)))       # create delete button
        addbutton.grid(row=0, padx=1, pady=3)          # grid buttons
        subbutton.grid(row=1, padx=1, pady=3)
        self.content[tag]['frame'] = frame
        self.content[tag]['widget'] = [tree, addbutton, subbutton] # list of treeview and buttons

    def _addrow(self, tag, widgets):
        """ Add items from other widgets to the treeview, do not call directly
        """

        tree = self.getWidget(tag)[0]                  # get the widget
        items = []                                     # create items list
        for widget in widgets:
            if isinstance(widget, str):                # check each widget
                value = self.get(widget)               # simple case
                if self.getType(widget) not in ['spin', 'option']:
                    self.set(widget, '')               # clear the widget
            else:
                win, wtag = widget
                value = win.get(wtag) # embedded case
                if win.content[wtag]['type'] not in ['spin', 'option']:
                    win.set(wtag, '')
            items.append(value)                        # get contents of other widgets
        for item in items:
            if item:
                break
        else:                                          # no breaks so...
            return                                     # don't add empty lists
        self.set(tag, items)

    def _delrow(self, tag):
        """ Delete selected row from treeview, do not call directly
        """

        tree = self.getWidget(tag)[0]
        select = tree.selection()                      # get the selection
        if select:
            tree.delete(select)                        # remove from treeview

    # widgets added for completeness

    def addSizegrip(self, tag, **tkparms):
        """ Add a sizegrip widget to the window.

        This places a sizegrip in the bottom right corner of the window. It is
        not needed since most platforms add this automatically. The programmer
        must use the configurerow and configurecolumn options when plotting
        widgets for this to work correctly. There is no frame. It was included
        for completeness.

        Parameters:
            tag (str): Reference to widget

        Keyword Arguments:
            style (ttk.Style): Style used for ttk.Sizegrip, mainly background
        """

        self.content[tag] = {'type': 'sizegrip'}
        sizegrip = ttk.Sizegrip(self.master, **tkparms)
        sizegrip.grid(row=999, column=999, sticky='se')  # bottom right corner
        self.content[tag]['widget'] = sizegrip

    def addScrollbar(self, tag, widgetTag, orient='horizontal', **tkparms):
        """ Add a scrollbar to a widget.

        This is usually this is done automatically. There is no frame. In order
        to plot the programmer must get the widget frame and use the correct sticky
        option. It was included for completeness.

        Parameters:
            tag (str): Reference to widget
            widgetTag (str): Tag of connected widget
            orient (str): ['horizontal'] or 'vertical'

        Keyword Arguments:
            style (ttk.Style): Style used for ttk.Scrollbar
        """

        self.content[tag] = {'type': 'scroll'}
        widget = self.getWidget(widgetTag)
        scroll = ttk.Scrollbar(self.master, orient=orient, **tkparms)
        if orient == 'horizontal':
            widget['xscrollcommand'] = scroll.set      # connect widget to hor scrollbar
            scroll['command'] = widget.xview           # connect scrollbar to widget
        else:
            widget['yscrollcommand'] = scroll.set      # connect widget to ver scrollbar
            scroll['command'] = widget.yview           # connect scrollbar to widget
        self.content[tag]['widget'] = scroll

    # container widgets

    def addFrame(self, tag, prompt='', **tkparms):
        """ Create a labeled or unlabeled frame container.

        This allows the programmer to group widgets into a new window.
        The window can have either a title or a relief style, but not both.

        Parameters:
            tag (str): Reference to container
            prompt (str): Text of frame label

        Keyword Arguments:
            boarderwidth (int): width of border (for relief styles only)
            height (int): Height of frame (pixels)
            padding (int): Spaces between frame and widgets (pixels)
            relief (str): 'flat','raised','sunken','groove', or 'ridge'
            style (int): Style used for ttk.Frame or ttk.LabelFrame
            width (int): Width of frame (pixels)

        Returns:
            The window
        """

        self.content[tag] = {'type': 'frame'}
        if prompt:
            frame = ttk.LabelFrame(self.master, text=prompt, **tkparms)  # create titled frame
        else:
            if 'borderwidth' not in tkparms:
                tkparms['borderwidth'] = 2
            frame = ttk.Frame(self.master, **tkparms)  # no title
        self.content[tag]['frame'] = frame
        window = Window(frame)
        return window

    def addNotebook(self, tag, tabs, **tkparms):
        """ Create a tabbed notebook container.

        This allows the programmer to group similar pages into a series of new windows.
        The user selected the active window by clicking on the tab. Assignment allows
        the program to display a page number (counting from 0), and return the
        currently selected page number. There is no frame.

        Parameters:
            tag (str): Reference to container
            tabs (list): Titles of each tab page

        Keyword Arguments:
            height (int): Height of frame (pixels)
            padding (int): Spaces between frame and widgets (pixels)
            style (int): Style used for ttk.Frame or ttk.LabelFrame
            width (int): Width of frame (pixels)

        Returns:
            List of windows
        """

        self.content[tag] = {'type': 'notebook'}        # data is list of lists
        pages = []                                     # pages will be other windows
        notebook = ttk.Notebook(self.master, **tkparms)  # create notebook
        for page in tabs:                              # each tab is a page
            window = self.addFrame(page)               # create frame
            notebook.add(self.getFrame(page), text=page, sticky='wens')  # fill up the entire page
            pages.append(window)                       # remember created windows
        self.content[tag]['widget'] = notebook         # add widget
        return pages


    def addPanes(self, tag, titles, **tkparms):
        """ Create a multipaned window with user adjustable columns.

        This is like a notebook but all the windows are visible. There is no
        frame.

        Parameters:
            tag (str): Reference to container
            panes (list): Tag and titles of all embedded windows

        Keyword Arguments:
            height (int): Height of frame (pixels)
            orient (str): ['horizontal'] or 'vertical'
            padding (int): Spaces between frame and widgets (pixels)
            style (int): Style used for ttk.Frame or ttk.LabelFrame
            width (int): Width of frame (pixels)

        Returns:
            List of windows
        """

        self.content[tag] = {'type': 'panes'}
        panes = []
        panedWindow = ttk.PanedWindow(self.master, **tkparms)
        for title in titles:
            window = self.addFrame(title, prompt=title)
            panedWindow.add(self.getFrame(title))
            panes.append(window)
        self.content[tag]['widget'] = panedWindow
        return panes

    # Styles are contained in the content dictionary as well

    def addStyle(self, tag, **tkparms):
        """ Add a ttk.Style to be used for other widgets.

        This is the method for changing the appearance of ttk widgets. Styles are
        strictly defined strings so look at the Tk documentation.

        Parameter:
            tag (str): Reference to style, must follow ttk naming

        Keyword Arguments:
            Varies with widget, see Tk documentation
        """

        self.style.configure(tag, **tkparms)

    def addMenuButton(self, tag, **tkparms):
        """ Add a menu button

        A menubuuton always stays on the screen and is what the user clicks on. A menu
        is attached to the menubutton. Menus are complex so read the Tk documentation
        carefully.

        Parameters:
            tag (str): Reference to menubutton

        Keyword Arguments:
            Varies (dict): see Tk documentation
        """

        self.content[tag] = {'type': 'menubutton'}
        menubutton = ttk.Menubutton(self.master, **tkparms)
        self.content[tag]['widget'] = menubutton

    def addMenu(self, tag, parent, items=None, **tkparms):
        """ Add a menu

        Menus are complex so read the Tk documentation carefully.

        Parameters:
            tag (str): Reference to menu
            items (list of type, coptions): 'cascade','checkbutton','command','radiobutton',
                'separator' and coptions (see Tk Documentation)
            parent (ttk.Menubutton or tk.Frame): What menu is attached to

        Keyword Arguments:
            Varies (dict): see Tk documentation
        """

        self.content[tag] = {'type': 'menu'}
        menu = tk.Menu(parent, **tkparms)
        if items:
            for type, coptions in items:
                menu.add(type, **coptions)
        self.content[tag]['widget'] = menu

    # premade popup windows

    def popMessage(self, message, mtype='showinfo', title='Information', **tkparms):
        """ Popup a tk message window.

        Parameters:
           message (str): Message in box
           mtype (str): 'showinfo', 'showwarning', 'showerror', 'askyesno',
               'askokcancel', or 'askretrycancel'
           title (str): Title of window

        Keyword Arguments:
            default (str): 'OK', 'Cancel', 'Yes', 'No', or 'Retry'
            icon (str): 'error', 'info', 'question', 'warning'

        Returns:
            'ok' for show* (weird, I know), or bool for ask*
        """

        # python magic, eval converts the string to a function and the...
        # parmeter list calls the function
        return eval(mtype)(title, message, **tkparms)   # cool, yes?

    def popColorChooser(self, **tkparms):
        """ Popup a color chooser dialog.

        This pops up a standard color chooser dialog.

        Keyword Arguments
            color (str): Initial color
            title (str): Title of pop-up window ['Color']
        """

        return askcolor(**tkparms)

    # support functions

    def get(self, tag, allValues=False):
        """ Get the contents of the ttwidget. With more complex widgets the programmer
        can choose to get all the values rather than user selected values.

        Parameters:
            tag (str): Reference to widget, created in add*
            allValues (bool): if true return all the values

        Returns:
            Contents of ttwidget
        """

        widgetType = self.getType(tag)                 # get type
        widget = self.getWidget(tag)                   # get widget(s)
        if widgetType in ('label', 'message'):
            value = widget['text']
        elif widgetType == 'entry':
            value = widget.get()
        elif widgetType == 'combo':
            if allValues:
                value = widget['values']               # get the pulldown list
            else:
                value = widget.get()                   # get entry
        elif widgetType in ('radio','open','saveas','choosedir','option','scale',
            'progress'):
            value = self.content[tag]['value'].get()   # get the tk variable
        elif widgetType == 'check':
            value = []                                 # create list
            for boolvar, check in zip(self.content[tag]['value'], widget):  # for every widget..
                if boolvar.get():                      # check boolean value
                    value.append(check['text'])        # add text to list
        elif widgetType == 'list':
            value = []
            if allValues:
                value = widget.get('0', 'end')         # get all rows
            else:
                indices = widget.curselection()        # get the selected rows
                for index in indices:
                    value.append(widget.get(index))    # get the row contenets
        elif widgetType == 'ledger':
            value = []
            if allValues:
                for rid in widget.get_children():      # get all rows
                    row = widget.set(rid)              # get the items as a dict
                    value.append(row)
            else:
                for rid in widget.selection():         # get the selected rows
                    row = widget.set(rid)
                    value.append(row)
        elif widgetType in ('collector'):
            widget = widget[0]                         # get treeview
            value = []
            for rid in widget.get_children():          # get the top-level items
                row = widget.set(rid)                  # get the dict
                value.append(row)
        elif widgetType == 'spin':
            value = []
            for item in self.content[tag]['value']:
                value.append(item.get())               # get all tk variables
        elif widgetType == 'text':
            value = widget.get('0.0', 'end')           # get all text
        elif widgetType == 'notebook':
            value = widget.index('current')            # get current page
        else:                                          # styles, menus, menubuttons
            value = widget
        return value

    def set(self, tag, value, allValues=False):
        """ Set the contents of the widget. The programmer has the option to replace
        all the values or just add new values.

        Parameters:
            tag (str): - Reference to widget
            value (object): - Value to set
            allValues (bool): if True, replace all values
        """

        widgetType = self.getType(tag)                 # get type
        widget = self.getWidget(tag)                   # get widget(s)
        if widgetType in ('label','message'):
            widget['text'] = value
        elif widgetType == 'entry':
            widget.delete(0, 'end')                    # delete current string
            value = widget.insert(0, value)            # insert new one
        elif widgetType == 'combo':
            if allValues:
                widget['values'] = value
            else:
                widget.set(value)
        elif widgetType in ('radio','open','saveas','choosedir','option','scale',
            'progress'):
            self.content[tag]['value'].set(value)
        elif widgetType == 'check':
            for var, check in zip(self.content[tag]['value'], widget):  # for every key in list...
                var.set(check['text'] in value)        # set tk boolean
        elif widgetType == 'list':
            if allValues:
                widget.delete(0, 'end')                # delete old list
            widget.insert('end', *value)               # add list
            for i in range(0, len(value), 2):
                widget.itemconfigure(i, background='#f0f0ff')  # color alt backgrounds
        elif widgetType == 'collector':
            widget = widget[0]                         # get tree widget
            if value:                                  # non-empty list
                widget.insert('', 'end', values=value) # add to tree
            else:                                      # clear tree
                for id in widget.get_children():       # get top-level items
                    widget.delete(id)                  # delete them
        elif widgetType == 'ledger':
            if allValues:
               for id in widget.get_children():        # get top-level items
                    widget.delete(id)                  # delete them
            for item in value:
                widget.insert('', 'end', values=item)  # add to tree
        elif widgetType == 'spin':
            for item in self.content[tag]['value']:    # for spinboxes
                if value == '':
                    item.set('')                       # clear it
                else:
                    item.set(value.pop(0))             # set it and get next
        elif widgetType == 'notebook':
            widget.select(value)                       # display that page
        elif widgetType == 'text':                     # unlike other widget this inserts!
            if allValues:
                widget.delete('1.0', 'end')            # clear everything
            widget.insert('end', value)                # add text
            widget.see('end')                          # scroll text so it is visible
        self.refresh()                                 # update display

    def plot(self, tag=None, **tkparms):
        """ Plot the ttwidget.

        Place a frame and widget in a cell of a window using the row and column.
        Plot was selected as an easier name for beginners than grid. Other tkparms
        are extremely useful here and should be understood. Look at the Tk
        documentation.

        Parameters:
            tag (str): Reference to widget

        Keyword Arguments:
            row (int): the row number counting from 0
            column (int): the column number
            rowspan (int): the number of rows to span
            columnspan (int): the number of columns to span
            sticky (str): the directions to fill the cell for the widget
            rowconfigure (int): rate widget expands in vertical if resized
            columnconfigure (int): rate widget expands in horizontal
            padx (int): horizontal space between widget cells (pixels)
            pady (int): vertical space between widget cells (pixels)
            ipadx (int): horizontal space within cell (pixels)
            ipady (int): vertical space within cell (pixels)
        """

        if not tag:
            self.master.grid(**tkparms)
        elif self.content[tag]['type'] in ('line','notebook','panes','menubutton'):  # no frames
            self.content[tag]['widget'].grid(**tkparms)  # grid widget
        else:
            self.content[tag]['frame'].grid(**tkparms)   # grid frame

    def getWidget(self, tag):
        """ Get the tk/ttk widget if present.

        Get the underlying tk or ttk widget so the programmer can use more advanced
        methods.

        Parameter:
            tag (str): - Reference to widget

        Returns:
            The tk or ttk widget
        """

        return self.content[tag].get('widget')

    def getFrame(self, tag):
        """ Get the ttk frame if present.

        Get the ttk.Frame or ttk.LabelFrame of the widget so the programmer can
        use more advanced methods.

        Parameters:
            tag (str): Reference to widget

        Returns:
            ttk.Frame or ttk.LabelFrame
        """

        return self.content[tag].get('frame')

    def getType(self, tag):
        """ Get the type of widget.

        Get the type of widget as a string. All widgets have a type.

        Parameters:
            tag (str): Reference to widget

        Returns:
            Type of widget as str
        """

        return self.content[tag]['type']

    def waitforUser(self):
        """ Alias for mainloop, better label for beginners.

        This starts the event loop so the user can interact with window.
        """

        self.master.mainloop()

    def close(self):
        """ Close the window.

        This stops the event loop and removes the window. However, the window
        structure can still be referenced, and the window can be redisplayed.
        """

        self.master.destroy()

    def cancel(self):
        """ Clear contents and exit mainloop.

        This stops the event loop, removes the window, and deletes the widget
        structure.
        """

        self.content = None                            # clear content
        self.master.destroy()                          # close the dialog window

    def breakout(self):
        """ Exit the mainloop but don't destroy the master.

        This stops the event loop, but window remains displayed.
        """

        self.master.quit()                            # break out of mainloop

    def refresh(self):
        """ Alias for update_idletasks, better label for beginners.

        This refreshes the appearance of all widgets. Usually this is called
        automatically after a widget contents are changed.
        """

        self.master.update_idletasks()

    def focus(self, tag):
        """ Switch focus to the desired widget.

        This is useful to select the desired widget at the beginning so the user
        does not have to click.

        Parameters:
            tag (str): Reference to widget
        """

        self.getWidget(tag).focus()

    def catchExcept(self):
        """ Catch the exception messages.

        Use this in a try/except block to catch any errors:

        Returns:
            str: The exception message
        """

        import traceback
        msg = traceback.format_exc()
        return msg

# end tkintertoy.py
