from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router yaratish
router = DefaultRouter()
router.register(r'postlar', views.PostViewSet, basename='post')



urlpatterns = [
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('post/<int:post_id>/', views.post_batafsil, name='post_batafsil'),
    path('ommabop/', views.ommabop_postlar, name='ommabop'),
    path('biz-haqimizda/', views.biz_haqimizda, name='biz_haqimizda'),
    path('aloqa/', views.aloqa, name='aloqa'),
    path('portfolio/', views.portfolio, name='portfolio'),  # Yangi
    path('yangi/', views.post_yaratish, name='post_yaratish'),
    path('post/<int:post_id>/izoh/', views.post_izoh, name='post_izoh'),
    path('post/<int:post_id>/tahrirlash/', views.post_tahrirlash, name='post_tahrirlash'),
    path('post/<int:post_id>/ochirish/', views.post_ochirish, name='post_ochirish'),
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('profil/tahrirlash/', views.profil_tahrirlash, name='profil_tahrirlash'),
    path('profil/<str:username>/', views.profil, name='profil'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),

    path('api/', include(router.urls)),

]