from enum import Enum

class HealthScore(Enum):
    Healthy = 1,
    Neutral = 2,
    Unhealthy = 3,
    Unknown = 9

def ScoreNutirion(nutrition_data: dict) -> {HealthScore, str}:
    score = HealthScore.Unknown
    score_string = str()

    if "trans fat" in nutrition_data or "saturated fat" in nutrition_data:
        score = HealthScore.Unhealthy
        score_string = "Too much unhealthy fat"
    else:
        score = HealthScore.Healthy
        score_string = "You're good"

    return {score, score_string}
    
if __name__ == '__main__':
    data = {"trans fat" : 0}
    print(ScoreNutirion(data))