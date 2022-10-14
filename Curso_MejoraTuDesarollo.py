class Intro():
    def __init__(self, valor):
        self.valor = valor
    
    def segundo(self):
        print("segundo")
    
    def tercero(self):
        print("tercero")

dato =  Intro("valor")

print(dir(dato))
