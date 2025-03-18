from django.urls import path
from BOTGEN_WEB.views import constructor_view, save_stage

urlpatterns = [
    path("", constructor_view, name="constructor"),
    path("save_stage/", save_stage, name="save_stage"),
]