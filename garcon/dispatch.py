import logging


class Dispatcher:
    """
    Accepts commands from the user, dispatches them to the appropriate plugin.
    """
    # The history interface should maybe capture the agent and the command that
    # was used, so that something like "re-dispatch" can be implemented.

    def initialize(self, app):
        self.plugin_manager = app.plugin_manager
        self._refresh_agents()
        self.command_history = []

    def dispatch_from_interface(self, command):
        self._dispatch(command)
        self.command_history.insert(0, command)

    def _dispatch(self, command):
        """
        Dispatches the command to the lowest priority plugin that can handle __init__.
        """
        logging.info("Dispatch received command '%s'. Looking for an agent who can handle it." %
                     (command))
        logging.debug("Currently have %d agents." % (len(self._active_agents)))
        for agent in self._active_agents:
            if agent.can_handle(command):
                logging.info("Agent %s can handle command '%s', dispatching command to it." %
                             (agent.name, command))
                agent.handle(command)
                return
        logging.info("Dispatch couldn't find an agent to handle command '%s'." % (command))

    def dispatch_command(self, command):
        """
        Dispatches command as though it came from the user interface.
        """
        # TODO: log somehow what plugin/agent/service dispatched this.
        logging.debug("Dispatch received the command '%s' from a plugin. Dispatching." % (command))
        self._dispatch(command)

    def _refresh_agents(self):
        """
        Makes sure the _active_agents list is up to date.
        """
        active_agents = self.plugin_manager.get_active_agents()
        self._active_agents = sorted(active_agents)

    def get_command_history(self, how_many=None):
        if how_many is None:
            return list(self.command_history)
        return self.command_history[:how_many]
