from django.template import Library

register = Library()

@register.filter
def make_num_space(value):
    value = str(value)
    res = ''
    count = 0
    for i in value[::-1]:
        if count>2:
            res +=' '
            count = 0
        res+=i
        count+=1
    return res[::-1]

@register.simple_tag
def make_sort_url(value, sorting):
    params_text = value.split('/')[-1]
    params_start = value.rfind(params_text)
    if len(params_text) == 0:
        res = value + f'?sort={sorting}'
    elif len(params_text) == 1 and params_text == '?':
        res = value + f'sort={sorting}'
    elif 'sort=' in params_text:
        pre_start = params_text.find('sort=')
        start = pre_start + 5
        end = params_text.find('&', start)
        if end == -1:
            end = None
        chosed = params_text[start:end]
        params_text  = params_text.replace(f"sort={chosed}", f'sort={sorting}')
        res = value[:params_start] + params_text
    else:
        res = value + f'&sort={sorting}'
    return res

@register.simple_tag
def check_price_value(min_price=None, max_price=None, min_price_default=None, max_price_default=None):
    if min_price and max_price:
        res_min = min_price >= min_price_default and min_price <= max_price_default and min_price <= max_price
        res_max = max_price <= max_price_default
        res = res_min and res_max
    elif min_price:
        res = min_price >= min_price_default and min_price <= max_price_default
    elif max_price:
        res = max_price <= max_price_default and max_price >= min_price_default
    else:
        return None
    return res


@register.filter
def my_truncatechars(val, size):
    size = int(size)
    res = val[:size]
    if len(val) <= size:
        pass
    elif val[size] == ' ':
        pass
    else:
        index_space = res.rfind(' ')
        res = res[:index_space]
    return res

@register.simple_tag
def make_like_link(value, item_id):
    params_text = value.split('/')[-1]
    if len(params_text) in (0, 1):
        params_text= f'?like={item_id}'
    else:
        if 'like=' in params_text:
            start = params_text.index('like=') + 5
            index_end = params_text.find('&', start)
            if index_end != -1:
                last_pk = params_text[start: index_end]
            else:
                last_pk = params_text[start:]
            params_text = params_text.replace(last_pk, str(item_id))
        else:
            params_text += f'&like={item_id}'
    end = value.rfind('/') + 1
    res = value[:end] + params_text
    return res

@register.simple_tag
def make_cart_link(value, item_id):
    params_text = value.split('/')[-1]
    if len(params_text) in (0, 1):
        params_text= f'?cart={item_id}'
    else:
        if 'cart=' in params_text:
            start = params_text.index('cart=') + 5
            index_end = params_text.find('&', start)
            if index_end != -1:
                last_pk = params_text[start: index_end]
            else:
                last_pk = params_text[start:]
            params_text = params_text.replace(last_pk, str(item_id))
        else:
            params_text += f'&cart={item_id}'
    end = value.rfind('/') + 1
    res = value[:end] + params_text
    return res

@register.simple_tag
def make_page_link(value, page):
    params_text = value.split('/')[-1]
    if len(params_text) in (0, 1):
        params_text= f'?page={page}'
    else:
        if 'page=' in params_text:
            start = params_text.index('page=') + 5
            index_end = params_text.find('&', start)
            if index_end != -1:
                last_pk = params_text[start: index_end]
            else:
                last_pk = params_text[start:]
            params_text = params_text.replace(last_pk, str(page))
        else:
            params_text += f'&page={page}'
    end = value.rfind('/') + 1
    res = value[:end] + params_text
    return res

