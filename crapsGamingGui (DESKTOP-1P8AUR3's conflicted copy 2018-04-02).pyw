__author__ = 'Mihir Shrestha'

from die import *
import random, sys, logging, crapsResources_rc, pickle
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox


class AppSettings(QDialog):
    def __init__(self, parent = None):
        # super(AppSettings, self).__init__(parent)
        super().__init__(parent)
        uic.loadUi('settings.ui', self)

        if crapsApp.initializationLogging == True:
            logging.info("Initialized settings app")

        self.buttonBox.accepted.connect(crapsApp.saveSettings)
        self.buttonBox.rejected.connect(lambda: self.close())

        self.restartButton.clicked.connect(crapsApp.restart)
        self.clearLog.clicked.connect(crapsApp.deleteLog)
        self.restoreButton.clicked.connect(self.restoreEverything)

        self.alwaysWinButton.toggled.connect(lambda: crapsApp.changeDifficulty(1))
        self.easyButton.toggled.connect(lambda: crapsApp.changeDifficulty(2))
        self.mediumButton.toggled.connect(lambda: crapsApp.changeDifficulty(3))
        self.hardButton.toggled.connect(lambda: crapsApp.changeDifficulty(4))
        self.impossibleButton.toggled.connect(lambda: crapsApp.changeDifficulty(5))
        self.enabledCheck.toggled.connect(self.loggingControl)

        self.classicTheme.toggled.connect(self.classicThemeApply)
        self.rainbowTheme.toggled.connect(self.rainbowThemeApply)
        self.laNoireTheme.toggled.connect(self.laNoireThemeApply)
        self.naturalTheme.toggled.connect(self.naturalThemeApply)

    def restoreEverything(self):
        crapsApp.difficultyLevel = 3
        crapsApp.minimumBet = 1
        crapsApp.maximumBet = 1000
        crapsApp.startingBank = 1000

        self.startingBankSpin.setValue(1000)
        self.minimumBetSpin.setValue(1)
        self.maximumBetSpin.setValue(1000)

        self.mediumButton.setChecked(True)
        self.classicThemeApply()
        self.classicTheme.setChecked(True)
        self.enabledCheck.setChecked(False)
        self.loggingControl()

    def classicThemeApply(self):
        if crapsApp.methodsLogging == True:
            logging.info("Called classicThemeApply method")

        crapsApp.centralwidget.setStyleSheet("")
        crapsApp.statusbar.setStyleSheet("")

    def rainbowThemeApply(self):
        if crapsApp.methodsLogging == True:
            logging.info("Called rainbowThemeApply method")

        crapsApp.centralwidget.setStyleSheet("background-color: #329992; color: black")
        crapsApp.statusbar.setStyleSheet("background-color: #329992; color: black;")


    def laNoireThemeApply(self):
        if crapsApp.methodsLogging == True:
            logging.info("Called laNoireThemeApply method")

        crapsApp.centralwidget.setStyleSheet("background-color: #462E2E; color: white;")
        crapsApp.statusbar.setStyleSheet("background-color: #462E2E; color: white;")

    def naturalThemeApply(self):

        if crapsApp.methodsLogging == True:
            logging.info("Called naturalThemeApply method")

        crapsApp.centralwidget.setStyleSheet("background-color: #8ff442; color: #000000;")
        crapsApp.statusbar.setStyleSheet("background-color: #8ff442; color: #000000;")

    def loggingControl(self):

        if crapsApp.methodsLogging == True:
            logging.info("Called loggingControl method")

        if self.enabledCheck.isChecked():
            self.difficultyCheck.setEnabled(True)
            self.errorsCheck.setEnabled(True)
            self.winsCheck.setEnabled(True)
            self.lossesCheck.setEnabled(True)
            self.rollsCheck.setEnabled(True)
            self.bankCheck.setEnabled(True)
            self.methodsCheck.setEnabled(True)
            self.initializationCheck.setEnabled(True)
            self.warningsCheck.setEnabled(True)

        else:
            self.difficultyCheck.setEnabled(False)
            self.errorsCheck.setEnabled(False)
            self.winsCheck.setEnabled(False)
            self.lossesCheck.setEnabled(False)
            self.rollsCheck.setEnabled(False)
            self.bankCheck.setEnabled(False)
            self.methodsCheck.setEnabled(False)
            self.initializationCheck.setEnabled(False)
            self.warningsCheck.setEnabled(False)


class HelpWindow(QDialog):
    def __init__(self, parent = None):
        # super(HelpWindow, self).__init__(parent)
        super().__init__(parent)
        uic.loadUi("helpDialog.ui", self)
        if crapsApp.initializationLogging == True:
            logging.info("Initialized help app")


class CrapsGame(QMainWindow):
    """A game of craps."""

    def __init__(self, parent = None):
        """Build a game with two dice."""

        super().__init__(parent)
        uic.loadUi("crapsUI.ui", self)

        self.actionHelp.triggered.connect(self.help)
        self.actionSettings.triggered.connect(self.settingView)
        self.cancelRoll.clicked.connect(self.cancelCurrentRoll)
        self.rollButton.clicked.connect(self.betChangedHandler)
        self.moneyBet.textChanged.connect(self.betVerifier)
        self.cancelRoll.setDisabled(True)

        self.bankPreference = 1000
        self.winsCount = 0
        self.lossesCount = 0
        self.currentBet = 10
        self.startingBank = self.bankPreference
        self.currentBank = self.startingBank
        self.currentRoll = 0
        self.secondRoll = False
        self.previousRoll = 0
        self.die1 = Die(6)
        self.die2 = Die(6)
        self.die1.setValue(6)
        self.die2.setValue(6)
        self.payout = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 1.2}
        self.results ="Welcome to the game of Craps!"
        self.betWins = 0
        self.betLosses = 0
        self.rollAmt = 0
        self.preferredDifficultyLevel = 3
        self.difficultyLevel = self.preferredDifficultyLevel
        self.minimumBet = 1
        self.maximumBet = self.currentBank
        self.logging = False
        self.difficultyLogging = False
        self.errorsLogging = False
        self.winsLogging = False
        self.lossesLogging = False
        self.rollsLogging = False
        self.bankLogging = False
        self.methodsLogging = False
        self.initializationLogging = False
        self.warningsLogging = False

        if self.initializationLogging:
            logging.info("Initialized game app")

    def __str__(self):
        """String representation for Dice"""
        return ""

    def getPreviousRoll(self):
        if self.methodsLogging:
            logging.info("Reached getPreviousRoll method")
        return self.previousRoll

    def setCurrentRoll(self, currentRoll):
        if self.methodsLogging:
            logging.info("Reached setCurrentRoll method")
        self.currentRoll = currentRoll

    def getCurrentRoll(self):
        if self.methodsLogging:
            logging.info("Reached getCurrentRoll method")
        return self.currentRoll

    def setCurrentBank(self, currentBank):
        if self.methodsLogging:
            logging.info("Reached setCurrentBank method")
        self.currentBank = currentBank

    def getCurrentBank(self):
        if self.methodsLogging:
            logging.info("Reached getCurrentBank method")
        return self.currentBank

    def setWinsCount(self, winsCount):
        if self.methodsLogging:
            logging.info("Reached setWinsCount method")
        self.winsCount = winsCount

    def getWinsCount(self):
        if self.methodsLogging:
            logging.info("Reached getWinsCount method")
        return self.winsCount

    def setLossesCount(self, lossesCount):
        if self.methodsLogging:
            logging.info("Reached setLossesCount method")
        self.lossesCount = lossesCount

    def getLossesCount(self):
        if self.methodsLogging:
            logging.info("Reached getLossesCount method")
        return self.lossesCount

    def setCurrentBet(self, currentBet):
        if self.methodsLogging:
            logging.info("Reached setCurrentBet method")
        self.currentBet = currentBet

    def getCurrentBet(self):
        if self.methodsLogging:
            logging.info("Reached getCurrentBet method")
        return self.currentBet

    def setStartingBank(self, startingBank):
        if self.methodsLogging:
            logging.info("Reached setStartingBank method")
        self.startingBank = startingBank

    def getStartingBank(self):
        if self.methodsLogging:
            logging.info("Reached getStartingBank method")
        return self.startingBank

    def placeBet(self, betValue):
        if self.methodsLogging:
            logging.info("Reached placeBet method")
        self.setCurrentBet(betValue)

    def settingView(self):
        if self.methodsLogging:
            logging.info("Reached settingView method")
        settingApp.clearLog.setEnabled(True)
        settingApp.setModal(True)
        settingApp.show()

    def help(self):
        if self.methodsLogging:
            logging.info("Reached help method")
        helpApp.show()

    def changeDifficulty(self, difficulty):
        if self.methodsLogging:
            logging.info("Reached changeDifficulty method")
        self.preferredDifficultyLevel = difficulty

    def saveSettings(self):
        if self.methodsLogging:
            logging.info("Reached saveSettings method")

        self.difficultyLevel = self.preferredDifficultyLevel
        self.bankPreference = settingApp.startingBankSpin.value()
        self.minimumBet = settingApp.minimumBetSpin.value()
        self.maximumBet = settingApp.maximumBetSpin.value()

        self.checkOptions = [settingApp.difficultyCheck, settingApp.errorsCheck, settingApp.winsCheck, settingApp.lossesCheck, settingApp.rollsCheck, settingApp.bankCheck, settingApp.warningsCheck, settingApp.initializationCheck, settingApp.methodsCheck]

        if self.difficultyLogging:
            logging.info("Changed difficulty level to " + str(self.difficultyLevel))

        if settingApp.enabledCheck.isChecked():
            self.logging = True
            for checkElement in self.checkOptions:
                if checkElement.isChecked():
                    exec("self." + checkElement.text().lower() + "Logging = True")
                else:
                    exec("self." + checkElement.text().lower() + "Logging = False")
            # print("self.difficultyLogging", self.difficultyLogging)
            # print("self.winsLogging", self.winsLogging)
            # print("self.methodsLogging", self.methodsLogging)
            # print("self.rollsLogging", self.rollsLogging)
            # print("self.errorsLogging", self.errorsLogging)
            # print("self.lossesLogging", self.lossesLogging)
            # print("self.bankLogging", self.bankLogging)
            # print("self.initializationLogging", self.initializationLogging)
            # print("self.warningsLogging", self.warningsLogging)

        else:
            self.logging = False
            for checkElement in self.checkOptions:
                exec("self." + checkElement.text().lower() + "Logging = False")

        self.updateUI()
        settingApp.close()

    def updateUI(self):
        if self.methodsLogging:
            logging.info("Reached updateUI method")

        if self.getCurrentBank() <= 0:
            if self.bankLogging:
                logging.info("Game over")
            self.hint.setText('Game over. You rolled the dice a total of %i times. Go to settings and click restart to play again!' %                           self.rollAmt)
            self.rollButton.setEnabled(False)
            self.moneyBet.setEnabled(False)
        # self.winsLabel.setText(str(self.getWinsCount()))
        # self.lossesLabel.setText(str(self.getLossesCount()))
        self.resultLabel.setText(self.results)
        self.bank.setText(str("$" + str(self.getCurrentBank())))
        # self.netProfit.setText("$" + str(self.currentBank - self.startingBank))
        # self.profitAmt.setText("$ +" + str(self.betWins))
        # self.lossAmt.setText("$ -" + str(self.betLosses))
        self.die1View.setPixmap(QtGui.QPixmap(":/" + str(self.die1.getValue())))
        self.die2View.setPixmap(QtGui.QPixmap(":/" + str(self.die2.getValue())))

    @pyqtSlot() #player asked for a roll
    def rollAction(self):
        if self.methodsLogging:
            logging.info("Reached rollAction method")

        self.rollAmt += 1

        if self.rollsLogging:
            logging.info("Increased roll amount to {}".format(self.rollAmt))

        self.hint.setText("")

        if self.difficultyLevel == 3:
            self.currentRoll = self.die1.roll(self.difficultyLevel) + self.die2.roll(self.difficultyLevel)
        else:
            self.currentRoll = self.die1.roll(self.difficultyLevel)
            if self.currentRoll < 7:
                self.die1.setValue(random.choice([x for x in range(1, self.currentRoll)])) # It's a throwaway variable, so I am using x.
            else:
                self.die1.setValue(random.choice([x for x in range(self.currentRoll - 6, 7)]))
            self.die2.setValue(self.currentRoll - self.die1.getValue())

        if self.rollsLogging:
            logging.info("Rolled {} & {}".format(self.die1.getValue(), self.die2.getValue()))

        self.results = "You rolled a %i and will have to roll again to win money." % (self.currentRoll)
        if self.secondRoll == False:
            if self.rollsLogging:
                logging.info("Rolled a first roll")

            if self.currentRoll == 7 or self.currentRoll == 11:
                if self.winsLogging:
                    logging.info("Won ${}".format(self.getCurrentBet()))

                self.results = "You win $%i!" % self.getCurrentBet()
                self.betWins += self.getCurrentBet()

                self.currentBank += self.getCurrentBet()

                if self.bankLogging:
                    logging.info("Bank amount increased to {}".format(self.currentBank))

                self.winsCount += 1

                if self.winsLogging:
                    logging.info("Increased wins amount to {}".format(self.winsCount))

            elif self.currentRoll == 2 or self.currentRoll == 3 or self.currentRoll == 12:

                self.results = "You lose $%i!" % self.getCurrentBet()
                self.betLosses += self.getCurrentBet()
                self.lossesCount += 1
                self.currentBank -= self.getCurrentBet()

                if self.bankLogging:
                    logging.info("Lost ${}".format(self.getCurrentBet()))

                if self.lossesLogging:
                    logging.info("Increased losses amount to {}".format(self.lossesCount))
            else:
                self.secondRoll = True
                self.previousRoll = self.currentRoll
                self.hint.setText("You may also choose to not roll again to only lose your placed amount bet without payout ratios.")
                self.moneyBet.setEnabled(False)
                self.cancelRoll.setEnabled(True)

                if self.rollsLogging:
                    logging.info("Got option to have a second roll")
        else:
            if self.rollsLogging:
                logging.info("Reached second roll")
            if self.previousRoll == self.currentRoll:
                self.winsCount += 1
                self.betAmt = int(self.getCurrentBet() * self.payout[self.getPreviousRoll()])
                self.currentBank += self.betAmt
                self.results = "You win $%i!" % self.betAmt
                self.betWins += self.betAmt

                if self.winsLogging:
                    logging.info("Increased wins amount to {}".format(self.winsCount))

                if self.bankLogging:
                    logging.info("Won ${}".format(self.betAmt))
            else:
                self.lossesCount += 1
                self.betAmt = int(self.getCurrentBet() * self.payout[self.getPreviousRoll()])
                self.currentBank -= self.betAmt
                self.results = "You lose $%i!" % self.betAmt
                self.betLosses += self.betAmt

                if self.lossesLogging:
                    logging.info("Increased losses amount to {}".format(self.winsCount))

                if self.bankLogging:
                    logging.info("Lost ${}".format(self.betAmt))

            self.moneyBet.setEnabled(True)
            self.cancelRoll.setEnabled(False)
            self.secondRoll = False
        self.updateUI()

    def betVerifier(self):
        if self.methodsLogging:
            logging.info("Reached betVerifier method")
        try:
            moneyBet = int(self.moneyBet.toPlainText())
            if moneyBet <= 0:
                self.results = "You cannot bet with amounts less than 0 or 0 itself."
                self.rollButton.setEnabled(False)

            elif moneyBet > self.maximumBet:
                self.results = "This bet of ${} is too high. Please change your settings or reduce ${} from your bet.".format(moneyBet, moneyBet - self.maximumBet)
                self.rollButton.setEnabled(False)

            elif moneyBet < self.minimumBet:
                self.results = "This bet of ${} is too low. Please change your settings or add ${} to your bet.".format(moneyBet, self.minimumBet - moneyBet)
                self.rollButton.setEnabled(False)

            elif moneyBet > self.getCurrentBank():
                self.results = "Error, you cannot bet with what you do not have. Please try again."
                self.rollButton.setEnabled(False)

            else:
                self.results = "Would you like to bet with $%i?" % moneyBet
                self.rollButton.setEnabled(True)
        except:
            moneyBet2 = self.moneyBet.toPlainText()
            if moneyBet2 == "":
                self.results = "Please type in something as a bet. You cannot bet nothing."
                self.rollButton.setEnabled(False)
            else:
                self.results = "Please type in an integer as a bet."
                self.rollButton.setEnabled(False)
        self.updateUI()

    @pyqtSlot() #player clicking the roll button
    def betChangedHandler(self):
        if self.methodsLogging:
            logging.info("Reached betChangedHandler method")
        try:
            moneyBet = int(self.moneyBet.toPlainText())
            # if self.getCurrentBank() <= 0:
            #     self.results = "Game over. You rolled the dice a total of %i times." % self.rollAmt
            #     self.hint.setText('Click restart to play again!')
            #     self.rollButton.setEnabled(False)
            #     self.moneyBet.setEnabled(False)
            # elif moneyBet <= 0:
            #     self.results = "You cannot bet with amounts less than 0 or 0 itself."
            #     self.rollButton.setEnabled(False)

            if moneyBet > self.maximumBet:
                self.results = "This bet of {} is too high. Please change your settings or reduce ${} from your bet.".format(moneyBet, moneyBet - self.maximumBet)
                self.rollButton.setEnabled(False)
                self.updateUI()
                return

            if moneyBet < self.minimumBet:
                self.results = "This bet of {} is too low. Please change your settings or add ${} to your bet.".format(moneyBet, self.minimumBet - moneyBet)
                self.rollButton.setEnabled(False)
                self.updateUI()
                return

            if moneyBet <= self.getCurrentBank():
                self.setCurrentBet(int(self.moneyBet.toPlainText()))
                self.rollAction()
            else:
                self.results = "Error, you cannot bet with what you do not have. Please try again."
                self.rollButton.setEnabled(False)

        except:
            print(self.moneyBet.toPlainText())
            self.results = "Please type in an integer as a bet."
            self.rollButton.setEnabled(False)
        self.updateUI()

    def cancelCurrentRoll(self):
        if self.methodsLogging:
            logging.info("Reached cancelCurrentRoll method")

        self.currentBank -= self.currentBet
        self.results = "You have decided to not roll and have lost your initial bet amount of $%i." % self.getCurrentBet()
        self.betLosses += self.currentBet
        self.hint.setText("")
        self.updateUI()
        self.cancelRoll.setEnabled(False)
        self.moneyBet.setEnabled(True)

        if self.rollsLogging:
            logging.info("Did not reach second roll")

        if self.bankLogging:
            logging.info("Lost ${}".format(self.currentBet))

    def restart(self):
        if self.methodsLogging:
            logging.info("Reached restart method")
        self.bankPreference = settingApp.startingBankSpin.value()
        self.winsCount = 0
        self.lossesCount = 0
        self.currentBet = 10
        self.startingBank = self.bankPreference
        self.currentBank = self.startingBank
        self.currentRoll = 0
        self.secondRoll = False
        self.previousRoll = 0
        self.results = "You have restarted the game."
        self.moneyBet.setEnabled(True)
        self.hint.setText("")
        self.rollButton.setEnabled(True)
        self.cancelRoll.setEnabled(False)
        self.betWins = 0
        self.betLosses = 0
        self.rollAmt = 0
        self.updateUI()

    def deleteLog(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, Qt.red)
        self.setPalette(palette)
        open("craps.log", 'w').close()
        logging.info("Cleared log")
        settingApp.clearLog.setEnabled(False)

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__== "__main__":
    app = QApplication(sys.argv)
    logger = logging.basicConfig(filename='craps.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s Ln %(lineno)d: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    crapsApp = CrapsGame()
    helpApp = HelpWindow()
    settingApp = AppSettings()
    crapsApp.updateUI()
    crapsApp.show()
    sys.exit(app.exec_())
