import os
import json
import re
from datetime import datetime
from .baseagent import BaseAgent
from memory import MemoryConfig, ModelApiType, create_memory_from_config


class LLMAgent(BaseAgent):
    def __init__(self, agent_name, llm_name, llm_api_type=ModelApiType.NVIDIA, input_receiver=None):
        self.llm_name = llm_name
        self.llm_api_type = llm_api_type
        self._setup_llm_client()
        
        super().__init__(agent_name=agent_name, input_receiver=input_receiver)
        
        # Override memory config for LLM agents with decay and LLM integration
        self._setup_llm_memory_system()

    def _setup_llm_client(self):
        """Setup LLM client based on API type."""
        if self.llm_api_type == ModelApiType.NVIDIA:
            from openai import OpenAI
            self.llm_client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.getenv("NVIDIA_API_KEY")
            )
        elif self.llm_api_type == ModelApiType.GOOGLE:
            import google.genai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.llm_client = genai.GenerativeModel(self.llm_name)
        else:
            raise ValueError(f"Unsupported LLM API type: {self.llm_api_type}")

    def _setup_llm_memory_system(self):
        """Setup memory system with LLM integration."""
        memory_config = MemoryConfig(
            storage_path=f"{self.memory_dir}/memory_data",
            max_entries=16,
            verbose=True,
            decay=0.1,
            model_name=self.llm_name,
            model_api_type=self.llm_api_type
        )
        self.memory = create_memory_from_config(memory_config)

    def _create_rule_summary(self, rules_content):
        """Create an AI-powered summary of the rules."""
        system_prompt = "You are a poker expert helping to summarize game rules."
        user_prompt = f"""
        {system_prompt}
        
        Please create a concise but comprehensive summary of the following Texas Hold'em poker rules. 
        Focus on the key strategic elements that would be important for an AI player to remember during gameplay.
        Include betting actions, hand rankings, and winning conditions.
        
        Rules:
        {rules_content}
        
        Please provide a summary in markdown format.
        """
        
        try:
            if self.llm_api_type == ModelApiType.NVIDIA:
                # Try with system message first
                try:
                    response = self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"""Please create a concise but comprehensive summary of the following Texas Hold'em poker rules. 
Focus on the key strategic elements that would be important for an AI player to remember during gameplay.
Include betting actions, hand rankings, and winning conditions.

Rules:
{rules_content}

Please provide a summary in markdown format."""}
                        ],
                        max_tokens=4096,
                        temperature=0.3
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    if "System role not supported" in str(e) or "system" in str(e).lower():
                        # Fallback: add system prompt to user message
                        response = self.llm_client.chat.completions.create(
                            model=self.llm_name,
                            messages=[
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=4096,
                            temperature=0.3
                        )
                        return response.choices[0].message.content
                    else:
                        raise e
            elif self.llm_api_type == ModelApiType.GOOGLE:
                response = self.llm_client.generate_content(user_prompt)
                return response.text
        except Exception as e:
            print(f"Error generating rule summary: {e}")
            return super()._create_rule_summary(rules_content)

    def _generate_thought(self, valid_actions, hole_card, round_state):
        """Generate AI-powered internal thought about the current situation."""
        # Get relevant memory context
        memory_context = self._get_memory_context()
        
        system_prompt = "You are an expert poker player analyzing the current game situation."
        user_prompt = f"""
        {system_prompt}
        
        You are playing Texas Hold'em poker. Analyze the current situation and provide your internal thought process.
        
        Your hole cards: {hole_card}
        Community cards: {round_state.get('community_card', [])}
        Current street: {round_state.get('street', 'unknown')}
        Pot size: {round_state.get('pot', {}).get('main', {}).get('amount', 0)}
        
        Valid actions: {[action['action'] for action in valid_actions]}
        
        Recent memory/context:
        {memory_context}
        
        Opponents' recent actions in this round:
        {self.opponents_actions[-5:] if self.opponents_actions else 'None yet'}
        
        Provide a brief internal thought about:
        1. Your hand strength assessment
        2. The current betting situation
        3. Your strategic considerations
        
        Keep it concise (2-3 sentences max).
        """
        
        try:
            if self.llm_api_type == ModelApiType.NVIDIA:
                # Try with system message first
                try:
                    response = self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt.replace(system_prompt + "\n\n", "")}
                        ],
                        max_tokens=800,
                        temperature=0.5
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    if "System role not supported" in str(e) or "system" in str(e).lower():
                        # Fallback: add system prompt to user message
                        response = self.llm_client.chat.completions.create(
                            model=self.llm_name,
                            messages=[
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=800,
                            temperature=0.5
                        )
                        return response.choices[0].message.content.strip()
                    else:
                        raise e
            elif self.llm_api_type == ModelApiType.GOOGLE:
                response = self.llm_client.generate_content(user_prompt)
                return response.text.strip()
        except Exception as e:
            print(f"Error generating thought: {e}")
            return super()._generate_thought(valid_actions, hole_card, round_state)

    def _make_decision(self, valid_actions, hole_card, round_state, thought):
        """Make AI-powered decision based on game state and thought."""
        # Get rule summary and memory context
        rule_summary = self._get_rule_summary()
        memory_context = self._get_memory_context()
        
        system_prompt = "You are an expert poker player making strategic decisions."
        user_prompt = f"""
        {system_prompt}
        
        You are playing Texas Hold'em poker and must decide your next action.
        
        RULES SUMMARY:
        {rule_summary}
        
        CURRENT SITUATION:
        Your hole cards: {hole_card}
        Community cards: {round_state.get('community_card', [])}
        Current street: {round_state.get('street', 'unknown')}
        Pot size: {round_state.get('pot', {}).get('main', {}).get('amount', 0)}
        Your stack: {self._get_my_stack(round_state)}
        
        VALID ACTIONS:
        {self._format_valid_actions(valid_actions)}
        
        YOUR ANALYSIS:
        {thought}
        
        RECENT CONTEXT:
        {memory_context}
        
        OPPONENTS' ACTIONS THIS ROUND:
        {self.opponents_actions[-5:] if self.opponents_actions else 'None yet'}
        
        Based on poker strategy and the current situation, choose your action.
        Respond with ONLY the action and amount in this exact format:
        ACTION: [fold/call/raise]
        AMOUNT: [number or 0 for fold/call]
        
        Example responses:
        ACTION: fold
        AMOUNT: 0
        
        ACTION: call
        AMOUNT: 0
        
        ACTION: raise
        AMOUNT: 150
        """
        
        try:
            if self.llm_api_type == ModelApiType.NVIDIA:
                # Try with system message first
                try:
                    response = self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt.replace(system_prompt + "\n\n", "")}
                        ],
                        max_tokens=800,
                        temperature=0.3
                    )
                    decision_text = response.choices[0].message.content.strip()
                except Exception as e:
                    if "System role not supported" in str(e) or "system" in str(e).lower():
                        # Fallback: add system prompt to user message
                        response = self.llm_client.chat.completions.create(
                            model=self.llm_name,
                            messages=[
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=800,
                            temperature=0.3
                        )
                        decision_text = response.choices[0].message.content.strip()
                    else:
                        raise e
            elif self.llm_api_type == ModelApiType.GOOGLE:
                response = self.llm_client.generate_content(user_prompt)
                decision_text = response.text.strip()
            
            # Parse the decision
            action, amount = self._parse_decision(decision_text, valid_actions)
            return action, amount
            
        except Exception as e:
            print(f"Error making AI decision: {e}")
            print("Falling back to random valid action...")
            return self._make_fallback_decision(valid_actions)

    def _generate_expression(self, action, amount, game_state):
        """Generate AI-powered expression based on action and game state."""
        system_prompt = "You are a poker player making natural comments during play with body language."
        user_prompt = f"""
        {system_prompt}
        
        You just made a poker action: {action} (amount: {amount}).
        Generate a brief, natural expression that includes both what you say and your body language.
        Keep it short (1-2 sentences), realistic, and appropriate for the action.
        Avoid giving away your strategy or hand strength.
        
        Format: "[Body language] + spoken words"
        
        Examples:
        - "*leans back casually* Let's see what happens."
        - "*taps fingers on table* I'm feeling confident about this one."
        - "*adjusts chips thoughtfully* Time to mix things up."
        - "*shrugs with a slight smile* Going with my gut here."
        - "*raises eyebrow* This should be interesting."
        - "*pushes chips forward decisively* Here we go."
        - "*pauses briefly, then nods* Alright, I'm in."
        - "*exhales slowly* Can't win them all."
        
        Generate a similar expression with body language for your {action} action:
        """
        
        try:
            if self.llm_api_type == ModelApiType.NVIDIA:
                # Try with system message first
                try:
                    response = self.llm_client.chat.completions.create(
                        model=self.llm_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt.replace(system_prompt + "\n\n", "")}
                        ],
                        max_tokens=500,
                        temperature=0.7
                    )
                    return response.choices[0].message.content.strip().strip('"\'')
                except Exception as e:
                    if "System role not supported" in str(e) or "system" in str(e).lower():
                        # Fallback: add system prompt to user message
                        response = self.llm_client.chat.completions.create(
                            model=self.llm_name,
                            messages=[
                                {"role": "user", "content": user_prompt}
                            ],
                            max_tokens=500,
                            temperature=0.7
                        )
                        return response.choices[0].message.content.strip().strip('"\'')
                    else:
                        raise e
            elif self.llm_api_type == ModelApiType.GOOGLE:
                response = self.llm_client.generate_content(user_prompt)
                return response.text.strip().strip('"\'')
        except Exception as e:
            print(f"Error generating expression: {e}")
            return super()._generate_expression(action, amount, game_state)

    def _get_memory_context(self):
        """Get relevant context from memory system."""
        try:
            self.memory.retrieve()
        except:
            return "No recent context available."

    def _get_rule_summary(self):
        """Get the stored rule summary."""
        summary_path = f"{self.memory_dir}/rule.md"
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                return f.read()
        return "Rules not summarized yet."

    def _format_valid_actions(self, valid_actions):
        """Format valid actions for the prompt."""
        formatted = []
        for action in valid_actions:
            if action['action'] == 'fold':
                formatted.append("fold (lose all bets)")
            elif action['action'] == 'call':
                formatted.append(f"call (match bet of {action['amount']})")
            elif action['action'] == 'raise':
                min_amt = action['amount']['min']
                max_amt = action['amount']['max']
                formatted.append(f"raise (bet between {min_amt} and {max_amt})")
        return "; ".join(formatted)

    def _get_my_stack(self, round_state):
        """Get current stack size from round state."""
        try:
            for seat in round_state.get('seats', []):
                if seat.get('uuid') == self.uuid:
                    return seat.get('stack', 0)
        except:
            pass
        return "unknown"

    def _parse_decision(self, decision_text, valid_actions):
        """Parse LLM decision response into action and amount."""
        try:
            action_match = re.search(r'ACTION:\s*(\w+)', decision_text, re.IGNORECASE)
            amount_match = re.search(r'AMOUNT:\s*(\d+)', decision_text, re.IGNORECASE)
            
            if action_match:
                action = action_match.group(1).lower()
                amount = int(amount_match.group(1)) if amount_match else 0
                
                # Validate against valid actions
                for valid_action in valid_actions:
                    if valid_action['action'] == action:
                        if action == 'raise':
                            min_amt = valid_action['amount']['min']
                            max_amt = valid_action['amount']['max']
                            if min_amt <= amount <= max_amt:
                                return action, amount
                            else:
                                # Clamp to valid range
                                amount = max(min_amt, min(amount, max_amt))
                                return action, amount
                        else:
                            return valid_action['action'], valid_action['amount']
        except Exception as e:
            print(f"Error parsing decision: {e}")
        
        # Fallback to valid action
        return self._make_fallback_decision(valid_actions)

    def _make_fallback_decision(self, valid_actions):
        """Make a safe fallback decision when AI decision fails."""
        # Prefer call over fold, fold over invalid raise
        for action in valid_actions:
            if action['action'] == 'call':
                return action['action'], action['amount']
        # If no call available, take first valid action (usually fold)
        return valid_actions[0]['action'], valid_actions[0]['amount']
