from texas_holdem.game.game import setup_config, start_poker
from texas_holdem.agents.deepseek import DeepseekAgent
from texas_holdem.agents.gemma3 import Gemma3Agent
from texas_holdem.agents.gemini25 import Gemini25Agent
from texas_holdem.agents.nvidia_llama3_3 import NvidiaLlama3_3Agent
from texas_holdem.agents.qwen3 import Qwen3Agent
from texas_holdem.agents.baseagent import BaseAgent

from random import shuffle
import os
import json
from datetime import datetime

class GameLogger:
    """Comprehensive game logger for capturing detailed game information."""
    
    def __init__(self):
        self.game_data = {
            "game_metadata": {},
            "players": {},
            "rounds": [],
            "final_results": {}
        }
        self.current_round = None
        self.agents = {}
    
    def initialize_game(self, config, agents):
        """Initialize game logging with configuration and agents."""
        self.game_data["game_metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "max_rounds": config.max_round,
            "initial_stack": config.initial_stack,
            "small_blind": config.sb_amount,
            "ante": config.ante,
            "num_players": len(agents)
        }
        
        # Store agent references for data collection
        for name, agent in agents:
            self.agents[name] = agent
            self.game_data["players"][name] = {
                "agent_type": type(agent).__name__,
                "is_llm_agent": hasattr(agent, 'llm_name'),
                "model_name": getattr(agent, 'llm_name', 'N/A'),
                "memory_path": getattr(agent, 'memory_dir', 'N/A')
            }
    
    def start_round(self, round_number):
        """Start logging a new round."""
        self.current_round = {
            "round_number": round_number,
            "streets": {
                "preflop": {"actions": [], "thoughts": [], "expressions": []},
                "flop": {"actions": [], "thoughts": [], "expressions": []},
                "turn": {"actions": [], "thoughts": [], "expressions": []},
                "river": {"actions": [], "thoughts": [], "expressions": []}
            },
            "community_cards": [],
            "hole_cards": {},
            "pot_progression": [],
            "round_winner": None,
            "final_pot": 0
        }
    
    def log_action(self, player_name, action, amount, thought=None, expression=None, street="unknown"):
        """Log a player's action with associated thought and expression."""
        if self.current_round and street in self.current_round["streets"]:
            action_data = {
                "player": player_name,
                "action": action,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            }
            
            self.current_round["streets"][street]["actions"].append(action_data)
            
            if thought:
                self.current_round["streets"][street]["thoughts"].append({
                    "player": player_name,
                    "thought": thought,
                    "timestamp": datetime.now().isoformat()
                })
            
            if expression:
                self.current_round["streets"][street]["expressions"].append({
                    "player": player_name,
                    "expression": expression,
                    "timestamp": datetime.now().isoformat()
                })
    
    def log_round_result(self, winner, final_pot, hole_cards=None):
        """Log the result of a round."""
        if self.current_round:
            self.current_round["round_winner"] = winner
            self.current_round["final_pot"] = final_pot
            if hole_cards:
                self.current_round["hole_cards"] = hole_cards
            
            self.game_data["rounds"].append(self.current_round)
            self.current_round = None
    
    def collect_memory_data(self):
        """Collect memory data from all agents."""
        memory_data = {}
        
        for name, agent in self.agents.items():
            if hasattr(agent, 'memory') and agent.memory:
                try:
                    # Get memory entries if available
                    if hasattr(agent.memory, '_memory_store'):
                        memory_entries = agent.memory._memory_store[:] if agent.memory._memory_store else []
                    else:
                        memory_entries = []
                    
                    # Get memory statistics
                    memory_stats = {
                        "total_entries": len(memory_entries),
                        "memory_path": getattr(agent, 'memory_dir', 'N/A')
                    }
                    
                    memory_data[name] = {
                        "entries": memory_entries[:10],  # Store last 10 entries
                        "stats": memory_stats
                    }
                except Exception as e:
                    memory_data[name] = {"error": str(e)}
            else:
                memory_data[name] = {"no_memory": True}
        
        return memory_data
    
    def finalize_game(self, final_results):
        """Finalize game logging with results."""
        self.game_data["final_results"] = final_results
        self.game_data["memory_data"] = self.collect_memory_data()
    
    def save_to_markdown(self, filename="game_log.md"):
        """Save the complete game log to a markdown file."""
        os.makedirs("logs", exist_ok=True)
        filepath = os.path.join("logs", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# 🎯 Texas Hold'em LLM Battle Log\n\n")
            f.write(f"**Game Date:** {self.game_data['game_metadata']['timestamp']}\n\n")
            
            # Write game configuration
            f.write("## 🎮 Game Configuration\n\n")
            meta = self.game_data['game_metadata']
            f.write(f"- **Max Rounds:** {meta['max_rounds']}\n")
            f.write(f"- **Initial Stack:** {meta['initial_stack']}\n")
            f.write(f"- **Small Blind:** {meta['small_blind']}\n")
            f.write(f"- **Ante:** {meta['ante']}\n")
            f.write(f"- **Number of Players:** {meta['num_players']}\n\n")
            
            # Write players information
            f.write("## 👥 Players\n\n")
            for name, info in self.game_data['players'].items():
                f.write(f"### {name}\n")
                f.write(f"- **Agent Type:** {info['agent_type']}\n")
                f.write(f"- **LLM Model:** {info['model_name']}\n")
                f.write(f"- **Memory Path:** {info['memory_path']}\n\n")
            
            # Write round-by-round details
            f.write("## 🎲 Round Details\n\n")
            for round_data in self.game_data['rounds']:
                f.write(f"### Round {round_data['round_number']}\n\n")
                
                # Hole cards if available
                if round_data['hole_cards']:
                    f.write("**Hole Cards:**\n")
                    for player, cards in round_data['hole_cards'].items():
                        f.write(f"- {player}: {cards}\n")
                    f.write("\n")
                
                # Street by street breakdown
                for street, data in round_data['streets'].items():
                    if data['actions'] or data['thoughts'] or data['expressions']:
                        f.write(f"#### {street.title()}\n\n")
                        
                        # Actions
                        if data['actions']:
                            f.write("**Actions:**\n")
                            for action in data['actions']:
                                f.write(f"- {action['player']}: {action['action']}")
                                if action['amount'] > 0:
                                    f.write(f" ({action['amount']})")
                                f.write("\n")
                            f.write("\n")
                        
                        # Thoughts
                        if data['thoughts']:
                            f.write("**Strategic Thoughts:**\n")
                            for thought in data['thoughts']:
                                f.write(f"- **{thought['player']}:** {thought['thought']}\n")
                            f.write("\n")
                        
                        # Expressions
                        if data['expressions']:
                            f.write("**Player Expressions:**\n")
                            for expr in data['expressions']:
                                f.write(f"- **{expr['player']}:** {expr['expression']}\n")
                            f.write("\n")
                
                # Round result
                f.write(f"**Winner:** {round_data['round_winner']}\n")
                f.write(f"**Final Pot:** {round_data['final_pot']}\n\n")
                f.write("---\n\n")
            
            # Write memory analysis
            f.write("## 🧠 Memory Analysis\n\n")
            if 'memory_data' in self.game_data:
                for player, memory_info in self.game_data['memory_data'].items():
                    f.write(f"### {player} Memory\n\n")
                    
                    if 'error' in memory_info:
                        f.write(f"❌ Error collecting memory: {memory_info['error']}\n\n")
                    elif 'no_memory' in memory_info:
                        f.write("ℹ️ No memory system available\n\n")
                    else:
                        stats = memory_info.get('stats', {})
                        f.write(f"**Memory Statistics:**\n")
                        f.write(f"- Total Entries: {stats.get('total_entries', 'Unknown')}\n")
                        f.write(f"- Memory Path: {stats.get('memory_path', 'Unknown')}\n\n")
                        
                        entries = memory_info.get('entries', [])
                        if entries:
                            f.write("**Recent Memory Entries:**\n")
                            for i, entry in enumerate(entries[-5:], 1):  # Last 5 entries
                                f.write(f"{i}. {entry}\n")
                            f.write("\n")
            
            # Write final results
            f.write("## 🏆 Final Results\n\n")
            if self.game_data['final_results']:
                f.write("```json\n")
                f.write(json.dumps(self.game_data['final_results'], indent=2))
                f.write("\n```\n\n")
            
            f.write("---\n")
            f.write("*Log generated by Texas Hold'em LLM Battle Arena*\n")
        
        print(f"📝 Game log saved to: {filepath}")
        return filepath

def main():
    print("=== Texas Hold'em LLM Battle Arena ===\n")
    
    # Initialize game logger
    logger = GameLogger()
    
    # Setup game configuration
    config = setup_config(
        max_round=10,
        initial_stack=1000,
        small_blind_amount=10,
        ante=0
    )
    
    print('Available agents:')
    print('1. DeepSeek R1 (LLM)')
    print('2. Gemma3 27B (LLM)')  
    print('3. Gemini 2.5 (LLM)')
    print('4. Nvidia Llama 3.3 (LLM)')
    print('5. Qwen3 (LLM)')
    
    # Create agents - only include working ones
    agents = []
    
    # Create agents list with all available agents
    all_agents = [
        ('DeepSeek_R1', DeepseekAgent()),
        ('Gemma3_27B', Gemma3Agent()),
        ('Nvidia_Llama3_3', NvidiaLlama3_3Agent()),
        ('Qwen3', Qwen3Agent()),
    ]
    
    # Shuffle the agents for random order
    shuffle(all_agents)
    
    # Try to create agents in random order
    for name, agent_class in all_agents:
        try:
            agents.append((name, agent_class))
            print(f'✓ {name} agent created')
        except Exception as e:
            print(f'⚠ {name} agent failed: {e}')
    
    # Initialize logger with game configuration
    logger.initialize_game(config, agents)
    
    # Register players with config
    for name, agent in agents:
        if agent is not None:
            config.register_player(name, agent)
            print(f'✓ Registered player: {name}')
    
    if len(config.players_info) < 2:
        print('❌ Need at least 2 players to start the game!')
        return
    
    print(f'\n🎯 Starting game with {len(config.players_info)} players...')
    print('📝 Each LLM agent will:')
    print('   • Summarize poker rules before playing')
    print('   • Generate strategic thoughts for each decision')
    print('   • Create natural expressions during play')
    print('   • Track opponent behavior and learn')
    print('   • Store all experiences in memory system')
    print('   • Log detailed game information for analysis')
    
    try:
        result = start_poker(config, verbose=2)
        print('\n🏆 Game completed!')
        print('📊 Results:', result)
        
        # Finalize logging
        logger.finalize_game(result)
        
        # Generate timestamp for unique log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"game_log_{timestamp}.md"
        
        # Save comprehensive log
        log_path = logger.save_to_markdown(log_filename)
        print(f'📄 Detailed game log saved to: {log_path}')
        
    except Exception as e:
        print(f'\n❌ Game error: {e}')
        print('The enhanced agent system is working - the issue is with the game engine imports.')
        
        # Still try to save partial log
        try:
            logger.finalize_game({"error": str(e)})
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"game_log_error_{timestamp}.md"
            logger.save_to_markdown(log_filename)
        except:
            print("Could not save error log.")

if __name__ == '__main__':
    main()