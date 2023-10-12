from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from pprint import pprint
from django.db.models import Max, Min, Q, Count, F, Exists, OuterRef
from django.contrib.messages import success
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

from .models import *
from .forms import *

# Create your views here.

def index(request):
    reviews = StoreReview.objects.all().order_by('-created')[:3]
    categories = Category.objects.all()
    context= {'reviews' : reviews, 'categories': categories}
    return render(request, 'shop/current/index.html', context=context)


class StoreReviewCreate(SuccessMessageMixin, CreateView):
    template_name = 'shop/current/store_reviews.html'
    form_class = StoreReviewForm
    model = StoreReview
    success_message = 'Ваш отзыв успешно добавлен'
    success_url = reverse_lazy('store_reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.model.objects.all()
        if context['form'].initial and 'buyer' in context['form'].initial:
            context['form'].fields['name'].widget.attrs['readonly'] = True
            context['form'].fields['email'].widget.attrs['readonly'] = True
        return context


    def get_initial(self):
        buyer_query = Buyer.objects.filter(user=self.request.user.id)
        if buyer_query:
            buyer = buyer_query[0]
            res = {'name': buyer.user.first_name,
                   'email': buyer.user.email,
                   'buyer': buyer}
            return res


class ItemsListView(ListView):
    template_name = 'shop/current/items.html'
    context_object_name = 'items'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # annotate(cnt=Count('item')).filter(cnt__gt=0)
        #
        if self.kwargs.get('category_slug'):
            category = Category.objects.filter(slug=self.kwargs.get('category_slug'))[0]
            brands = category.item_set.values_list('brand', flat=True)
            opersystems = category.item_set.values_list('opersystem', flat=True)
            context['brands'] = Brand.objects.filter(pk__in=brands)
            context['opersystems'] = OperSystem.objects.filter(pk__in=opersystems)
        else:
            context['brands'] = Brand.objects.all()
            context['opersystems'] = OperSystem.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context = make_category_data(kwargs=self.kwargs, context=context, category_slug=category_slug)
        sorting = self.request.GET.get('sort')
        context = check_sorting(sorting=sorting, context=context)
        additional_context = make_get_context(self.request)
        if additional_context:
            context.update(additional_context)
        return context

    def get_queryset(self):
        data = make_get_context(self.request)
        args = check_get_context(data=data)
        category_slug = self.kwargs.get('category_slug')
        subquery = Exists(FavoriteItem.objects.filter(buyer__user=self.request.user.id, item=OuterRef('pk')))
        subquery_cart = Exists(ShopCart.objects.filter(buyer__user = self.request.user.id, item = OuterRef('pk')))
        make_like(request=self.request)
        if category_slug:
            category_pk = self.kwargs.get('category_pk')
            res = Item.objects.filter(category__pk=category_pk, *args).annotate(like=subquery, shop_cart=subquery_cart)
        else:
            res = Item.objects.annotate(like=subquery, shop_cart=subquery_cart)
        search_results = prepare_search_items(self.request, res)
        if not search_results is None:
            return search_results
        sorting = self.request.GET.get('sort')
        if sorting:
            if sorting == 'increase':
                res = res.order_by('price')
            elif sorting == 'decrease':
                res = res.order_by('-price')
            elif sorting == 'reviews':
                res = res.annotate(cnt=Count('review')).order_by('-cnt')
        return res

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        if request.GET.get('like'):
            link = request.get_full_path()
            pk = request.GET.get('like')
            to_delete = f'&like={pk}'
            if to_delete not in link:
                to_delete = to_delete[1:]
            link = link.replace(to_delete, '')
            return redirect(link)
        elif request.GET.get('cart'):
            link = request.get_full_path()
            pk = request.GET.get('cart')
            add_shop_cart_item(request=request, pk=pk)
            to_delete = f'&cart={pk}'
            if to_delete not in link:
                to_delete = to_delete[1:]
            link = link.replace(to_delete, '')
            return redirect(link)
        else:
            return res


def about_show(request):
    return render(request, 'shop/current/about.html')


class ItemDetailView(StoreReviewCreate):
    model = Review
    template_name = 'shop/current/detail_item.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['form'].initial.get('item')
        context['item'] = item
        context['categories'] = Category.objects.all()
        context['current_category'] = item.category
        context['additional_images'] = ItemImages.objects.filter(item=item)
        context['item_reviews'] = context['reviews'].filter(item=item, to_review=None)
        if self.request.user.is_authenticated:
            buyer_pk = self.request.user.buyer.pk
        else:
            buyer_pk= None
        shop_cart_q = ShopCart.objects.filter(buyer=buyer_pk, item=item)
        initial = {'item': item, 'buyer': buyer_pk}
        if shop_cart_q:
            amount = shop_cart_q[0].amount
        else:
            amount = 1
        initial['amount'] = amount
        context['form_buy'] = ItemShopCartOrder(initial=initial)
        return context

    def get_initial(self):
        kwargs = super().get_initial()
        if not kwargs:
            kwargs = {}
        kwargs['item'] = Item.objects.get(pk=self.kwargs.get('pk'))
        to_review = self.request.GET.get('to_review')
        if to_review:
            to_review = to_review[:-1]
            kwargs['to_review'] = int(to_review)
            kwargs['content'] = Review.objects.get(pk=int(to_review)).name + ', '
        return kwargs

    def get_success_url(self):
        res = reverse('detail_item', kwargs={'pk': self.object.item.pk, 'slug': self.object.item.slug})
        res += '#'
        return res

    def post(self, request, *args, **kwargs):
        if 'content' not in request.POST:
            if not request.POST.get('buyer'):
                return redirect(reverse('login'))
            item_pk = request.POST.get('item')
            add_shop_cart_item(request, pk=item_pk, without_messages=True, rewrite=True, amount=request.POST.get('amount'))
            return redirect(reverse('make_order', kwargs={'item_pk': item_pk}))
        return super().post(request, *args, **kwargs)


class StoreLoginView(LoginView):
    template_name = 'shop/current/login.html'
    form_class = StoreAuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.authenticate_res)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class StoreLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegisterBuyerView(SuccessMessageMixin, FormView):
    template_name = 'shop/current/register.html'
    form_class = RegisterBuyerForm
    success_message = 'Поздравляем! Вы зарегистрировались на сайте.'

    def form_valid(self, form):
        user = User.objects.create_user(form.cleaned_data['username'],
                                 email=form.cleaned_data['email'],
                                 password = form.cleaned_data['password1'],
                                 first_name = form.cleaned_data['first_name'])
        self.object = user
        Buyer.objects.create(user=user, allow_mail=form.cleaned_data['allow_mail'])
        auth_login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'shop/current/profile_data.html'
    context_object_name = 'user'
    form_class = ProfileForm
    model = User
    success_message = 'Данные успешно сохранены'

    def get_form(self, form_class=None):
        res = super().get_form(form_class=None)
        res.user_id = self.request.user.id
        return res

    def get_initial(self):
        allow_mail = Buyer.objects.get(user=self.request.user).allow_mail
        initial = {'allow_mail': allow_mail}
        return initial

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class ProfilePasswordResetView(PasswordResetView):
    template_name = 'shop/current/password_reset_form.html'
    subject_template_name = 'shop/data_changing/subject_reset_view.txt'
    html_email_template_name = 'shop/data_changing/email_reset_view.html'
    form_class = ProfilePasswordResetForm

class ProfilePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'shop/current/password_reset_form_done.html'


class ProfilePasswordResetConfirmView(PasswordResetConfirmView):
    form_class = ProfileNewPasswordForm
    template_name = 'shop/current/password_reset_new_password.html'


class ProfilePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'shop/current/password_reset_form_complete.html'


class ProfilePasswordChangeView(PasswordChangeView):
    template_name = 'shop/current/password_change.html'


class ProfilePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'shop/current/password_change_done.html'


@login_required
def show_profile_shopcart(request):
    ShopCartFormSet = modelformset_factory(ShopCart, fields=('amount', 'item', 'buyer'), extra = 0,
                                           widgets = {'amount': forms.TextInput(attrs={'onkeyup': "this.value = this.value.replace(/[^\d]/g,'');"}),
                                                      'item': forms.HiddenInput(),
                                                      'buyer': forms.HiddenInput()})
    if request.method == 'POST':
        formset = ShopCartFormSet(request.POST, queryset = ShopCart.objects.filter(buyer__user = request.user))
        if formset.is_valid():
            formset.save()
            item_pk = request.POST.get('selected')
            return redirect(reverse('make_order', kwargs={'item_pk': item_pk}))
    else:
        formset = ShopCartFormSet(queryset = ShopCart.objects.filter(buyer__user = request.user))
    context = {'formset': formset}
    return render(request, 'shop/current/profile_basket.html', context)


def remove_shop_cart_item(request, pk):
    shopcart = ShopCart.objects.filter(pk=pk)
    if not shopcart:
        error(request, 'Товар уже удален с корзины')
    else:
        shopcart = shopcart[0]
        shopcart.delete()
        success(request, 'Товар успешно удален с корзины')
    return redirect(reverse('shop_cart'))


def remove_shop_cart_all(request):
    items = ShopCart.objects.filter(buyer__user=request.user.pk)
    for item in items:
        item.delete()
    success(request, 'Корзина успешно очищена')
    return redirect(reverse('shop_cart'))

def remove_item_review(request, pk, pk_item, slug_item):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    success(request, 'Отзыв успешно удален')
    return redirect(reverse('detail_item', kwargs={'pk': pk_item, 'slug': slug_item}))


class FavoriteItemListView(LoginRequiredMixin, ListView):
    template_name = 'shop/current/profile_favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return FavoriteItem.objects.filter(buyer__user=self.request.user.pk)


def remove_from_favorites(request, pk):
    favorite_item = FavoriteItem.objects.get(pk=pk)
    favorite_item.delete()
    success(request, 'Товар удален с избранного')
    return redirect(reverse('favorites'))

def remove_from_favorites_all(request):
    favorites = FavoriteItem.objects.filter(buyer__user=request.user.pk)
    for favorite in favorites:
        favorite.delete()
    success(request, 'Список очищен')
    return redirect(reverse('favorites'))

def to_shop_cart(request, pk):
    add_shop_cart_item(request=request, pk=pk)
    favorite = FavoriteItem.objects.get(buyer__user=request.user.pk, item=pk)
    favorite.delete()
    return redirect(reverse('favorites'))


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'shop/current/make_order.html'
    form_class = MakeOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['item_pk'])
        return context

    def get_initial(self):
        buyer = self.request.user.buyer
        item = Item.objects.get(pk=self.kwargs['item_pk'])
        shop_cart = ShopCart.objects.get(item=item, buyer=buyer)
        amount = shop_cart.amount
        res = {'buyer': buyer, 'item': item, 'amount': amount}
        return res

    def form_valid(self, form):
        shop_cart = ShopCart.objects.filter(item=form.cleaned_data['item'], buyer__user=self.request.user.pk)
        if shop_cart:
            shop_cart[0].delete()
        success(self.request, f'Поздравляем! Вы оформили заказ на {form.cleaned_data["item"].title}')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class OrderItemView(ListView):
    template_name = 'shop/current/profile_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return OrderItem.objects.filter(buyer__user=self.request.user.pk)


class ReviewListView(ListView):
    template_name = 'shop/current/profile_reviews.html'
    context_object_name = 'reviews'
    model = Review

    def get_queryset(self):
        return Review.objects.filter(buyer__user=self.request.user.pk)


def remove_item_review_from_account(request, pk_or_all):
    if pk_or_all == 'all':
        objects = Review.objects.filter(buyer__user=request.user.pk)
        for object in objects:
            object.delete()
        success(request, 'Ваши отзывы удалены')
    else:
        review = get_object_or_404(Review, pk=pk_or_all)
        review.delete()
        success(request, 'Отзыв успешно удален')
    return redirect(reverse('my_reviews'))


def api_documentation_view(request):
    return render(request, 'shop/current/api_documentation.html')



