#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing libraries
import os
import re
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from functools import partial

labels = {
    "APPConfig": "APP - Configuration",
    "InstallationFolder": "Installation Folder",
    "SelectComponents": "Select Components",
    "LicenseAgreement": "License Agreement",
    "ReadyToInstall": "Ready to Install",
    "Installing": "Installing",
    "Finished": "Finished",
    "Welcome": "Welcome to the Setup Wizard",
    "SubTitle": "Please select the directory where app will be installed.",
    "SelectiFolderBtn": "Select Folder",
    "SubtitleFolder": "Please select the components you want to install.",
    "SelectBtn": "Select",
    "UndoBtn": "Undo",
    "SelectallBtn": "Select All",
    "UnselectallBtn": "Unselect All",
    "Restart": "To finish the installation, please restart your computer.",
}

# region Functions


def createTextHeader(controller) -> None:
    controller.topFrame = QFrame(controller)
    controller.topFrame.setFixedHeight(65)
    controller.topFrame.setFixedWidth(controller.width())
    controller.topFrame.setStyleSheet(
        "background-color: #f7f7f7;border-bottom: 1px solid #8e8e8e;"
    )
    controller.topFrame.setFrameShape(QFrame.StyledPanel)

    controller.label = QLabel(controller)
    controller.label.setText(controller.labelHeaderText)
    controller.label.setStyleSheet(
        "color: black; font-weight: bold; font-size: 15px; background-color: #f7f7f7;"
    )
    controller.label.move(20, 14)


def createSubtitleHeader(controller, subtitle) -> None:
    controller.subtitleLabel = QLabel(controller)
    controller.subtitleLabel.setText(subtitle)
    controller.subtitleLabel.setStyleSheet(
        "color: black; font-size: 12px; background-color: #f7f7f7;"
    )
    controller.subtitleLabel.move(45, 35)


def createTextFooter(controller) -> None:
    controller.bottomFrame = QFrame(controller)
    controller.bottomFrame.setFixedHeight(50)
    controller.bottomFrame.setFixedWidth(controller.width())
    controller.bottomFrame.setStyleSheet(
        "background-color: #f7f7f7;border-top: 1px solid #8e8e8e;")
    controller.bottomFrame.setFrameShape(QFrame.StyledPanel)
    controller.bottomFrame.move(0, 310)


def createSideLabes(controller, index) -> None:
    # Default styles
    selectedStyle = "color: black; font-weight: bold; font-size: 15px;"
    passedStyle = "color: black; font-size: 15px;"

    # Creating labels
    appconfig = QLabel(controller, text=labels["APPConfig"])
    folder = QLabel(controller, text=labels["InstallationFolder"])
    component = QLabel(controller, text=labels["SelectComponents"])
    licence = QLabel(controller, text=labels["LicenseAgreement"])
    toInstall = QLabel(controller, text=labels["ReadyToInstall"])
    installing = QLabel(controller, text=labels["Installing"])
    finished = QLabel(controller, text=labels["Finished"])

    # Positioning labels
    appconfig.move(20, 90)
    folder.move(20, 120)
    component.move(20, 150)
    licence.move(20, 180)
    toInstall.move(20, 210)
    installing.move(20, 240)
    finished.move(20, 270)

    # Styling labels
    style = "color: #9a9797; font-size: 12px;"
    appconfig.setStyleSheet(style)
    folder.setStyleSheet(style)
    component.setStyleSheet(style)
    licence.setStyleSheet(style)
    toInstall.setStyleSheet(style)
    installing.setStyleSheet(style)
    finished.setStyleSheet(style)

    # Restylings labels base on selected index.
    if index == 0:
        appconfig.setStyleSheet(appconfig.styleSheet() + selectedStyle)
    elif index > 0:
        appconfig.setStyleSheet(appconfig.styleSheet() + passedStyle)

    if index == 1:
        folder.setStyleSheet(folder.styleSheet() + selectedStyle)
    elif index > 1:
        folder.setStyleSheet(folder.styleSheet() + passedStyle)

    if index == 2:
        component.setStyleSheet(component.styleSheet() + selectedStyle)
    elif index > 2:
        component.setStyleSheet(component.styleSheet() + passedStyle)

    if index == 3:
        licence.setStyleSheet(licence.styleSheet() + selectedStyle)
    elif index > 3:
        licence.setStyleSheet(licence.styleSheet() + passedStyle)

    if index == 4:
        toInstall.setStyleSheet(toInstall.styleSheet() + selectedStyle)
    elif index > 4:
        toInstall.setStyleSheet(toInstall.styleSheet() + passedStyle)

    if index == 5:
        installing.setStyleSheet(installing.styleSheet() + selectedStyle)
    elif index > 5:
        installing.setStyleSheet(installing.styleSheet() + passedStyle)

    if index == 6:
        finished.setStyleSheet(finished.styleSheet() + selectedStyle)
    elif index > 6:
        finished.setStyleSheet(finished.styleSheet() + passedStyle)


def createInstallButton(controller) -> None:
    controller.installButton = QPushButton(controller)
    controller.installButton.setText("Install")
    controller.installButton.setStyleSheet(QPushButtonStyle)
    controller.installButton.move(
        controller.width() - 200,
        controller.height() - 37
    )
    controller.installButton.clicked.connect(controller.root.install)
    controller.installButton.setCursor(Qt.PointingHandCursor)


def createNextButton(controller, text="Next >") -> None:
    controller.nextButton = QPushButton(controller)
    controller.nextButton.setText(text)
    controller.nextButton.setStyleSheet(QPushButtonStyle)
    controller.nextButton.move(
        controller.width() - 200, controller.height() - 37)
    controller.nextButton.clicked.connect(controller.root.nextPage)
    controller.nextButton.setCursor(Qt.PointingHandCursor)


def createPreviousButton(controller) -> None:
    controller.previousButton = QPushButton(controller)
    controller.previousButton.setText("< Previous")
    controller.previousButton.setStyleSheet(QPushButtonStyle)
    controller.previousButton.move(
        controller.width() - 300, controller.height() - 37)
    controller.previousButton.clicked.connect(controller.root.previousPage)
    controller.previousButton.setCursor(Qt.PointingHandCursor)


def createCancelButton(controller, text="Cancel") -> None:
    controller.cancelButton = QPushButton(controller)
    controller.cancelButton.setText(text)
    controller.cancelButton.setStyleSheet(QPushButtonStyle)
    controller.cancelButton.move(
        controller.width() - 100, controller.height() - 37)
    controller.cancelButton.clicked.connect(controller.root.cancel)
    controller.cancelButton.setCursor(Qt.PointingHandCursor)

# endregion


"""Main component, to Manage all sceens/widgets."""


class Main(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle("Setup Wizard")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(800, 360)

        # Add steps widgets in order.
        self.addWidget(InitialScreen(self))
        self.addWidget(InstallationFolder(self))
        self.addWidget(SelectComponents(self))
        self.addWidget(LicenseAgreement(self))
        self.addWidget(ReadToInstall(self))
        self.addWidget(Install(self))
        self.addWidget(Finished(self))

    def nextPage(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def previousPage(self):
        self.setCurrentIndex(self.currentIndex() - 1)

    def cancel(self):
        self.close()

    def closeEvent(self, event):
        currentIndex = self.currentIndex()
        if currentIndex == 0 or currentIndex == 6:
            event.accept()
            self.destroy()
            app.quit()
        else:
            messageBox = QMessageBox(self)
            response = messageBox.question(
                self,
                "Installation Cancel",
                "Are you sure to cancel installation?",
                messageBox.Yes | messageBox.No,
                messageBox.No
            )

            if response == messageBox.Yes:
                currentWidget = self.widget(currentIndex)
                if hasattr(currentWidget, "process"):
                    currentWidget.process.terminate()
                    currentWidget.process.waitForFinished()
                event.ignore()
                self.setCurrentIndex(6)
                self.widget(6).label.setText("Installation Cancelled")
            else:
                event.ignore()

    def install(self):
        self.nextPage()
        self.currentWidget().install()

#region: Screens/Widgets


class InitialScreen(QFrame):
    labelHeaderText = labels["APPConfig"]

    def __init__(self, parent=None):
        super(InitialScreen, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)

        createTextFooter(self)
        createSideLabes(self, 0)

        createNextButton(self)
        createCancelButton(self, "Sair")

        # Create label for the first step.
        self.label = QLabel(self)
        self.label.setText(labels["Welcome"])
        self.label.setStyleSheet("color: black; font-size: 12px;")
        self.label.move(220, 90)


class InstallationFolder(QFrame):
    labelHeaderText = labels["InstallationFolder"]

    def __init__(self, parent=None):
        super(InstallationFolder, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)

        createTextFooter(self)
        createSideLabes(self, 1)

        createNextButton(self)
        createCancelButton(self)
        createPreviousButton(self)

        # Create label for the first step.
        self.label = QLabel(self)
        self.label.setText(labels["SubTitle"])
        self.label.setStyleSheet("color: black; font-size: 12px;")
        self.label.move(220, 90)

        # Create line edit for the second step.
        global directory
        self.lineEdit = QLineEdit(
            self, placeholderText=labels["SelectiFolderBtn"]
        )
        self.lineEdit.setText('{}'.format(directory))
        self.lineEdit.setFixedHeight(25)
        self.lineEdit.setFixedWidth(400)
        self.lineEdit.move(220, 110)
        self.lineEdit.textChanged.connect(self.onTextChanged)

        # Create QPushbutton to open a directory.
        self.pushButton = QPushButton(self)
        self.pushButton.setText(labels["SelectBtn"])
        self.pushButton.setStyleSheet(
            """
            QPushButton {
                background-color: #f7f7f7;
                font-size: 15px;
                color: black;
            }
            QPushButton:hover {
                font-size: 13px;
                padding-top: 1px;
                padding-left: 1px;
            }
            """
        )
        self.pushButton.setFixedWidth(100)
        self.pushButton.move(640, 110)
        self.pushButton.clicked.connect(self.openDirectory)
        self.pushButton.setCursor(Qt.PointingHandCursor)

    def openDirectory(self):
        global directory
        selectedDirectory = str(QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            os.path.expanduser('~'),
            QFileDialog.ShowDirsOnly
        ))
        if selectedDirectory == "":
            return
        else:
            directory = selectedDirectory
        self.lineEdit.setText('{}'.format(directory))

    def onTextChanged(self):
        global directory
        directory = self.lineEdit.text()


class SelectComponents(QFrame):
    labelHeaderText = labels["SelectComponents"]
    checkBoxes = {}

    def __init__(self, parent=None):
        super(SelectComponents, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)
        createSubtitleHeader(
            self,
            labels["SubtitleFolder"]
        )

        createTextFooter(self)
        createSideLabes(self, 2)

        createNextButton(self)
        createCancelButton(self)
        createPreviousButton(self)

        # Create frame to group the checkboxes.
        self.frame = QFrame(self)
        self.frame.setFixedWidth(380)
        self.frame.setFixedHeight(180)
        self.frame.move(220, 110)
        self.frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1.5px solid #adabab;
            }
            """
        )

        for app in appList:
            component = app["componentName"]
            index = appList.index(app)
            self.checkBoxes[component] = QCheckBox(self.frame)
            self.checkBoxes[component].setText(app["name"])
            self.checkBoxes[component].setCursor(Qt.PointingHandCursor)
            self.checkBoxes[component].move(20, 20 + (40 * index))
            self.checkBoxes[component].setChecked(app["selected"])
            self.checkBoxes[component].stateChanged.connect(
                partial(self.onCheckBoxChanged, component, app)
            )

        # Create Buttons.
        self.deselectAll = QPushButton(self)
        self.undoButton = QPushButton(self)
        self.selectAll = QPushButton(self)

        # Set Buttons text.
        self.undoButton.setText(labels["UndoBtn"])
        self.selectAll.setText(labels["SelectallBtn"])
        self.deselectAll.setText(labels["UnselectallBtn"])

        # Set Buttons position.
        self.deselectAll.move(450, 75)
        self.undoButton.move(220, 75)
        self.selectAll.move(315, 75)

        # Set Buttons style.
        buttonStyle = """
            QPushButton {
                background-color: #f7f7f7;
                font-size: 15px;
                color: black;
            }
            QPushButton:disabled {
                background-color: #d2d0d0;
                color: #312f2f;
            }
            QPushButton:hover {
                font-size: 13px;
                padding-top: 1px;
                padding-left: 1px;
            }
            """
        self.deselectAll.setStyleSheet(buttonStyle)
        self.undoButton.setStyleSheet(buttonStyle)
        self.selectAll.setStyleSheet(buttonStyle)

        # Change cursor to hand.
        self.deselectAll.setCursor(Qt.PointingHandCursor)
        self.undoButton.setCursor(Qt.PointingHandCursor)
        self.selectAll.setCursor(Qt.PointingHandCursor)

        # Connect Buttons to functions.
        self.deselectAll.clicked.connect(self.onDeselectAll)
        self.undoButton.clicked.connect(self.onSelectAll)
        self.selectAll.clicked.connect(self.onSelectAll)

        # Set button width.
        self.deselectAll.setFixedWidth(150)
        self.undoButton.setFixedWidth(85)
        self.selectAll.setFixedWidth(130)

        # Set buttons enebled state.
        self.selectAll.setDisabled(True)
        self.undoButton.setDisabled(True)
        self.deselectAll.setDisabled(False)

    def onCheckBoxChanged(self, component, app):
        global appList
        appList[appList.index(
            app)]["selected"] = self.checkBoxes[component].isChecked()
        self.validateCheckedButtons()

    def onSelectAll(self):
        global appList
        for app in appList:
            appList[appList.index(app)]["selected"] = True
            self.checkBoxes[app["componentName"]].setChecked(True)

        self.validateCheckedButtons()

    def onDeselectAll(self):
        global appList
        for app in appList:
            appList[appList.index(app)]["selected"] = False
            self.checkBoxes[app["componentName"]].setChecked(False)

        self.validateCheckedButtons()

    def validateCheckedButtons(self):
        global appList

        if all(app["selected"] for app in appList):
            self.selectAll.setDisabled(True)
            self.undoButton.setDisabled(True)
            self.deselectAll.setDisabled(False)

            self.nextButton.setDisabled(False)
        elif all(not app["selected"] for app in appList):
            self.selectAll.setDisabled(False)
            self.undoButton.setDisabled(False)
            self.deselectAll.setDisabled(True)

            self.nextButton.setDisabled(True)
        else:
            self.selectAll.setDisabled(False)
            self.undoButton.setDisabled(False)
            self.deselectAll.setDisabled(False)

            self.nextButton.setDisabled(False)


class LicenseAgreement(QFrame):
    labelHeaderText = labels["LicenseAgreement"]

    def __init__(self, parent=None):
        super(LicenseAgreement, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)

        createTextFooter(self)
        createSideLabes(self, 3)

        createNextButton(self)
        createCancelButton(self)
        createPreviousButton(self)

        self.liscenseAgreement = QTextEdit(
            self,
            readOnly=True,
            lineWrapColumnOrWidth=100,
        )
        self.liscenseAgreement.setFixedWidth(550)
        self.liscenseAgreement.setFixedHeight(220)
        self.liscenseAgreement.move(220, 77)

        with open('LiscenseAgreement.txt', 'r') as file:
            self.liscenseAgreement.setText(file.read())


class ReadToInstall(QFrame):
    labelHeaderText = labels["ReadyToInstall"]

    def __init__(self, parent=None):
        super(ReadToInstall, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)

        createTextFooter(self)
        createSideLabes(self, 4)

        createInstallButton(self)
        createCancelButton(self)
        createPreviousButton(self)

        self.readToInstall = QLabel(self)
        self.readToInstall.setText(self.labelHeaderText)
        self.readToInstall.move(220, 90)


class Install(QFrame):
    labelHeaderText = labels["Installing"]
    currentStep = None

    def __init__(self, parent=None):
        super(Install, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)

        createTextFooter(self)
        createSideLabes(self, 5)

        createNextButton(self, "Finish")
        createCancelButton(self)

        self.logText = QTextEdit(
            self,
            placeholderText='Application logs will be shown here...',
            readOnly=True
        )
        self.logText.setFixedWidth(560)
        self.logText.setFixedHeight(220)
        self.logText.move(220, 77)

    def install(self):
        global appList
        self.nextButton.setDisabled(True)
        appList = [app for app in appList if app["selected"]]

        if self.currentStep is not None:
            if len(self.currentStep["commands"]) > 0:
                step = self.currentStep["commands"].pop(0)
                self.startQprocess(step)
            else:
                self.currentStep = None
                self.install()
        elif len(appList) > 0:
            self.currentStep = appList.pop(0)
            self.logText.append(self.currentStep["step"])
            self.install()
        else:
            self.nextButton.setDisabled(False)
            self.logText.append("Installation finished.")

    def startQprocess(self, command):
        pattern = r"\{(.*?)\}"
        matches = re.findall(pattern, command)
        for match in matches:
            try:
                command = command.replace("{" + match + "}", globals()[match])
            except:
                pass

        self.process = QProcess()
        self.process.start(command)
        self.process.finished.connect(self.handle_finished)
        self.process.readyReadStandardOutput.connect(
            self.handle_readyReadStandardOutput
        )
        self.process.readyReadStandardError.connect(
            self.handle_readyReadStandardOutput
        )

    def handle_finished(self):
        exitCode = self.process.exitCode()
        if exitCode == 0:
            self.install()
        else:
            self.root.setCurrentIndex(6)
            self.root.widget(6).label.setText(
                f"Installation error finished with exit code {exitCode}"
            )

    def handle_readyReadStandardOutput(self):
        output = self.process.readAllStandardOutput()
        output = output.data().decode('utf-8').strip('\n')
        self.logText.append(output)


class Finished(QFrame):
    labelHeaderText = labels["Finished"]

    def __init__(self, parent=None):
        super(Finished, self).__init__()
        self.root = parent
        self.load_ui()

    def load_ui(self):
        self.setFixedSize(800, 360)

        createTextHeader(self)

        createTextFooter(self)
        createSideLabes(self, 6)

        createCancelButton(self, "Finish")

        # Create label for the first step.
        self.label = QLabel(self)
        self.label.setText(labels["Restart"])
        self.label.setStyleSheet("color: black; font-size: 14px;")
        self.label.move(220, 90)


# endregion


"""Password component, to request root password."""
# TODO: change to be more user friendly, like linux root password prompt screen.


class PasswordTest(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setFixedHeight(300)
        self.setFixedWidth(400)
        self.setWindowTitle("Root Password")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setStyleSheet("background-color: #ffffff;")

        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('images/user.png'))
        self.image.setScaledContents(True)
        self.image.setFixedWidth(160)
        self.image.setFixedHeight(160)
        self.image.move(120, 0)

        self.entry = QLineEdit(self)
        self.entry.setEchoMode(QLineEdit.Password)
        self.entry.setPlaceholderText("Enter with root password")
        self.entry.setToolTip("Enter with root password")
        self.entry.setFixedHeight(30)
        self.entry.setFixedWidth(250)
        self.entry.move(82, 180)

        self.enterBtn = QPushButton("Enter", self)
        self.enterBtn.setCursor(Qt.PointingHandCursor)
        self.enterBtn.move(165, 230)

        self.entry.returnPressed.connect(self.on_returnPressed)
        self.enterBtn.clicked.connect(self.entry_cb)

    def entry_cb(self, event):
        self.turn_as_root()

    def on_returnPressed(self):
        self.turn_as_root()

    def turn_as_root(self):
        password = self.entry.text().strip()
        if password == "":
            return

        global passwd
        global isClosed
        passwd = password
        exitCode = os.system("echo "+password+" | sudo -S echo ''")
        if exitCode == 0:
            isClosed = True
            self.close()
        else:
            self.entry.setText("")
            self.entry.setPlaceholderText("Wrong password ... try again")


"""
    List of apps to install.
    Each app is a dictionary with the following keys:
    - name: name of the app to show in the selection list
    - selected: boolean, if the app is selected or not
    - step: string, the step to install the app, this is gonna be logged in the log text
    - commands: list of commands to run during the installation, each script is a string
        and can contain variables, for example:
        - "echo 'Installing {app}'" and app is the global variable app
    - componentName: name of the component to install

    Observation:
    - The order of the apps is important, the first app will be installed first,
    - The last app will be installed last,
    - The apps list supports only 4 steps, in the future this will be changed to accept more steps, with no limit.
"""
appList = [
    {
        "name": "myApp Client",
        "step": "Installing myApp Client APP.",
        "commands": [
            "echo myApp Client gonna be installed in few seconds...",
            "sleep 2",
            "echo Installation is done!",
        ],
        "selected": True,
        "componentName": "client"
    }
]

QPushButtonStyle = """
QPushButton {
    background-color: #f7f7f7;
    font-size: 15px;
    color: black;
}
QPushButton:hover {
    font-size: 13px;
    padding-top: 1px;
    padding-left: 1px;
}
QPushButton:disabled {
    background-color: #d2d0d0;
    color: #312f2f;
}
"""

passwd = ""
version = '{{version}}'
platform = '{{platform}}'
directory = "/usr/local/myApp/"

if __name__ == "__main__":
    isClosed = False
    euid = os.geteuid()

    if euid != 0:
        passApp = QApplication(sys.argv)
        widget = PasswordTest()
        widget.show()

        try:
            sys.exit(passApp.exec_())
        except:
            print("Pass app quiting...")

    if isClosed == False:
        sys.exit(1)

    # Create an PyQT5 application object.
    app = QApplication(sys.argv)
    mainScreen = Main()
    mainScreen.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
