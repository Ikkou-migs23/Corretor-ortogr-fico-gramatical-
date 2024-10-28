import nltk
from nltk.tokenize import word_tokenize
import language_tool_python
from spellchecker import SpellChecker
import tkinter as tk
from tkinter import scrolledtext

# Baixando os dados do nltk necessários
nltk.download('punkt')

# Inicializando ferramentas de linguagem
spell = SpellChecker(language='pt')
tool = language_tool_python.LanguageTool('pt-BR')

# Funções principais
def verificar_gramatica_e_corrigir():
    text_phrase = entry_text.get("1.0", tk.END)
    result_text.delete("1.0", tk.END)  # Limpar resultados anteriores

    # Verificação e sugestão de correções gramaticais
    erros = tool.check(text_phrase)
    if erros:
        result_text.insert(tk.END, "\nErros gramaticais encontrados:\n", 'bold')
        for erro in erros:
            mensagem = erro.message
            sugestao = ', '.join(erro.replacements)
            result_text.insert(tk.END, f" - Erro: {mensagem}\n   Sugestões: {sugestao}\n")
    else:
        result_text.insert(tk.END, "\nSem erros gramaticais.\n", 'bold')

    # Tokenização e correção de acentuação
    tokens = word_tokenize(text_phrase, language='portuguese')
    erros_acento = [(palavra, list(spell.candidates(palavra))) for palavra in tokens if palavra in spell.unknown([palavra])]
    
    if erros_acento:
        result_text.insert(tk.END, "\nErros de acentuação corrigidos:\n", 'bold')
        for palavra, correcoes in erros_acento:
            # Exibe todas as sugestões para cada palavra
            sugestoes = ', '.join(correcoes)
            result_text.insert(tk.END, f" - Palavra: {palavra} -> Sugestões: {sugestoes}\n")
    else:
        result_text.insert(tk.END, "\nSem erros de acentuação.\n", 'bold')

# Interface gráfica
root = tk.Tk()
root.title("Corretor Gramátical/Ortográfico")
root.geometry("500x600")
root.config(bg="#34495e")

# Configurações de fonte
font_title = ("Helvetica", 16, "bold")
font_text = ("Arial", 12)

# Título
title_label = tk.Label(root, text="Corretor Gramátical/Ortográfico", font=font_title, bg="#34495e", fg="#ecf0f1")
title_label.pack(pady=10)

# Entrada de texto
entry_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=5, font=font_text)
entry_text.pack(pady=10)
entry_text.insert(tk.END, "Digite seu texto aqui...")

# Botão de verificação e correção
btn_verificar = tk.Button(root, text="Verificar e Corrigir", command=verificar_gramatica_e_corrigir, bg="#3498db", fg="#ecf0f1", font=font_text)
btn_verificar.pack(pady=10)

# Área de resultados
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=font_text)
result_text.pack(pady=10)

# Estilos de tags para resultados
result_text.tag_configure('bold', font=("Arial", 12, "bold"))

# Execução da interface
root.mainloop()
