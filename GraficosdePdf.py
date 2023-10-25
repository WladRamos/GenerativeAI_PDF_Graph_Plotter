import requests
import matplotlib.pyplot as plt

def plot_bar_type(data):
    labels = [entry[0] for entry in data[1:]]
    values = [entry[1] for entry in data[1:]]

    plt.bar(labels, values)

    plt.xlabel(data[0][0])
    plt.ylabel(data[0][1])
    plt.title('Gráfico de Barras')

    plt.xticks(rotation=90)

    plt.show()

def plot_plot_type(data):
    labels = data[0][1:]
    x = [entry[0] for entry in data[1:]]
    y = [entry[1:] for entry in data[1:]]

    y = list(zip(*y))

    for label, value in zip(labels, y):
        plt.plot(x, value, label=label)

    plt.xlabel(data[0][0])
    plt.ylabel('Valores')
    plt.title('Gráfico')

    plt.xticks(rotation=90)

    plt.legend()
    plt.show()


def chama_grafico_correspondente(tipo_grafico, dados):
    
    if "bar" in tipo_grafico:
        plot_bar_type(dados)
    elif "plot" in tipo_grafico:
        plot_plot_type(dados)

files = [
    ('file', ('file', open('XXXXXXX.pdf', 'rb'), 'application/octet-stream'))
]
headers = {
    'x-api-key': 'sec_xxxxxxxxxxxx'
}


response = requests.post(
    'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

if response.status_code == 200:
    print('Source ID:', response.json()['sourceId'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)


data = {
    "stream": True,
    'sourceId': response.json()['sourceId'],
    'messages': [
        {
            'role': "user",
            'content': "Analise o conteúdo da tabela presente no PDF e diga se o conteúdo pode ser melhor representado por um gráfico de linha(plot) ou um gráfico de barras(bar). Caso a tabela apresente variação de algo ao longo do tempo, a resposta deve ser (plot). Caso contrário, a resposta deve ser (bar). Após isso, os dados da tabela devem ser agrupados em uma lista de listas, de forma que a primeira sublista sirva apenas para identificar o que aquela posição representará nas próximas sub-listas. Note que caso a tabela apresenta variação de algo ao longo do tempo, a lista deve seguir o formato de [['t', 'elemento_1', 'elemento_2', 'elemento_n'], ['t1', valor do elemento_1 em t1, valor do elemento_2 em t1, valor do elemento_n em t1]...] onde t representa o tempo/período referido, como por exemplo mês, ano, hora, século, etc, e os elementos são os objetos nos quais os valores variam ao longo desses tempos t.",
        }
    ]
}

url = "https://api.chatpdf.com/v1/chats/message"

resultado = ""
try:
    response = requests.post(url, json=data, headers=headers, stream=True)
    response.raise_for_status()

    if response.iter_content:
        max_chunk_size = 1024
        for chunk in response.iter_content(max_chunk_size):
            text = chunk.decode()
            resultado = resultado + text.strip()
    else:
        raise Exception("No data received")
except requests.exceptions.RequestException as error:
    print("Error:", error)

print(resultado)

#tratamento do tipo de grafico retornado
indice_fim_tipo = resultado.index('.')
result_tipo_grafico = resultado[:indice_fim_tipo]
#print(result_tipo_grafico)

#tratamento da lista de saída
indice_inicio_lista = resultado.index('[')
indice_fim_lista = resultado.rindex(']')

result_lista = resultado[indice_inicio_lista:indice_fim_lista + 1]

lista_dados = eval(result_lista)
#print(lista_dados)

chama_grafico_correspondente(result_tipo_grafico, lista_dados)
