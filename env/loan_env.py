class LoanEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.state = None

    def reset(self):
        self.state = self._get_task_state()
        return self.state

    def step(self, action):
        default = self._simulate_default(self.state)

        if action == "approve":
            reward = 1.0 if not default else 0.0
        elif action == "reject":
            reward = 1.0 if default else 0.0
        else:
            return self.state, 0.0, True, {"error": "invalid_action"}
        return self.state, reward, True, {}

    def _simulate_default(self, state):
        score = 0
            score += 1
        if state["loan_amount"] < 50000:
            score += 1
        return score < 2

    def _get_task_state(self):
        if self.task == "easy":
            return {
                "income_stability": "stable",
                "credit_history": "good",
                "employment_type": "salaried",
                "loan_amount": 20000
            }
        elif self.task == "medium":
            return {
                "income_stability": "stable",
                "credit_history": "bad",
                "employment_type": "self-employed",
                "loan_amount": 70000
            }
        else:
            return {
                "income_stability": "unstable",
                "credit_history": "good",
                "employment_type": "self-employed",
                "loan_amount": 120000
            }
