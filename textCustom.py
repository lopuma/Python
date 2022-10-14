try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
class CustomText(tk.Text):
    def __init__(self, parent, delimiters=[]):
        tk.Text.__init__(self, parent)
        #   test text
        self.insert('1.0', '1111111 222222'
                           '\n'
                           '1111111.222222'
                           '\n'
                           '1111111.222222,333333'
                           '\n'
                           '444444444444444444')
        #   binds
        self.bind('<Double-1>', self.on_dbl_click)
        self.bind('<<Selection>>', self.handle_selection)
        #   our delimiters
        
        self.delimiters = ' '.join(delimiters)
        print("1 ", self.delimiters)
        #   stat dictionary for double-click event
        self.dbl_click_stat = {'clicked': False,
                               'current': '',
                               'start': '',
                               'end': ''
                               }
    # def on_dbl_click(self, event):
    #     #   store stats on dbl-click
    #     self.dbl_click_stat['clicked'] = True
    #     #   clicked position
    #     self.dbl_click_stat['current'] = self.index('@%s,%s' % (event.x, event.y))
    #     #   start boundary
    #     self.dbl_click_stat['start'] = self.index('@%s,%s wordstart' % (event.x, event.y))
    #     #   end boundary
    #     self.dbl_click_stat['end'] = self.index('@%s,%s wordend' % (event.x, event.y))
    def on_dbl_click(self, event):
        if self.delimiters:
            #   click position
            current_idx = self.index('@%s,%s' % (event.x, event.y))
            #   start boundary
            start_idx = self.search(r'[%s\s]' % self.delimiters, index=current_idx,
                                    stopindex='1.0', backwards=True, regexp=True)
            #   quick fix for first word
            start_idx = start_idx + '+1c' if start_idx else '1.0'
            #   end boundary
            end_idx = self.search(r'[%s\s]' % self.delimiters, index=current_idx,
                                stopindex='end', regexp=True)
        else:
            #   start boundary
            start_idx = self.index('@%s,%s wordstart' % (event.x, event.y))
            #   end boundary
            end_idx = self.index('@%s,%s wordend' % (event.x, event.y))
        self.tag_add('sel', start_idx, end_idx)
        return 'break'

    def handle_selection(self, event):
        if self.dbl_click_stat['clicked']:
            #   False to prevent a loop
            self.dbl_click_stat['clicked'] = False
            if self.delimiters:
                #   Preserve "default" selection
                start = self.index('sel.first')
                end = self.index('sel.last')
                #   Remove "default" selection
                self.tag_remove('sel', '1.0', 'end')
                #   search for occurrences
                occurrence_forward = self.search(r'[%s]' % self.delimiters, index=self.dbl_click_stat['current'],
                                                 stopindex=end, regexp=True)
                occurrence_backward = self.search(r'[%s]' % self.delimiters, index=self.dbl_click_stat['current'],
                                                  stopindex=start, backwards=True, regexp=True)
                boundary_one = occurrence_backward + '+1c' if occurrence_backward else start
                boundary_two = occurrence_forward if occurrence_forward else end
                #   Add selection by boundaries
                self.tag_add('sel', boundary_one, boundary_two)
            else:
                #   Remove "default" selection
                self.tag_remove('sel', '1.0', 'end')
                #   Add selection by boundaries
                self.tag_add('sel', self.dbl_click_stat['start'], self.dbl_click_stat['end'])

root = tk.Tk()
text = CustomText(root)
text.pack()
root.mainloop()