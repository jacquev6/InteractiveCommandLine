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
        ICL.Program.__init__(self)
        self.__printer = Printer()
        self.addCommand("echo", self.Echo(self.__printer))
        self.addOption("verbose", self.Verbose(self.__printer))

    class Verbose(ICL.Option):
        def __init__(self, printer):
            ICL.Option.__init__(self)
            self.__printer = printer

        def activate(self, *args):
            self.__printer.verbose = True
            return args

    class Echo(ICL.Command):
        def __init__(self, printer):
            ICL.Command.__init__(self)
            self.__printer = printer
            self.addOption("upper", self.Upper(printer))

        class Upper(ICL.Option):
            def __init__(self, printer):
                ICL.Option.__init__(self)
                self.__printer = printer

            def activate(self):
                self.__printer.upper = True
                return args

        def execute(self, *text):
            self.__printer.do(" ".join(text))

ExampleProgram().execute()
