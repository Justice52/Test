from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('elections/', views.election_list, name='election_list'),
    path('election/<int:election_id>/', views.election_detail, name='election_detail'),
    path('election/<int:election_id>/vote/', views.vote, name='vote'),
    path('vote/<int:vote_id>/confirmation/', views.vote_confirmation, name='vote_confirmation'),
    path('election/<int:election_id>/results/', views.results, name='results'),
    path('blockchain/', views.blockchain_view, name='blockchain'),
]
