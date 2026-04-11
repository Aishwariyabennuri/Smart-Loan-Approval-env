import random

class LoanEnv:
    def __init__(self,task="easy"):
        self.task=task
        self.current_state = None

    def reset(self):
        self.current_state = self._get_task_state()
        return self.current_state
    
    def state(self):
        return self.current_state

    def step(self, action):
        default = self._simulate_default(self.current_state)

        if action == "approve":  #1
            reward = 1.0 if not default else -1.0
        elif action == "reject": #0
            reward = 1.0 if default else -0.5
        else:
            return self.current_state, 0.0, True, {"error": "invalid_action"}
        done = True
        return self.current_state, reward, done, {}

    def _simulate_default(self, state):
        # Simple logic for default probability
        score = 0

        if state["income_stability"] == "stable":
            score += 1
        if state["credit_history"] == "good":
            score += 1
        if state["employment_type"] == "salaried":
            score += 1
        if state["loan_amount"] < 50000:
            score += 1
            
        return score < 2

def _get_task_state(self):
        return {
            "income_stability": random.choice(["stable", "unstable"]),
            "credit_history": random.choice(["good", "bad"]),
            "employment_type": random.choice(["salaried", "self-employed"]),
            "loan_amount": random.randint(5000, 200000)
        }
    
   
