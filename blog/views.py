from .models import Post, Item_User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from blog.forms import ItemForm


class RegistrationFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "site/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "site/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    success_url = "/"

    def get(self, request):
        return_path = request.META.get('HTTP_REFERER', '/')
        logout(request)
        return redirect(return_path)


def post_list(request, page_number=1):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    current_page = Paginator(posts, 3)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.commented = '0'
            post.save()
            return redirect('itempage', pk=post.pk)
    else:
        form = ItemForm()
    return render(request, 'site/postlist.html', {'posts': current_page.page(page_number), 'form': form})


def items(request, pk):
    post = get_object_or_404(Post, pk=pk)
    item_user = Item_User.objects.filter(item=pk)
    return render(request, 'site/itempage.html', {'post': post, 'item_user': item_user})


def test(request):
    return render(request, 'site/mainpage.html', {})


def addtocomment(request, pk):
    try:
        return_path = request.META.get('HTTP_REFERER', '/')
        post = get_object_or_404(Post, pk=pk)
        post.commented += 1
        post.save()
        if post.pk > 0:
            if Item_User.objects.filter(user=request.user.username, item=pk).exists():
                u_i = Item_User.objects.get(user=request.user.username, item=pk)
                u_i.number += 1
                u_i.save()
            else:
                u_i = Item_User(user=request.user.username, item=pk, number=1)
                u_i.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect(return_path)


def add(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
    else:
        form = ItemForm()
    return render(request, 'site/additionitem.html', {'form': form})
