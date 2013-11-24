class ConsoleInterface():
    def start(self):
        print_intro()
        while True:
            command = get_command()
            if len(command) > 0:
                self.dispatcher.dispatch_from_interface(command)

    def initialize(self, app):
        self.dispatcher = app.dispatcher


def print_intro():
    print("How may Garçon be of service?")


def get_command():
    return input('Garçon!>>> ')
