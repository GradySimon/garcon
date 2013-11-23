class ConsoleInterface():
    def start(self, dispatcher):
        print_intro()
        while True:
            command = get_command()
            self.dispatcher.dispatch(command)

    def initialize(self, app):
        self.dispatcher = app.dispatcher


def print_intro(self):
    print("How may Garçon be of service?")


def get_command(self):
    return input('Garçon!>>> ')
