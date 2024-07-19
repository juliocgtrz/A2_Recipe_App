from django.test import TestCase, Client
from .models import Recipe
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RecipesSearchForm

# Create your tests here.
class RecipeModelTest(TestCase):
    # set up non-modified objects used by all test methods
    def setUpTestData():
        Recipe.objects.create(
            name = "Tea",
            ingredients = "Tea leaves, Sugar, Water",
            cooking_time = 5,
        )

    # NAME
    def test_recipe_name(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'name' field and use it to query its data
        field_label = recipe._meta.get_field("name").verbose_name

        # compare the value to the expected result
        self.assertEqual(field_label, "name")

    def test_recipe_name_max_length(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'name' field and use it to query its data
        max_length = recipe._meta.get_field("name").max_length

        # compare the value to the expected result
        self.assertEqual(max_length, 50)

    # INGREDIENTS
    def test_ingredients_max_length(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'ingredients' field and use it to query its data
        max_length = recipe._meta.get_field("ingredients").max_length

        # compare the value to the expected result
        self.assertEqual(max_length, 225)

    # COOKING TIME
    def test_cooking_time_value(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'cooking_time' field and use it to query its data
        cooking_time_value = recipe.cooking_time

        # compare the value to the expected result
        self.assertIsInstance(cooking_time_value, int)

    # DIFFICULTY
    def test_difficulty_calculation(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # compare the value to the expected result
        self.assertEqual(recipe.difficulty(), "Easy")

    # URL
    def test_get_absolute_url(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # compare the value to the expected result
        self.assertEqual(recipe.get_absolute_url(), "/list/1")

# SEARCH
class RecipeFormTest(TestCase):
    def test_search_form_valid_data(self):
        #creates a RecipesSearchForm instance with valid data
        form = RecipesSearchForm(data={
            "search_by": "name",
            "search_term": "Test Recipe",
            "cooking_time": "",
            "difficulty": "",
        })

        #checks if form is valid
        self.assertTrue(form.is_valid())

    def test_search_form_invalid_data(self):
        #creates a RecipesSearchForm instance with empty data
        form = RecipesSearchForm(data={})

        #checks if form is invalid
        self.assertFalse(form.is_valid())

    def test_search_form_field_labels(self):
        #creates a RecipesSearchForm instance
        form = RecipesSearchForm()

        #checks if "search_by" field label is "Search by"
        self.assertEqual(form.fields["search_by"].label, "Search by")

        #checks if "search_term" field label is "Search term"
        self.assertEqual(form.fields["search_term"].label, "Search term")

        #checks if "cooking_time" field label is "Cooking Time (minutes)"
        self.assertEqual(form.fields["cooking_time"].label, "Cooking Time in Minutes")

        #checks if "difficulty" field label is "Difficulty"
        self.assertEqual(form.fields["difficulty"].label, "Difficulty")


class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #creates test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

        #creates test recipes
        cls.recipe1 = Recipe.objects.create(name="Recipe 1", ingredients="ingredient1, ingredient2", cooking_time=10)
        cls.recipe2 = Recipe.objects.create(name="Recipe 2", ingredients="ingredient1, ingredient2", cooking_time=20)

    def setUp(self):
        #initializes test client
        self.client = Client()

    def test_recipe_list_view_login_required(self):
        #sends GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        #checks if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:list')}")

    def test_recipe_list_view(self):
        #logs test user in
        self.client.login(username="testuser", password="12345")

        #sends GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        #checks if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #checks if correct template is used
        self.assertTemplateUsed(response, "recipes/list.html")

        #checks if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

        #checks if response contains the second recipe name
        self.assertContains(response, "Recipe 2")

    def test_recipe_detail_view_login_required(self):
        #sends GET request to recipe detail view for the first recipe
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe1.pk}))

        #checks if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:detail', kwargs={'pk': self.recipe1.pk})}")

    def test_recipe_detail_view(self):
        #logs test user in
        self.client.login(username="testuser", password="12345")

        #sends GET request to recipe detail view for the first recipe
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe1.pk}))

        #checks if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #checks if correct template is used
        self.assertTemplateUsed(response, "recipes/detail.html")

        #checks if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

    def test_search_view_login_required(self):
        #sends GET request to search view
        response = self.client.get(reverse("recipes:search"))

        #checks if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:search')}")

    def test_search_view(self):
        #logs test user in
        self.client.login(username="testuser", password="12345")

        #sends POST request to search view with valid data
        response = self.client.post(reverse("recipes:search"), data={
            "search_by": "name",
            "search_term": "Recipe 1",
            "cooking_time": "",
            "difficulty": "",
        })

        #checks if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #checks if correct template is used
        self.assertTemplateUsed(response, "recipes/search.html")

        #checks if response contains the first recipe name
        self.assertContains(response, "Recipe 1")
