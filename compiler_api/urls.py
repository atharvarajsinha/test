from django.urls import path
from .views import CompileView, RunCodeView, HistoryView

urlpatterns = [
    path('compile/', CompileView.as_view(), name='compile'),
    path('run/', RunCodeView.as_view(), name='run'),
    path('history/', HistoryView.as_view(), name='history'),
]
