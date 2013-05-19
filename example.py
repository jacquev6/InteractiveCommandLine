import InteractiveCommandLine as ICL


class Printer:
    def __init__(self):
        self.verbose = False
        self.upper = False

    def do(self, message):
        if self.verbose:
            message = "Verbose " + message
        if self.upper:
            message = message.upper()
        print message


class ExampleProgram(ICL.Program):
    def __init__(self):
        ICL.Program.__init__(self, "example")
        self.__printer = Printer()
        self.addCommand(self.Echo(self.__printer))
        self.addOption(ICL.StoringOption("verbose", self.__printer, "verbose", True, False))

    class Echo(ICL.Command):
        def __init__(self, printer):
            ICL.Command.__init__(self, "echo")
            self.__printer = printer
            self.addOption(ICL.StoringOption("upper", printer, "upper", True))

        def execute(self, *text):
            self.__printer.do(" ".join(text))

ExampleProgram().execute()
