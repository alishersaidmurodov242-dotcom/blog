from django.contrib import admin
from .models import Kategoriya, Profil, Post, Izoh, Like, Reel


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom']
    search_fields = ['nom']


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ism']
    search_fields = ['user__username', 'ism']
    fields = ['user', 'ism', 'bio', 'rasm', 'cover_rasm']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'sarlavha', 'muallif', 'kategoriya', 'nashr_etilgan', 'yaratilgan_sana', 'korildi']
    list_filter = ['nashr_etilgan', 'kategoriya', 'yaratilgan_sana']
    search_fields = ['sarlavha', 'matn', 'muallif__username']
    list_editable = ['nashr_etilgan']


@admin.register(Izoh)
class IzohAdmin(admin.ModelAdmin):
    list_display = ['id', 'muallif', 'post', 'yaratilgan_sana']
    search_fields = ['muallif__username', 'post__sarlavha', 'matn']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
    search_fields = ['user__username', 'post__sarlavha']


@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'yaratilgan_vaqt']
    search_fields = ['nom']