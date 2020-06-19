from fastapi import Depends, APIRouter,  Path
from pathlib import Path as Path2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.model import erpssplus as dataerpssplus


class Pessoa(BaseModel):
    codstatus : str
    status    : str
    telefone  : str
    nome      : str
    fantasia  : str


modulo = "/"+Path2(__file__).stem

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.get(modulo+"/pessoas/{id}",
            summary="Verificar registro de pessoa por telefone",
            response_model=Pessoa)
async def check_registro_pessoa(
        id: str = Path(None, description='Número do telefone exemplo (46988016163) (ddd+numerotelefone)')
    ):

    """Operação responsável por verificar através do telefone registrado no whatsapp,
       se a mesma possui um cadastro ativo no ERP

       **codstatus** = [1] Caso tenha encontrado o registro, [0] Caso não tenha encontrado o registro...

       **status**    = string informando se o registro foi encontrado ou não....

       **telefone**  = número de telefone encontrado...

       **nome**      = Nome do cliente encontrado na base de dados do ERP

       **fantasia**  = Nome fantasia registarado na base de dados do ERP

    """
    retPessoa  = dataerpssplus.getPessoaPorTelefone(Pessoa, id=id)
    x = retPessoa.dict()

    return x
    #return {"codstatus": "1", "status":"teste", "telefone":"46998016165", "nome":"Rodrigo", "fantasia":retPessoa.fantasia}

