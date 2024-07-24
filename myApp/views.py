# Create your views here.
import django
import requests
import operator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .utitlies import rutronik_request, element14_request, mouser_request

from django.utils.decorators import method_decorator

method_decorator(csrf_protect)


def SearchPartNumberPage(request):
    if request.method == 'POST':
        partNumber = request.POST.get('part_number')
        volume = int(request.POST.get('volume'))
        html_data = []
        html_data += rutronik_request(partNumber, volume)
        html_data += element14_request(partNumber, volume)
        html_data += mouser_request(partNumber, volume)
        html_data.sort(key=operator.itemgetter('total_price'))

        return render(request, 'display.html', {"html_data": html_data})

    return render(request, 'search.html')


def ViewDataPage(request):
    partNumbers = ['CC0402KRX7R7BB104', 'GRM155R71H104KE14D', 'CC0603KRX7R9BB103']
    volumes = ['20000', '30000', '8000']
    html_data = []
    for partNumber, volume in zip(partNumbers, volumes):
        html_data += rutronik_request(partNumber, volume)
    html_data.sort(key=operator.itemgetter('total_price'))
    return render(request, 'view.html',
                  context={'html_data': html_data[1:],
                           'first_data': html_data[0]})


def AddCartPage(request):

    return render(request, 'addCart.html')
