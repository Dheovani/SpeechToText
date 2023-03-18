import azure.cognitiveservices.speech as speechsvc
import pyttsx3

# Essa classe cuidará da interpretação de áugio e da transformação de texto em áudio

# Utilizaremos o Speech Services do Azure para converter áudio em texto
key, location = '4dc742bc2b734905b1fd98ae4ae61f07', 'brazilsouth' # Chaves de acesso

def mic_recongnition():
    speech_config = speechsvc.SpeechConfig(key, location) # Configuração do receptor
    speech_recognizer = speechsvc.SpeechRecognizer(speech_config=speech_config) # Configuração do recognizer

    text_to_speech('Speak now.')

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsvc.ResultReason.RecognizedSpeech:
        return result.text # Retornaremos apenas os arquivos de texto
        # Abaixo, estamos apenas lidando com possíveis erros
    elif result.reason == speechsvc.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        text_to_speech("Sorry, i couldn't listen. Please, repeat your command.")
        return no_speech()
    elif result.reason == speechsvc.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsvc.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

# Caso o microfone não capte nenhum som, este método será invocado para reiniciar o processo de captação de áudio
def no_speech():
    return mic_recongnition()

# Converteremos texto em áudio com a lib pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init() # Criando o motor
    engine.setProperty("rate", 170) # Diminuindo a velocidade da fala
    voices = engine.getProperty('voices') # 0 = Português, 1 = Inglês
    engine.setProperty('voice', voices[1].id)
    engine.say(text) # Iremos informar ao usuário o texto recebido
    engine.runAndWait()

# Caso estejamos executando essa classe, o algoritmo a seguir irá testar o método 'get_connection()'
if __name__ == '__main__':
    text = mic_recongnition()
    text_to_speech(text)