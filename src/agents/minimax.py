import time
from src.agents.agent import Agent
from random import shuffle


class MinimaxABAgent(Agent):
    """
        Minimax agent with Alpha Beta Pruning inspired from https://github.com/haryoa/evo-pawness/blob/master/ai_modules/classic_algorithm.py
    """
    def __init__(self, max_depth=4, player_color=0):
        """
        Initiation
        Parameters
        ----------
        max_depth : int
            The max depth of the tree
        player_color : int
            The player's index as MAX in minimax algorithm
        """
        super(MinimaxABAgent, self).__init__()
        self.max_depth = max_depth
        self.player_color = player_color
        self.node_expanded = 0

    def enemy_turn_action(self, action_key, new_state):
        """
        Nothing to do here
        """
        pass

    def choose_action(self, state):
        """
        Predict the move using minimax alpha beta pruning algorithm
        Parameters
        ----------
        state : State
        Returns
        -------
        float, str:
            The evaluation or utility and the action key name
        """
        self.node_expanded = 0

        start_time = time.time()

        print("MINIMAX AB : Wait AI is choosing")
        list_action = self.get_possible_action(state)
        eval_score, selected_key_action = self._minimax(0, state, True, float('-inf'), float('inf'))
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        print("--- %s seconds ---" % (time.time() - start_time))

        return selected_key_action, list_action[selected_key_action]

    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):
        """
        Helper function of minimax
        :param current_depth: The current depth on the tree in recursive
        :param state: State of the current node in recursive
        :param is_max_turn: Check if the current node is the max turn in recursive
        :param alpha: parameter of AB Prunning, save the current maximizer best value
        :param beta: parameter of AB Prunning, save the current minimizer best value
        :return: int , str The value of the best action and the name of the action
        """
        if current_depth == self.max_depth or state.is_terminal():
            return self.evaluation_function(state, self.player_color), ""

        self.node_expanded += 1

        possible_action = self.get_possible_action(state)
        key_of_actions = list(possible_action.keys())

        shuffle(key_of_actions) # add randomness here
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = self.result_function(state,possible_action[action_key])

            eval_child, action_child = self._minimax(current_depth+1, new_state, not is_max_turn, alpha, beta)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_key
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_key
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, action_target
