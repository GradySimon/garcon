import re
import garcon.plugin


class DoAgainAgent(garcon.plugin.AgentBase):
    name = "DoAgainAgent"
    priority = 4

    def can_handle(self, command):
        return command.strip().lower() in ["do that again", "do again", "again"]

    def handle(self, command):
        dispatcher = self.plugin_manager.get_dispatcher()
        previous_command = dispatcher.get_command_history(how_many=1)[0]
        dispatcher.dispatch_command(previous_command)


class DoMultipleTimesAgent(garcon.plugin.AgentBase):
    name = "DoMultipleTimesAgent"
    priority = 3
    _can_handle_matcher = re.compile("^(.+)\s+(\d+)\stimes\s*$")

    def can_handle(self, command):
        return self._can_handle_matcher.match(command)

    def handle(self, command):
        match = self._can_handle_matcher.match(command)
        if match:
            command_to_repeat = match.group(1)
            times_to_repeat = int(match.group(2))
            for i in range(times_to_repeat):
                self.plugin_manager.get_dispatcher().dispatch_command(command_to_repeat)
