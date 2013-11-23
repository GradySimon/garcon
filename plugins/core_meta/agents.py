import re
import garcon.plugin
import garcon.dispatch

class DoAgainAgent(garcon.plugin.AgentBase):
    name = "DoAgainAgent"
    priority = 4

    def can_handle(self, command):
        return command.lower() in ["do that again", "again"]


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
            for i in xrange(times_to_repeat):
                