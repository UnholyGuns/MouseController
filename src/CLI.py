from states import StateNames
import sys
import select

class CommandInterface:

    MAX_CMD_LEN = 20

    def __init__(self, controller):
        self.controller = controller

        self.poller = select.poll()
        self.poller.register(sys.stdin, select.POLLIN)
        self.commandBuff = ""



    def begin(self):
        print("Mouse Controller")
        print("Type 'help' for available commands.")
        print("> ", end="")



    def run(self):
        if self.poller.poll(0):
            char = sys.stdin.read(1)

            if char == "\n":
                self.processCommand()

            elif char == "\b":
                self.commandBuff = self.commandBuff[:-1]

            elif len(self.commandBuff) < self.MAX_CMD_LEN: 
                self.commandBuff += char



    def processCommand(self):

        command = self.commandBuff.strip().lower()

        if command == "record":
            self.controller.nextState = StateNames.RECORDING

        elif command == "play":
            self.controller.nextState = StateNames.PLAYBACK

        elif command == "stop":
            self.controller.nextState = StateNames.IDLE

        elif command == "help":
            self.printHelp()

        elif command == "":
            pass

        else:
            print("Unrecognized command")
            self.printHelp()

        self.commandBuff = ""
        print("> ", end="")



    def printHelp(self):
        print("")
        print("Available commands:")
        print("  record   Start recording")
        print("  play     Play current recording")
        print("  stop     Stop recording/playback")
        print("  help     Show this menu")
        print("")