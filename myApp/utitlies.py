import requests


def rutronik_request(part_number, volume):
    rutronik_url = "https://www.rutronik24.com/api/search/?apikey=cc6qyfg2yfis&searchterm="
    rutronik_url = rutronik_url + part_number
    rutronik_response = requests.get(rutronik_url)
    rutronik_json = rutronik_response.json()
    rutronik_json_data = []
    for i in rutronik_json:
        rutronik_json_data.append(modifyRutronikJsonData(i, "RUTRONIK", volume))
    return rutronik_json_data


def mouser_request(part_number, volume):
    mouser_url = "https://api.mouser.com/api/v1/search/partnumber?apiKey=82675baf-9a58-4d5a-af3f-e3bbcf486560"
    json_data = {"SearchByPartRequest": {
                    "mouserPartNumber": part_number,
                    "partSearchOptions": "string"
                }
            }
    headers = {'Content-Type': 'application/json'}
    mouser_response = requests.post(mouser_url, json=json_data, headers=headers)
    mouser_json = mouser_response.json().get('SearchResults', None)
    if mouser_json:
        mouser_json = mouser_json.get('Parts', None)
    mouser_json_data = []
    if mouser_json:
        for i in mouser_json:
            mouser_json_data.append(modifyMouserJsonData(i, "MOUSER", volume))
    return mouser_json_data


def element14_request(part_number, volume):
    element14_url = "http://api.element14.com//catalog/products?term=manuPartNum:" + part_number + "&storeInfo.id=in.element14.com&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.refinements.filters=inStock&resultsSettings.responseGroup=medium&callInfo.omitXmlSchema=false&callInfo.callback=&callInfo.responseDataFormat=json&callinfo.apiKey=wb9wt295qf3g6m842896hh2u"
    element14_response = requests.get(element14_url)
    element14_json = element14_response.json().get('manufacturerPartNumberSearchReturn', None)
    if element14_json:
        element14_json = element14_json.get('products', None)
    element14_json_data = []
    if element14_json:
        for i in element14_json:
            element14_json_data.append(modifyElementJsonData(i, "ELEMENT 14", volume))
    return element14_json_data


def getUnitPrice(price_breaks, volume, quantity_key, price_key, parse=False):
    quantity_ranges = [d.get(quantity_key, None) for d in price_breaks]
    unit_price = 0
    for i in range(len(quantity_ranges)):
        if volume <= quantity_ranges[i]:
            unit_price = [element for element in price_breaks if element[quantity_key] == quantity_ranges[i]]
            unit_price = unit_price[0].get(price_key, 0)
            break
    if unit_price == 0:
        price_range = [element for element in price_breaks if element[quantity_key] == quantity_ranges[-1]]
        unit_price = price_range[0].get(price_key, 0)
        if parse:
            unit_price = unit_price[1:]

    return unit_price


def modifyRutronikJsonData(response, data_provider, volume):
    manufacturer = response['manufacturer']
    manufacture_part_number = response['mpn']
    price_breaks = response['pricebreaks']
    unit_price = float(getUnitPrice(price_breaks, volume, 'quantity', 'price'))
    currency = response['currency']
    if currency == 'USD':
        unit_price *= 84
    elif currency == 'EUR':
        unit_price *= 90
    total_price = unit_price * volume
    result_data = {'data_provider': data_provider, 'manufacturer': manufacturer, 'part_number': manufacture_part_number,
                   'volume': volume, 'unit_price': unit_price, 'total_price': total_price}
    return result_data


def modifyMouserJsonData(response, data_provider, volume):
    manufacturer = response['Manufacturer']
    manufacture_part_number = response['ManufacturerPartNumber']
    price_breaks = response['PriceBreaks']
    unit_price = float(getUnitPrice(price_breaks, volume, 'Quantity', 'Price', True))
    total_price = unit_price * volume
    result_data = {'data_provider': data_provider, 'manufacturer': manufacturer, 'part_number': manufacture_part_number,
                   'volume': volume, 'unit_price': unit_price, 'total_price': total_price}
    return result_data


def modifyElementJsonData(response, data_provider, volume):
    manufacturer = response['vendorName']
    manufacture_part_number = response['translatedManufacturerPartNumber']
    price_breaks = response['prices']
    unit_price = float(getUnitPrice(price_breaks, volume, 'to', 'cost'))
    total_price = unit_price * volume
    result_data = {'data_provider': data_provider, 'manufacturer': manufacturer, 'part_number': manufacture_part_number,
                   'volume': volume, 'unit_price': unit_price, 'total_price': total_price}
    return result_data
