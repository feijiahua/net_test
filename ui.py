import urwid

choices = u'ICMP ARP IP TCP UDP'.split()


class UI(urwid.WidgetPlaceholder):
    def __init__(self):
        self.box_level = 0
        self.max_box_level = 3

    def menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        type = urwid.Edit(u'Type ')
        code = urwid.Edit(u'Code ')
        layout = urwid.Columns([type, code])
        # response = urwid.Text([u'You chosen ', choice, u'\n'])
        done = urwid.Button(u'OK')
        urwid.connect_signal(done, 'click', self.exit_program)
        main.original_widget = urwid.Filler(urwid.Pile(
            [layout, urwid.AttrMap(done, None, focus_map='reversed')]))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def open_box(self, box):
        self.original_widget = urwid.Padding(urwid.LineBox(box),
                                             align='left', width=('relative', 100),
                                             min_width=None,
                                             left=0,
                                             right=0)

    def icmp_ui(self):
        type = urwid.Edit(u'Type')
        code = urwid.Edit(u'Code')
        cksum = urwid.Edit(u'Cksum')
        layout = urwid.Columns([type, code, cksum])


if __name__ == '__main__':
    top = UI()
    main = urwid.Padding(top.menu(u'Python', choices), left=2, right=2)
    top_menu = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                             align='center', width=('relative', 60),
                             valign='middle', height=('relative', 60),
                             min_width=20, min_height=9)
    urwid.MainLoop(top_menu, palette=[('reversed', 'standout', '')]).run()
