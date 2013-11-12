def accept_commands_forever(dispatcher):
    print_intro()
    while True:
        command = get_command()
        dispatcher.dispatch(command)


def print_intro():
    print("How may Garçon be of service?")


def get_command():
    return input('Garçon!>>> ')
