from django import forms
from recipes.models import Author, RecipeItem



class RecipesAddForm(forms.Form):
    title = forms.CharField(max_length = 30)
    description = forms.CharField(widget = forms.Textarea)
    author = forms.ModelChoiceField(queryset = Author.objects.all())

class AuthorAddForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            "name",
            "bio"
        ]

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 50)
    password = forms.CharField(widget = forms.PasswordInput)


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = RecipeItem
        fields = [
            'title',
            'author',
            'description',
            'time_required',
            'instructions'
        ]
