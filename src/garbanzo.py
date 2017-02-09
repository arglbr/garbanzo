#!/usr/bin/python
"""This module solves the challenge for Spotippos.
Example requests:
* http://{host}:{port}/garbanzo-api/provinces
* http://{host}:{port}/garbanzo-api/properties
* http://{host}:{port}/garbanzo-api/properties/2
* http://{host}:{port}/garbanzo-api/properties?ax=630&ay=680&bx=685&by=675

"""
import urllib
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, abort, make_response, request

# Base URL for provinces and properties.
BASE_URL        = "https://raw.githubusercontent.com/VivaReal/code-challenge"

# Provinces data.
provinces_url   = BASE_URL + "/master/provinces.json"
provinces_resp  = urllib.urlopen(provinces_url)
provinces_json  = json.loads(provinces_resp.read())

# Properties data.
properties_url  = BASE_URL + "/master/properties.json"
properties_resp = urllib.urlopen(properties_url)
properties_json = json.loads(properties_resp.read())

# FlaskApp
app = Flask(__name__)

# Garbanzo "business" methods
@app.errorhandler(404)
def not_found(error):
    """Method to handle 404

    Just a helper to make a default response for 404 status code. 

    """
    return make_response(jsonify({'error': 'Not found'}, 404))

def findProperty(property_id):
    """Method to find a property inside the JSON of properties.

    Receives an integer to find the related property among the JSON
    properties.
          :param property_id: Integer representing the ID of the
                              property.

    """
    if 'properties' in properties_json:
        for p in properties_json['properties']:
            if p.get('id') == property_id:
                ret = p
    return ret

def searchProperties(p_ax, p_ay, p_bx, p_by):
    """Method to find properties inside an area.

    Receives four integers that represents the upper-left and
    bottom-right of the are that need to be explored. Returns all
    properties inside that area.
          :param property_id: Integer representing the ID of the
                              property.

    """
    ret = []

    if 'properties' in properties_json:
        for p in properties_json['properties']:
            if ((p_ax <= p['long']) \
                    and (p_ay >= p['lat'])) \
                    and ((p_bx >= p['long']) \
                    and (p_by <= p['lat'])):
                p['provinces'] = setProvince(p['long'], p['lat'])
                ret.append(p)

    return ret

def setNewPropertyID():
    """Generates a new ID for a created property.

    Iterate over the whole JSON to garantee that a new ID will be
    generated for the new Property.

    """
    ret = 0

    if 'properties' in properties_json:
        for p in properties_json['properties']:
            if p.get('id') > ret:
                ret = p.get('id')

    ret += 1
    return ret

def setProvince(p_x, p_y):
    """Defines the provice for a property.

    Based on its X/Y positions, defines the set of provinces the
    property belongs to.

    """
    province_list = ['Gode', 'Groola', 'Jaby', 'Nova', 'Ruja', 'Scavy']
    pvlist_len    = len(province_list)
    ret = []

    for idx in range(0, pvlist_len):
        pv = province_list[idx]

        if (p_x >= provinces_json[pv]['boundaries']['upperLeft']['x']) \
            and (p_y <= provinces_json[pv]['boundaries']['upperLeft']['y']) \
            and (p_x <= provinces_json[pv]['boundaries']['bottomRight']['x']) \
            and (p_y >= provinces_json[pv]['boundaries']['bottomRight']['y']):
            ret.append(pv)

    return ret

def validateHouse(p_data):
    """Run the range business validation rules.

    Validates if a property has the right values for its attributes.

    """
    ret = False

    if (p_data['beds'] in range(1, 5)) \
            and (p_data['baths'] in range(1, 4)) \
            and (p_data['squareMeters'] in range(20, 240)) \
            and (p_data['long'] in range(0, 1400)) \
            and (p_data['lat'] in range(0, 1000)):
        ret = True

    return ret

# REST Services
API_ROOT = '/garbanzo-api'

@app.route(API_ROOT + '/provinces', methods=['GET'])
def get_provinces():
    """Return all the provinces."""
    return jsonify(provinces_json)

@app.route(API_ROOT + '/properties', methods=['GET', 'POST'])
def property():
    """Return and create properties."""
    if request.method == 'GET':
        if len(properties_json) == 0:
            app.logger.info('The properties data is empty. Aborting.')
            abort(404)

        if len(request.args) == 0:
            app.logger.info('Properties operation without query string.')
            return jsonify(properties_json)

        if len(request.args) == 4:
            app.logger.info('Properties operation with geo querystring.')
            qs_ax = request.args.get('ax')
            qs_ay = request.args.get('ay')
            qs_bx = request.args.get('bx')
            qs_by = request.args.get('by')

            if len(qs_ax) > 0 and len(qs_ay) > 0 \
                    and len(qs_bx) > 0 and len(qs_by) > 0:
                compl = ""
                lista = searchProperties(int(qs_ax), int(qs_ay),
                                         int(qs_bx), int(qs_by))
                ret = [{'foundProperties' : len(lista),
                        'properties' : lista}]
                return jsonify(ret)
            else:
                app.logger.error('Properties query string informed but invalid.')
                abort(500)
        else:
            abort(500)

    if request.method == 'POST':
        data                  = request.data
        dataDict              = json.loads(data)
        dataDict['id']        = setNewPropertyID()
        dataDict['provinces'] = setProvince(dataDict['long'], dataDict['lat'])

        if validateHouse(dataDict) == False:
           app.logger.error('The property data contains invalid information. Review your beds, baths or area parameters.')
           abort(500);

        properties_json['properties'].append(dataDict)
        prop_id = dataDict['id']
        ret = {'id': prop_id, 'provinces' : dataDict['provinces']}
        app.logger.info('Created property#' + `prop_id`)
        return jsonify(ret), \
                       201, \
                       {'Content-Type': 'application/json', \
                        'Location': '/garbanzo-api/properties/' + `prop_id`}

@app.route(API_ROOT + '/properties/<int:property_id>', methods=['GET'])
def get_property_by_id(property_id):
    """Return a specific property."""
    property = findProperty(property_id)

    if len(property) == 0:
        app.logger.error('The property data contains invalid information. Review your beds, baths or area parameters.')
        abort(404)

    property['provinces'] = setProvince(property['long'], property['lat'])
    app.logger.info('Grabbing property#' + `property['id']`)
    return jsonify(property)


# Start app
if __name__ == '__main__':
    log_format  = "[%(asctime)s] {%(pathname)s"
    log_format += ":%(lineno)d} %(levelname)s - %(message)s"
    formatter   = logging.Formatter(log_format)
    handler     = RotatingFileHandler('/var/log/garbanzo.log',
                                      maxBytes=1073741824, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run()

