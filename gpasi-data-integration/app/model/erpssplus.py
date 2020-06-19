
def getPessoaPorTelefone(Pessoa, **args):

    Pessoa.codstatus = "1"
    Pessoa.status    = "Pessoa encontrado!"
    Pessoa.nome      = "Rodrigo Della Justina"
    Pessoa.fantasia  = "Rodrigo Auto Peças"
    Pessoa.telefone  = args["id"]

    Pessoa.codstatus = "0"
    Pessoa.status = "Pessoa não encontrada !"
    Pessoa.nome = ""
    Pessoa.fantasia = ""
    Pessoa.telefone = args["id"]

    return Pessoa(codstatus=Pessoa.codstatus,
                  status=Pessoa.status,
                  nome=Pessoa.nome,
                  fantasia=Pessoa.fantasia,
                  telefone=Pessoa.telefone)