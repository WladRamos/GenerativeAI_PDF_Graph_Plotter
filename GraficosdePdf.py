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
    ('file', ('file', open('ArquivoTeste3.pdf', 'rb'), 'application/octet-stream'))
]
headers = {
    'x-api-key': 'sec_xxxxxxxxxx'
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
            'content': "Diga qual é o tipo de gráfico que deve ser utilizado para representar os dados da tabela presente no pdf entre as seguintes opções: plot (gráfico de linha) ou bar. Em seguida, agrupe os dados da tabela em uma lista de listas. Exemplos: Ex1 - tabela contendo variações de preço de moedas de acordo com o tempo. Note que a primeira sub-lista apenas mostra qual será o dado que estará em cada index nas próximas sub-listas, que essa estrutura serve para a variação de qualquer tipo de variação de valores, não apenas preços e moedas, note também que a variação de tempo pode ser por anos, décadas,... e não meses, e por fim, note que podem haver mais ou menos produtos sendo analisados na tabela, e todos devem estar na lista. Resposta esperada para Ex1: Tipo de gráfico - plot; lista com os dados = [['Mês', 'Dólar', 'Euro'], ['Janeiro', 5.20, 6.10], ['Fevereiro', 5.18, 6.08], ['Março', 5.15, 6.05],['Abril', 5.10, 6.00], ['Maio', 5.05, 5.95], ['Junho', 5.00, 5.90], ['Julho', 4.95, 5.85], ['Agosto', 4.90, 5.80], ['Setembro', 4.85, 5.75], ['Outubro', 4.80, 5.70], ['Novembro', 4.75, 5.65], ['Dezembro',4.70, 5.60]]. Ex2 - Preços de produtos em lojas . Note que pode haver qualquer quantidade de produtos e todos devem estar na lista, note também que esse tipo de gráfico pode estar comparando também o mesmo produto em diferentes lojas, fazendo com que a lista fique da seguinte forma [['Loja', 'Valor'], ['Loja A', 100], ['Loja B', 150], ...], ou seja, nesse tipo de gráfico, o produto ou loja ao qual o preço faz referência ficará no eixo x enquanto o seu preço ficará no eixo y. Resposta esperada para Ex2: Tipo de gráfico - bar; lista com os dados = [['Mercadoria', 'Valor'], ['Produto A', 100], ['Produto B', 150], ...].",
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