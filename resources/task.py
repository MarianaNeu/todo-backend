from models.task import TaskModel
from flask_restful import Resource,reqparse
from flasgger import swag_from


class Task(Resource):

#peticiones http?

    parser = reqparse.RequestParser() 
    parser.add_argument ('id', type=int)
    parser.add_argument ('description', type = str)

    @swag_from('../swagger/task/get_task.yaml')
    def get(self, id):
        tarea = TaskModel(1,"Hola Mundo") #construir un objeto
        if tarea:
            return tarea.json() #de este objeto que yo cree, retorname su json
        return {'Message': 'No se encuentra la tarea'},404  #MESSAGE SI O SI COMILLA SIMPLE, lo otro puede estar con comilla doble 
