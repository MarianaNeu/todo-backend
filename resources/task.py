from models.task import TaskModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from utils import paginated_results, restrict
from flask import request

class Task(Resource):

#peticiones http?

    parser = reqparse.RequestParser() 
    parser.add_argument ('id', type=int)
    parser.add_argument ('descrip', type = str)
    parser.add_argument ('status', type = str)

    @swag_from('../swagger/task/get_task.yaml')
    def get(self, id):
        tarea = TaskModel.find_by_id(id) #construir un objeto
        if tarea:
            return tarea.json() #de este objeto que yo cree, retorname su json
        return {'Message': 'No se encuentra la tarea'},404  #MESSAGE SI O SI COMILLA SIMPLE, lo otro puede estar con comilla doble 

    @swag_from('../swagger/task/put_task.yaml')
    def put(self, id): #actualizar la informacion de un resgistro ya existente
        tarea = TaskModel.find_by_id(id) 
        print(tarea)
        if tarea:
            newdata = Task.parser.parse_args()
            tarea.from_reqparse(newdata)
            tarea.save_to_db()
            return tarea.json()

    @swag_from('../swagger/task/delete_task.yaml')
    def delete(self, id):
        tarea = TaskModel.find_by_id(id) #construir un objeto
        if tarea:
            tarea.delete_from_db()
        return {'message': 'Se ha borrado la tarea'}

class TaskList(Resource):
    @swag_from('../swagger/task/list_task.yaml')
    def get(self):
        query = TaskModel.query
        return paginated_results(query)

    @swag_from('../swagger/task/post_task.yaml')
    def post(self): #Para crear nuevos registros, como los INSERT
        data = Task.parser.parse_args()

        tarea = TaskModel(**data) #para convertir el json en un objeto tarea

        try: 
            tarea.save_to_db() #trata de ejecutar un conjunto de sentencias
        except Exception as e: #es como el CATCH, Exception es la excepcion mas global. Para manejar los errores que pueden haber
            print(e) # para que se pueda ver tambien exactamente cual es el error
            return {'message':'Ocurrio un error al crear la tarea'}, 500

        return tarea.json(), 201 #201 significa creacion exitosa


class TaskSearch(Resource):
    @swag_from('../swagger/task/search_task.yaml')
    def post(self):
        query = TaskModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: TaskModel.id == x)
            query = restrict(query,filtros,'descrip',lambda x: TaskModel.descrip.contains(x))
            query = restrict(query,filtros,'status',lambda x: TaskModel.status.contains(x))
            #logica de filtrado de datos
        return paginated_results(query)