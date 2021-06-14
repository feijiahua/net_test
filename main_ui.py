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
        self.main.original_widget = getattr(
            self, choice.lower())()

    def main_menu(self):
        return self.menu(self.title, self.choices)

    def icmp(self):
        icmp_choices = u'Ping Customize'.split()
        body = [urwid.Text(u'ICMP'), urwid.Divider()]
        for c in icmp_choices:

            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        choices_list = urwid.ListBox(urwid.SimpleFocusListWalker(body))

        back = urwid.Button(u'Back')
        urwid.connect_signal(back, 'click', self.item_chosen, 'main')

        return urwid.Padding(choices_list)

    def ping(self):
        src = urwid.Edit(u'src: ')
        dst = urwid.Edit(u'dst: ')
        data = urwid.Edit(u'data: ')
        send = urwid.Button(u'send')
        back = urwid.Button(u'back')

        urwid.connect_signal(back, 'click', self.item_chosen, 'main_menu')

        return urwid.ListBox([src, dst, data, send, back])

    def send(self, button):
        pass

    def return_main(self, button, choice):
        self.main.original_widget = self.menu(self.title, self.choices)

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
