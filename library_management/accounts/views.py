from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        occupation = request.POST.get("occupation")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Mật khẩu nhập lại không khớp!")
            return redirect("/accounts/register/")

        # Kiểm tra username đã tồn tại
        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
            return redirect("/accounts/register/")
        # Tạo User
        user = User.objects.create_user(username=username, email=email, password=password)
        # Tạo UserProfile với tất cả các trường
        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            gender=gender ,
            date_of_birth=date_of_birth or None,
            address=address
        )

        messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
        return redirect("/accounts/login/")

    else:
        # GET → render template form đăng ký
        return render(request, "accounts/register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "accounts/home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, UserProfileForm

@login_required
def profile_view(request):
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect("profile_view")
        else:
            messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại.")
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


# views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    if request.method == 'POST':
        # Truyền user trước, data=POST sau
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # giữ session login
            messages.success(request, 'Password changed successfully!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


