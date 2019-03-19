import tkinter as tk

class Example(tk.Frame):
  def __init__(self, parent):
    tk.Frame.__init__(self, parent)
    self.text = tk.Text(self, wrap="none")
    self.text.pack(fill="both", expand=True)
    self.start = tk.StringVar()
    self.end = tk.StringVar()

    self.text.bind("<Button-1>", self.button_down)
    self.text.bind("<ButtonRelease-1>", self.button_up)
    #self.text.bind("<B1-Motion>", self._on_click)
    self.text.tag_configure("highlight", background="green", foreground="black")

    with open(__file__, "rU") as f:
      data = f.read()
      self.text.insert("1.0", data)

  def button_down(self, event):
      self.start = self.text.index('@%s,%s wordstart' % (event.x, event.y))
      print(self.start)

  def button_up(self, event):
      self.end = self.text.index('@%s,%s wordend' % (event.x, event.y))
      print(self.end)

      self.text.tag_add("highlight", self.start, self.end)



if __name__ == "__main__":
  root = tk.Tk()
  Example(root).pack(fill="both", expand=True)
  root.mainloop()