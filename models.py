from twistar.dbobject import DBObject


#Registry.DBPOOL = adbapi.ConnectionPool('psycopg2', user="gpsweb", password="gpsweb", database="gpsweb",host='190.54.34.35')

class Mobile(DBObject):
	TABLENAME=""" "Mobile" """
class HistoryGps(DBObject):
	TABLENAME=""" "HistoryGps" """
class GpsResponse(DBObject):
	TABLENAME=""" "GpsResponse" """

if __name__ == '__main__':
	imei='356612023066451'
	Mobile.find(where=['imei=?',imei],limit=1).addCallback(done)
	reactor.run()