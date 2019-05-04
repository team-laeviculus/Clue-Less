

"""
This file contains common classes each game might need,
or the Server needs to keep track of persistently.
"""


# State Machine Data
class GameState:

    # STATES
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    GAME_RUNNING = "GAME_RUNNING"
    GAME_VER = "GAME_OVER"

    def __init__(self):
        self.CURRENT_STATE = self.WAITING_FOR_PLAYERS

    def set_state(self, state):
        """
        Note: No state validation
        :param state: A game state from the static class variables above
        :return:
        """
        if hasattr(self, state):
            self.CURRENT_STATE = state
        else:
            raise Exception(f"GameState Exception! Unknown State {state}")

    def get_state(self):
        return self.CURRENT_STATE

    def __repr__(self):
        return f"GameState: {self.CURRENT_STATE}"
