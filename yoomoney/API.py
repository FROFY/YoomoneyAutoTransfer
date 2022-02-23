import json.decoder
import sqlite3
import time

import requests
import Config
import SQLite

conn = sqlite3.connect('yoomoney.db')
cursor = conn.cursor()
conn.commit()


def balance(token, account):
    request = requests.Session()
    request.headers['Accept'] = 'application/json'
    request.headers['authorization'] = 'Bearer ' + token
    response = request.get('https://edge.qiwi.com/funding-sources/v2/persons/' + account + '/accounts')
    bal = response.json()['accounts']
    rub = [x for x in bal if x['alias'] == 'qw_wallet_rub']
    return rub


def get_number(token):
    request = requests.Session()
    request.headers['Accept'] = 'application/json'
    request.headers['authorization'] = 'Bearer' + token
    response = request.get('https://edge.qiwi.com/person-profile/v1/profile')
    return response.json()['authInfo']['personId']


def transfer(token, to):
    request = requests.Session()
    request.headers = {'content-type': 'application/json'}
    request.headers['authorization'] = 'Bearer ' + token
    request.headers['Accept'] = 'application/json'
    postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"}, "comment":"'+comment+'","fields":{"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = balance(token, get_number(token))
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to
    res = request.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
    return res.json()
