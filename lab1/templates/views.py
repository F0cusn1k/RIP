from datetime import date
from django.shortcuts import render

def hello(request):
    return render(request, 'index.html', { 'data' : {
        'current_date': date.today(),
        'list': ['python', 'django', 'html']
    }})

# def GetOrders(request):
#     return render(request, 'orders.html', {'data' : {
#         'current_date': date.today(),
#         'orders': [
#             {'title': 'Книга с картинками', 'id': 1},
#             {'title': 'Бутылка с водой', 'id': 2},
#             {'title': 'Коврик для мышки', 'id': 3},
#         ]
#     }})

TOTAL_SERVICES = 8
BASE_IMAGE_LINK = 'http://127.0.0.1:9000/rip/'
TITLES = ['Факториал',
          'Квадрат',
          'Корень',
          'Логарифм',
          'НОК',
          'НОД',
          'C из n по k',
          'A из n по k'
]

DESCRIPTIONS = ['   Факториал — функция, определённая на множестве неотрицательных целых чисел. Факториалом числа n называют произведение всех натуральных чисел от 1 до n включительно.',
          '    Квадрат числа — результат умножения числа на само себя. Обратной операцией является извлечение квадратного корня.',
          '    Арифметическим квадратным корнем из неотрицательного числа n называется такое неотрицательное число, квадрат которого равен n.',
          '    Натуральным логарифмом числа x называется такое число n, такое что математическая константа e в степени n равна x.',
          '    Наименьшее общее кратное для нескольких чисел — это наименьшее натуральное число, которое делится на каждое из этих чисел.',
          '    Наибольший общий делитель двух натуральных чисел — это наибольшее число, на которое числа и делятся без остатка.',
          '    Числом сочетаний С(n, k) называется количество способов выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются одинаковыми).',
          '    Числом размещений A(n, k) называется количество способов упорядоченно выбрать k из n различных предметов (наборы, отличающиеся только порядком, считаются различными).'
]

ROWS = [0,
        1]

COLUMNS = [0, 1, 2, 3]

orders = []
for i in range (TOTAL_SERVICES):
    temp = {}
    temp['title'] = TITLES[i]
    temp['id'] = i+1
    temp['image'] = BASE_IMAGE_LINK + str(i+1) + '.png'
    temp['description'] = DESCRIPTIONS[i]
    orders.append(temp)

def GetSearchedOrders(search_query: str):
    res = []
    count=0
    for order in orders:
        if order["title"].lower().startswith(search_query.lower()):
            res.append(order)
            count+=1
    return res, count

def GetOrders(request):
    search_query = request.GET.get('q', '')
    order_list, count = GetSearchedOrders(search_query)
    if count==0: count=8


    return render(request, 'orders.html',
                  {'data': {
                      'orders': order_list,
                      'search_query': search_query,
                      'count': count,
                      'rows' : ROWS,
                      'columns' : COLUMNS
                  }})


# def GetOrders(request):
#     return render(request, 'orders.html', {'data' : {
#         'orders': orders,
#         'rows' : ROWS,
#         'columns' : COLUMNS
#     }})

def GetBasket(request):
    return render(request, 'basket.html', {'data': {
        'title' : 'Корзина',
        'ordercounter': 52
    }})

def GetOrder(request, id):
    for order in orders:
        if order['id'] == id:
            return render(request, 'order.html',
                          {'data': order})

    render(request, 'order.html')