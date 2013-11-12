def accept_commands_forever(dispatcher):
    print_intro()
    while True:
        print_prompt()
        command = get_command()
        dispatcher.dispatch(command)


def print_intro():
    print("How may Garçon be of service?")


def print_prompt():
    print("Garçon!>>>", end='')