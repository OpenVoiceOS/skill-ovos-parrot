import QtQuick 2.12
import QtQuick.Window 2.12
import QtWebEngine 1.7
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    property bool animationRunning: sessionData.running
    leftPadding: 0
    rightPadding: 0
    topPadding: 0
    bottomPadding: 0

    onAnimationRunningChanged: {
        if(animationRunning){
            if (wView.loadProgress == 100) {
                wView.runJavaScript("startTalking()")
            }
        } else {
            if (wView.loadProgress == 100) {
                wView.runJavaScript("stopTalking()")
            }
        }
    }

    WebEngineView {
        id: wView
        anchors.fill: parent
        url: Qt.resolvedUrl("parrot.html")
    }
}
