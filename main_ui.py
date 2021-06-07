import urwid


class UI():
    def __init__(self):
        self.choices = u'ICMP ARP IP TCP UDP'.split()
        self.title = u'Network Packet Test'

    def menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reserved'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        choice_widget = getattr(self, choice.lower())()
        self.main.original_widget = choice_widget  # urwid.Filler(choice_ui)

    def main(self):
        main_widget = urwid.Padding(
            self.menu(self.title, self.choices), left=2, right=2)
        return main_widget

    def icmp(self):
        e_type = urwid.Edit(u'Type: ')
        e_code = urwid.Edit(u'Code: ')
        e_data = urwid.Edit(u'Data: ')
        send = urwid.Button(u'Send')
        urwid.connect_signal(send, 'click', self.send_program)
        back = urwid.Button(u'Back')
        urwid.connect_signal(back, 'click', self.item_chosen, 'main')

        return urwid.Filler(urwid.Pile([urwid.Columns([e_type, e_code]), e_data, urwid.Columns([send, back])]))

    def send_program(self, button):
        pass

    def return_main(self, button, choice):
        self.main.original_widget = urwid.Padding(
            self.menu(self.title, self.choices), left=2, right=2)

    def start(self):
        self.main = urwid.Padding(
            self.menu(self.title, self.choices), left=2, right=2)
        self.top = urwid.Overlay(self.main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 60),
                                 valign='middle', height=('relative', 60),
                                 min_width=20, min_height=9)
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()


if __name__ == '__main__':
    ui = UI()
    ui.start()
