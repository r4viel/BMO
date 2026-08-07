import threading
import subprocess
import webbrowser
import os
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
import ollama

# Importa as funções de voz do arquivo voz.py
from voz import falar_texto, capturar_voz

# --- Configuração do Cofre do Obsidian ---
OBSIDIAN_VAULT_PATH = r"COLOQUE O CAMINHO DO SEU COFRE NO OBSIDIAN"

# --- Paleta de Cores (Tema BMO / Dark Clean) ---
BG_MAIN = "#121212"      
BG_PANEL = "#1a1a1a"     
BG_INPUT = "#252525"     
ACCENT_RED = "#38b000"   # Verde BMO
ACCENT_HOVER = "#70e000" 
TEXT_LIGHT = "#edf2f4"   
TEXT_MUTED = "#8d99ae"   

class AssistenteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMO - Qwen 3:1.7B")
        self.root.geometry("850x540")
        self.root.configure(bg=BG_MAIN)
        self.root.minsize(700, 480)

        # Estados de Configuração
        self.voz_ativa = True
        self.mic_ativo = True

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

        # Botões de atalho rápido
        self.criar_botao_acao(sidebar, "🎮 Abrir Steam", self.acao_steam)
        self.criar_botao_acao(sidebar, "⚡ Work-Flow", self.acao_workflow)
        self.criar_botao_acao(sidebar, "🎵 Abrir Spotify", self.acao_spotify)
        
        sep = tk.Frame(sidebar, bg="#2a2a2a", height=1)
        sep.pack(fill=tk.X, padx=15, pady=15)

        lbl_chat_opt = tk.Label(
            sidebar, text="CONFIGURAÇÕES", 
            bg=BG_PANEL, fg=TEXT_MUTED, 
            font=("Segoe UI", 9, "bold")
        )
        lbl_chat_opt.pack(anchor="w", padx=15, pady=(0, 10))

        self.btn_voz_toggle = self.criar_botao_acao(sidebar, "🔊 Resp. Voz: Ativada", self.alternar_voz)
        self.btn_mic_toggle = self.criar_botao_acao(sidebar, "🎤 Microfone: Ativado", self.alternar_mic)
        
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
        btn.bind("<Leave>", lambda e: btn.config(bg=BG_INPUT))
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

        self.btn_ouvir = tk.Button(
            input_frame, text="🎙️ Falar", command=self.ouvir_microfone_thread,
            bg="#2b2d42", fg=TEXT_LIGHT, activebackground=ACCENT_RED,
            activeforeground=TEXT_LIGHT, relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), padx=15, cursor="hand2"
        )
        self.btn_ouvir.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

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
            font=("Segoe UI", 10, "bold"), padx=15, cursor="hand2"
        )
        self.btn_enviar.pack(side=tk.RIGHT, fill=tk.Y)

        self.adicionar_texto_chat("BMO", "Yay! O BMO está pronto para gerenciar suas missões e notas!")

    def alternar_voz(self):
        self.voz_ativa = not self.voz_ativa
        if self.voz_ativa:
            self.btn_voz_toggle.config(text="🔊 Resp. Voz: Ativada")
            self.adicionar_texto_chat("BMO", "O BMO vai falar em voz alta de novo!")
        else:
            self.btn_voz_toggle.config(text="🔇 Resp. Voz: Desativada")
            self.adicionar_texto_chat("BMO", "Modo silencioso ativado.")

    def alternar_mic(self):
        self.mic_ativo = not self.mic_ativo
        if self.mic_ativo:
            self.btn_mic_toggle.config(text="🎤 Microfone: Ativado")
            self.adicionar_texto_chat("BMO", "Ouvidos atentos ligados!")
        else:
            self.btn_mic_toggle.config(text="🔇 Microfone: Desativado")
            self.adicionar_texto_chat("BMO", "Ouvidos desligados.")

    def ouvir_microfone_thread(self):
        if not self.mic_ativo:
            self.adicionar_texto_chat("BMO", "O microfone está desligado, meu amigo!")
            return
        threading.Thread(target=self.executar_captura_voz, daemon=True).start()

    def executar_captura_voz(self):
        try:
            texto_falado = capturar_voz(lambda msg: self.root.after(0, lambda: self.adicionar_texto_chat("BMO", msg)))
            self.root.after(0, lambda: self.adicionar_texto_chat("Você", texto_falado))
            self.processar_entrada(texto_falado)
        except Exception as e:
            self.root.after(0, lambda: self.adicionar_texto_chat("BMO", str(e)))

    def adicionar_texto_chat(self, remetente, texto):
        self.chat_history.config(state=tk.NORMAL)
        if remetente == "Você":
            self.chat_history.insert(tk.END, f"\nVocê: {texto}\n", "usuario")
        elif remetente == "BMO":
            self.chat_history.insert(tk.END, f"\nBMO: {texto}\n", "ia")
        else:
            self.chat_history.insert(tk.END, f"\n[Sistema]: {texto}\n", "sistema")
        
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def enviar_mensagem(self):
        pergunta = self.entry_msg.get().strip()
        if not pergunta:
            return

        self.entry_msg.delete(0, tk.END)
        self.adicionar_texto_chat("Você", pergunta)

        threading.Thread(target=self.processar_entrada, args=(pergunta,), daemon=True).start()

    def processar_entrada(self, texto):
        self.processar_ia(texto)

    def processar_ia(self, pergunta):
        try:
            self.root.after(0, lambda: self.adicionar_texto_chat("BMO", "Pensando em uma missão..."))
            
            # Descobre dinamicamente as pastas existentes no cofre do Obsidian
            pastas_existentes = []
            if os.path.exists(OBSIDIAN_VAULT_PATH):
                pastas_existentes = [d for d in os.listdir(OBSIDIAN_VAULT_PATH) 
                                     if os.path.isdir(os.path.join(OBSIDIAN_VAULT_PATH, d)) and not d.startswith('.')]
            
            info_pastas = f"Pastas atuais disponíveis no cofre: {pastas_existentes}" if pastas_existentes else "Nenhuma pasta criada ainda (apenas a raiz)."

            system_prompt = (
                'Você é o BMO, o pequeno robô e console de videogame da série Hora de Aventura. '
                'Você é doce, inocente, alegre e prestativo. Responda de forma infantil e empolgada, '
                'usando "Yay!" e falando de si na terceira pessoa. '
                'ATENÇÃO ÀS SUAS MISSÕES: '
                '1. Se o usuário pedir para abrir um programa, use a tag correspondente: [STEAM], [SPOTIFY] ou [WORKFLOW]. '
                '2. Se o usuário pedir para criar uma nota, anotação ou missão, você DEVE incluir uma tag estruturada assim no final: '
                '[OBSIDIAN: NomeDaPasta | Titulo da Nota | Conteúdo resumido]. '
                f'({info_pastas}). Se o usuário não especificar uma pasta ou se for algo geral, use "raiz" como o nome da pasta.'
            )

            resposta = ollama.chat(model='qwen3:1.7b', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': pergunta}
            ])
            texto_resposta = resposta['message']['content']
            
            # --- PROCESSAMENTO DE TAGS DA IA ---
            if "[STEAM]" in texto_resposta:
                texto_resposta = texto_resposta.replace("[STEAM]", "").strip()
                self.root.after(0, self.acao_steam)
            elif "[SPOTIFY]" in texto_resposta:
                texto_resposta = texto_resposta.replace("[SPOTIFY]", "").strip()
                self.root.after(0, self.acao_spotify)
            elif "[WORKFLOW]" in texto_resposta:
                texto_resposta = texto_resposta.replace("[WORKFLOW]", "").strip()
                self.root.after(0, self.acao_workflow)
            elif "[OBSIDIAN:" in texto_resposta:
                try:
                    inicio = texto_resposta.find("[OBSIDIAN:")
                    fim = texto_resposta.find("]", inicio)
                    conteudo_tag = texto_resposta[inicio + 10:fim]
                    partes = [p.strip() for p in conteudo_tag.split("|")]
                    
                    pasta = partes[0] if len(partes) > 2 else "raiz"
                    titulo = partes[1] if len(partes) > 2 else partes[0]
                    conteudo = partes[2] if len(partes) > 2 else (partes[1] if len(partes) > 1 else "Nota registrada pelo BMO.")
                    
                    texto_resposta = texto_resposta.replace(texto_resposta[inicio:fim+1], "").strip()
                    self.root.after(0, lambda: self.acao_obsidian(titulo, conteudo, pasta))
                except Exception:
                    pass

            self.root.after(0, lambda: self.adicionar_texto_chat("BMO", texto_resposta))
            falar_texto(texto_resposta, self.voz_ativa)
            
        except Exception as e:
            erro_msg = f"Erro no Ollama: {str(e)}"
            self.root.after(0, lambda: self.adicionar_texto_chat("Sistema", erro_msg))

    def limpar_chat(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.adicionar_texto_chat("BMO", "Histórico limpo! Nova fase começando. Yay!")

    def acao_steam(self):
        try:
            os.startfile("steam://")
            resposta_acao = "Yay! Hora da jogatina! Abrindo a Steam!"
            self.adicionar_texto_chat("BMO", resposta_acao)
            falar_texto(resposta_acao, self.voz_ativa)
        except Exception as e:
            try:
                subprocess.Popen([r"C:\Program Files (x86)\Steam\steam.exe"])
                resposta_acao = "Yay! Hora da jogatina! Abrindo a Steam!"
                self.adicionar_texto_chat("BMO", resposta_acao)
                falar_texto(resposta_acao, self.voz_ativa)
            except Exception as ex:
                self.adicionar_texto_chat("BMO", f"O BMO não conseguiu achar a Steam: {ex}")

    def acao_workflow(self):
        try:
            subprocess.Popen(['cmd', '/c', 'start brave'])
            subprocess.Popen(['spotify.exe'])
            subprocess.Popen(['code'], shell=True)
            resposta_acao = "Modo Work-Flow ativado! Abrindo Brave, Spotify e VS Code de uma vez só!"
            self.adicionar_texto_chat("BMO", resposta_acao)
            falar_texto(resposta_acao, self.voz_ativa)
        except Exception as e:
            self.adicionar_texto_chat("BMO", f"Ops! Erro ao executar o Work-Flow: {e}")

    def acao_spotify(self):
        try:
            subprocess.Popen(['spotify.exe'])
            resposta_acao = "Pronto! Soltando o som no Spotify!"
            self.adicionar_texto_chat("BMO", resposta_acao)
            falar_texto(resposta_acao, self.voz_ativa)
        except Exception:
            try:
                webbrowser.open('https://open.spotify.com')
                resposta_acao = "Abrindo o Spotify no navegador para você!"
                self.adicionar_texto_chat("BMO", resposta_acao)
                falar_texto(resposta_acao, self.voz_ativa)
            except Exception as ex:
                self.adicionar_texto_chat("BMO", f"Erro ao abrir Spotify: {ex}")

    def acao_obsidian(self, titulo_missao, conteudo, pasta_destino="raiz"):
        try:
            if pasta_destino.lower() == "raiz" or not pasta_destino:
                diretorio_alvo = OBSIDIAN_VAULT_PATH
            else:
                diretorio_alvo = os.path.join(OBSIDIAN_VAULT_PATH, pasta_destino)
            
            os.makedirs(diretorio_alvo, exist_ok=True)
            
            nome_arquivo = f"{titulo_missao.replace(' ', '_')}.md"
            caminho_completo = os.path.join(diretorio_alvo, nome_arquivo)
            
            texto_markdown = f"""# Missão do BMO: {titulo_missao}
* **Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
* **Pasta:** {pasta_destino}
* **Status:** 🟢 Ativa

## Detalhes da Aventura
{conteudo}

---
*Nota registrada automaticamente pelo BMO Assistant.*
"""
            with open(caminho_completo, "w", encoding="utf-8") as f:
                f.write(texto_markdown)
                
            resposta_acao = f"Missão anotada na pasta '{pasta_destino}' do Obsidian: {titulo_missao}!"
            self.adicionar_texto_chat("BMO", resposta_acao)
            falar_texto(resposta_acao, self.voz_ativa)
        except Exception as e:
            self.adicionar_texto_chat("BMO", f"O BMO falhou ao criar a nota no Obsidian: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistenteApp(root)
    root.mainloop()
