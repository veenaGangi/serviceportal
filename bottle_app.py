#  A very simple Bottle Hello World app for you to get started with...
import datetime
import time
import os
from logging import debug

import pymongo
from bson.objectid import ObjectId
ON_PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ

client = pymongo.MongoClient("mongodb://vgangi_alpa:Aruvi1028@vgangi-shard-00-00.3wnqg.mongodb.net:27017,vgangi-shard-00-01.3wnqg.mongodb.net:27017,vgangi-shard-00-02.3wnqg.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-abxara-shard-0&authSource=admin&retryWrites=true&w=majority",
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None,
                             # socketKeepAlive=True,
                             connect=False, maxPoolsize=1)
db = client.userdb
db2 = client.employee

from bottle import get, post, request, response, template, redirect, default_app, run


# APPLICATION PAGES AND ROUTES

# assume collection contains fields "id", "task", "status"

@get('/')
def get_search_list():
    # return list(result)
    # get all the items in the collection as a list of dictionaries
    return template("searchList",session={})
@get('/todo')
def get_show_list():
    result = db.task.find()
    # return list(result)
    # get all the items in the collection as a list of dictionaries
    return template("show_list", rows=result,session={}, testList=result)

@get('/employeeManager')
def get_show_list():
    result = db2.task.find()
    # return list(result)
    # get all the items in the collection as a list of dictionaries
    return template("employeeController", rows=result,session={})

@get('/new_employee')
def get_new_item():
    return template("createEmployee")

@post('/add_employee')
def post_new_employee():
    # given a new task in a form, create and insert a document and with that task value
    name = request.forms.get("name").strip()
    role = request.forms.get("role").strip()
    phoneNumber = request.forms.get("phoneNumber").strip()
    city = request.forms.get("city").strip()
    state = request.forms.get("state").strip()
    projectStatus = request.forms.get("projectStatus").strip()
    email = request.forms.get("email").strip()
    result = db2.task.insert_one( {'name': name,'role': role,'phoneNumber': phoneNumber,'city': city,'state': state,'projectStatus': projectStatus,'email':email, 'status':False} )
    redirect('/employeeManager')

@get('/update_employee/<_id>')
def get_update_employee(_id):
    # given an id, get the document and populate a form
    result = db2.task.find_one( {"_id": ObjectId(_id)} )
    return template("updateEmployee", row=dict(result))

@post('/update_employee')
def post_update_task():
    # given an id and an updated task in a form, find the document and modify the task value
    _id = request.forms.get("_id").strip()
    name = request.forms.get("name").strip()
    role = request.forms.get("role").strip()
    phoneNumber = request.forms.get("phoneNumber").strip()
    city = request.forms.get("city").strip()
    state = request.forms.get("state").strip()
    projectStatus = request.forms.get("projectStatus").strip()
    email = request.forms.get("email").strip()
    result = db2.task.update_one( {"_id" : ObjectId(_id)}, {'$set': {'name': name,'role': role,'phoneNumber': phoneNumber,'city': city,'state': state,'email':email,'projectStatus': projectStatus, 'status':False}} )
    redirect('/employeeManager')

@get('/deleteEmployee/<_id>')
def get_delete_employee(_id):
    # given an id, delete the relevant document
    result = db2.task.delete_one( {"_id": ObjectId(_id)} )
    redirect('/employeeManager')

@post('/search_employee')
def post_update_task():
    # given an id and an updated task in a form, find the document and modify the task value
    searchName = request.forms.get("searchName").strip()
    result = db2.task.find_one({"name": searchName})
    return template("updateEmployee", row=dict(result))

@get('/update_status/<_id>/<value:int>')
def get_update_status(_id, value):
    result = db.task.update_one( {"_id" : ObjectId(_id)}, {'$set': {'status': (value!=0)}} )
    redirect('/')


@get('/delete_item/<_id>')
def get_delete_item(_id):
    # given an id, delete the relevant document
    result = db.task.delete_one( {"_id": ObjectId(_id)} )
    redirect('/')


@get('/update_task/<_id>')
def get_update_task(_id):
    # given an id, get the document and populate a form
    result = db.task.find_one( {"_id": ObjectId(_id)} )
    return template("update_task", row=dict(result))

@post('/update_task')
def post_update_task():
    # given an id and an updated task in a form, find the document and modify the task value
    _id = request.forms.get("_id").strip()
    updated_task = request.forms.get("updated_task").strip()
    result = db.task.update_one( {"_id" : ObjectId(_id)}, {'$set': {'task': updated_task}} )
    redirect('/')

@get('/new_item')
def get_new_item():
    return template("new_item")


@post('/new_item')
def post_new_item():
    # given a new task in a form, create and insert a document and with that task value
    new_task = request.forms.get("new_task").strip()
    result = db.task.insert_one( {'task': new_task, 'status':False} )
    redirect('/')

if ON_PYTHONANYWHERE:
    # on PA, connect to the WSGI server
    application = default_app()
else:
    # on the development environment, run the development server
    debug(True)
    run(host='localhost', port=8080)

if __name__ == "__main__":
    #db.tasks.insert_one({'id':1, 'task':"read a book on Mongo", "status":False})
    #db.tasks.insert_one({'id':2, 'task':"read a another book on PyMongo", "status":False})
    print(get_show_list())