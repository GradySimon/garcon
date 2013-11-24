import garcon.plugin


class NoAgentAgent(garcon.plugin.AgentBase):
    priority = 10
    name = "NoAgentAgent"

    def can_handle(self, command):
        return True

    def handle(self, command):
        # TODO: Integrate with Indentity
        print("I do apologize, sir. I'm afraid I do not know how to do that. "
              "Might I suggest installing more plugins?")


class QuitAgent(garcon.plugin.AgentBase):
    name = "QuitAgent"

    def can_handle(self, command):
        return command.strip().lower() in ["close",
                                           "goodbye",
                                           "bye",
                                           "exit",
                                           "quit",
                                           "go away"]

    def handle(self, command):
        # TODO: integrate with Indentity
        pass
