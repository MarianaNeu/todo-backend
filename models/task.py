class TaskModel (): #Definicion de una clase
    
    #definicion de los atributos de la clase
    id = int 
    description = str

    def __init__(self, id, description): #Definicion de un constructror para una clase. Self es el objeto, seria el THIS de java
   
    #def se utiliza para definir metodos y lo de init para los constructores
    
        self.id = id
        self.description = description 

    def json (self, depth =0): #que retorne en formato json o formato diccionario
        json = {
            'id' : self.id,
            'description' : self.description
        }
        return json 


