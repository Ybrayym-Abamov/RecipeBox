from django import forms
from recipes.models import Author

class RecipesAddForm(forms.Form):
    title = forms.CharField(max_length = 30)
    description = forms.CharField(widget = forms.Textarea)
    author = forms.ModelChoiceField(queryset = Author.objects.all())

class AuthorAddForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            "name"
        ]
