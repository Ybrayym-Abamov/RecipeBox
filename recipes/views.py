from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from recipes.models import RecipeItem, Author
from recipes.forms import RecipesAddForm, AuthorAddForm, LoginForm, EditRecipeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data["username"],
                password=data["password"]
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage"))
                )
    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

def index(request):
    data = RecipeItem.objects.all()
    return render(request, "index.html", {"data": data})

@login_required
def recipesadd(request):
    html = "generic_form.html"
    if request.method == "POST":
        form = RecipesAddForm(request.POST)
        if form.is_valid():
            recipe = form.cleaned_data
            RecipeItem.objects.create(
                title = recipe['title'],
                description = recipe['description'],
                author = recipe['author']
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = RecipesAddForm()
    return render(request, html, {"form": form})


@login_required
@staff_member_required
def editrecipeform(request, id):
    recipe = RecipeItem.objects.get(id=id)
    if request.method == "POST":
        form = EditRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data['title']
            recipe.author = data['author']
            recipe.description = data['description']
            recipe.time_required = data['time_required']
            recipe.instructions = data['instructions']
            recipe.save()
            return HttpResponseRedirect(reverse('recipe_view', args=(id, )))
    form = EditRecipeForm(initial={
        'title': recipe.title,
        'author': recipe.author.id,
        'description': recipe.description,
        'time_required': recipe.time_required,
        'instructions': recipe.instructions
    })
    return render(request, 'generic_form.html', {"form": form})

@login_required
def authoradd(request):
    html = "generic_form.html"
    if not request.user.is_staff:
        return HttpResponse("Sorry buddy Admin only privileges!")
    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        new_author = form.save(commit=False)
        user = User.objects.create_user(username = new_author.name, password = "Bienvenue")
        new_author.User = user
        new_author.save()
        return HttpResponseRedirect(reverse("homepage"))
    form = AuthorAddForm()
    return render(request, html, {"form": form})


def recipe_view(request, id):
    recipe = RecipeItem.objects.get(id=id)
    return render(request, "recipe.html", {"recipe": recipe})

def author_view(request, id):
    author = Author.objects.get(id=id)
    recipes = RecipeItem.objects.filter(author=author)
    return render(request, "bio.html", {"info": author, "recipes": recipes})


@login_required
def favorites_view(request, id):
    html = 'favorites.html'
    data = Author.objects.get(id=id)
    context = {
        'data': data
    }
    return render(request, html, context)


@login_required
def add_favorite(request, id):
    recipe = RecipeItem.objects.get(id=id)
    request.user.author_view.favorites_view.add(recipe)
    return HttpResponseRedirect(reverse('recipe_view', kwargs={'id': id}))


@login_required
def del_favorite(request, id):
    recipe = RecipeItem.objects.get(id=id)
    request.user.author_view.favorites_view.remove(recipe)
    return HttpResponseRedirect(reverse('recipe_view', kwargs={'id': id}))


def recipe(request, id):
    recipe = RecipeItem.objects.get(id=id)
    if request.user.is_authenticated:
        if recipe in request.user.author.favorites_view.all():
            in_favorites = True
        else:
            in_favorites = False
        return render(
            request,
            'recipe.html',
            {'recipe': recipe, 'in_favorites': in_favorites})
    else:
        return render(
            request,
            'recipe.html',
            {'recipe': recipe})
