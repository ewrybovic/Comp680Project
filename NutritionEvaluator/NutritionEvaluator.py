from enum import Enum


class HealthScore(Enum):
    Healthy = (1,)
    Neutral = (2,)
    Unhealthy = (3,)
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
    marcro_percents = {"fat": 0, "carbs": 0, "protein": 0}

    # If calories were not found we can't proceed
    if "calories" not in nutrition_data.keys():
        return score, "No calories data"

    # Find the percentage each macro contributes to the overall calories
    if "total fat" in nutrition_data.keys():
        marcro_percents["fat"] = (
            nutrition_data["total fat"] * CAL_FAT_GRAM
        ) / nutrition_data["calories"]
    if "total carbohydrate" in nutrition_data.keys():
        marcro_percents["carbs"] = (
            nutrition_data["total carbohydrate"] * CAL_CARBS_GRAM
        ) / nutrition_data["calories"]
    if "protein" in nutrition_data.keys():
        marcro_percents["protein"] = (
            nutrition_data["protein"] * CAL_PROTEIN_GRAM
        ) / nutrition_data["calories"]

    print(marcro_percents)

    # Compare the macro percents to see what if higher
    if (
        marcro_percents["fat"] > marcro_percents["protein"]
        and marcro_percents["fat"] > marcro_percents["carbs"]
    ):
        score = HealthScore.Unhealthy
        score_string = "Too many calories come from fat."
    elif (
        marcro_percents["carbs"] > marcro_percents["protein"]
        and marcro_percents["carbs"] > marcro_percents["fat"]
    ):
        score = HealthScore.Unhealthy
        score_string = "Too many calories come from carbs."
    elif (
        marcro_percents["protein"] > marcro_percents["fat"]
        and marcro_percents["protein"] > marcro_percents["carbs"]
    ):
        score = HealthScore.Healthy
        score_string = "Good amount of protein."
    else:
        score = HealthScore.Healthy
        score_string = "Even distribution of calories."

        # Check overall calories per serving
        if nutrition_data["calories"] > 200:
            score = HealthScore.Neutral
            score_string = score_string + " Lots of calorries per serving."

    if "saturated fat" in nutrition_data.keys():
        sat_fat_grams = nutrition_data["saturated fat"]
        if sat_fat_grams > 3:
            score_string = (
                score_string
                + " Lots of saturated fat per serving be careful of excess consumption of saturdated fat"
            )

    return score, score_string


if __name__ == "__main__":
    data = {
        "calories": 255,
        "total fat": 3,
        "saturated fat": 7,
        "total carbohydrate": 8,
        "protein": 8,
    }
    score, reason = ScoreNutirion(data)
    print(score.name)
    print(reason)
