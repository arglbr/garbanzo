#!/usr/bin/python
import urllib
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

# Global variables
provinces_url   = "https://raw.githubusercontent.com/VivaReal/code-challenge/master/provinces.json"
provinces_resp  = urllib.urlopen(provinces_url)
provinces_json  = json.loads(provinces_resp.read())
properties_url  = "https://raw.githubusercontent.com/VivaReal/code-challenge/master/properties.json"
properties_resp = urllib.urlopen(properties_url)
properties_json = json.loads(properties_resp.read())

# FlaskApp
app = Flask(__name__)

# Global methods
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}, 404))

def findProperty(property_id):
    if 'properties' in properties_json:
        for p in properties_json['properties']:
            if p.get('id') == property_id:
                ret = p
    return ret

def searchProperties(p_ax, p_ay, p_bx, p_by):
    ret = []

    if 'properties' in properties_json:
        for p in properties_json['properties']:
            # app.logger.info('p_ax=' + `p_ax` + '#p_ay=' + `p_ay` + '#p_bx=' + `p_bx` + '#p_by=' + `p_by` + '#p-long=' + `p['long']` + '#p-lat=' + `p['lat']`)
            if ((p_ax <= p['long']) and (p_ay >= p['lat'])) and ((p_bx >= p['long']) and (p_by <= p['lat'])):
                p['provinces'] = setProvince(p['long'], p['lat'])
                ret.append(p)

    return ret

def setNewPropertyID():
    ret = 0

    if 'properties' in properties_json:
        for p in properties_json['properties']:
            if p.get('id') > ret:
                ret = p.get('id')

    ret += 1
    return ret

def setProvince(p_x, p_y):
    province_list = ['Gode', 'Groola', 'Jaby', 'Nova', 'Ruja', 'Scavy']
    pvlist_len    = len(province_list)
    ret = []

    for idx in range(0, pvlist_len):
        pv = province_list[idx]

        if (p_x >= provinces_json[pv]['boundaries']['upperLeft']['x']) and (p_y <= provinces_json[pv]['boundaries']['upperLeft']['y']) and (p_x <= provinces_json[pv]['boundaries']['bottomRight']['x']) and (p_y >= provinces_json[pv]['boundaries']['bottomRight']['y']):
            ret.append(pv)

    return ret

def validateHouse(p_data):
    ret = False

    if (p_data['beds'] in range(1, 5)) and (p_data['baths'] in range(1, 4)) and (p_data['squareMeters'] in range(20, 240)) and (p_data['long'] in range(0, 1400)) and (p_data['lat'] in range(0, 1000)):
        ret = True

    return ret

# REST operations
@app.route('/garbanzo-api/provinces', methods=['GET'])
def get_provinces():
    return jsonify(provinces_json)

@app.route('/garbanzo-api/properties', methods=['GET', 'POST'])
def property():
    if request.method == 'GET':
        app.logger.info('Entrou no GET')

        if len(properties_json) == 0:
            app.logger.info('Entrou como se nao houvesse dados pra mostrar')
            abort(404)

        if len(request.args) == 0:
            app.logger.info('Entrou no ZERO')
            return jsonify(properties_json)

        if len(request.args) == 4:
            app.logger.info('Entrou no QUATRO')
            qs_ax = request.args.get('ax')
            qs_ay = request.args.get('ay')
            qs_bx = request.args.get('bx')
            qs_by = request.args.get('by')

            if len(qs_ax) > 0 and len(qs_ay) > 0 and len(qs_bx) > 0 and len(qs_by) > 0:
                app.logger.info('Entrou no ESTRANHO')
                compl = ""
                lista = searchProperties(int(qs_ax), int(qs_ay), int(qs_bx), int(qs_by))
                ret = [ { 'foundProperties' : len(lista), 'properties' : lista } ]
                return jsonify(ret)
            else:
                abort(500)
        else:
            abort(500)

    if request.method == 'POST':
        data                  = request.data
        dataDict              = json.loads(data)
        dataDict['id']        = setNewPropertyID()
        dataDict['provinces'] = setProvince(dataDict['long'], dataDict['lat'])

        if validateHouse(dataDict) == False:
           abort(500);

        properties_json['properties'].append(dataDict)
        new_data = {'id': dataDict['id'], 'provinces' : dataDict['provinces']}
        return jsonify(new_data), 201, {'Content-Type': 'application/json', 'Location': '/garbanzo-api/properties/' + `dataDict['id']`}

@app.route('/garbanzo-api/properties/<int:property_id>', methods=['GET'])
def get_property_by_id(property_id):

    property = findProperty(property_id)

    if len(property) == 0:
        abort(404)

    property['provinces'] = setProvince(property['long'], property['lat'])
    return jsonify(property)

# Start app
if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler   = RotatingFileHandler('/var/log/garbanzo.log', maxBytes=1073741824, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=80, debug=True)

