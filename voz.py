import pyttsx3
import speech_recognition as sr

def falar_texto(texto, voz_ativa=True):
    if not voz_ativa:
        return
    try:
        engine = pyttsx3.init()
        
        engine.setProperty('rate', 210)
        
        voices = engine.getProperty('voices')
        voz_escolhida = None
        
        for voice in voices:
            nome_voz = voice.name.lower()
            id_voz = voice.id.lower()
            if "pt-br" in id_voz or "brazil" in nome_voz or "portuguese" in voice.languages:
                if "maria" in nome_voz or "female" in nome_voz or "zira" in nome_voz:
                    voz_escolhida = voice.id
                    break
                elif not voz_escolhida:
                    voz_escolhida = voice.id
                    
        if voz_escolhida:
            engine.setProperty('voice', voz_escolhida)

        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro no áudio: {e}")

def capturar_voz(callback_status):
    """Ouve o microfone via SpeechRecognition e retorna o texto transcrito."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        callback_status("Ouvindo... Fale agora!")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            texto_falado = r.recognize_google(audio, language="pt-BR")
            return texto_falado
        except sr.WaitTimeoutError:
            raise Exception("Tempo limite esgotado. Nenhuma fala detectada.")
        except sr.UnknownValueError:
            raise Exception("Não foi possível entender o áudio.")
        except Exception as e:
            raise Exception(f"Erro no microfone: {e}")