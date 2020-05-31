import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import json
from urllib.request import urlopen
import ssl

class DB:
    def __init__(self, address, port, login, password, name='Weed', structureURL='https://raw.githubusercontent.com/SharagaFun/DB-Laba-4/master/structure.sql'):
    	self.structureURL = structureURL
    	self.address = address
    	self.port = port
    	self.login = login
    	self.password = password
    	self.name = name
    	self.__createDB ()
    
    def __createDB(self):
    	conn_string = "host=" + self.address + " port=" + self.port + " dbname=postgres" + " user=" + self.login + " password=" + self.password
    	conn = psycopg2.connect(conn_string)
    	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    	cursor = conn.cursor()
    	cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (self.name, ))
    	exists = cursor.fetchone()
    	if not exists:
    		cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.name)))
    	conn.close()
    	self.__connectDB()
    	if not exists:
    		self.__initDB()
    		
    def __connectDB(self):
    	conn_string = "host=" + self.address + " port=" + self.port + " dbname=" + self.name + " user=" + self.login + " password=" + self.password
    	self.conn = psycopg2.connect(conn_string)
    	self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    	self.cursor = self.conn.cursor()
    		
    def __initDB(self):
    	self.cursor.execute(urlopen(self.structureURL, context=ssl._create_unverified_context()).read())
    	
    def deleteDB(self):
    	conn_string = "host=" + self.address + " port=" + self.port + " dbname=postgres" + " user=" + self.login + " password=" + self.password
    	self.conn.close()
    	conn = psycopg2.connect(conn_string)
    	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    	cursor = conn.cursor()
    	cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(self.name)))
    	conn.close()
    	del self
    		
    def addItem(self, name, stock, price):
    	self.cursor.execute("SELECT add_item(%s, %s, %s)", (name, stock, price, ))
    	
    def addOrder(self, item, quantity):
    	self.cursor.execute("SELECT add_order(%s, %s)", (item, quantity, ))
    	
    def clearAssortment(self):
    	self.cursor.execute("SELECT clear_assortment()")
    	
    def clearOrders(self):
    	self.cursor.execute("SELECT clear_orders()")
    	
    def clearAll(self):
    	self.cursor.execute("SELECT clear_all()")
    	
    def getAssortment(self):
    	self.cursor.execute("SELECT get_assortment()")
    	return self.cursor.fetchone()[0]
    	
    def getOrders(self):
    	self.cursor.execute("SELECT get_orders()")
    	return self.cursor.fetchone()[0]
    
    def getAssortment(self):
    	self.cursor.execute("SELECT get_assortment()")
    	return self.cursor.fetchone()[0]
    
    def search(self, query):
    	self.cursor.execute("SELECT search(%s)", (query, ))
    	return self.cursor.fetchone()[0]
    	
    def deleteByName(self, name):
    	self.cursor.execute("SELECT delete_by_name(%s)", (name, ))
    	
    def deleteOrder(self, id):
    	self.cursor.execute("SELECT delete_order(%s)", (id, ))
    	
    def deleteItem(self, id):
    	self.cursor.execute("SELECT delete_item(%s)", (id, ))
    	
    def updateItemName(self, id, name):
    	self.cursor.execute("SELECT update_item_name(%s, %s)", (id, name, ))
    	
    def updateItemStock(self, id, stock):
    	self.cursor.execute("SELECT update_item_stock(%s, %s)", (id, stock, ))
    	
    def updateItemPrice(self, id, price):
    	self.cursor.execute("SELECT update_item_price(%s, %s)", (id, price, ))
   		
    def updateOrderItem(self, id, item):
    	self.cursor.execute("SELECT update_order_item(%s, %s)", (id, item, ))
   		
    def updateOrderQuantity(self, id, quantity):    	
    	self.cursor.execute("SELECT update_order_quantity(%s, %s)", (id, quantity, ))

