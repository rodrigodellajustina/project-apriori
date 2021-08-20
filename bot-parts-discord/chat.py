import discord
import asyncio
from discord.ext import commands, tasks
client = discord.Client()
from datetime import datetime, timezone

def getMensagem():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	hora = int(now.strftime("%H"))
	minuto = int(now.strftime("%M"))
	dia = datetime.now().day
	mes = datetime.now().month

	semana = datetime.today().weekday()

	agenda = [{"dia": 0, "mes": 0, "hora" : 7, "minuto": 41, "msg" : "Bom dia Dev's !, ótimo dia de trabalho, não esqueça de registrar o ponto ;)", "dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora" : 7, "minuto": 42, "msg" : "Dev's !, não esqueça de registrar o ponto :)","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 11, "minuto": 55, "msg": "Bom almoço !, não deixe de comitar o seu código e registrar o ponto ;)","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 11, "minuto": 58, "msg": "Hora do Almoço pessoal !, não deixe de comitar o seu código e registrar o ponto :)","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 13, "minuto": 28,  "msg": "Preguiça né ?, mas vamos codar com um café preto sem esquecer do ponto ;)","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 13, "minuto": 30,  "msg": "Café ta pronto ? e versão sai hoje ? rsrs, só mais meio dia pessoal, sem esquecer do registro do ponto ;)","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 17, "minuto": 56,  "msg": "Nem acredito que se já vai embora, e o terceiro turno ? rsrs, obrigado por mais um dia galera vocês são F..A, ah não esquece não do ponto...","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 18, "minuto": 00, "msg" : "Bom descanço galera até amanhã..., registra o......","dayofweek" : [0,1,2,3,4]},
			  {"dia": 0, "mes": 0, "hora": 13, "minuto": 29, "msg": "Vamos para Daily Scrum  ;)  segue o link --> https://meet.google.com/xcg-yukg-mfu <-- ", "dayofweek" : [0,1,2,3,4]},
			  {"dia": 20, "mes": 5, "hora": 9, "minuto": 30, "msg" : "Mas que beleza, hoje temos festa, Parabéns Jonas tudo de bom pra vc, saúde sucesso e muitas felicidades ","dayofweek" : [0,1,2,3,4,5,6]},
			  {"dia": 15, "mes": 10, "hora": 9, "minuto": 30, "msg" : "Mas que beleza, hoje temos festa, Parabéns Willl tudo de bom pra vc, saúde sucesso e muitas felicidades ","dayofweek" : [0,1,2,3,4,5,6]},
			  {"dia": 15, "mes": 4, "hora": 9, "minuto": 30, "msg" : "Mas que beleza, hoje temos festa, Parabéns Abel Roque tudo de bom pra vc, saúde sucesso e muitas felicidades ","dayofweek" : [0,1,2,3,4,5,6]},
			  {"dia": 12, "mes": 4, "hora": 9, "minuto": 30, "msg" : "Mas que beleza, hoje temos festa, Parabéns Della tudo de bom pra vc, saúde sucesso e muitas felicidades ","dayofweek" : [0,1,2,3,4,5,6]}]

	for t in agenda:
		if (t["dia"] == 0 and t["mes"] == 0 and t["hora"] == hora and t["minuto"] == minuto and semana in t['dayofweek']):
			return t["msg"]

		if (t["dia"] == dia and t["mes"] == mes and t["hora"] == hora and t["minuto"] == minuto and semana in t['dayofweek']):
			return t["msg"]

	return ''




# aqui foi útil um dia
'''
async def anuncio():
	while True:
                # É importante usar o Asyncio, pois cria um thread paralelo e se restringe apenas ao thread
                # Se usássemos o modulo sleep "time.sleep(tempo)" ele pararia o processo inteiro até o tempo chegar
                # use await asyncio.sleep(tempo em segundos), 10800 = 3 horas
		#await asyncio.sleep(2)
		# canal de produção
		#canal = client.get_guild(id=770487481426509876).get_channel(id=770487481426509879)


		# canal de teste
		canal = client.get_channel(id=770487481426509879)
		cMsg = getMensagem()

		if cMsg != "":
			print('Enviando Mensagem...')
			await canal.send(cMsg)
		else:
			print('Sem Mensagem para Enviar...')

		await asyncio.sleep(60)
# Aqui criamos um loop restrito apenas ao "anuncio", ou seja, não interfere nas outras tarefas

#client.loop.create_task(anuncio())
#client.run('NzcwNDYzOTI3NDE4ODgwMDEx.X5d8cg.4YImqdCZ_1AR-1YbTKgDDbF59NI')


#getMensagem()
'''