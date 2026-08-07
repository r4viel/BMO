# BMO Assistant 🎮🤖

Um painel de controle interativo e assistente de desktop desenvolvido em Python, cujo objetivo principal é criar um assistente inteligente com a adorável, inocente e divertida personalidade do **BMO** (da série *Hora de Aventura*). 

O projeto roda localmente utilizando o **Ollama** (`qwen3:1.7b`), permitindo interações por texto ou voz, além de automações no Windows acionadas diretamente por comandos de voz ou botões na interface.

---

## 🚀 Funcionalidades

* **Personalidade do BMO:** O assistente responde de forma empolgada, fofa, usando "Yay!" e tratando você como seu melhor amigo de aventuras.
* **Inteligência por Tags:** O BMO decide autonomamente quando executar automações ou criar notas no seu computador através de tags na conversa.
* **Interação por Voz:** 
  * **Ouvir:** Captura sua fala pelo microfone usando `SpeechRecognition`.
  * **Falar:** Converte as respostas em áudio com ritmo acelerado (`pyttsx3`) para simular o estilo enérgico do personagem.
* **Automações de Desktop:**
  * **Abrir Steam**
  * **Work-Flow:** Abre o Brave, o Spotify e o VS Code simultaneamente.
  * **Abrir Spotify** dedicado.
  * **Criar Nota** cria nota no seu cofre do obsidian
* **Interface Gráfica Moderna (Tkinter):** Layout minimalista e customizado em modo escuro com toques de verde inspirados no BMO.

---

## 🛠️ Pré-requisitos e Dependências

Certifique-se de ter o **Python** e o **Ollama** instalados no seu computador.

1. **Instalar as dependências via terminal:**
   ```bash
   pip install ollama pyttsx3 SpeechRecognition pyaudio

```

*(Nota: Caso o `pyaudio` apresente erros no Windows, instale o pipwin rodando `pip install pipwin` e depois `pipwin install pyaudio`).*

2. **Garantir que o Ollama está ativo:**
Certifique-se de que o aplicativo do Ollama está rodando em segundo plano e com o modelo baixado:
```bash
ollama run qwen3:1.7b

```



---

## 📁 Estruturação do Projeto

O projeto é dividido em dois arquivos principais na mesma pasta:

1. **`voz.py`**: Gerencia a captura de áudio do microfone e a síntese de voz (TTS).
2. **`painel.py`**: Controla a interface gráfica (Tkinter), o chat, as regras de negócio e a integração com a IA do Ollama.

---

## ▶️ Como Executar

1. Abra o terminal (CMD ou PowerShell) na pasta onde estão os arquivos `painel.py` e `voz.py`.
2. Inicie o painel com o comando:
```bash
python painel.py

```


3. Divirta-se conversando ou dando missões para o seu próprio BMO!

```

```
