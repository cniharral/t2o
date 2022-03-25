#!/usr/bin/env python3

"""
Se necesita entrar en https://exchange.blockchain.com , crear un usuario para logarse y una vez logado, generar la clave API, tal y como se especifica en: https://api.blockchain.com/v3/#/.

  To Get Started

  Create or log into your existing Blockchain.com Exchange account
  Select API from the drop down menu
  Fill out form and click “Create New API Key Now”
  Once generated you can view your keys under API Settings.
  Please be aware that the API key can only be used once it was verified via email.

  The API key must be set via the
    X-API-Token
  header.

  The base URL to be used for all calls is
  https://api.blockchain.com/v3/exchange

  Autogenerated clients for this API can be found here.

Ejemplo de llamada para obtener los datos:

  curl -H "X-API-Token: <api_token>" -X GET "https://api.blockchain.com/v3/exchange/l3/BTC-USD"

"""

import sys
import pycurl
import io
import simplejson
import numpy as np
import pprint
from optparse import OptionParser
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

pp = pprint.PrettyPrinter(indent=4)

class Blockchain:
	"""Clase maestra que maneja el diálogo con el API Exchange de Blockchain.com
	"""

	baseurl = "https://api.blockchain.com/v3/exchange"
	api_token = ""
	data = {}

	def __init__ (self, api_token):
		"""Inicializa la clase.

        :param api_token: API token
        :type api_token: str
		"""

		self.api_token = api_token


	def get_info (self, order):
		"""Obtiene los datos de compras (bids) y ventas (asks) con respecto a la relación entre la cryptomoneda y moneda real definidas (symbol).

        :param order: 
        :type order: str
        :return: Info
        :rtype: dict
		"""

		url = "%s/%s" % (self.baseurl, order)

		s = io.BytesIO()

		curl = pycurl.Curl()
		curl.setopt(pycurl.URL, url)
		curl.setopt(pycurl.HTTPHEADER, [ "X-API-Token: %s" % self.api_token ])
		curl.setopt(pycurl.FOLLOWLOCATION, True)
		curl.setopt(pycurl.WRITEFUNCTION, s.write)
		curl.setopt(pycurl.VERBOSE, 0)
		curl.perform()
		curl.close()

		self.data = simplejson.loads(s.getvalue())

		return self.data


class Blockchain_L3 (Blockchain):
	"""Clase maestra que maneja el diálogo con el API Exchange de Blockchain.com para la orden l3 ("Level 3 Order Book")
	"""

	symbol = ""
	crypto = ""
	realmoney = ""

	def get_info (self, crypto, realmoney):
		"""Obtiene los datos de compras (bids) y ventas (asks) con respecto a la relación entre la cryptomoneda y moneda real definidas (symbol).

        :param order: 
        :type order: str
        :param crypto: Cryptomoneda (BTC=bitcoin, ETH=Ethereum, ...)
        :type crypto: str
        :param realmoney: Moneda real (USD=dolar, GBP=libra esterlina, EUR=euro, ...)
        :type realmoney: str
        :return: Info
        :rtype: dict
		"""

		self.crypto = crypto
		self.realmoney = realmoney
		self.symbol = "%s-%s" % (crypto, realmoney)
		order = "l3/%s" % self.symbol

		return super().get_info(order)


	def get_stats_bids_asks (self, order_type):
		"""Obtiene las estadísticas de compras (bids) y ventas (asks):
        + Media de cantidad
        + Datos correspondientes a la mayor cantidad
        + Datos correspondientes a la menor cantidad
        + Precio total acumulado
        + Cantidad total acumulada

        :param order_type: "bids" (compras) o "asks" (ventas)
        :type order_type: str
        :return r: Estadísticas de compras y ventas
        :rtype: dict
		"""

		average_value = np.mean([ bid["qty"]*bid["px"] for bid in self.data[order_type] ])
		max_value = max(self.data[order_type], key=lambda x: x["qty"]*x["px"])
		max_value["value"] = max_value["qty"] * max_value["px"]
		min_value = min(self.data[order_type], key=lambda x: x["qty"]*x["px"])
		min_value["value"] = min_value["qty"] * min_value["px"]
		total_qty = sum([ bid["qty"] for bid in self.data[order_type] ])
		total_px = sum([ bid["px"] for bid in self.data[order_type] ])

		r = {
			order_type: {
				"average_value": average_value,
				"greater_value": max_value,
				"lesser_value": min_value,
				"total_qty": total_qty,
				"total_px": total_px
			}
		}

		return r


	def get_stats_general (self):
		"""Obtiene las estadísticas generales de compras (bids) y ventas (asks):
        + Número de órdenes de compra.
        + Número de órdenes de venta.
        + Valor total de las órdenes de compra.
        + Valor total de las órdenes de venta.
        + El total de monedas de las órdenes de compra.
        + El total de monedas de las órdenes de venta.

        :return r: Estadísticas generales de compras y ventas
        :rtype: dict
		"""

		count_bids = len(self.data["bids"])
		count_asks = len(self.data["asks"])
		total_qty_bids = sum([ bid["qty"] for bid in self.data["bids"] ])
		total_qty_asks = sum([ bid["qty"] for bid in self.data["asks"] ])
		total_value_bids = sum([ bid["qty"]*bid["px"] for bid in self.data["bids"] ])
		total_value_asks = sum([ bid["qty"]*bid["px"] for bid in self.data["asks"] ])

		r = {
			self.symbol: {
				"bids": {
					"count": count_bids,
					"qty": total_qty_bids,
					"value": total_value_bids
				},
				"asks": {
					"count": count_asks,
					"qty": total_qty_asks,
					"value": total_value_asks
				}
			}
		}

		return r


if __name__ == "__main__":

	usage = """
  %prog [-t|--api-token] [-c|--crypto <cryptomoneda>] [-r|--realmoney <moneda real>] [-s|--stats <general,bids,asks>] [-h|--help]

Example:
  %prog -t e3b35a91-ec09-40b1-a2ef-f09f66e1f8d8 -c BTC -r EUR --stats bids
  %prog -t e3b35a91-ec09-40b1-a2ef-f09f66e1f8d8 -c BTC -r USD --stats asks
  %prog -t e3b35a91-ec09-40b1-a2ef-f09f66e1f8d8 -c BTC -r GBP --stats general
	"""

	parser = OptionParser(usage)
	parser.add_option("-t", "--api-token", dest="api_token", default="", help="[Obligatorio] API token")
	parser.add_option("-c", "--crypto", dest="crypto", default="BTC", help="[Obligatorio] Cryptomoneda")
	parser.add_option("-r", "--realmoney", dest="realmoney", default="EUR", help="[Obligatorio] Moneda real")
	parser.add_option("-s", "--stats", dest="stats", default="general", help="[Obligatorio] Estadísticas (con valores: general [generales], bids [de compras], asks [de ventas])")

	(options, args) = parser.parse_args()

	if not options.api_token:
		print("WARNING: Se necesita el token del API (ver info en https://api.blockchain.com/v3/")
		print(usage)
		sys.exit(-1)
	if options.api_token and options.crypto and options.realmoney:
		bc = Blockchain_L3(options.api_token)
		bc.get_info(options.crypto, options.realmoney)
	if options.stats == "general":
		pp.pprint(bc.get_stats_general())
	elif options.stats == "bids":
		pp.pprint(bc.get_stats_bids_asks("bids"))
	elif options.stats == "asks":
		pp.pprint(bc.get_stats_bids_asks("asks"))
	else:
		print("WARNING: Valor no soportado")
		print(usage)
		sys.exit(-1)

	sys.exit(0)


