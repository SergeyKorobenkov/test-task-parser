import pip
import importlib
import requests
import json


def import_with_auto_install(package):
    """Установка необходимых пакетов.
    Для установки нескольких пакетов вызовите функцию 
    из тела скрипта столько раз, сколько нужно установить 
    библиотек, передав в переменную функции название 
    желаемого пакета в str формате.
    """
    try:
        return importlib.import_module(package)
    except ImportError:
        pip.main(['install', package])
    return importlib.import_module(package)

# формирование урла для ссылки на планировку
def plan_url_create(index):
    if index == 'rose':
        return
    plan_url = 'https://spires.ru/hydra/svg'
    plan_url += plans_data['flats'][index]['apartment'][0] # доступ по второму ключу осуществляется из файла apartments.json
    return plan_url


# формирование дополнительных сведений о квартире (если имеются)
def feature(spec):
    goods = []
    if spec['dl'] == 1:
        goods.append('двойной свет')
    if spec['pent'] == 1:
        goods.append('пентхаус')
    if spec['balc'] == 1:
        goods.append('балкон')
    if spec['ih'] == 1:
        goods.append('высокие потолки')
    if spec['tl'] == 1:
        goods.append('двухуровневая')
    if spec['bw'] == 1:
        goods.append('окна в ванной')
    if spec['ter'] == 1:
        goods.append('терраса')
    if spec['pano'] == 1:
        goods.append('панорамные окна')
    if spec['se'] == 1:
        goods.append('отдельный вход')
    if goods:
        return goods
    else:
        return 'None'

if __name__ == '__main__':
    pack_install = import_with_auto_install('requests') # ставим запросы
    pack_install2 = import_with_auto_install('json') # ставим json для работы с данными


    # выдираем с сайта интересующие нас данные в виде .json файлов
    villas_url = 'https://spires.ru/hydra/json/data_villas.json?v=1594305931' # урбан-виллы
    try:
        villas = requests.get(villas_url) 
        with open('villas.json', 'w', encoding='utf-8') as output_file: # создаем json-файл
            output_file.write(villas.text) # записываем в него данные ответа
    except:
        print('проблемы с получением данных об урбан-виллах')


    map_json_url = 'https://spires.ru/hydra/svg/map.json?v=20201002' # картинки с планировками
    try:    
        plans = requests.get(map_json_url)
        with open('plans.json', 'w') as output_file:
            output_file.write(plans.text)
    except:
        print('проблемы с получением данных о планировках')

    apartments_url = 'https://spires.ru/hydra/json/data.json?v=1601559156' # квартиры
    try:
        apartments = requests.get(apartments_url)
        with open('apartments.json', 'w', encoding='utf-8') as output_file:
            output_file.write(apartments.text)
    except:
        print('проблемы с получением данных о квартирах')


    parking_url = 'https://spires.ru/hydra/json/data_park.json?v=1601560513' # паркинг
    try:
        parking = requests.get(parking_url)
        with open('parking.json', 'w', encoding='utf-8') as output_file:
            output_file.write(parking.text)
    except:
        print('проблемы с получением данных о парковках')


    # подгрузка данных из содранных с сайта файлов
    with open('plans.json') as plan_file:
        plans_data = json.load(plan_file) # получаем данные из json формата о планировках квартир

    with open('apartments.json') as apartments_file:
        apartments_data = json.load(apartments_file)  # получаем данные из json формата о квартирах

    with open('villas.json') as villas_file:
        villas_data = json.load(villas_file) # получаем данные из json формата об урбан-виллах

    with open('parking.json') as parking_file:
        parking_data = json.load(parking_file) # получаем данные из json формата о паркинге


    output_list = [] # список для выгрузки в файл
    example_json = {
        'complex':'ЖК Spires',
        'type':'flat', # для вилл и квартир, 'parking' для парковок
        'phase':'None',
        'building':'None', # data['apartments'][key]['b'],
        'section':'None', # data['apartments'][key]['s'],
        'price_base':'None', #data['apartments'][key]['tc'],
        'price_finished':'None',
        'price_sale':'None',
        'price_finished_sale':'None',
        'area':'None', #data['apartments'][key]['sq'],
        'living_area':'None', #data['apartments'][key]['living_sq'] or None,
        'number':'None', #data['apartments'][key]['n'],
        'number_on_site':'None',
        'rooms':'None', #data['apartments'][key]['rc'],
        'floor':'None', #data['apartments'][key]['f'],
        'in_sale':'None', #data['apartments'][key]['st'],
        'sale_status': 'None', #'в продаже' if in_sale=1 else sale_status = 'продано',
        'finished': 'None', # 0 if price_base 
        'currency':'None',
        'ceil':'None', # высота потолков (ceil для вилл)
        'article':'None',
        'finishing_name':'None',
        'furniture':'None',
        'furniture_price':'None',
        'plan':'None', # def plan_url_create(index), возвращает строку с урлом
        'feature':'None', #заполнить особенности в соответсвии с тегом 'spec',
        'view':'None',
        'euro_planning':'None',
        'sale':'None',
        'discount_percent':'None',
        'discount':'None',
        }


    # перерабатываем исходные данные из квартир в нужый нам вид
    for key in apartments_data['apartments']:
        json_out = example_json.copy()
        json_out['building'] = apartments_data['apartments'][key]['b']
        json_out['section'] = apartments_data['apartments'][key]['s']
        json_out['price_base'] = apartments_data['apartments'][key]['tc']
        json_out['area'] = apartments_data['apartments'][key]['sq']
        json_out['number'] = apartments_data['apartments'][key]['n']
        json_out['rooms'] = apartments_data['apartments'][key]['rc']
        json_out['floor'] = apartments_data['apartments'][key]['f']
        json_out['in_sale'] = apartments_data['apartments'][key]['st']
        if json_out['in_sale'] == 1:
            json_out['sale_status'] = 'в продаже'
        else:
            json_out['sale_status'] = 'продано'
        json_out['plan'] = plan_url_create(key)
        json_out['feature'] = feature(apartments_data['apartments'][key]['spec'])
        output_list.append(json_out)


    # перерабатываем исходные данные из урбан-вилл в нужый нам вид
    for key in villas_data['apartments']:
        json_out = example_json.copy()
        json_out['type'] = 'townhouse'
        json_out['building'] = villas_data['apartments'][key]['b']
        json_out['number'] = villas_data['apartments'][key]['n']
        json_out['area'] = villas_data['apartments'][key]['sq']
        json_out['rooms'] = villas_data['apartments'][key]['rc']
        json_out['in_sale'] = 0
        json_out['ceil'] = villas_data['apartments'][key]['ceil']
        json_out['living_area'] = villas_data['apartments'][key]['living_sq']
        json_out['plan'] = ['https://spires.ru/hydra/svg/villa/f0-p{key}.svg',
                            'https://spires.ru/hydra/svg/villa/f1-p{key}.svg',
                            'https://spires.ru/hydra/svg/villa/f2-p{key}.svg',
                            'https://spires.ru/hydra/svg/villa/f3-p{key}.svg',
        ]
        output_list.append(json_out)


    # перерабатываем исходные данные паркинга в нужный нам вид
    for key in parking_data['apartments']:
        json_out = example_json.copy()
        json_out['type'] = 'parking'
        json_out['building'] = parking_data['apartments'][key]['b']
        json_out['price_base'] = parking_data['apartments'][key]['tc']
        json_out['area'] = parking_data['apartments'][key]['sq']
        json_out['number'] = parking_data['apartments'][key]['n']
        json_out['floor'] = parking_data['apartments'][key]['f']
        json_out['in_sale'] = parking_data['apartments'][key]['st']
        if json_out['in_sale'] == 1:
            json_out['sale_status'] = 'в продаже'
        else:
            json_out['sale_status'] = 'продано'
        output_list.append(json_out)


    # Записываем нужные нам данные в файл
    with open('result.json', 'w',) as output_file:
        json.dump(output_list, output_file)
