import signal
import json
import os
import threading
import time
import Queue

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

from urllib2 import Request, urlopen, URLError

APPINDICATOR_ID = 'liveCricketScore'
match_id = Queue.Queue()
id_arr = []
si = ""
de = ""


def fetch_id():
    request = Request('http://cricscore-api.appspot.com/csa')
    response = urlopen(request)
    id_arr = json.loads(response.read())
    return id_arr


def build_menu():
    menu = gtk.Menu()

    id_arr = fetch_id()

    for match in id_arr:
        item_match = gtk.MenuItem(match["t1"] + ' vs ' + match["t2"])
        item_match.connect('activate', select_active, match["id"])
        menu.append(item_match)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu


def select_active(widget, id):
    match_id.get()
    match_id.put(id)


def quit(_):
    notify.uninit()
    gtk.main_quit()


def show_notification():
    notify.init(APPINDICATOR_ID)
    while True:
        id = match_id.get()
        match_id.put(id)
        if id != 0:
            request = Request('http://cricscore-api.appspot.com/csa?id=' + str(id))
            response = urlopen(request)
            if response.getcode() == 200:
                match_data = json.loads(response.read())
                si = match_data[0]["si"]
                de = match_data[0]["de"]
            notify.Notification.new(si, de, None).show()
        time.sleep(60)


def indicator_panel():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('icon.svg'),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    match_id.put(0)
    i_panel = threading.Thread(target=indicator_panel)
    notif = threading.Thread(target=show_notification)
    i_panel.start()
    notif.start()


if __name__ == "__main__":
    main()
