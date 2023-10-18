import requests
import matplotlib.pyplot as plt


files = [
    ('file', ('file', open('ArquivoTeste2.pdf', 'rb'), 'application/octet-stream'))
]
headers = {

    'x-api-key': 'sec_xxxxxxxxx'
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
            'content': "Agrupe os valores apresentados nas n linhas e também os meses relatados no PDF, em formato de lista de listas em python. Por exemplo [[mes_1, valor_1.1, valor_1.2, ..., valor_1.n], [mes_2, valor_2.1, valor_2.2, ..., valor_2.n], ...]. Forneça apenas esse agrupamento como resposta, sem textos adicionais, comentários ou explicações, tanto antes quanto depois da lista.",
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

#tratamento da string de saída
indice_inicio = resultado.index('[')
indice_fim = resultado.rindex(']]')

resultado = resultado[indice_inicio:indice_fim + 2]
print(resultado)

dados_lista = eval(resultado)

num_linhas = len(dados_lista)
num_colunas = len(dados_lista[0]) if num_linhas > 0 else 0

meses = [item[0] for item in dados_lista]
valores = [[] for _ in range(num_colunas-1)]  

for item in dados_lista:
    for i, valor in enumerate(item[1:]):
        valores[i].append(valor)


plt.figure(figsize=(10, 6))

for i, valores_coluna in enumerate(valores):
    plt.plot(meses, valores_coluna, marker='o', label=f'Valores da linha {i+1}')

plt.xlabel('Mês')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()









