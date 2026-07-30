import threading
import subprocess
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
import ollama
import pyttsx3

# Paleta de Cores 
BG_MAIN = "#121212"      # Fundo principal preto fosco
BG_PANEL = "#1a1a1a"     # Fundo dos painéis laterais/chat
BG_INPUT = "#252525"     # Fundo das caixas de entrada
ACCENT_RED = "#d90429"   # Vermelho moderno principal
ACCENT_HOVER = "#ef233c" # Vermelho mais claro para efeito hover
TEXT_LIGHT = "#edf2f4"   # Texto principal claro
TEXT_MUTED = "#8d99ae"   # Texto secundário/dicas

class AssistenteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Controle - Qwen 3:1.7B")
        self.root.geometry("850x520")
        self.root.configure(bg=BG_MAIN)
        self.root.minsize(700, 450)

        # Estado da Voz (True = Fala ativada, False = Apenas texto)
        self.voz_ativa = True

        # Layout Principal
        self.criar_sidebar()
        self.criar_painel_chat()

    def criar_sidebar(self):
        sidebar = tk.Frame(self.root, bg=BG_PANEL, width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        lbl_titulo = tk.Label(
            sidebar, text="AUTOMAÇÕES", 
            bg=BG_PANEL, fg=TEXT_MUTED, 
            font=("Segoe UI", 9, "bold")
        )
        lbl_titulo.pack(anchor="w", padx=15, pady=(20, 10))

        self.criar_botao_acao(sidebar, "📝 Abrir Bloco de Notas", self.acao_bloco_notas)
        self.criar_botao_acao(sidebar, "🌐 Abrir Navegador", self.acao_navegador)
        self.criar_botao_acao(sidebar, "📁 Abrir Arquivos", self.acao_documentos)
        
        sep = tk.Frame(sidebar, bg="#2a2a2a", height=1)
        sep.pack(fill=tk.X, padx=15, pady=20)

        lbl_chat_opt = tk.Label(
            sidebar, text="GERENCIAMENTO", 
            bg=BG_PANEL, fg=TEXT_MUTED, 
            font=("Segoe UI", 9, "bold")
        )
        lbl_chat_opt.pack(anchor="w", padx=15, pady=(0, 10))

        # Botão para ligar/desligar a voz
        self.btn_voz_toggle = self.criar_botao_acao(sidebar, "🔊 Voz: Ativada", self.alternar_voz)
        self.criar_botao_acao(sidebar, "🧹 Limpar Conversa", self.limpar_chat)

        lbl_info = tk.Label(
            sidebar, text="Modelo: Qwen 3:1.7B\nStatus: Local (Ollama)", 
            bg=BG_PANEL, fg="#555555", 
            font=("Segoe UI", 8), justify="left"
        )
        lbl_info.pack(side=tk.BOTTOM, anchor="w", padx=15, pady=15)

    def criar_botao_acao(self, parent, texto, comando):
        btn = tk.Button(
            parent, text=texto, command=comando,
            bg=BG_INPUT, fg=TEXT_LIGHT, activebackground=ACCENT_RED,
            activeforeground=TEXT_LIGHT, relief="flat", bd=0,
            font=("Segoe UI", 9), anchor="w", padx=12, pady=8,
            cursor="hand2"
        )
        btn.pack(fill=tk.X, padx=10, pady=4)
        btn.bind("<Enter>", lambda e: btn.config(bg="#333333"))
        btn.bind("<Leave>", lambda e: btn.config(bg=BG_INPUT if btn != getattr(self, 'btn_voz_toggle', None) or self.voz_ativa else "#331111"))
        return btn

    def criar_painel_chat(self):
        chat_frame = tk.Frame(self.root, bg=BG_MAIN)
        chat_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=15, pady=15)

        self.chat_history = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, bg=BG_PANEL, fg=TEXT_LIGHT,
            font=("Segoe UI", 10), insertbackground=TEXT_LIGHT,
            relief="flat", bd=0, padx=10, pady=10
        )
        self.chat_history.pack(expand=True, fill=tk.BOTH, pady=(0, 10))
        self.chat_history.config(state=tk.DISABLED)

        input_frame = tk.Frame(chat_frame, bg=BG_MAIN)
        input_frame.pack(fill=tk.X)

        self.entry_msg = tk.Entry(
            input_frame, bg=BG_INPUT, fg=TEXT_LIGHT,
            font=("Segoe UI", 11), relief="flat", insertbackground=TEXT_LIGHT
        )
        self.entry_msg.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, ipady=8, padx=(0, 8))
        self.entry_msg.bind("<Return>", lambda event: self.enviar_mensagem())

        self.btn_enviar = tk.Button(
            input_frame, text="Enviar", command=self.enviar_mensagem,
            bg=ACCENT_RED, fg=TEXT_LIGHT, activebackground=ACCENT_HOVER,
            activeforeground=TEXT_LIGHT, relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), padx=20, cursor="hand2"
        )
        self.btn_enviar.pack(side=tk.RIGHT, fill=tk.Y)

        self.adicionar_texto_chat("Sistema", "Painel iniciado. Use o botão na lateral para alternar entre modo voz ou texto.")

    def alternar_voz(self):
        """Alterna o estado de reprodução de voz da IA"""
        self.voz_ativa = not self.voz_ativa
        if self.voz_ativa:
            self.btn_voz_toggle.config(text="🔊 Voz: Ativada", bg=BG_INPUT)
            self.adicionar_texto_chat("Sistema", "Modo de voz ativado.")
        else:
            self.btn_voz_toggle.config(text="🔇 Voz: Desativada", bg="#331111")
            self.adicionar_texto_chat("Sistema", "Modo de voz desativado (apenas texto).")

    def falar_texto(self, texto):
        if not self.voz_ativa:
            return
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.say(texto)
            engine.runAndWait()
        except Exception as e:
            print(f"Erro no áudio: {e}")

    def adicionar_texto_chat(self, remetente, texto):
        self.chat_history.config(state=tk.NORMAL)
        if remetente == "Você":
            self.chat_history.insert(tk.END, f"\nVocê: {texto}\n", "usuario")
        elif remetente == "Sistema":
            self.chat_history.insert(tk.END, f"\n[Sistema]: {texto}\n", "sistema")
        else:
            self.chat_history.insert(tk.END, f"\nQwen 1.7B: {texto}\n", "ia")
        
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def enviar_mensagem(self):
        pergunta = self.entry_msg.get().strip()
        if not pergunta:
            return

        self.entry_msg.delete(0, tk.END)
        self.adicionar_texto_chat("Você", pergunta)

        threading.Thread(target=self.processar_ia, args=(pergunta,), daemon=True).start()

    def processar_ia(self, pergunta):
        try:
            self.root.after(0, lambda: self.adicionar_texto_chat("Sistema", "Pensando..."))
            
            resposta = ollama.chat(model='qwen3:1.7b', messages=[
                {'role': 'user', 'content': pergunta}
            ])
            texto_resposta = resposta['message']['content']
            
            self.root.after(0, lambda: self.adicionar_texto_chat("IA", texto_resposta))
            
            # Só fala em voz alta se a opção estiver ativada
            if self.voz_ativa:
                self.falar_texto(texto_resposta)
            
        except Exception as e:
            erro_msg = f"Erro no Ollama: {str(e)}"
            self.root.after(0, lambda: self.adicionar_texto_chat("Sistema", erro_msg))

    def limpar_chat(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.adicionar_texto_chat("Sistema", "Histórico limpo.")

    def acao_bloco_notas(self):
        try:
            subprocess.Popen(['notepad.exe'])
            self.adicionar_texto_chat("Sistema", "Bloco de notas aberto.")
        except Exception as e:
            self.adicionar_texto_chat("Sistema", f"Erro: {e}")

    def acao_navegador(self):
        try:
            webbrowser.open('https://www.google.com')
            self.adicionar_texto_chat("Sistema", "Navegador aberto.")
        except Exception as e:
            self.adicionar_texto_chat("Sistema", f"Erro: {e}")

    def acao_documentos(self):
        try:
            subprocess.Popen(['explorer.exe'])
            self.adicionar_texto_chat("Sistema", "Explorador de Arquivos aberto.")
        except Exception as e:
            self.adicionar_texto_chat("Sistema", f"Erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistenteApp(root)
    root.mainloop()
