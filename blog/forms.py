from django import forms
from .models import Post, Izoh, Reel, Profil


class PostForm(forms.ModelForm):
    """Post yaratish va tahrirlash uchun forma"""
    class Meta:
        model = Post
        fields = ['sarlavha', 'matn', 'kategoriya', 'rasm', 'nashr_etilgan']
        widgets = {
            'sarlavha': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '📝 Post sarlavhasi',
                'required': True
            }),
            'matn': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '✍️ Post matni yozing...',
                'required': True
            }),
            'kategoriya': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'rasm': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*'
            }),
            'nashr_etilgan': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class IzohForm(forms.ModelForm):
    """Post izohini yaratish uchun forma"""
    class Meta:
        model = Izoh
        fields = ['matn']
        widgets = {
            'matn': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '💬 Izohingizni yozing...',
                'required': True
            }),
        }


class ReelForm(forms.ModelForm):
    """Video reel yaratish uchun forma"""
    class Meta:
        model = Reel
        fields = ['nom', 'video']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '🎬 Reel nomi',
                'required': True
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'video/*'
            }),
        }


class ProfilForm(forms.ModelForm):
    """Foydalanuvchi profileni tahrirlash uchun forma"""
    class Meta:
        model = Profil
        fields = ['ism', 'bio', 'rasm', 'cover_rasm']
        widgets = {
            'ism': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '👤 To\'liq ismingiz',
                'required': True
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '✨ O\'zingiz haqida qisqacha malumat...'
            }),
            'rasm': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*'
            }),
            'cover_rasm': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*'
            }),
        }
