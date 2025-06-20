import texas_holdem.game.visualize_utils as U
from texas_holdem.game.players import BasePokerPlayer
import os
import json
from datetime import datetime
from memory import create_memory_from_config, MemoryConfig, ModelApiType

class BaseAgent(BasePokerPlayer):
    def __init__(self, agent_name=None, input_receiver=None):
        self.agent_name = agent_name or "BaseAgent"
        self.input_receiver = (
            input_receiver if input_receiver else self.__gen_raw_input_wrapper()
        )
        
        # Initialize memory system
        self.memory_dir = f"texas_holdem/memory/{self.agent_name}"
        self._setup_memory_system()
        
        # Game state tracking
        self.round_count = 0
        self.game_info = None
        self.opponents_actions = []
        self.opponents_expressions = []
        self.my_actions_history = []
        self.my_expressions_history = []
        self.my_thoughts_history = []
        
        # Data for external logging
        self.last_thought = None
        self.last_expression = None
        self.last_action = None

    def declare_action(self, valid_actions, hole_card, round_state):
        print(
            U.visualize_declare_action(valid_actions, hole_card, round_state, self.uuid)
        )
        
        # Generate thought about the situation
        thought = self._generate_thought(valid_actions, hole_card, round_state)
        self.last_thought = thought
        
        # Get action from decision-making process
        action, amount = self._make_decision(valid_actions, hole_card, round_state, thought)
        self.last_action = {"action": action, "amount": amount}
        
        # Generate expression based on action
        expression = self._generate_expression(action, amount, round_state)
        self.last_expression = expression
        
        # Store the action, thought, and expression
        self._store_action_and_expression(action, amount, expression, thought, round_state)
        
        # Print expression (if agents should express themselves)
        print(f"[{self.agent_name}]: {expression}")
        
        return action, amount
    
    def _generate_thought(self, valid_actions, hole_card, round_state):
        """Generate internal thought about the current situation. Override in LLM agents."""
        return f"Analyzing situation with {len(valid_actions)} valid actions."
    
    def _make_decision(self, valid_actions, hole_card, round_state, thought):
        """Make the actual decision. Base implementation uses console input."""
        return self.__receive_action_from_console(valid_actions)

    def receive_game_start_message(self, game_info):
        print(U.visualize_game_start(game_info, self.uuid))
        self.game_info = game_info
        
        # Summarize rules before the first round
        rule_summary = self._summarize_rules()
        print(f"[{self.agent_name}] Rules summarized and stored.")
        
        self.__wait_until_input()

    def receive_round_start_message(self, round_count, hole_card, seats):
        print(U.visualize_round_start(round_count, hole_card, seats, self.uuid))
        self.round_count = round_count
        
        # Store opponent's action on the last round in memory
        stored_info: str = ''.join(
            f"{action['player_name']} {action['action']}({action['amount']}) at {action['timestamp']}\n"
            for action in self.opponents_actions
        )
        if len(stored_info) > 0:
            self.memory.store(f"Round {self.round_count} opponent actions:\n{stored_info}")
        
        # Reset round-specific tracking
        self.opponents_actions = []
        self.opponents_expressions = []
        
        self.__wait_until_input()

    def receive_street_start_message(self, street, round_state):
        print(U.visualize_street_start(street, round_state, self.uuid))
        self.__wait_until_input()

    def receive_game_update_message(self, new_action, round_state):
        print(U.visualize_game_update(new_action, round_state, self.uuid))
        
        # Track opponent actions and expressions (if available)
        if new_action.get("player_uuid") != self.uuid:
            player_name = new_action.get("player_name", new_action.get("player_uuid", "Unknown"))
            opponent_data = {
                "player_uuid": new_action.get("player_uuid"),
                "player_name": player_name,
                "action": new_action.get("action"),
                "amount": new_action.get("amount"),
                "timestamp": datetime.now().isoformat()
            }
            self.opponents_actions.append(opponent_data)
        self.__wait_until_input()

    def receive_round_result_message(self, winners, hand_info, round_state):
        print(U.visualize_round_result(winners, hand_info, round_state, self.uuid))
        
        # Store round result in memory
        result_summary = f"Round {self.round_count} ended. Winners: {[w.get('name', 'Unknown') for w in winners]}"
        self.memory.store(result_summary)
        
        # Save round summary to file
        round_summary = {
            "round": self.round_count,
            "winners": winners,
            "hand_info": hand_info,
            "my_actions": self.my_actions_history,
            "opponents_actions": self.opponents_actions,
            "timestamp": datetime.now().isoformat()
        }
        
        summary_file = f"{self.memory_dir}/round_{self.round_count}_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(round_summary, f, indent=2)
        
        self.__wait_until_input()

    def __wait_until_input(self):
        # Auto-continue for demonstration - remove input requirement
        pass  # input("Enter some key to continue ...")

    def __gen_raw_input_wrapper(self):
        return lambda msg: input(msg)

    def __receive_action_from_console(self, valid_actions):
        flg = self.input_receiver("Enter f(fold), c(call), r(raise).\n >> ")
        if flg in self.__gen_valid_flg(valid_actions):
            if flg == "f":
                return valid_actions[0]["action"], valid_actions[0]["amount"]
            elif flg == "c":
                return valid_actions[1]["action"], valid_actions[1]["amount"]
            elif flg == "r":
                valid_amounts = valid_actions[2]["amount"]
                raise_amount = self.__receive_raise_amount_from_console(
                    valid_amounts["min"], valid_amounts["max"]
                )
                return valid_actions[2]["action"], raise_amount
        else:
            return self.__receive_action_from_console(valid_actions)

    def __gen_valid_flg(self, valid_actions):
        flgs = ["f", "c"]
        is_raise_possible = valid_actions[2]["amount"]["min"] != -1
        if is_raise_possible:
            flgs.append("r")
        return flgs

    def __receive_raise_amount_from_console(self, min_amount, max_amount):
        raw_amount = self.input_receiver(
            "valid raise range = [%d, %d]" % (min_amount, max_amount)
        )
        try:
            amount = int(raw_amount)
            if min_amount <= amount and amount <= max_amount:
                return amount
            else:
                print("Invalid raise amount %d. Try again.")
                return self.__receive_raise_amount_from_console(min_amount, max_amount)
        except:
            print("Invalid input received. Try again.")
            return self.__receive_raise_amount_from_console(min_amount, max_amount)

    def _setup_memory_system(self):
        """Setup memory system and directory structure."""
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Initialize memory manager with basic config (no decay for base agents)
        memory_config = MemoryConfig(
            storage_path=f"{self.memory_dir}/memory_data",
            max_entries=50,
            verbose=True,
            decay=0.0  # No decay for base agents to avoid LLM requirement
        )
        self.memory = create_memory_from_config(memory_config)
        
    def _summarize_rules(self):
        """Read and summarize the rules.md file before the first round."""
        rules_path = "texas_holdem/rules.md"
        summary_path = f"{self.memory_dir}/rule.md"
        
        if os.path.exists(summary_path):
            # Already summarized
            with open(summary_path, 'r') as f:
                return f.read()
                
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                rules_content = f.read()
            
            # Basic summarization - subclasses can override for LLM-based summarization
            summary = self._create_rule_summary(rules_content)
            
            # Store summary
            with open(summary_path, 'w') as f:
                f.write(summary)
                
            return summary
        return ""
    
    def _create_rule_summary(self, rules_content):
        """Create a summary of the rules. Override in LLM agents for AI-powered summarization."""
        # Basic summary for base agent
        return f"Texas Hold'em Rules Summary (Generated: {datetime.now().isoformat()}):\n\n{rules_content[:500]}..."
    
    def _generate_expression(self, action, amount, game_state):
        """Generate an expression based on the action and game state. Override in LLM agents."""
        expressions = [
            "Let's see how this plays out.",
            "Making my move.",
            "Interesting situation here.",
            "Time to act.",
            "Here we go."
        ]
        import random
        return random.choice(expressions)
    
    def _store_action_and_expression(self, action, amount, expression, thought, game_state):
        """Store action, expression and thought in memory and file."""
        action_data = {
            "timestamp": datetime.now().isoformat(),
            "round": self.round_count,
            "action": action,
            "amount": amount,
            "expression": expression,
            "thought": thought,
            "game_state_summary": self._summarize_game_state(game_state)
        }
        
        # Store in memory system
        memory_content = f"Round {self.round_count}: Thought: {thought} | Action: {action}({amount}) | Expression: {expression}"
        self.memory.store(memory_content)
        self.memory.save_to_file()
        
        # Store in file
        action_file = f"{self.memory_dir}/actions_round_{self.round_count}.json"
        if os.path.exists(action_file):
            with open(action_file, 'r') as f:
                actions = json.load(f)
        else:
            actions = []
            
        actions.append(action_data)
        with open(action_file, 'w') as f:
            json.dump(actions, f, indent=2)
            
        # Update history
        self.my_actions_history.append(action_data)
    
    def _summarize_game_state(self, game_state):
        """Create a summary of current game state."""
        if not game_state:
            return "No game state available"
            
        return {
            "street": game_state.get("street", "unknown"),
            "pot": game_state.get("pot", {}).get("main", {}).get("amount", 0),
            "community_cards": str(game_state.get("community_card", [])),
            "active_players": len([p for p in game_state.get("seats", []) if p.get("state") != "folded"])
        }
    
    def get_logging_data(self):
        """Get all logging data for external logger."""
        return {
            "last_thought": self.last_thought,
            "last_expression": self.last_expression,
            "last_action": self.last_action,
            "actions_history": self.my_actions_history,
            "expressions_history": self.my_expressions_history,
            "thoughts_history": self.my_thoughts_history,
            "opponents_actions": self.opponents_actions,
            "round_count": self.round_count
        }