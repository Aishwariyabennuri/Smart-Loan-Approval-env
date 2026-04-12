import random

class LoanEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.current_state = None

    def reset(self):
        self.current_state = self._get_task_state()
        return self.current_state

    def step(self, action):
        default = self._simulate_default(self.current_state)

        if action == "approve":
            if not default:
                reward = 0.9
            else:
                reward = 0.1
        elif action == "reject":
            if default:
                reward = 0.8
            else:
                reward = 0.3
        else:
            return self.current_state, 0.01, True, {"error": "invalid_action"}

        return self.current_state, reward, True, {}

    def _simulate_default(self, state):
        score = 0

        if state["income_stability"] == "stable":
            score += 1
        if state["credit_history"] == "good":
            score += 1
        if state["employment_type"] == "salaried":
            score += 1
        if state["loan_amount"] < 50000:
            score += 1
        if state["past_defaults"] == 0:
            score += 1

        return score < 3

def _get_task_state(self):
    if self.task == "easy_low_risk_customer":
        return random.choice([
            {
                "income_stability": "stable",
                "credit_history": "good",
                "employment_type": "salaried",
                "loan_amount": 20000,
                "past_defaults": 0
            },
            {
                "income_stability": "stable",
                "credit_history": "good",
                "employment_type": "salaried",
                "loan_amount": 30000,
                "past_defaults": 0
            }
        ])

    elif self.task == "medium_conflicting_signals":
        return random.choice([
            {
                "income_stability": "stable",
                "credit_history": "bad",
                "employment_type": "self-employed",
                "loan_amount": 60000,
                "past_defaults": 1
            },
            {
                "income_stability": "unstable",
                "credit_history": "good",
                "employment_type": "self-employed",
                "loan_amount": 70000,
                "past_defaults": 1
            }
        ])

    elif self.task == "hard_high_uncertainty":
        return random.choice([
            {
                "income_stability": "unstable",
                "credit_history": "good",
                "employment_type": "self-employed",
                "loan_amount": 120000,
                "past_defaults": 2
            },
            {
                "income_stability": "unstable",
                "credit_history": "bad",
                "employment_type": "self-employed",
                "loan_amount": 100000,
                "past_defaults": 3
            }
        ])
