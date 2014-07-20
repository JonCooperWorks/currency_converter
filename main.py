import decimal
from decimal import Decimal
import os

from flask import Flask
from flask.ext import restful
from flask.ext.restful.reqparse import RequestParser
from suds.client import Client


ENDPOINT_URL = 'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL'
DEBUG = os.environ.get('HEROKU') is None

app = Flask(__name__)
api = restful.Api(app)
currency_client = Client(ENDPOINT_URL)
currency_service = currency_client.service
rate_parser = RequestParser()
converter_parser = RequestParser()
rate_parser.add_argument(
    'from', type=str, help='from must be a valid currency code.')
rate_parser.add_argument(
    'to', type=str, help='to must be a valid currency code.')
rate_parser.add_argument(
    'from', type=str, help='from must be a valid currency code.')
rate_parser.add_argument(
    'to', type=str, help='to must be a valid currency code.')
converter_parser.add_argument(
    'from', type=str, help='from must be a valid currency code.')
converter_parser.add_argument(
    'to', type=str, help='to must be a valid currency code.')
converter_parser.add_argument(
    'amount',
    type=decimal.Decimal,
    help='amount must be a valid decimal number.')


class RateResource(restful.Resource):

    def get(self):
        args = rate_parser.parse_args()
        conversion_rate = currency_service.ConversionRate(
            args['from'], args['to'])
        response = {
            'from': args['from'],
            'to': args['to'],
            'conversion_rate': conversion_rate,
        }
        return response


class ConversionResource(restful.Resource):

    def get(self):
        args = converter_parser.parse_args()
        conversion_rate = currency_service.ConversionRate(
            args['from'], args['to'])
        converted_amount = (args['amount'] *
                            Decimal.from_float(conversion_rate))
        response = {
            'from': args['from'],
            'to': args['to'],
            'conversion_rate': conversion_rate,
            'converted_amount': '%.2f' % converted_amount,
        }
        return response


api.add_resource(RateResource, '/rate')
api.add_resource(ConversionResource, '/convert')


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=os.environ.get('PORT', 5000))
