from django.urls import path
from . import views

from strategy.dash_apps import strategy_analyzer, experimental, hedge

urlpatterns = [
    path('', views.home, name="strategy-home"),
    path('experimental/', views.experimental, name="strategy-experimental"),
    path('hedge/', views.hedge, name="strategy-hedge"),
]