import csv
import time
from datetime import datetime
import serial
import matplotlib.pyplot as plt  # Biblioteca para gerar o gráfico

# Caminho dos arquivos CSV e HTML
csv_filename = 't:\\dados_irrigacao.csv'
html_filename = 't:\\dados.html'

# Configuração da porta serial (ajuste "COM3" para a porta onde o Arduino está conectado)
arduino_serial = serial.Serial('COM3', 9600, timeout=1)

# Função para salvar dados no CSV
def salvar_dados(umidade, status_bomba):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([data_hora, umidade, status_bomba])

# Função para atualizar o HTML com os dados do CSV e aplicar estilo CSS
def atualizar_html():
    with open(csv_filename, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        linhas = list(reader)

    # Gerar conteúdo HTML com CSS embutido
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Dados de Irrigação</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #005f73;
            text-align: center;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
            font-size: 16px;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #005f73;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #e0f7fa;
        }
        tr:hover {
            background-color: #d1e7dd;
        }
    </style>
</head>
<body>
    <h1>Registro de Irrigação</h1>
    <table>
        <tr>
            <th>Data e Hora</th>
            <th>Umidade</th>
            <th>Status da Bomba</th>
        </tr>"""

    # Preencher as linhas da tabela com os dados do CSV
    for linha in linhas[1:]:  # Ignorar cabeçalho
        html_content += f"""
        <tr>
            <td>{linha[0]}</td>
            <td>{linha[1]}</td>
            <td>{linha[2]}</td>
        </tr>"""

    html_content += """
    </table>
</body>
</html>"""

    # Salvar HTML no diretório especificado
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

# Função para gerar gráfico de umidade
def gerar_grafico():
    datas = []
    umidades = []

    # Ler dados do CSV
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Pular cabeçalho
        for linha in reader:
            datas.append(datetime.strptime(linha[0], '%Y-%m-%d %H:%M:%S'))
            umidades.append(int(linha[1]))

    # Gerar gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(datas, umidades, label='Umidade do Solo', color='b')
    plt.xlabel('Data e Hora')
    plt.ylabel('Umidade')
    plt.title('Níveis de Umidade ao Longo do Tempo')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar gráfico em arquivo
    plt.savefig('t:\\grafico_umidade.png')
    plt.show()

# Adicionar cabeçalho ao CSV se não existir
try:
    with open(csv_filename, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Data e Hora', 'Umidade', 'Status da Bomba'])
except FileExistsError:
    pass

# Loop para coletar dados do Arduino e atualizar HTML periodicamente
try:
    while True:
        # Receber dados do Arduino pela serial
        if arduino_serial.in_waiting > 0:
            linha = arduino_serial.readline().decode().strip()
            umidade = int(linha)  # Converte a leitura para um número inteiro
            status_bomba = "Ligada" if umidade < 500 else "Desligada"

            # Salvar e atualizar HTML com os dados reais do sensor
            salvar_dados(umidade, status_bomba)
            atualizar_html()  # Atualiza o HTML após salvar os dados
            print(f"Data e Hora: {datetime.now()}, Umidade: {umidade}, Status da Bomba: {status_bomba}")
        
        time.sleep(5)  # Intervalo de atualização de 5 segundos

except KeyboardInterrupt:
    print("Encerrado pelo usuário.")
    gerar_grafico()  # Gerar o gráfico ao encerrar o programa
