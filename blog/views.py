from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.core.paginator import Paginator

from .models import Post, Kategoriya, Izoh, Like, Reel, Profil
from .forms import (
    ReelForm,
    IzohForm,
    PostForm,
    ProfilForm,
)

User = get_user_model()


# ===== ASOSIY SAHIFA =====
def bosh_sahifa(request):
    barcha_postlar = Post.objects.filter(nashr_etilgan=True).order_by('-yaratilgan_sana')

    paginator = Paginator(barcha_postlar, 4)
    sahifa_raqami = request.GET.get('sahifa')
    postlar = paginator.get_page(sahifa_raqami)

    return render(request, 'blog/bosh.html', {'postlar': postlar})


# ===== ASOSIY SAHIFA 2 (agar alohida ishlatsang) =====
def asosiy_sahifa(request):
    postlar_list = Post.objects.filter(nashr_etilgan=True).order_by('-yaratilgan_sana')
    paginator = Paginator(postlar_list, 3)
    sahifa_raqami = request.GET.get('sahifa')
    postlar = paginator.get_page(sahifa_raqami)

    return render(request, 'blog/asosiy.html', {'postlar': postlar})


# ===== STATIK SAHIFALAR =====
def aloqa(request):
    return render(request, 'blog/aloqa.html')


def portfolio(request):
    return render(request, 'blog/portfolio.html')


def biz_haqimizda(request):
    return render(request, 'blog/biz_haqimizda.html')


def kitoblar(request):
    kitoblar = [
        {'nom': 'Python Crash Course', 'muallif': 'Eric Matthes'},
        {'nom': 'Clean Code', 'muallif': 'Robert Martin'},
    ]
    return render(request, 'blog/kitoblar.html', {'kitoblar': kitoblar})


# ===== OMMABOP POSTLAR =====
def ommabop_postlar(request):
    postlar = Post.objects.filter(nashr_etilgan=True).order_by('-korildi')[:5]
    return render(request, 'blog/ommabop.html', {'postlar': postlar})


# ===== POST BATAFSIL =====
def post_batafsil(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Ko‘rish soni
    post.korildi += 1
    post.save(update_fields=['korildi'])

    izohlar = post.izohlar.all().order_by('-yaratilgan_sana')

    like_bor = False
    if request.user.is_authenticated:
        like_bor = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Iltimos, izoh yozish uchun tizimga kiring.")
            return redirect('kirish')

        forma = IzohForm(request.POST)
        if forma.is_valid():
            izoh_obj = forma.save(commit=False)
            izoh_obj.post = post
            izoh_obj.muallif = request.user
            izoh_obj.save()
            messages.success(request, "✅ Izoh muvaffaqiyatli saqlandi!")
            return redirect('post_batafsil', post_id=post.id)
    else:
        forma = IzohForm()

    context = {
        'post': post,
        'izohlar': izohlar,
        'forma': forma,
        'like_bor': like_bor,
        'like_soni': post.likes.count(),
    }

    return render(request, 'blog/post_batafsil.html', context)


# ===== QIDIRUV =====
def qidiruv(request):
    soz = request.GET.get('q', '')
    postlar = Post.objects.filter(
        nashr_etilgan=True,
        sarlavha__icontains=soz
    ).order_by('-yaratilgan_sana')

    return render(request, 'blog/qidiruv.html', {'postlar': postlar, 'soz': soz})


# ===== QORALAMA POSTLAR =====
@login_required
def qorovogozlar(request):
    postlar = Post.objects.filter(
        muallif=request.user,
        nashr_etilgan=False
    ).order_by('-yaratilgan_sana')

    return render(request, 'blog/qora_qogozlar.html', {'postlar': postlar})


# ===== PROFIL =====
def profil(request, username):
    foydalanuvchi = get_object_or_404(User, username=username)
    postlar = Post.objects.filter(
        muallif=foydalanuvchi,
        nashr_etilgan=True
    ).order_by('-yaratilgan_sana')

    profil_obj, created = Profil.objects.get_or_create(user=foydalanuvchi)

    context = {
        'profil_egasi': foydalanuvchi,
        'profil': profil_obj,
        'postlar': postlar,
        'postlar_soni': postlar.count()
    }
    return render(request, 'blog/profil.html', context)


# ===== RO‘YXATDAN O‘TISH =====
def royxatdan_otish(request):
    from django.contrib.auth.forms import UserCreationForm

    if request.method == 'POST':
        forma = UserCreationForm(request.POST)
        if forma.is_valid():
            user = forma.save()
            login(request, user)
            messages.success(request, f'✅ Xush kelibsiz, {user.username}!')
            return redirect('bosh_sahifa')
    else:
        forma = UserCreationForm()

    return render(request, 'blog/royxatdan_otish.html', {'forma': forma})


# ===== KIRISH =====
def kirish(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Xush kelibsiz, {user.username}!')
            return redirect('bosh_sahifa')
        else:
            messages.error(request, '❌ Noto‘g‘ri foydalanuvchi nomi yoki parol!')

    return render(request, 'blog/kirish.html')


# ===== CHIQISH =====
def chiqish(request):
    logout(request)
    messages.info(request, '👋 Chiqdingiz. Tez orada qaytib keling!')
    return redirect('bosh_sahifa')


# ===== POST YARATISH =====
@login_required
def post_yaratish(request):
    if request.method == 'POST':
        forma = PostForm(request.POST, request.FILES)
        if forma.is_valid():
            post = forma.save(commit=False)
            post.muallif = request.user
            post.save()
            messages.success(request, '✅ Post yaratildi!')
            return redirect('post_batafsil', post_id=post.id)
    else:
        forma = PostForm()

    return render(request, 'blog/post_yaratish.html', {'forma': forma})


# ===== POST TAHRIRLASH =====
@login_required
def post_tahrirlash(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.muallif != request.user:
        messages.error(request, '❌ Siz faqat o‘zingizning postingizni tahrirlashingiz mumkin!')
        return redirect('post_batafsil', post_id=post.id)

    if request.method == 'POST':
        forma = PostForm(request.POST, request.FILES, instance=post)
        if forma.is_valid():
            forma.save()
            messages.success(request, '✅ Post yangilandi!')
            return redirect('post_batafsil', post_id=post.id)
    else:
        forma = PostForm(instance=post)

    return render(request, 'blog/post_tahrirlash.html', {'forma': forma, 'post': post})


# ===== POST O‘CHIRISH =====
@login_required
def post_ochirish(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.muallif != request.user:
        messages.error(request, '❌ Siz faqat o‘zingizning postingizni o‘chirishingiz mumkin!')
        return redirect('post_batafsil', post_id=post.id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, '✅ Post o‘chirildi!')
        return redirect('bosh_sahifa')

    return render(request, 'blog/post_ochirish.html', {'post': post})


# ===== LIKE =====
@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_obj, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like_obj.delete()
        messages.success(request, '👍 Like olib tashlandi')
    else:
        messages.success(request, '❤️ Like qo‘shildi')

    return redirect('post_batafsil', post_id=post.id)


# ===== REELS =====
def reels_feed(request):
    reels = Reel.objects.all().order_by('-yaratilgan_vaqt')
    return render(request, 'blog/reels_feed.html', {'reels': reels})


@login_required
def reel_yaratish(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Reel yuklandi!")
            return redirect('reels_feed')
    else:
        form = ReelForm()

    return render(request, 'blog/reel_yaratish.html', {'form': form})


# ===== PROFIL TAHRIRLASH =====
@login_required
def profil_tahrirlash(request):
    user = request.user
    profil, created = Profil.objects.get_or_create(user=user)

    if request.method == 'POST':
        f_forma = UserChangeForm(request.POST, instance=user)
        p_forma = ProfilForm(request.POST, request.FILES, instance=profil)

        if f_forma.is_valid() and p_forma.is_valid():
            f_forma.save()
            p_forma.save()
            messages.success(request, '✅ Profil muvaffaqiyatli yangilandi!')
            return redirect('profil', username=user.username)
    else:
        f_forma = UserChangeForm(instance=user)
        p_forma = ProfilForm(instance=profil)

    context = {
        'f_forma': f_forma,
        'p_forma': p_forma,
        'profil': profil,
    }

    return render(request, 'blog/profil_tahrirlash.html', context)


# ===== GALEREYA =====
def galereya(request):
    post_rasmlar = Post.objects.filter(
        nashr_etilgan=True,
        rasm__isnull=False
    ).exclude(rasm='').order_by('-yaratilgan_sana')

    profil_rasmlar = Profil.objects.exclude(rasm='').order_by('user__username')
    
    cover_rasmlar = Profil.objects.exclude(cover_rasm='').order_by('user__username')

    context = {
        'post_rasmlar': post_rasmlar,
        'profil_rasmlar': profil_rasmlar,
        'cover_rasmlar': cover_rasmlar,
    }
    return render(request, 'blog/galereya.html', context)