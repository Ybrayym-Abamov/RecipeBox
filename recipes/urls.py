from django.urls import path
from recipes import views


urlpatterns = [
    path('', views.index, name= "homepage"),
    path('recipesadd/', views.recipesadd),
    path('authoradd/', views.authoradd),
    path('recipe/<int:id>/', views.recipe_view, name="recipe_view"),
    path('author/<int:id>/', views.author_view),
    path('login/', views.loginview),
    path('logout/', views.logoutview),
    path('recipe/edit/<int:id>/', views.editrecipeform),
    path('favorites/<int:id>/', views.favorites_view),
    path('favorite/add/<int:id>/', views.add_favorite),
    path('favorite/remove/<int:id>/', views.del_favorite)
]

