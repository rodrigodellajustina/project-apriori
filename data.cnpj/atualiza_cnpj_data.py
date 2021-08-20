import psycopg2
import requests

lerro = False
cAmbiente = "192.168.10.11"


try:
    #ambiente MASSTER
    conn = psycopg2.connect(host='177.155.126.76', user='clientess', password='massterssplus', dbname='masster', port='8745')
    conn.autocommit = True
except Exception as e:
    print(e)
    lerro = True
    print('Erro Conexão MASSTER')
    conn = 0

try:
    #ambiente de API-VEICULOS
    conn2 = psycopg2.connect(host='localhost', user='postgres', password='pgsql', dbname='apiveiculos', port='5494')
    conn2.autocommit = True
except:
    lerro = True
    print('Erro Conexão API-VEICULOS')
    conn2 = 0

try:
    #ambiente de API-placas
    conn3 = psycopg2.connect(host='localhost', user='postgres', password='pgsql', dbname='apiplacas', port='5494')
    conn3.autocommit = True
except:
    lerro = True
    print('Erro Conexão API-PLACAS')
    conn3 = 0

try:
    #ambiente de Thompson
    conn4 = psycopg2.connect(host='192.168.11.12', user='postgres', password='pgsql', dbname='bdprdthompson', port='23450')
    conn4.autocommit = True
except:
    lerro = True
    print('Erro Conexão THOMPSON')
    conn4 = 0

try:
    #ambiente de osmobile
    conn5 = psycopg2.connect(host='192.168.11.12', user='postgres', password='pgsql', dbname='bdprdosmobile', port='23450')
    conn5.autocommit = True
except Exception as e:
    print(e)
    lerro = True
    print('Erro Conexão OSMOBILE')
    conn5 = 0


# seleciona do Masster
curEmpresa = conn.cursor()
cSelect = "select * From cnpj_Data_vw"
curEmpresa.execute(cSelect)
curDadosEmpresa = curEmpresa.fetchall()


# Envia dados para cnpj_data API-VEICULOS
try:
    print('Enviando Dados para API-VEICULOS ')
    curEmpresaDel = conn2.cursor()
    cDelete = "truncate table cnpj_data"
    curEmpresaDel.execute(cDelete)
    cur = conn2.cursor()
    cur.executemany("INSERT INTO cnpj_data(cnpj,razao,fantasia,cidade,uf) VALUES (%s , %s , %s , %s , %s)", curDadosEmpresa)
except:
    lerro = True
    print('#ERRO - Enviando Dados para API-VEICULOS ')


# Envia dados para cnpj_data API-PLACAS
try:
    print('Enviando Dados para API-PLACAS ')
    curEmpresaDel = conn3.cursor()
    cDelete = "truncate table cnpj_data"
    curEmpresaDel.execute(cDelete)
    cur = conn3.cursor()
    cur.executemany("INSERT INTO cnpj_data(cnpj,razao,fantasia,cidade,uf) VALUES (%s , %s , %s , %s , %s)", curDadosEmpresa)
except:
    lerro = True
    print('#ERRO - Enviando Dados para API-PLACAS')


# Envia dados para cnpj_data osmobile
try:
    print('Enviando Dados para OSMobile ')
    curEmpresaDel = conn5.cursor()
    cDelete = "truncate table cnpj_data"
    curEmpresaDel.execute(cDelete)
    cur = conn5.cursor()
    cur.executemany("INSERT INTO cnpj_data(cnpj,razao,fantasia,cidade,uf) VALUES (%s , %s , %s , %s , %s)", curDadosEmpresa)
except Exception as e:
    print(e)
    lerro = True
    print('#ERRO - Enviando Dados para OSMobile')


# Envia dados para cnpj_data thomson
try:
    print('Enviando Dados para THOMPSON ')
    curEmpresa = conn.cursor()
    cSelect = "select cnpj,razao,fantasia From cnpj_Data_vw"
    curEmpresa.execute(cSelect)
    curDadosEmpresa = curEmpresa.fetchall()
    curEmpresaDel = conn4.cursor()
    cDelete = "truncate table dados.empresa"
    curEmpresaDel.execute(cDelete)
    cur = conn4.cursor()
    cur.executemany("INSERT INTO dados.empresa(cnpj_cpf,nome,fantasia) VALUES (%s , %s , %s)",
                    curDadosEmpresa)
except:
    lerro = True
    print('#ERRO - Enviando Dados para THOMPSON')


if lerro:
    print("Erro ao enviar dados para as bases")
else:
    print('Concluiu com sucesso')
