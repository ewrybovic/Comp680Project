from enum import Enum

class HealthScore(Enum):
    Healthy = 1,
    Neutral = 2,
    Unhealthy = 3,
    Unknown = 9

CAL_PROTEIN_GRAM = 4
CAL_FAT_GRAM = 9
CAL_CARBS_GRAM = 4

# TODO Find out the percentagge of calories that come from fat/carbs/protein 
# Higher percentage of protein is better than higher fat/carbs

def ScoreNutirion(nutrition_data: dict) -> {HealthScore, str}:
    score = HealthScore.Unknown
    score_string = str()

    # Percentage of calories that in the order: Fat, Carbs, Protein
    marcro_percents = {
        "fat": 0,
        'carbs': 0,
        'protein': 0
    }

    print(data)

    # If calories were not found we can't proceed
    if 'calories' not in data.keys():
        return {score, "No calories data"}

    # Find the percentage each macro contributes to the overall calories
    if 'total fat' in data.keys():
        marcro_percents['fat'] = (data['total fat'] * CAL_FAT_GRAM) / data['calories']
    if 'total carbohydrate' in data.keys():
        marcro_percents['carbs'] = (data['total carbohydrate'] * CAL_CARBS_GRAM) / data['calories']
    if 'protein' in data.keys():
        marcro_percents['protein'] = (data['protein'] * CAL_PROTEIN_GRAM) / data['calories']

    print(marcro_percents)

    return {score, score_string}
    
if __name__ == '__main__':
    data = {"calories": 100, "total fat" : 11, "saturated fat": 7, "total carbohydrate": 0, "protein":0}
    print(ScoreNutirion(data))