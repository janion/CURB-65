class CurbResult:

    def __init__(self, score):
        self.score = score
        self.recommendation = self._get_recommendation()

    def _get_recommendation(self):
        if self.score <= 1:
            return "Likely suitable for home treatment"
        elif self.score <= 1:
            return "Consider hospital supervised treatment"
        else:
            return "Manage in hospital as severe pneumonia"


def calculate_curb(confusion, urea, resp_rate, sbp, dbp, age):
    if None in [confusion, urea, resp_rate, sbp, dbp]:
        return None

    score = 1 if confusion else 0;
    if urea > 7:
        score += 1
    if resp_rate >= 30:
        score += 1
    if sbp < 90:
        score += 1
    if age >= 65:
        score += 1

    return CurbResult(score)
