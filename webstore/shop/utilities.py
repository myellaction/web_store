from datetime import datetime
from os.path import splitext
import os

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.core.exceptions import ValidationError
from django.db.models import Max, Min, Q
from django import forms

from django.contrib.messages import warning, success, error, info



def get_path_image(instance, filename):
    return os.path.join('items', instance.created.strftime("%d-%m-%Y %H-%M-%S"), f'{datetime.now().timestamp()}{splitext(filename)[1]}')

def get_path_add_image(instance, filename):
    return os.path.join('items', instance.item.created.strftime("%d-%m-%Y %H-%M-%S"), 'additional_images', f'{datetime.now().timestamp()}{splitext(filename)[1]}')


def make_get_context(request):
    res = {}
    for i in request.GET:
        if request.GET[i]:
            if i in ('min_price', 'max_price'):
                res[i] = int(request.GET.get(i))
            else:
                res[i] = request.GET.getlist(i)
    return res

def check_sorting(sorting, context):
    if sorting:
        if sorting == 'increase':
            context['sorting'] = 'increase'
        elif sorting == 'decrease':
            context['sorting'] = 'decrease'
        elif sorting == 'reviews':
            context['sorting'] = 'reviews'
    return context

def make_category_data(kwargs, context, category_slug):
    from .models import Category, Item
    category_pk = kwargs.get('category_pk')
    current_category = Category.objects.filter(slug=category_slug, pk=category_pk)[0]
    context['current_category'] = current_category
    context['min_price_default'] = Item.objects.aggregate(min_price=Min('price', filter=Q(category=current_category)))['min_price']
    context['max_price_default'] = Item.objects.aggregate(max_price=Max('price', filter=Q(category=current_category)))['max_price']
    return context

def check_get_context(data):
    args=[]
    chose_brand = Q(brand__slug__in=data.get('brand'))
    chose_opersystem = Q(opersystem__slug__in=data.get('opersystem'))
    chose_min_price = Q(price__gte=data.get('min_price'))
    chose_max_price = Q(price__lte=data.get('max_price'))
    chose_available_yes = Q(available=True)
    chose_available_no = Q(available=False)
    if data.get('brand'):
        args.append(chose_brand)
    if data.get('opersystem'):
        args.append(chose_opersystem)
    if data.get('min_price') and type(data.get('min_price')) ==int:
        args.append(chose_min_price)
    if data.get('max_price') and type(data.get('max_price')) ==int:
        args.append(chose_max_price)
    if data.get('available'):
        if len(data.get('available'))==1:
            if data.get('available')[0]=='available_yes':
                args.append(chose_available_yes)
            else:
                args.append(chose_available_no)
    return args

def make_like(request):
    from .models import FavoriteItem, Item
    like = request.GET.get('like')
    if like:
        if request.user.is_authenticated:
            res = FavoriteItem.objects.filter(item=int(like), buyer__user=request.user.id)
            if res:
                favoriteitem = res[0]
                favoriteitem.delete()
                warning(request, 'Товар удален из избранного')
            else:
                item = Item.objects.get(pk=int(like))
                FavoriteItem.objects.create(item=item, buyer=request.user.buyer)
                success(request, 'Товар добавлен в избранное')
            return True
        info(request, 'Чтобы добавить товар в избранное, нужно выполнить вход')
    return False

def add_shop_cart_item(request, pk, without_messages=None, rewrite=False, amount=1):
    from .models import ShopCart, Item
    if not request.user.is_authenticated:
        return info(request, 'Чтобы добавить товар в корзину, нужно выполнить вход')
    shop_cart_q = ShopCart.objects.filter(buyer=request.user.buyer, item=pk)
    if shop_cart_q:
        if rewrite:
            shop_cart_q.update(amount=amount)
        if not without_messages:
            info(request, 'Товар уже добавлен в корзину')
    else:
        item = Item.objects.get(pk=pk)
        ShopCart.objects.create(buyer=request.user.buyer, item=item, amount=amount)
        if not without_messages:
            success(request, 'Товар успешно добавлен в корзину')


# validators
class ForbiddenCharsValidator:
    def __init__(self, forbidden_chars=''):
        self.forbidden_chars = forbidden_chars

    def validate(self, password, user=None):
        for fc in self.forbidden_chars:
            if fc in password:
                raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return f'недопустимые символы: {self.forbidden_chars}'


class MaxLengthPasValidator:
    def __init__(self, max_length=20):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password)>self.max_length:
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return f'длинна не должна превышать {self.max_length} символов'

class MinLengthPasValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password)<self.min_length:
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return f'длинна не должна быть меньше {self.min_length} символов'

class BigCharValidator:
    def validate(self, password, user=None):
        if not any([i.isupper() for i in password]):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return 'пароль должен включать хотя бы одну заглавную букву'

class OneNumberValidator:
    def validate(self, password, user=None):
        if not any([i.isdigit() for i in password]):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return 'пароль должен включать хотя бы одну цифру'

# end validators


#search_form

class SearchForm(forms.Form):
    content = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'введите название',
                                                                            'class': 'search-block__input'}))

#end search_form

#context processors

def add_search_form_to_context(request):
    search_form = SearchForm()
    context = {'search_form': search_form}
    return context

#end context processors


def prepare_search_items(request, res):
    content = request.GET.get('content')
    if not content:
        return None
    answers = res.annotate(simil=TrigramSimilarity('title', content)).filter(simil__gte=0.1)
    if not answers:
        sr = SearchVector('title', 'description')
        answers = res.annotate(search_vector=sr).filter(search_vector=content)
    return answers

