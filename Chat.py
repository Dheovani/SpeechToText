from flask import Flask, render_template,request,Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings
from Bot import ActivityBot
from http.server import SimpleHTTPRequestHandler, HTTPServer
import asyncio

# Criando o app e o loop
app = Flask(__name__)
loop = asyncio.get_event_loop()

# Definindo as configurações do activity handler
botadaptersettings = BotFrameworkAdapterSettings("","")
botadapter = BotFrameworkAdapter(botadaptersettings)

bot = ActivityBot()

@app.route("/")
def index():
    return render_template('index.html')

# Gerando condição de finalização do loop e transmissão de informações da API
@app.route("/api/messages/", methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
      jsonmessage = request.json
    else:
      return Response(status=415)

    activity = Activity().deserialize(jsonmessage)

    # Criando a função que irá reconhecer a mudança de 'contexto de turno' após a realização de cada operação
    async def turn_call(turn_context):
        await bot.on_conversation_update(turn_context)
        await bot.on_command_update(turn_context)
        await bot.end_of_conversation(turn_context)

    task = loop.create_task(botadapter.process_activity(activity,"",turn_call))
    loop.run_until_complete(task)

    return jsonmessage

# Função para derrubar a conexão com o servidor
def shutdown_server():
    server_address = ('localhost', 5500)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.shutdown()
    if loop.is_running:
      loop.stop()
    else:
      loop.close()

if __name__ == '__main__':
    app.run('localhost', 5500)