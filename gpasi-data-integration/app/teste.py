import json

class Pessoa():
    codstatus : str
    status    : str
    telefone  : str
    nome      : str
    fantasia  : str


a = Pessoa()
a.codstatus="1"
a.nome = "rodrigo"
a.status="teste"
a.fantasia="teste"
a.status="teste"

t = json.dumps(a.__dict__)
print(t)