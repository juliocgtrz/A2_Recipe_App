from django.shortcuts import render
from django.views.generic import ListView, DetailView   #to display lists and details
from .models import Recipe   #to access Recipe model
from django.contrib.auth.mixins import LoginRequiredMixin   #to protect class-based view
# from django.contrib.auth.decorators import login_required   #to protect function-based views

# Create your views here.
def home(request):
    return render(request, 'recipes/home.html')
    
class RecipeListView(LoginRequiredMixin, ListView):             #class-based "protected" view
    model = Recipe                                              #specify model
    template_name = 'recipes/list.html'                         #specify template

class RecipeDetailView(LoginRequiredMixin, DetailView):         #class-based "protected" view
    model = Recipe                                              #specify model
    template_name = 'recipes/detail.html'                       #specify template
