class RiskService:
    @staticmethod
    def calculate_risk_level(probability: float) -> str:
        """
        Determine risk level based on the probability of missing a vaccination.
        """
        if probability < 0.33:
            return 'LOW'
        elif probability < 0.66:
            return 'MEDIUM'
        else:
            return 'HIGH'
