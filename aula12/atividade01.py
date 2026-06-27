import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Obtendo os dados

try:

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep = ';', encoding= 'iso-8859-1')

    # DELIMITANDO AS VARIÁVEIS
    df_recuperacao_veiculo = df_ocorrencias[['cisp', 'recuperacao_veiculos']]
    # TOTALIZANDO AS RECUPERAÇÕES POR CISP
    df_recuperacao_veiculo = df_recuperacao_veiculo.groupby('cisp', as_index= False)['recuperacao_veiculos'].sum()
    # ORDENANDO O DATAFRAME
    df_recuperacao_veiculo = df_recuperacao_veiculo.sort_values(by = 'recuperacao_veiculos', ascending=False)

    #print(df_recuperacao_veiculo.head(10))

except Exception as e:
    print(f'Erro ao obter os dados: {e}')



# Obtendo as medidas

try:
    print('\nCalculando medidas...')

    array_recuperacao_veiculos = np.array(df_recuperacao_veiculo['recuperacao_veiculos'])

    media_recuperacao_veiculo = np.mean(array_recuperacao_veiculos)
    mediana_recuperacao_veiculo = np.median(array_recuperacao_veiculos)
    distancia = abs((media_recuperacao_veiculo - mediana_recuperacao_veiculo)/ mediana_recuperacao_veiculo * 100)

    print('\nMedidas de Tendência Central:')
    print(30 * '=')
    print(f'Média: {media_recuperacao_veiculo:.2f}')
    print(f'Mediana: {mediana_recuperacao_veiculo:.2f}')
    print(f'Distância: {distancia:.2f}')


except Exception as e:
    print(f'Erro ao processar medidas: {e}')



# Obtendo a distribuição
try:
    print('\nProcessando os quartis')
    q1 = np.quantile(array_recuperacao_veiculos, .25)
    q3 = np.quantile(array_recuperacao_veiculos, .75)

    print('\nQuartis:')
    print(30 * '=')

    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_recuperacao_veiculo}')
    print(f'Q3: {q3}')

    # Delegacias com menos recuperações
    df_recuperacao_menores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] < q1]
    df_recuperacao_menores = df_recuperacao_menores.sort_values(by = 'recuperacao_veiculos', ascending=True)
    # Delegacias com mais recuperações
    df_recuperacao_maiores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] > q3]

    print(f'\nDelegacias com menos recuperações de roubos de veiculos: {df_recuperacao_menores}')
    print(f'\nDelegacias com mais recuperações de roubos de veiculos: {df_recuperacao_maiores}')

except Exception as e:
    print(f'Erro ao obter a distribuição: {e}')



# Obtendo medidas de dispersão
try: 
    maximo = np.max(array_recuperacao_veiculos)
    minimo = np.min(array_recuperacao_veiculos)
    amplitude = maximo - minimo

    print('\nMedidas de dispersão')
    print(30 * '=')

    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão {e}')



# Calculando Outliers
try:
    iqr = q3 - q1

    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    print()
    print(f'IQR: {iqr}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Limite Superior: {limite_superior}')


except Exception as e:
    print(f'Erro ao calcular os limites: {e}')



# Exibindo Outliers
try:
    df_outliers_superiores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] > limite_superior]

    df_outliers_inferiores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] < limite_inferior]

    print('\nDelegacias com Outliers Inferiores')
    print(30 * '=')

    if len(df_outliers_inferiores) == 0:
        print(f'\nNão existe Outliers inferiores!')
    
    else:
        print(df_outliers_inferiores.sort_values(by = 'recuperacao_veiculos', ascending=True))


    print('\nDelegacias com Outliers Superiores')
    print(30 * '=')

    if len(df_outliers_superiores) == 0:
        print(f'\nNão existe Outliers superiores!')
    
    else:
        print(df_outliers_superiores)

except Exception as e:
    print(f'Erro ao calcular outliers: {e}')



# Obtendo Assimetria e Curtose
try:

    assimetria = df_recuperacao_veiculo['recuperacao_veiculos'].skew()
    curtose = df_recuperacao_veiculo['recuperacao_veiculos'].kurtosis()

    print('\nMedidas de Distribuição')
    print(30 * '=')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')


except Exception as e:
    print(f'Erro ao obter medidas de distribuição: {e}')



# Medidas de Variabilidade
try:

    #Variancia
    variancia = np.var(array_recuperacao_veiculos)

    #distancia entre média e variância
    distancia_var_media = variancia / (media_recuperacao_veiculo ** 2) * 100

    #desvio padrao
    desvio_padrao = np.std(array_recuperacao_veiculos)

    #coeficiente de variação
    coef_variacao = desvio_padrao / media_recuperacao_veiculo * 100

    print('\nMedidas de Variabilidade')
    print(30 * '=')
    print(f'Variância: {variancia}')    
    print(f'Distância entre Variâcia e a média: {distancia_var_media} %')
    print(f'Desvio Padrão: {desvio_padrao}')
    print(f'Coeficiente de variação: {coef_variacao}')

 

except Exception as e:
    print(f'Erro ao calcular variabilidade dos dados: {e}')



#Visualizando os dados
    
try:

    plt.subplots(2, 2, figsize=(16,8))
    plt.suptitle('Recuperação de veículos por delegacia', fontsize = 16, fontweight='bold')

    # POSIÇÃO 01
    plt.subplot(2, 2, 1)
    plt.boxplot(array_recuperacao_veiculos, vert=False, showmeans=True)
    plt.title('Distribuição da recuperação de veículos')

    # POSIÇÃO 02
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_recuperacao_veiculo:.2f}', fontsize = 9)
    plt.text(0.1, 0.8, f'Distância: {distancia:.2f}', fontsize = 9)
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.2f}', fontsize = 9)
    plt.text(0.1, 0.6, f'Mínimo: {minimo:.2f}', fontsize = 9)
    plt.text(0.1, 0.5, f'Q1: {q1:.2f}', fontsize = 9)
    plt.text(0.1, 0.4, f'Mediana: {mediana_recuperacao_veiculo:.2f}', fontsize = 9)
    plt.text(0.1, 0.3, f'Q3: {q3:.2f}', fontsize = 9)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior:.2f}', fontsize = 9)
    plt.text(0.1, 0.1, f'Máximo: {maximo:.2f}', fontsize = 9)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude:.2f}', fontsize = 9)

    plt.axis('off')
    plt.title('Resumo Estatístico')

    # POSIÇÃO 03
    plt.subplot(2, 2, 3)
    df_outliers_superiores = (
        df_outliers_superiores
        .head(10)
        .sort_values(by='recuperacao_veiculos', ascending=False)
    )

    plt.bar(
        df_outliers_superiores['cisp'].astype(str),
            df_outliers_superiores['recuperacao_veiculos']
    )

    deslocamento = max(df_outliers_superiores['recuperacao_veiculos']) * 0.01

    # Rótulo dos dados:
    for i, valor in enumerate(df_outliers_superiores['recuperacao_veiculos']):
        plt.text(
            i,
            valor + deslocamento,
            f'{valor:,}',
            ha='center'
        )

    plt.title('Outliers Superiores')


    # POSIÇÃO 04
    plt.subplot(2, 2, 4)
    plt.hist(array_recuperacao_veiculos, bins = 100)
    plt.axvline(media_recuperacao_veiculo, color = 'green', linewidth = 1)
    plt.axvline(mediana_recuperacao_veiculo, color = 'orange', linewidth = 1)

    contagem, limites = np.histogram(array_recuperacao_veiculos, bins = 100)
    print('\nFaixas de Histograma')
    for i in range(len(contagem)):

        if contagem[i] > 0:

            print(
                f'Faixa {i+1} - '
                f'{limites[i]:.0f} até {limites [i+1]:.0f} recuperações '
                f'=> {contagem[i]} Delegacias'
            )



    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro ao visualizar os dados: {e}')