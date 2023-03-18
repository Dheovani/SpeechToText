import SpeechToText, ConnectionFactory, js2py
from botbuilder.core import TurnContext
from botbuilder.schema import ActivityTypes

class ActivityBot:
    # Mensagem de boas vindas
    def welcome_msg(self, site_name):
        SpeechToText.text_to_speech(f'''Hi. Welcome to {site_name}!
                    I am this site's attendance specialized AI.
                    I will be with you during your stay on our website.
                    Feel free to talk to me whenever you want.
                    ''')

    # Esse comando serve apenas para informar o usuário que as palavras chave serão informadas em sequência, dessa maneira, o usuário poderá optar por ouví-las posteriormente sem precisar ouvir essa mensagem toda vez
    def next_msg(self):
        SpeechToText.text_to_speech('''
                    Now, i'm going to inform you about the commands you can use to navigate through the website and communicate with me. Please, pay attention.
                    ''')
    
    # Informação dos comandos reconhecidos
    def commands_info(self):
        # Aqui, vamos informar o usuário a respeito dos comandos que este pode invocar para ativar as funções do bot
        conn = ConnectionFactory.get_connection("localhost\SQLEXPRESS", "ImagineCup")
        cursor = conn.cursor()
        sql_text = "SELECT PALAVRA_CHAVE, FUNCAO FROM Comando ORDER BY FUNCAO"
        command_function = ''
        for command in cursor.execute(sql_text).fetchall():
            if command_function != command[1]:
                # Informar ao usuário o propósito/função de cada botão
                command_function = command[1]
                SpeechToText.text_to_speech(command_function)
            SpeechToText.text_to_speech(command[0])

    # Preços e informações a respeito dos produtos
    def products_info(self):
        conn = ConnectionFactory.get_connection('localhost\SQLEXPRESS', 'ImagineCup')
        cursor = conn.cursor()
        sql_text = '''SELECT NOME, CATEGORIA, PRECO, TIPO_PRECO, PROMO FROM Produto ORDER BY CATEGORIA'''
        categoria = ''
        for info in cursor.execute(sql_text).fetchall():
            if categoria != info[1]:
                categoria = info[1]
                SpeechToText.text_to_speech(f'''Category: {categoria}.''')
            if info[4] == 1:
                SpeechToText.text_to_speech(f'''{info[0]} is in promotion. ${info[2]} the {info[3]}.''')
            else:
                SpeechToText.text_to_speech(f'''{info[0]}: ${info[2]} the {info[3]}.''')
                

    # Mensagem de despedida
    def goodbye_msg(self):
        SpeechToText.text_to_speech('''It was a pleasure to help you during your stay in our website.
                    I hope you might return when you need something.
                    Until next time. Have an amazing day!
                    ''')

    # Clicar em componentes do site
    def click(self, id):
        js_code = '''
        function selectID(id) {
            document.getElementById(id).click();
        }
        '''
        py_code = js2py.eval_js(js_code)
        py_code(id)

    # Buscar comandos no banco de dados
    def get_command(self, my_text):
        my_text = str(my_text).strip('.').split()
        conn = ConnectionFactory.get_connection("localhost\SQLEXPRESS", "ImagineCup")
        cursor = conn.cursor()
        result = []
        for command in my_text:
            try:
                # Como nosso banco de comandos terá apenas um COMANDO para cada PALAVRA_CHAVE e considerando que o método fetchall() irá retornar um 'SQL ROW', podemos selecionar o primeiro valor do primeiro row
                key_word = cursor.execute('SELECT COMANDO FROM Comando WHERE PALAVRA_CHAVE = ?', command).fetchall()[0][0]
                result.append(key_word)
            except IndexError:
                # Caso a palavra que o usuário falou não conste no banco de dados, passamos para a próxima palavra
                pass
        if result != []:
            return result
        else:
            # Se nenhum comando válido for inserido, iremos reiniciar o processo
            SpeechToText.text_to_speech('''Sorry, i didn't understand. If you didn't hear the commands options, say command to hear them again.''')
            self.get_command(SpeechToText.mic_recongnition())

    # Usuário entra na sala de bate-papo
    async def on_conversation_update(self, turn_context:TurnContext):
        if turn_context.activity.type == ActivityTypes.conversation_update:
            self.welcome_msg('Kunz')
            # Informar o usuário a respeito dos comandos disponíveis
            self.next_msg()
            self.commands_info()

    # Reconhecendo comandos de voz
    async def on_command_update(self, turn_context:TurnContext):
        while turn_context.activity.type != ActivityTypes.end_of_conversation:
            turn_context.activity.text = SpeechToText.mic_recongnition()

            if turn_context.activity.type == ActivityTypes.message or ActivityTypes.message_update:
                command = self.get_command(turn_context.activity.text)
                # Utilizando o comando extraído, o bot realizará uma operação
                for cmd in command:
                    if cmd == '<welcome-msg>':
                        # Dar as boas vindas novamente
                        self.welcome_msg('Kunz')
                    elif cmd == '<info-command>':
                        # Informar os comandos novamente
                        self.commands_info()
                    elif cmd == '<info-products>':
                        # Informar os preços dos produtos
                        if command.__len__() == 1:
                            self.products_info()
                        else:
                            conn = ConnectionFactory.get_connection("localhost\SQLEXPRESS", "ImagineCup")
                            cursor = conn.cursor()
                            result = cursor.execute('SELECT NOME, PRECO, TIPO_PRECO, PROMO FROM Produto ORDER BY NOME').fetchall()
                            for item in command:
                                # Nessa função devemos verificar se algum produto com preço foi informado pelo usuário e retornar o preço do mesmo
                                for product in result:
                                    if item == product[0]:
                                        SpeechToText.text_to_speech(f'The price of {product[0]} is ${product[1]} the {product[2]}.')
                                        if product[3] == 1:
                                            SpeechToText.text_to_speech('It is in promotion.')

                    elif cmd == '<click-command>':
                        conn = ConnectionFactory.get_connection("localhost\SQLEXPRESS", "ImagineCup")
                        cursor = conn.cursor()
                        result = cursor.execute('SELECT NOME FROM Produto ORDER BY NOME').fetchall()
                        for element_command in command:
                            # Se o usuário mandar o bot clicar em algum componente do site, tentaremos identificar um elemento clicável (como uma fruta ou algum outro produto) e, a partir daí, realizaremos as demais operações
                            for element_product in result:
                                if element_command == element_product:
                                    self.click(element_product)
                                    # Vamos atualizar o turn_context, pois assim iremos disparar automaticamente um ActivityTypes.message_update
                                    turn_context.activity.text = f'price {element_product}'
                                else:
                                    SpeechToText.text_to_speech('You told me to click on somethink, but i didnt understando what should i click on. Please, repet your command.')
                    elif cmd == '<goodbye-msg>':
                        from Chat import loop
                        loop.stop()
                        turn_context.activity.type = ActivityTypes.end_of_conversation
                    else:
                        SpeechToText.text_to_speech('''Sorry, i didn't recognize your command.
                                    Please, enter a valid command''')

    # Fim da conversa
    async def end_of_conversation(self, turn_context:TurnContext):
        if turn_context.activity.type == ActivityTypes.end_of_conversation:
            self.goodbye_msg()
            import Chat
            Chat.shutdown_server()

if __name__ == '__main__':
    my_bot = ActivityBot()
    my_bot.products_info()