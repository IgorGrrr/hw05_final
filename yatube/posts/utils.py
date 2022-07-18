from django.core.paginator import Paginator


def paginator(request, queryset):
    quantity = 10
    paginator = Paginator(queryset, quantity)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
