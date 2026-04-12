import numpy as np

class LoanEnv:
    def __init__(self, data, max_steps=50):
        self.data = data
        self.max_steps = max_steps
        self.reset()

    def reset(self):
        self.current_step = 0
        self.balance = 100000
        self.min_balance = 20000
        self.active_loans = []
        self.approvals_by_group = {}
        self.total_by_group = {}
        self.current_applicant = self.data[self.current_step]
        return self._get_state()

    def _get_state(self):
        return {
            "applicant": self.current_applicant,
            "balance": self.balance,
            "active_loans": len(self.active_loans)
        }

    def compute_fairness_gap(self, action, applicant):
        group = applicant.get("group", "A")

        if group not in self.approvals_by_group:
            self.approvals_by_group[group] = 0
            self.total_by_group[group] = 0

        self.total_by_group[group] += 1
        if action == 1:
            self.approvals_by_group[group] += 1

        rates = []
        for g in self.total_by_group:
            if self.total_by_group[g] > 0:
                rates.append(self.approvals_by_group[g] / self.total_by_group[g])

        if len(rates) < 2:
            return 0

        return max(rates) - min(rates)

    def step(self, action):
        applicant = self.current_applicant

        loan_amount = applicant["loan_amount"]
        interest = applicant["interest_rate"]
        default_prob = applicant["default_prob"]
        repaid = applicant["repaid"]

        reward = 0

        if action == 1:
            reward += loan_amount * ((1 - default_prob) * interest - default_prob)

            self.active_loans.append({
                "amount": loan_amount,
                "interest": interest,
                "repaid": repaid,
                "time_left": np.random.randint(2, 5)
            })

            self.balance -= loan_amount

        new_active_loans = []
        for loan in self.active_loans:
            loan["time_left"] -= 1

            if loan["time_left"] == 0:
                if loan["repaid"]:
                    reward += loan["amount"] * loan["interest"]
                    self.balance += loan["amount"]
                else:
                    reward -= loan["amount"]
            else:
                new_active_loans.append(loan)

        self.active_loans = new_active_loans

        return self._get_state(), reward, done, {}
