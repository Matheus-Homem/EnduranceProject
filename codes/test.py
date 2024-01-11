import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, date
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Obtém o diretório atual do script
file_path = os.getcwd()

# Obtém o diretório pai do diretório atual
dir_path = os.path.dirname(file_path)

# Constrói o caminho absoluto para a pasta pdf
pdf_path = os.path.join(dir_path, "pdf")

# Carregando secrets definidos pelo arquivo .env
load_dotenv()

# Configurações do servidor SMTP do Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "pleasecallmekindness@gmail.com"
smtp_password = os.getenv("EMAIL_PASSWORD")

# Definição de um dicionário contendo as configuções SMTP
smtp_config = {"server": smtp_server,
               "port": smtp_port,
               "user": smtp_user,
               "password": smtp_password}

# Destinatário
destinatario = "matheuschomem@hotmail.com"

# Obtenha o diretório do notebook Jupyter
notebook_directory = os.getcwd()

# Definição dos caminhos relativos dos dataframes
morning_path = os.path.join(notebook_directory, "../files/data/morning_routine_v2.xlsx")
night_path = os.path.join(notebook_directory, "../files/data/night_routine_v2.xlsx")

# Criação dos dataframes diurno e noturno a partir dos caminhos definidos
sun_df = pd.read_excel(morning_path)
moon_df = pd.read_excel(night_path)

def send_email(smtp_config, destinatario, assunto:str, corpo_email, anexo_nome=None):
    # Passando informações da lista parametrizada
    smtp_server = smtp_config["server"]
    smtp_port = smtp_config["port"]
    smtp_user = smtp_config["user"]
    smtp_password = smtp_config["password"]
    remetente = smtp_config["user"]

    # Construa a mensagem
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    # Adicione o corpo do e-mail
    mensagem.attach(MIMEText(corpo_email, "plain"))

    # Adicione anexo, se fornecido
    if anexo_nome:
        with open(anexo_nome, "rb") as arquivo:
            anexo = MIMEText(arquivo.read())
            anexo["Content-Disposition"] = f"attachment; filename={anexo_nome}"
            mensagem.attach(anexo)

    # Conecte-se ao servidor SMTP e envie o e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(remetente, destinatario, mensagem.as_string())

    print("E-mail enviado com sucesso!")

def translate_weekday(english_weekday):
    # Definição do Dicionário de Tradução de Dia da Semana
    translate_dict = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"        
    }
    # Retorna a versão do dia da semana traduzida
    return translate_dict[english_weekday]

def centralize_text(canvas, altura_inicial, texto, fonte, tamanho_fonte):
    canvas.setFont(fonte, tamanho_fonte)
    largura_texto = canvas.stringWidth(texto, fonte, tamanho_fonte)
    posicao_inicial = (595.276 - largura_texto) / 2
    canvas.drawString(posicao_inicial, altura_inicial, texto)

# Definição do dicionário com os novos nomes dos campos
map_columns = {
    moon_df.columns[9]: "wis_memo",
    moon_df.columns[20]: "con_memo",
    moon_df.columns[40]: "str_memo",
    moon_df.columns[53]: "cha_memo",
    moon_df.columns[57]: "fth_memo"
}

# Aplicação do dicionário, renomeado os campos selecionados
moon_df.rename(columns=map_columns, inplace=True)

# Obtém a data atual
today = date.today()

# Obtém a data atual formatada
today_fmt = date.today().strftime("%d/%m/%Y")

# Obtém a data atual como timestamp
data_atual = datetime.now()

# Obtém o número da semana do ano
semana_do_ano = int(data_atual.strftime("%U")) + 1

# Obtém a data atual
data_atual = datetime.now()

# Obtém o nome do dia da semana
dia_da_semana = data_atual.strftime("%A")

# Criando um variável com os registros do formulário do dia anterior
yest_regs = moon_df.iloc[-1]

# Construção da Lista de Mementos
memento_list = [
    yest_regs["wis_memo"],
    yest_regs["con_memo"],
    yest_regs["str_memo"],
    yest_regs["cha_memo"],
    yest_regs["fth_memo"]
]

# Obtém o diretório atual do script
file_path = os.getcwd()

# Obtém o diretório pai do diretório atual
dir_path = os.path.dirname(file_path)

# Constrói o caminho absoluto para a pasta pdf
df_path = os.path.join(dir_path, "reports/dev/")

# Constrói o caminho para o arquivo pdf que será gerado
pdf_file_path = os.path.join(df_path, f"{today}.pdf")

def generate_text(c, text, x, y, font, font_size):
    cm = 28.346456692913385
    
    # Configuração da fonte
    c.setFont(font, font_size)

    # Inicializar o objeto de texto
    textobject = c.beginText(x, y)
    #textobject.setFont(font, font_size)

    # Divisão do texto em palavras
    palavras = text.split()

    # Adicionar cada palavra ao objeto de texto com quebra de linha conforme necessário
    for palavra in palavras:
        # Calcular a largura necessária para a palavra atual
        palavra_width = c.stringWidth(palavra + " ", font, font_size)
        
        # Se a palavra não couber na página, começar uma nova linha
        if x + palavra_width > A4[0] - 2 * cm:
            textobject.textLine("")
            x, y = 2 * cm, y - c.stringWidth("A", font, font_size)

        # Adicionar a palavra ao objeto de texto
        textobject.textOut(palavra + " ")
        x += palavra_width

    # Adicionar o restante do texto ao canvas
    c.drawText(textobject)

def add_mementos(c):
	# Header de Mementos
	c.setFont("Times-Bold", 24)
	c.drawString(100, 750, "Mementos")

	# Subtítulo: Sabedoria
	c.setFont("Times-Roman", 18)
	c.drawString(100, 725, "Sabedoria")
	# Texto com o memento de sabedoria
	generate_text(c, yest_regs["wis_memo"], 100, 710, "Times-Roman", 12)

	# Subtítulo: Estabilidade
	c.setFont("Times-Roman", 18)
	c.drawString(100, 625, "Estabilidade")
	# Texto com o memento de estabilidade
	generate_text(c, yest_regs["con_memo"], 100, 610, "Times-Roman", 12)

	# Subtítulo: Força
	c.setFont("Times-Roman", 18)
	c.drawString(100, 525, "Força")
	# Texto com o memento de força
	generate_text(c, yest_regs["str_memo"], 100, 510, "Times-Roman", 12)

	# Subtítulo: Gentileza
	c.setFont("Times-Roman", 18)
	c.drawString(100, 425, "Gentileza")
	# Texto com o memento de gentileza
	generate_text(c, yest_regs["cha_memo"], 100, 410, "Times-Roman", 12)

	# Subtítulo: Devoção
	c.setFont("Times-Roman", 18)
	c.drawString(100, 325, "Devoção")
	# Texto com o memento de devoção
	generate_text(c, yest_regs["fth_memo"], 100, 310, "Times-Roman", 12)
     
def add_header(c):
    centralize_text(c, 800, "Relatório Diário", "Times-Bold", 30)
    centralize_text(c, 780, f"{today_fmt} | {translate_weekday(dia_da_semana)} | Semana: {semana_do_ano}", "Courier", 15)
    c.line(100, 775, 500, 775)

def generate_report(file_path, margin=2):
    # Crie um objeto canvas para gerar o PDF
    c = canvas.Canvas(file_path, pagesize=A4)

    # Definição das dimensões da página do PDF
    width, height = A4
    
    # Adicione um cabeçalho ao PDF    
    add_header(c)

    # Criação da Primeira Divisão do Relatório: Mementos
    add_mementos(c)    

    # Salve o PDF
    c.save()

generate_report(pdf_file_path)

