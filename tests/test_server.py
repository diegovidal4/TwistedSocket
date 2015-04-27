import sys,ConfigParser,unittest,imp
sys.path.append('../')
import utils
from database import Database
from psycopg2 import DatabaseError

#Load Server Class
server=imp.load_source("Server","../event_server")
global config_file
config_file=False

class TestConfig(unittest.TestCase):
	def setUp(self):
		pass

	def test_config_file(self):
		try:
			config=ConfigParser.ConfigParser()
			config.readfp(open('/etc/default/event_server'))
			data=utils.as_dict(config)
			config_file=True
			if 'Database' not in data.keys():
				self.fail("Config file error: No database section")
			elif 'Log' not in data.keys():
				self.fail("No logs section")
			elif 'Default' not in data.keys():
				self.fail("No default section")
			elif 'Errors' not in data.keys():
				self.fail("No errors section")	
			else:
				self.assertTrue(True)
		except Exception as e:
			self.assertFalse(True,"Error Raised:"+str(e))


class TestDatabase(unittest.TestCase):
	def setUp(self):
		self.config=ConfigParser.ConfigParser()
		self.config.readfp(open('/etc/default/event_server'))
		self.config=utils.as_dict(self.config)

	def test_database(self):
		try:
			db=Database(self.config['Database']['host'],self.config['Database']['dbname'],self.config['Database']['user'],self.config['Database']['pass'])
			db.close()
			self.assertTrue(True)
		except DatabaseError, e:
			self.assertFalse(True,str(e))
			
class TestData(unittest.TestCase):

	def setUp(self):
		self.config=ConfigParser.ConfigParser()
		self.config.readfp(open('/etc/default/event_server'))
		self.config=utils.as_dict(self.config)

	def test_syrus_format_data(self):
		self.assertEqual(utils.get_data(">heracles<"),{})
		self.assertEqual(utils.get_data("nada"),{})
		self.assertEqual(utils.get_data(">RXART;2.0.51;ID=356612023066451<"),{'qualifier': 'R', 'format': 'Syrus', 'misc': '2.0.51', 'command': 'XART', 'imei': '356612023066451', 'data': '>RXART;2.0.51;ID=356612023066451<', 'response': ''})
		self.assertEqual(utils.get_data(">RSI8956021100034202273;ID=356612023066451<"),{'qualifier': 'R', 'format': 'Syrus', 'misc': 'ID=356612023066451', 'command': 'SI', 'imei': '356612023066451', 'data': '>RSI8956021100034202273;ID=356612023066451<', 'response': '8956021100034202273'})

	def test_error_format(self):
		#Test string: >RER13:QSI;ID=356612022471983<
		self.assertEqual(utils.get_data(">RER<"),{})
		self.assertEqual(utils.get_data("RER"),{})
		self.assertEqual(utils.get_data(">RER13:QSI;ID=356612022471983<"),{'command_error': 'QSI', 'qualifier': 'R', 'format': 'Syrus', 'err_number': '13', 'command': 'ER', 'imei': '356612022471983', 'data': '>RER13:QSI;ID=356612022471983<'})



if __name__ == '__main__':
    unittest.main(verbosity=3)