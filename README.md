# BMO

## Visão Geral

Sistema de painel gráfico leve (BMO) desenvolvido em **Python (Tkinter)** que integra uma Inteligência Artificial local (**Qwen 3:1.7B** via **Ollama**) e ferramentas de automação para o sistema operacional, com suporte opcional a síntese de voz (**pyttsx3**).

---

## Requisitos do Sistema

* **Hardware:** Processador compatível com instruções AVX2, mínimo de 12GB de RAM e espaço livre em SSD.
* **Dependências Python:** `ollama`, `pyttsx3` (ambas executadas localmente).
* **Serviço de IA:** Ollama rodando o modelo `qwen3:1.7b`.

---

## Arquitetura e Funcionalidades

* **Interface Gráfica (`painel.py`):**
* Desenvolvida em Tkinter com design minimalista Dark e paleta de cores em preto fosco e vermelho.
* Uso de *threads* para garantir que a interface não sofra congelamentos durante o processamento da IA.


* **Barra Lateral de Automações:**
* **Bloco de Notas:** Aciona a abertura instantânea do `notepad.exe`.
* **Navegador:** Abre a página padrão no navegador web.
* **Explorador de Arquivos:** Dispara o gerenciador de diretórios (`explorer.exe`).
* **Alternância de Voz:** Botão de controle dinâmico para habilitar ou desabilitar a reprodução de áudio das respostas da IA.
* **Limpeza de Chat:** Reseta o histórico visual da conversa.


* **Chat Inteligente:**
* Comunicação direta e 100% offline via API local do Ollama (`http://localhost:11434`).



---

## Guia Rápido de Execução

1. Certifique-se de que o modelo leve está baixado e ativo no terminal:
```bash
ollama run qwen3:1.7b

```


2. Na pasta onde o script está salvo, execute o painel pelo terminal:
```bash
python painel.py

```
