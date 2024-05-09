from django.db import models


class Serving(models.Model):
    name = models.CharField("Food", max_length=120)
    calories = models.IntegerField("Calories")
    totalFat = models.FloatField("Total Fat")
    saturatedFat = models.FloatField("Saturated Fat")
    transFat = models.FloatField("Trans Fat")
    sodium = models.FloatField("Sodium")
    totalCarb = models.FloatField("Total Carbohydrates")
    addedSugars = models.FloatField("Added Sugar")
    protein = models.FloatField("Protein")

    def __str__(self):
        return self.name


class DateEaten(models.Model):
    name = models.DateField("Date")
    eaten = models.ManyToManyField(Serving, blank=True)

    def __str__(self):
        return str(self.name)


class NutritionUser(models.Model):
    name = models.CharField("Name", max_length=40)
    totalFood = models.ForeignKey(
        DateEaten, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
