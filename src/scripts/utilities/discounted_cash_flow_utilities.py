import math


class DiscountedCashFlowUtils:

    @staticmethod
    def dcf(cash_flows, discount_value):
        total = 0
        for i, cash in enumerate(cash_flows, 1):
            total += cash / math.pow((1 + discount_value), i)
        return total

    @staticmethod
    def estimate_future_cash_flows():
        # TODO: research how to estimate future cash flow
        pass

    @staticmethod
    def get_discount_rate(equity_amount, debt_amount, tax_rate, risk_free_rate, beta, market_return, debt_yield):
        """
        Uses Weighted Average Capital Cost
        https://corporatefinanceinstitute.com/resources/knowledge/finance/what-is-wacc-formula/
        """
        total_capital = equity_amount + debt_amount
        cost_of_equity = DiscountedCashFlowUtils.get_cost_of_equity(risk_free_rate, beta, market_return)
        cost_of_debt = DiscountedCashFlowUtils.get_cost_of_debt(debt_amount, debt_yield)

        equity_portion = equity_amount / total_capital * cost_of_equity
        debt_portion = debt_amount / total_capital * cost_of_debt * (1 - tax_rate)

        return equity_portion + debt_portion

    @staticmethod
    def get_cost_of_equity(risk_free_rate, beta, market_return):
        """
        Uses the Capital Asset Pricing Model
        https://corporatefinanceinstitute.com/resources/knowledge/finance/what-is-capm-formula/
        """
        return risk_free_rate + beta * (market_return - risk_free_rate)

    @staticmethod
    def get_cost_of_debt(debt_amount, debt_yield):
        """
        https://corporatefinanceinstitute.com/resources/knowledge/finance/cost-of-debt/
        """
        pass
