# Create your views here.
import django
import requests
import operator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .utitlies import rutronik_request, element14_request, mouser_request, getTotalData

from django.utils.decorators import method_decorator

method_decorator(csrf_protect)

html_data = getTotalData()


def SearchPartNumberPage(request):
    if request.method == 'POST':
        partNumber = request.POST.get('part_number')
        volume = int(request.POST.get('volume', 0))
        _html_data = []
        _html_data += rutronik_request(partNumber, volume)
        _html_data += element14_request(partNumber, volume)
        _html_data += mouser_request(partNumber, volume)
        _html_data.sort(key=operator.itemgetter('total_price'))

        return render(request, 'display.html', {"html_data": html_data})

    return render(request, 'search.html')


def ViewDataPage(request):
    return render(request, 'view.html',
                  context={'html_data': html_data[1:],
                           'first_data': html_data[0]})


def AddCartPage(request):
    return render(request, 'addCart.html',
                  {'data': html_data[0]})
