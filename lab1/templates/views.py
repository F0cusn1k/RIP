from datetime import date
from django.shortcuts import render

def hello(request):
    return render(request, 'index.html', { 'data' : {
        'current_date': date.today(),
        'list': ['python', 'django', 'html']
    }})

TOTAL_SERVICES = 8
ROWS = [0,
        1]

COLUMNS = [0, 1, 2, 3]
# BASE_IMAGE_LINK = 'http://127.0.0.1:9000/rip/'
# TITLES = ['Факториал',
#           'Квадрат',
#           'Корень',
#           'Логарифм',
#           'НОК',
#           'НОД',
#           'C из n по k',
#           'A из n по k'
# ]

# DESCRIPTIONS = ['   Факториал — функция, определённая на множестве неотрицательных целых чисел. Факториалом числа n называют произведение всех натуральных чисел от 1 до n включительно.',
#           '    Квадрат числа — результат умножения числа на само себя. Обратной операцией является извлечение квадратного корня.',
#           '    Арифметическим квадратным корнем из неотрицательного числа n называется такое неотрицательное число, квадрат которого равен n.',
#           '    Натуральным логарифмом числа x называется такое число n, такое что математическая константа e в степени n равна x.',
#           '    Наименьшее общее кратное для нескольких чисел — это наименьшее натуральное число, которое делится на каждое из этих чисел.',
#           '    Наибольший общий делитель двух натуральных чисел — это наибольшее число, на которое числа и делятся без остатка.',
#           '    Числом сочетаний С(n, k) называется количество способов выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются одинаковыми).',
#           '    Числом размещений A(n, k) называется количество способов упорядоченно выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются различными).'
# ]

# ROWS = [0,
#         1]

# COLUMNS = [0, 1, 2, 3]

# orders = []
# for i in range (TOTAL_SERVICES):
#     temp = {}
#     temp['title'] = TITLES[i]
#     temp['id'] = i+1
#     temp['image'] = BASE_IMAGE_LINK + str(i+1) + '.png'
#     temp['description'] = DESCRIPTIONS[i]
#     orders.append(temp)

services = [
    {'title': 'Факториал', 'id': 1, 'image': 'http://127.0.0.1:9000/rip/1.png', 'description': '   Факториал — функция, определённая на множестве неотрицательных целых чисел. Факториалом числа n называют произведение всех натуральных чисел от 1 до n включительно.'},
    {'title': 'Квадрат', 'id': 2, 'image': 'http://127.0.0.1:9000/rip/2.png', 'description': '    Квадрат числа — результат умножения числа на само себя. Обратной операцией является извлечение квадратного корня.'},
    {'title': 'Корень', 'id': 3, 'image': 'http://127.0.0.1:9000/rip/3.png', 'description': '    Арифметическим квадратным корнем из неотрицательного числа n называется такое неотрицательное число, квадрат которого равен n.'},
    {'title': 'Логарифм', 'id': 4, 'image': 'http://127.0.0.1:9000/rip/4.png', 'description': '    Натуральным логарифмом числа x называется такое число n, такое что математическая константа e в степени n равна x.'},
    {'title': 'НОК', 'id': 5, 'image': 'http://127.0.0.1:9000/rip/5.png', 'description': '    Наименьшее общее кратное для нескольких чисел — это наименьшее натуральное число, которое делится на каждое из этих чисел.'},
    {'title': 'НОД', 'id': 6, 'image': 'http://127.0.0.1:9000/rip/6.png', 'description': '    Наибольший общий делитель двух натуральных чисел — это наибольшее число, на которое числа и делятся без остатка.'},
    {'title': 'C из n по k', 'id': 7, 'image': 'http://127.0.0.1:9000/rip/7.png', 'description': '    Числом сочетаний С(n, k) называется количество способов выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются одинаковыми).'},
    {'title': 'A из n по k', 'id': 8, 'image': 'http://127.0.0.1:9000/rip/8.png', 'description': '    Числом размещений A(n, k) называется количество способов упорядоченно выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются различными).'}
]

def GetSearchedServices(search_query: str):
    res = []
    count=0
    for service in services:
        if service["title"].lower().startswith(search_query.lower()):
            res.append(service)
            count+=1
    return res, count

def GetServices(request):
    # search_query = request.GET.get('query', '')
    # order_list, count = GetSearchedServices(search_query)
    # if count==0: 
    #     count=8
    #     order_list = services
    search_query = request.GET.get('query', '')
    if search_query:
        order_list, count = GetSearchedServices(search_query)
    else:
        order_list = services
        count = 8


    # software_title = request.GET.get('software_title', '')
    # req = Request.objects.filter(client_id=USER_ID, status=Request.RequestStatus.DRAFT).first()
    # software_list = Software.objects.filter(title__istartswith=software_title, is_active=True)


    return render(request, 'services.html',
                  {'data': {
                      'services': order_list,
                      'search_query': search_query,
                      'count': count,
                      'rows' : ROWS,
                      'columns' : COLUMNS,
                      'logo1': 'http://127.0.0.1:9000/rip/10.png',
                      'logo2': 'http://127.0.0.1:9000/rip/11.png',
                      'basket_logo': 'http://127.0.0.1:9000/rip/12.png',
                      'calculation_id': 0
                  }})

basket_arr = [
    {'title': 'Факториал', 'id': 1, 'image': 'http://127.0.0.1:9000/rip/1.png', 'description': '   Факториал — функция, определённая на множестве неотрицательных целых чисел. Факториалом числа n называют произведение всех натуральных чисел от 1 до n включительно.'},
    {'title': 'C из n по k', 'id': 7, 'image': 'http://127.0.0.1:9000/rip/7.png', 'description': '    Числом сочетаний С(n, k) называется количество способов выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются одинаковыми).'},
    {'title': 'Корень', 'id': 3, 'image': 'http://127.0.0.1:9000/rip/3.png', 'description': '    Арифметическим квадратным корнем из неотрицательного числа n называется такое неотрицательное число, квадрат которого равен n.'},
    {'title': 'НОК', 'id': 5, 'image': 'http://127.0.0.1:9000/rip/5.png', 'description': '    Наименьшее общее кратное для нескольких чисел — это наименьшее натуральное число, которое делится на каждое из этих чисел.'}
]

def GetBasket(request):
    return render(request, 'basket.html', {'data': {
        'title' : 'Корзина',
        'logo1': 'http://127.0.0.1:9000/rip/10.png',
        'services': basket_arr
    }})

def GetService(request, id):
    for service in services:
        if service['id'] == id:
            return render(request, 'service.html', {'data': {
                            'info': service,
                           'logo1': 'http://127.0.0.1:9000/rip/10.png'
            }})

    render(request, 'service.html')

def GetCalculation(request, id):

    return render(request, 'basket.html', {'data': {
        'title' : 'Корзина',
        'logo1': 'http://127.0.0.1:9000/rip/10.png',
        'services': basket_arr
    }})