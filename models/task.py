from argparse import Namespace
from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something

class TaskModel (db.Model): #Definicion de una clase
    __tablename__ = 'task'
    
    #definicion de los atributos de la clase
    id = db.Column(db.Integer, primary_key = True)
    descrip = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, id, descrip, status): #Definicion de un constructror para una clase. Self es el objeto, seria el THIS de java
    #def se utiliza para definir metodos y lo de init para los constructores
        self.id = id
        self.descrip = descrip
        self.status = status

    def json (self, depth =0): #que retorne en formato json o formato diccionario
        json = {
            'id' : self.id,
            'descrip' : self.descrip,
            'status' : self.status
        }
        return json 
    
    @classmethod #para indicar que este metodo es un metodo de la clase de tarea que va a ser utilizado en otro lado
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def from_reqparse(self, newdata: Namespace):
        for no_pk_key in ['descrip','status']:
            _assign_if_something(self, newdata, no_pk_key)


