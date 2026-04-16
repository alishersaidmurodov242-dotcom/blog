from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# ===== FILE SIZE VALIDATOR =====
def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB
    if value.size > max_size:
        raise ValidationError("Fayl hajmi 5MB dan oshmasligi kerak!")


# ===== KATEGORIYA =====
class Kategoriya(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


# ===== PROFIL =====
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ism = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    rasm = models.ImageField(
        upload_to='profil_rasmlari/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_file_size,
        ]
    )
    cover_rasm = models.ImageField(
        upload_to='profillar/cover/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_file_size,
        ]
    )

    def __str__(self):
        return self.user.username


# ===== POST =====
class Post(models.Model):
    sarlavha = models.CharField(max_length=200, db_index=True)
    matn = models.TextField()
    muallif = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='postlar',
        db_index=True
    )
    kategoriya = models.ForeignKey(
        Kategoriya,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='postlar'
    )
    yaratilgan_sana = models.DateTimeField(auto_now_add=True, db_index=True)
    yangilangan_sana = models.DateTimeField(auto_now=True)
    nashr_etilgan = models.BooleanField(default=True)
    korildi = models.PositiveIntegerField(default=0)

    rasm = models.ImageField(
        upload_to='postlar/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_file_size,
        ]
    )

    class Meta:
        ordering = ['-yaratilgan_sana']
        indexes = [
            models.Index(fields=['-yaratilgan_sana', 'nashr_etilgan']),
        ]

    def __str__(self):
        return self.sarlavha


# ===== IZOH =====
class Izoh(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='izohlar')
    muallif = models.ForeignKey(User, on_delete=models.CASCADE)
    matn = models.TextField()
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-yaratilgan_sana']

    def __str__(self):
        return f"{self.muallif.username} - {self.post.sarlavha}"


# ===== LIKE =====
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_like')
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.sarlavha}"


# ===== REEL =====
class Reel(models.Model):
    nom = models.CharField(max_length=200)
    video = models.FileField(
        upload_to='reels/',
        validators=[
            FileExtensionValidator(['mp4', 'mov', 'avi', 'mkv'])
        ]
    )
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom