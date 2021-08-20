from discord.ext import tasks
from chat import getMensagem

import discord

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.my_background_task.start()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'service?':
            await message.channel.send('Acesse e veja os status ...-> http://www.databaseit.com.br/service.html')

    @tasks.loop(seconds=60) # task runs every 60 seconds
    async def my_background_task(self):
        # canal de produção
        channel = channel = self.get_channel(615744386306670611)

        # canal de teste
        #channel = channel = self.get_channel(770487481426509879)
        cMsg = getMensagem()

        if cMsg != "":
            print('Enviando Mensagem...')
            await channel.send(cMsg)
        else:
            print('Sem Mensagem para Enviar...')

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

client = MyClient()
client.run('NzcwNDYzOTI3NDE4ODgwMDEx.X5d8cg.4YImqdCZ_1AR-1YbTKgDDbF59NI')