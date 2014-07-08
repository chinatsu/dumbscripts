#!/bin/python

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import subprocess, shlex
import signal, atexit
import os, sys

def main():
    stations = [
        {"d":"nrk", "station":"p1_more_og_romsdal", "name":"NRK P1"},
        {"d":"nrk", "station":"p2", "name":"NRK P2"},
        {"d":"nrk", "station":"p3", "name":"NRK P3"},
        {"d":"mms", "station":"p4_norge", "name":"P4 - Lyden av Norge"},
        {"d":"sbs", "station":"radionorge", "name":"Radio Norge"},
        {"stream":"http://stream.jaerradiogruppen.no:8008/listen.pls", "name":"Radio Ålesund"},
        {"d":"nrk", "station":"jazz", "name":"NRK Jazz"},
        {"d":"nrk", "station":"klassisk", "name":"NRK Klassisk"},
        {"d":"nrk", "station":"mp3", "name":"NRK MP3"},
        {"d":"nrk", "station":"p13", "name":"NRK P13"},
        {"d":"nrk", "station":"p1pluss", "name":"NRK P1+"},
        {"d":"nrk", "station":"p3_pyro", "name":"NRK P3 Pyro"},
        {"d":"nrk", "station":"p3_national_rap_show", "name":"NRK P3 National Rap Show"},
        {"d":"nrk", "station":"p3_radioresepsjonen", "name":"NRK P3 Radioresepsjonen"},
        {"d":"nrk", "station":"p3_urort", "name":"NRK P3 Urørt"},
        {"d":"nrk", "station":"sport", "name":"NRK Sport"},
        {"d":"nrk", "station":"super", "name":"NRK Radio Super"},
        {"d":"nrk","station":"folkemusikk","name":"NRK Folkemusikk"},
        {"stream":"http://mms-live.online.no/p5_oslo_hq.m3u", "name":"P5 Hits Oslo"},
        {"d":"mms", "station":"p4_p6", "name":"P6 Rock"},
        {"d":"mms", "station":"p4_klem", "name":"KlemFM - Rolige Favoritter"},
        {"d":"mms", "station":"p4_nrj", "name":"NRJ - Hit Music Only!"},
        {"d":"mms", "station":"p4_hits", "name":"P4 Hits"},
        {"d":"mms", "station":"p4_ballade", "name":"P4 Ballade"},
        {"d":"mms", "station":"p4_country", "name":"Radio Country"},
        {"d":"mms", "station":"p4_retro", "name":"RadioRetro",},
        {"d":"sbs", "station":"radio1", "name":"Radio1"},
        {"d":"sbs", "station":"radiorock", "name":"Radio Rock"},
        {"d":"sbs", "station":"rockklassiker", "name":"Rock Klassiker"},
        {"d":"sbs", "station":"thevoiceoslo", "name":"The Voice Oslo"},
        {"d":"sbs", "station":"tv2nyhetskanalen", "name":"TV2 Nyhetskanalen"},
        {"d":"nrk", "station":"alltid_nyheter", "name":"NRK Alltid Nyheter"}
    ]
    app = QApplication(sys.argv)
    screen = QWidget()

    playStatus = QLabel("Choose radio station:", screen)
    playStatus.setGeometry(QRect(0, 0, 320, 20));
    playStatus.setAlignment(Qt.AlignCenter);
    stationSelect = QComboBox(screen)
    
    stationSelect.setGeometry(QRect(80, 20, 161, 22))
    stationIndex = QComboBox.currentIndex(stationSelect)
    

    for key in stations:
        QComboBox.addItem(stationSelect,key["name"])

    submitButton = QPushButton("&Listen", screen)
    submitButton.setGeometry(QRect(80, 45, 161, 42))
    exitButton = QPushButton("&This sucks", screen)
    exitButton.setGeometry(QRect(80, 87, 161, 22))
    nextButton = QPushButton("&Next", screen)
    nextButton.setGeometry(QRect(241, 20, 80, 22))
    prevButton = QPushButton("&Previous", screen)
    prevButton.setGeometry(QRect(0, 20, 80, 22))

    buttonLayout1 = QGridLayout()
    buttonLayout1.addWidget(playStatus)
    buttonLayout1.addWidget(stationSelect)
    buttonLayout1.addWidget(prevButton)
    buttonLayout1.addWidget(submitButton)
    buttonLayout1.addWidget(nextButton)
    buttonLayout1.addWidget(exitButton)
    


    def killChildren():
        if ns.child_pid is None:
            pass
        else:
            os.kill(ns.child_pid, signal.SIGTERM)
    def shitMusic():
        exit()
    def playStation():
        killChildren()
        player = "mpv -cache 256 --msg-level all=error:lavf=info --playlist "
        qname = QComboBox.currentText(stationSelect)
        qindex = QComboBox.currentIndex(stationSelect)
        if 'stream' in stations[qindex]:
            url = stations[qindex]['stream']
        elif stations[qindex]['d'] == 'nrk':
            url = ('http://lyd.nrk.no/nrk_radio_' + stations[qindex]["station"] + '_mp3_h.m3u')
        elif stations[qindex]['d'] == 'mms':
            url = ('http://mms-live.online.no/' + stations[qindex]["station"] + '_mp3_hq.m3u')
        elif stations[qindex]['d'] == 'sbs':
            url = ('http://stream.sbsradio.no:8000/' + stations[qindex]["station"] + '.mp3.m3u')
        
        QLabel.setText(playStatus,"Playing: " + str(qname))
        qargs = shlex.split(player + url)
        qplayer = subprocess.Popen(qargs)
        ns.child_pid = qplayer.pid
    
    def nextStation():
         if QComboBox.currentIndex(stationSelect) == len(stations) - 1:
             pass
         else:
             nextIndex = stationSelect.setCurrentIndex(QComboBox.currentIndex(stationSelect) + 1)
         if ns.child_pid is None:
             pass
         else:
             playStation()

    def prevStation():
         if QComboBox.currentIndex(stationSelect) == 0:
             pass
         else:
             prevIndex = stationSelect.setCurrentIndex(QComboBox.currentIndex(stationSelect) - 1)
         
         if ns.child_pid is None:
             pass
         else:
             playStation()

    class dicksuck: pass

    ns = dicksuck()
    ns.child_pid = None

    atexit.register(killChildren)

    submitButton.clicked.connect(playStation)
    exitButton.clicked.connect(shitMusic)
    nextButton.clicked.connect(nextStation)
    prevButton.clicked.connect(prevStation)
    screen.setWindowTitle("Radio")
    screen.resize(320, 112)
    screen.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
