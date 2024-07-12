from django.db import models

# Create your models here.
class Recipe(models.Model):
    # class attributes
    name = models.CharField(max_length=50)
    ingredients = models.CharField(
        max_length=225,
        help_text="Enter the ingredients, separated by a comma"
    )
    cooking_time = models.IntegerField(help_text="Enter cooking time in minutes")
    difficulty = None

    # determine recipe difficulty
    def difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            return "Hard"
        return "Unknown"

    # string representation
    def __str__(self):
        return str(self.name)