from django.urls import path
from . import views

urlpatterns = [
    # Asosiy sahifalar
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('asosiy/', views.asosiy_sahifa, name='asosiy'),
    path('aloqa/', views.aloqa, name='aloqa'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('biz_haqimizda/', views.biz_haqimizda, name='biz_haqimizda'),
    path('kitoblar/', views.kitoblar, name='kitoblar'),
    path('ommabop/', views.ommabop_postlar, name='ommabop'),
    path('galereya/', views.galereya, name='galereya'),
    
    # Post operatsiyalar
    path('post/<int:post_id>/', views.post_batafsil, name='post_batafsil'),
    path('post/yaratish/', views.post_yaratish, name='post_yaratish'),
    path('post/<int:post_id>/tahrirlash/', views.post_tahrirlash, name='post_tahrirlash'),
    path('post/<int:post_id>/ochirish/', views.post_ochirish, name='post_ochirish'),
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
    
    # Qidiruv va qora qogozlar
    path('qidiruv/', views.qidiruv, name='qidiruv'),
    path('qora-qogozlar/', views.qorovogozlar, name='qorovogozlar'),
    
    # Autentifikatsiya
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),
    
    # Profil
    path('profil/<str:username>/', views.profil, name='profil'),
    path('profil-tahrirlash/', views.profil_tahrirlash, name='profil_tahrirlash'),
    
    # Reels
    path('reels/', views.reels_feed, name='reels_feed'),
    path('reel-yaratish/', views.reel_yaratish, name='reel_yaratish'),
]