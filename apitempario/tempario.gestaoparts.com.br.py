import pandas as pd
import json
from collections import OrderedDict
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask_cors import CORS, cross_origin
from flask_compress import Compress
from waitress import serve
import requests
import psycopg2
import decimal
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from psycopg2.extras import RealDictCursor
import time
import datetime as date
import asyncio



#por Rodrigo Della Justina
#09/09/2020
production = True
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
Compress(app)
CORS(app)
statusservice = "[PRD] - Teste Consulta Serviço Tempário Gestão Parts"


try:
    #ambiente de produção
    print('Conexão com PostgreSQL Ok')
    connpgtemp = psycopg2.connect(host='localhost', user='postgres', password='pgsql', dbname='apitempario', port='5494')
    connpgtemp.autocommit = True
except:
    print('Conexão com PostgreSQL Falhou')
    connpgtemp = 0


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        # Any other serializer if needed
        return super(CustomJSONEncoder, self).default(o)

class Tempario:

    ambiente       = "HOMOLOGAÇÃO"
    curl           = ""
    urlProducao    = "https://api.tempario.com.br"
    urlHomologacao = "http://api.dev.tempario.com.br"
    cnpj           = ""
    token          = ""
    segmento       = ""

    def __init__(self, cnpj):
        self.getDadosEmpresa(cnpj)
        self.setAmbiente(self.ambiente)

    def setAmbiente(self, ambiente):
        self.ambiente = ambiente

    def geturl(self):
        if (self.ambiente == "PRODUÇÃO"):
            self.curl = self.urlProducao
        else:
            self.curl = self.urlHomologacao

        return self.curl

    def getDadosEmpresa(self, pcnpj):
        curEmpresa = connpgtemp.cursor()
        cSelect = "select cnpj, fantasia, modulo, token, segmentos from empresa where cnpj = '"+pcnpj+"'"
        curEmpresa.execute(cSelect)
        curDadosEmpresa = curEmpresa.fetchall()

        if len(curDadosEmpresa) > 0:
            self.segmento = curDadosEmpresa[0][4]
            self.token    = curDadosEmpresa[0][3]
            self.ambiente = curDadosEmpresa[0][2]

    def getMarcaVeiculo(self):
        try:
            listMarca = list()
            url = self.geturl()+"/api/brands"

            payload = {}
            headers = {
                'Authorization': 'Bearer '+self.token+''
            }

            response = requests.request("GET", url, headers=headers, data=payload, timeout=30)
            listMarcaVeiculo = json.loads(response.text.encode('utf8'))
            for marca in listMarcaVeiculo["result"]["brands"]:
                listMarca.append({"idmarca": marca["id"], "marca": marca["name"].upper(), "idsegmento" : marca["segment_id"]})

            dfMarca = pd.DataFrame(listMarca, columns=["idmarca", "marca", "idsegmento"])
            dfMarca.set_index(["marca", "idsegmento"])
            return dfMarca
        except:
            print("#ERRO ao Carregar as marcas da API Tempário")

    def getModeloVeiculo(self, dfSelecaoMarca, modeloveiculo):
        try:
            listVeiculo = list()
            listSelecaoMarca =  dfSelecaoMarca.values.tolist()

            for marca in listSelecaoMarca:
                sidmarcaTempario = str(marca[0])
                sidsegmentoTempario = str(marca[2])
                url = self.geturl()+"/api/models?api-version="+API_VERSION_TEMPARIO+"&brand_id="+sidmarcaTempario+"&name="+modeloveiculo+"&segment_id="+sidsegmentoTempario+""

                payload = {}
                headers = {
                    'Authorization': 'Bearer ' + self.token + ''
                }

                response = requests.request("GET", url, headers=headers, data=payload, timeout=30)
                listModeloVeiculo = json.loads(response.text.encode('utf8'))

                for modelo in listModeloVeiculo["result"]["models"]:
                    listVeiculo.append({"idmodelo": modelo["id"], "fabricante" : marca[1] , "modelo": modelo["name"].upper(), "idsegmento": sidsegmentoTempario})

                dfModelo = pd.DataFrame(listVeiculo, columns=["idmodelo", "fabricante", "modelo", "idsegmento"])
                return dfModelo
        except:
            print("Erro ao Carregar Modelo da API Tempário")
            listVeiculo = list()
            dfModelo = pd.DataFrame(listVeiculo, columns=["idmodelo", "fabricante", "modelo", "idsegmento"])
            return dfModelo

    def getServico(self, idmodelo, servico):
        try:
            url = self.geturl() + "/api/services?api-version=" + API_VERSION_TEMPARIO + "&model_id=" + str(idmodelo) + "&name="+servico

            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token + ''
            }

            response = requests.request("GET", url, headers=headers, data=payload, timeout=30)
            listModeloVeiculo = json.loads(response.text.encode('utf8'))

            return listModeloVeiculo
        except:
            print("Erro ao Carregar Serviço da API Tempário")
            listModeloVeiculo = {}
            return listModeloVeiculo

    def minuto_to_hora_relogio(self, minutos):
        nContHora = 0
        minutoDesc = minutos
        minuto = 60
        retHora = 0
        retMinuto = 0
        while(True):
            if minutoDesc >= 60:
                nContHora = nContHora + 1
                minutoDesc = minutoDesc - 60
            else:
                break

        if minutos >= 60:
            retMinuto = minutoDesc
        else:
            retMinuto = minutos

        retHora   = nContHora

        return {"hora" : retHora, "minuto" : retMinuto}



    async def armazenamodeloveiculo(self, dfModelo):
        print('Salvando Veículos')
        for index, veiculo in dfModelo.iterrows():
            cUpdate = '''            
                        insert into veiculo_retornado (idmodelo, fabricante, modelo, idsegmento, modulo) 
	                    select '''+str(veiculo['idmodelo'])+''', $$'''+veiculo['fabricante']+'''$$, 
	                    $$'''+veiculo['modelo']+'''$$, $$'''+veiculo['idsegmento']+'''$$, 
	                    $$'''+self.ambiente+'''$$ 
	                    where not exists(select 1 from veiculo_retornado
	                                     where idmodelo = $$'''+str(veiculo['idmodelo'])+'''$$ and 
	                                           modulo = $$'''+self.ambiente+'''$$)
                      '''
            curVeiculoRetornado = connpgtemp.cursor()
            curVeiculoRetornado.execute(cUpdate)

    async def armazenamodeloservico(self, listRetorno, idmodelo):
        print('Salvando Serviços')
        for servico in listRetorno:
            cUpdate = '''            
                        insert into servico_retornado (idservico, idmodelo, servico, tempo_minuto, tempo_hora, tempo_texto, pecas, modulo)
                        select '''+str(servico["idservico"])+''',
                               '''+str(idmodelo)+''', 
                             $$'''+servico["servico"]+'''$$,
                               '''+str(servico["tempo_minuto"])+''', 
                               '''+str(servico["tempo_hora"])+''', 
                               $$'''+servico["tempo_texto"]+'''$$, 
                               $$'''+str(servico["pecas"]).replace("'", '"')+'''$$, 
                               $$'''+self.ambiente+'''$$
                        where not exists(select 1 from servico_retornado 
                                         where idservico = '''+str(servico["idservico"])+''' and 
                                               modulo = $$'''+self.ambiente+'''$$ and
                                               idmodelo = '''+str(idmodelo)+'''  
                                        )                           
                      '''
            # apenas usado em teste
            #print(cUpdate)

            curServicoRetornado = connpgtemp.cursor()
            curServicoRetornado.execute(cUpdate)







@app.route('/v1/tempario/veiculo', methods=['POST'])
def apitempario_veiculo():
    try:
        print(request.form.get("cnpj") + " --> " + request.form.get("usererp") + "... Requisitando Modelo de Veículo... " + request.form.get("fabricante") + "-" + request.form.get("modelobase") + "-" + request.form.get("modelo"))
        objTempario = Tempario(request.form.get("cnpj"))
        if objTempario.token != "":

            curLogRequisicao = connpgtemp.cursor()
            cInsert = '''
                        INSERT INTO requisicao_veiculo(
                                cnpj,
                                usererp, 
                                fabricante, 
                                modelobase, 
                                modelo, 
                                nome_aplicativo, 
                                versao_aplicativo,
                                token, 
                                modulo,
                                dtrequisicao, 
                                hrrequisicao)
                        VALUES ($$'''+request.form.get("cnpj")+'''$$, 
                                $$'''+request.form.get("usererp")+'''$$,
                                $$'''+request.form.get("fabricante")+'''$$,
                                $$'''+request.form.get("modelobase")+'''$$,
                                $$'''+request.form.get("modelo")+'''$$,
                                $$'''+request.form.get("nome_aplicativo")+'''$$,
                                $$'''+request.form.get("versao_aplicativo")+'''$$,
                                $$'''+request.form.get("token")+'''$$,
                                $$'''+objTempario.ambiente+'''$$,                                
                                current_date,
                                current_time
                                )            
                      '''
            curLogRequisicao.execute(cInsert)


            dfMarca = pd.DataFrame(listMarca, columns=["marca", "idsegmento"])
            dfModelo = pd.DataFrame(listVeiculo, columns=["idmodelo", "fabricante", "modelo", "idsegmento", "status"])
            dfMarca = objTempario.getMarcaVeiculo()
            _marcaveiculo  = request.form.get("fabricante")
            selecaomarca   = dfMarca.query("(marca == '"+_marcaveiculo+"' and idsegmento in("+str(objTempario.segmento).replace('[', '').replace(']', '')+"))")
            # buscar pelo modelo completo
            dfModelo = objTempario.getModeloVeiculo(selecaomarca, modeloveiculo=request.form.get("modelo"))

            # vai buscar pelo modelo base listar alguma coisa
            if dfModelo.__len__() == 0:
                dfModelo = objTempario.getModeloVeiculo(selecaomarca, modeloveiculo=request.form.get("modelobase"))

            if dfModelo.__len__() == 0:
                print(request.form.get("cnpj") + " --> " + request.form.get("usererp") + "... Não retornou nenhum modelo de veículo ")
            else:
                print(request.form.get("cnpj") + " --> " + request.form.get("usererp") + "... retornou " + str(dfModelo.__len__())+ " modelo de veículos ")
                #objTempario.armazenamodeloveiculo(dfModelo)
                asyncio.run(objTempario.armazenamodeloveiculo(dfModelo))

            print('Retornando dados de veículo ....')
            print(dfModelo)
            print('')


            #json_teste = json.dumps(array_veiculo, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')
            json_teste = json.dumps(json.loads(dfModelo.reset_index().to_json(orient='records')), indent=2, sort_keys=True, ensure_ascii=False).encode('utf8')
            return json_teste
    except:
        cRetorno = "Solicitação de veículo não encontrada ou houve alguma falha no processamento"
        print(cRetorno)
        json_teste = json.dumps({"result": cRetorno}, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')
        return json_teste


@app.route('/v1/tempario/servico', methods=['POST'])
def apitempario_servico():
    try:
        print(request.form.get("cnpj") + " --> " + request.form.get("usererp") + "... Requisitando Serviço para o modelo do veículo...  " + str(request.form.get("idmodelo")))
        objTempario = Tempario(request.form.get("cnpj"))
        if objTempario.token != "":

            curLogRequisicao = connpgtemp.cursor()
            cInsert = '''
                        INSERT INTO requisicao_servico(
                                cnpj,
                                usererp, 
                                idmodelo, 
                                nome_aplicativo, 
                                versao_aplicativo,
                                token, 
                                modulo,
                                servico,
                                dtrequisicao, 
                                hrrequisicao)
                        VALUES ($$'''+request.form.get("cnpj")+'''$$, 
                                $$'''+request.form.get("usererp")+'''$$,
                                $$'''+str(request.form.get("idmodelo"))+'''$$,
                                $$'''+request.form.get("nome_aplicativo")+'''$$,
                                $$'''+request.form.get("versao_aplicativo")+'''$$,
                                $$'''+request.form.get("token")+'''$$,
                                $$'''+objTempario.ambiente+'''$$,
                                $$'''+request.form.get("servico")+'''$$,                                
                                current_date,
                                current_time
                                )            
                      '''
            curLogRequisicao.execute(cInsert)

            dados = objTempario.getServico(idmodelo=request.form.get("idmodelo"), servico=request.form.get("servico"))

            if dados.__len__() != 0:
                array_parts   = {}
                listParts = list()
                listRetorno = list()
                nContService = 0
                nContProduct = 0
                for servicos in dados['result']['services_times']:
                    nContService += 1
                    ser_idservico     = servicos['service']['id']
                    ser_tempo_minutos = servicos['minutes']
                    ser_tempo_horas   = servicos['minutes']/60
                    ser_servico       = servicos['service']['name'].upper().replace("'", " ")
                    jMinutoTexto = objTempario.minuto_to_hora_relogio(ser_tempo_minutos)
                    # para testes ;)
                    #jMinutoTexto = objTempario.minuto_to_hora_relogio(120)
                    if jMinutoTexto['hora'] > 0:

                        if jMinutoTexto['hora'] > 1:
                            ser_tempo_texto = str(jMinutoTexto['hora']) + " horas"
                        else:
                            ser_tempo_texto = str(jMinutoTexto['hora']) + " hora"

                        if jMinutoTexto['minuto'] == 0:
                            ser_tempo_texto = ser_tempo_texto
                        if jMinutoTexto['minuto'] == 1:
                            ser_tempo_texto = ser_tempo_texto + str(jMinutoTexto['minuto']) + " minuto"
                        if jMinutoTexto['minuto'] > 1:
                            ser_tempo_texto = ser_tempo_texto + str(jMinutoTexto['minuto']) + " minutos"

                    else:
                        ser_tempo_texto = str(jMinutoTexto['minuto']) + " minutos"

                    nContProduct = 0
                    for pecas in servicos['pieces']:
                        nContProduct += 1
                        pec_id = pecas['id']
                        pec_peca = pecas['name'].upper().replace("'", "")
                        peca_quantidade = pecas['quantity']
                        array_parts = {"idpeca" : pec_id,
                                       "peca" : pec_peca.upper(),
                                       "quantidade" : peca_quantidade}
                        listParts.append(array_parts)

                        # limitador de retorno de produto por serviço por pesquisa
                        if (nContService > 20):
                            break

                    listRetorno.append({"idservico" : ser_idservico, "servico" : ser_servico, "tempo_minuto" : ser_tempo_minutos, "tempo_hora" : ser_tempo_horas,"tempo_texto" : ser_tempo_texto, "pecas" : listParts})

                    # limitador de retorno de serviço por pesquisa
                    if nContService > 40:
                        break


                #objTempario.armazenamodeloservico(listRetorno)
                asyncio.run(objTempario.armazenamodeloservico(listRetorno, request.form.get("idmodelo")))
                print('Retornando dados de veículo ....')
                print(listRetorno.__len__())
                print('')
                json_teste = json.dumps(listRetorno, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')
                return json_teste
            else:
                cRetorno = "Não retornou nenhuma informação do Tempário... api.tempario.com.br"
                print(cRetorno)
                json_teste = json.dumps({"result" : cRetorno}, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')
                return json_teste
    except Exception as ex:
        print(ex)
        cRetorno = "Solicitação de serviço encontrada ou houve alguma falha no processamento"
        print(cRetorno)
        json_teste = json.dumps({"result": cRetorno}, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')
        return json_teste


@app.route('/v1/tempario/teste', methods=['GET'])
def home():
    print("Consultando Status de Serviço")
    if request.remote_addr in listIpBloqueia:
        array_teste = {}
        array_teste['service'] = 'Bloqueio no Host muitas solicitações nessa API'
        json_teste = json.dumps(array_teste, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')
    else:
        array_teste = {}
        array_teste['service'] = statusservice
        json_teste = json.dumps(array_teste, sort_keys=True, indent=1, ensure_ascii=False).encode('utf8')

    return json_teste

if __name__ == "__main__":
    listIpBloqueia           = ["200.200.200.200"]
    listMarca = list()
    listVeiculo = list()
    API_VERSION_TEMPARIO = "1"
    print("SRV PRINCIAL Consulta Serviços Tempário Gestão Parts [ATIVO] Versão = 1.1")
    if production:
        # ambiente de produção
        serve(app, host='0.0.0.0', port=6006, threads=2)
    else:
        # ambiente de teste e desenvolvimento
        app.run("0.0.0.0", 6006)



