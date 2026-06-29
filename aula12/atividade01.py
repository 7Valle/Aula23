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

    # print('\nMedidas de Tendência Central:')
    # print(30 * '=')
    # print(f'Média: {media_recuperacao_veiculo:.2f}')
    # print(f'Mediana: {mediana_recuperacao_veiculo:.2f}')
    # print(f'Distância: {distancia:.2f}')


except Exception as e:
    print(f'Erro ao processar medidas: {e}')



# Obtendo a distribuição
try:
    print('\nProcessando os quartis')
    q1 = np.quantile(array_recuperacao_veiculos, .25)
    q3 = np.quantile(array_recuperacao_veiculos, .75)

    # print('\nQuartis:')
    # print(30 * '=')

    # print(f'Q1: {q1}')
    # print(f'Mediana: {mediana_recuperacao_veiculo}')
    # print(f'Q3: {q3}')

    # Delegacias com menos recuperações
    df_recuperacao_menores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] < q1]
    df_recuperacao_menores = df_recuperacao_menores.sort_values(by = 'recuperacao_veiculos', ascending=True)
    # Delegacias com mais recuperações
    df_recuperacao_maiores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] > q3]

    # print(f'\nDelegacias com menos recuperações de roubos de veiculos: {df_recuperacao_menores}')
    # print(f'\nDelegacias com mais recuperações de roubos de veiculos: {df_recuperacao_maiores}')

except Exception as e:
    print(f'Erro ao obter a distribuição: {e}')



# Obtendo medidas de dispersão
try: 
    maximo = np.max(array_recuperacao_veiculos)
    minimo = np.min(array_recuperacao_veiculos)
    amplitude = maximo - minimo

    # print('\nMedidas de dispersão')
    # print(30 * '=')

    # print(f'Máximo: {maximo}')
    # print(f'Mínimo: {minimo}')
    # print(f'Amplitude total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão {e}')



# Calculando Outliers
try:
    iqr = q3 - q1

    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    # print()
    # print(f'IQR: {iqr}')
    # print(f'Limite Inferior: {limite_inferior}')
    # print(f'Limite Superior: {limite_superior}')


except Exception as e:
    print(f'Erro ao calcular os limites: {e}')



# Exibindo Outliers
try:
    df_outliers_superiores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] > limite_superior]

    df_outliers_inferiores = df_recuperacao_veiculo[df_recuperacao_veiculo['recuperacao_veiculos'] < limite_inferior]

    # print('\nDelegacias com Outliers Inferiores')
    # print(30 * '=')

    # if len(df_outliers_inferiores) == 0:
    #     print(f'\nNão existe Outliers inferiores!')
    
    # else:
    #     print(df_outliers_inferiores.sort_values(by = 'recuperacao_veiculos', ascending=True))


    # print('\nDelegacias com Outliers Superiores')
    # print(30 * '=')

    # if len(df_outliers_superiores) == 0:
    #     print(f'\nNão existe Outliers superiores!')
    
    # else:
    #     print(df_outliers_superiores)

except Exception as e:
    print(f'Erro ao calcular outliers: {e}')



# Obtendo Assimetria e Curtose
try:

    assimetria = df_recuperacao_veiculo['recuperacao_veiculos'].skew()
    curtose = df_recuperacao_veiculo['recuperacao_veiculos'].kurtosis()

    # print('\nMedidas de Distribuição')
    # print(30 * '=')
    # print(f'Assimetria: {assimetria}')
    # print(f'Curtose: {curtose}')


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

    # print('\nMedidas de Variabilidade')
    # print(30 * '=')
    # print(f'Variância: {variancia}')    
    # print(f'Distância entre Variâcia e a média: {distancia_var_media} %')
    # print(f'Desvio Padrão: {desvio_padrao}')
    # print(f'Coeficiente de variação: {coef_variacao}')

 

except Exception as e:
    print(f'Erro ao calcular variabilidade dos dados: {e}')



#Visualizando os dados
try:

    plt.subplots(2, 3, figsize=(22,10))
    plt.suptitle('Recuperação de veículos por delegacia',
                 fontsize=16,
                 fontweight='bold')

    # POSIÇÃO 01 - BOXPLOT
    plt.subplot(2,3,1)

    plt.boxplot(
        array_recuperacao_veiculos,
        vert=False,
        showmeans=True
    )

    plt.title('Distribuição da recuperação de veículos')

    # POSIÇÃO 02 - RESUMO ESTATÍSTICO
    plt.subplot(2,3,2)

    plt.text(0.1,0.90,f'Média: {media_recuperacao_veiculo:.2f}',fontsize=9)
    plt.text(0.1,0.82,f'Distância: {distancia:.2f}',fontsize=9)
    plt.text(0.1,0.74,f'Limite Inferior: {limite_inferior:.2f}',fontsize=9)
    plt.text(0.1,0.66,f'Mínimo: {minimo:.2f}',fontsize=9)
    plt.text(0.1,0.58,f'Q1: {q1:.2f}',fontsize=9)
    plt.text(0.1,0.50,f'Mediana: {mediana_recuperacao_veiculo:.2f}',fontsize=9)
    plt.text(0.1,0.42,f'Q3: {q3:.2f}',fontsize=9)
    plt.text(0.1,0.34,f'Limite Superior: {limite_superior:.2f}',fontsize=9)
    plt.text(0.1,0.26,f'Máximo: {maximo:.2f}',fontsize=9)
    plt.text(0.1,0.18,f'Amplitude: {amplitude:.2f}',fontsize=9)

    plt.axis('off')
    plt.title('Resumo Estatístico')


    # POSIÇÃO 03 - HISTOGRAMA
    plt.subplot(2,3,3)

    plt.hist(array_recuperacao_veiculos, bins=20)

    plt.axvline(media_recuperacao_veiculo,
                color='green',
                linewidth=1,
                label='Média')

    plt.axvline(mediana_recuperacao_veiculo,
                color='orange',
                linewidth=1,
                label='Mediana')

    plt.legend()

    plt.title('Histograma')


    # POSIÇÃO 04 - MENORES RECUPERAÇOES
    plt.subplot(2,3,4)

    menores_q1 = (
        df_recuperacao_menores
        .head(10)
    )

    plt.bar(
        menores_q1['cisp'].astype(str),
        menores_q1['recuperacao_veiculos'],
        color='firebrick'
    )

    plt.title('Delegacias com menos recuperações de veículos')
    plt.xlabel('CISP')
    plt.ylabel('Recuperações')

    deslocamento = max(menores_q1['recuperacao_veiculos']) * 0.01

    for i, valor in enumerate(menores_q1['recuperacao_veiculos']):

        plt.text(
            i,
            valor + deslocamento,
            f'{valor:,}',
            ha='center',
            fontsize=8
        )

    # POSIÇÃO 05 - ACIMA DO Q3
    plt.subplot(2,3,5)

    maiores_q3 = (
        df_recuperacao_maiores
        .head(10)
    )

    plt.bar(
        maiores_q3['cisp'].astype(str),
        maiores_q3['recuperacao_veiculos'],
        color='forestgreen'
    )

    plt.title('Delegacias com mais recuperações de veículos')
    plt.xlabel('CISP')
    plt.ylabel('Recuperações')

    deslocamento2 = max(maiores_q3['recuperacao_veiculos']) * 0.01

    for i, valor in enumerate(maiores_q3['recuperacao_veiculos']):

        plt.text(
            i,
            valor + deslocamento2,
            f'{valor:,}',
            ha='center',
            fontsize=8
        )

    # POSIÇÃO 06 - OUTLIERS
    plt.subplot(2,3,6)

    plt.bar(
        df_outliers_superiores['cisp'].astype(str),
        df_outliers_superiores['recuperacao_veiculos'],
        color='darkorange'
    )

    deslocamento3 = max(df_outliers_superiores['recuperacao_veiculos']) * 0.01

    for i, valor in enumerate(df_outliers_superiores['recuperacao_veiculos']):

        plt.text(
            i,
            valor + deslocamento3,
            f'{valor:,}',
            ha='center',
            fontsize=8
        )

    plt.title('Delegacias que possuem recuperações discrepantes das demais')
    plt.xlabel('CISP')
    plt.ylabel('Recuperações')


    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro ao visualizar os dados: {e}')

    # Amplitude Total
    # amplitude = maximo - minimo
    # Resultado mais próximo do minimo, baixa dispersão.
    # Se for 0, quer dizer que todos os dado são iguais
    # Resultado mais próximo do maximo, alta dispersão.

    # IQR (Intervalo Interquartil) - Amplitude dos 50% dos dados mais centrais.
    # IQR = Q3 - Q1
    # Ele ignora os valores extremos. Max e Min estão fora do IQR
    # Não sofre interferência dos valores extremos.
    # Quanto mais próximo do zero, mais homogênenos são os dados
    # Quanto mais próximo do Q3, menos homogênenos são os dados (Mais dispersos)

    # Limite inferior:
    # É uma medida que vai identificar como outliers, os valores abaixo dele.

    # Limite superior:
    # É uma medida que vai identificar como outliers, os valores acima dele.

    #================================================================

    # Assimetria
    # Indica como os dados estão distribuidos em torno de um valor central.
    # Usada pra descrever o grau de assimetria de uma distribuição.    
    # Os valores estão equilibrados?
    # Existe uma maior quantidade de observações de registros maiores ou menores?
    # O peso da distribuição está mais para qual dos lados? "p/ os mais baixos ou mais altos?"

    # Interpretação
    # Resultado da Assimetria > 1
    # Assimetra Positiva Alta
    # Calda Longa à Direita
    # Existem valores muito alto puxando a média para cima
    # A tendência de que a média seja bem maior que a mediana. 
        

    # Resultado da Assimetria entre> 0.5 e 1
    # Assimetra Positiva Moderada
    # Calda à Direita
    # Existem valores altos puxando a média para cima, mas é menos acentuada.
    # A tendência de que a média seja maior que a mediana.


    # Resultado da Assimetria entre> -0.5 até 0.5
    # Distribuição aproximadamente simétrica
    # Os dados estão equilibrados em torno da média.
    # A tendência que a media seja muito próxima da mediana
        

    # Resultado da Assimetria entre> -0.5 e -1.0
    # Assimetria Negativa Moderada
    # Calda a esquerda.
    # Valores baixos puxando à média para baixo, mas menos acentuada.
    # A tendência que a media seja menor que a mediana
        

    # Resultado da Assimetria < -1
    # Assimetrai Negativa Alta.
    # Calda Longa a Esquerda
    # Existem valores muito baixo puxando a média para baixo.
    # A tendência de que a média seja muito menor que a mediana.

    #================================================================

    # Curtose:
    # Medida que descreve o formato da distribuição
    # Nos ajuda a entender, se os valores estão espalhados,
    # ou mais próximos da média.
    #Ajuda a entender, se existe outliers.


    # Curtose Alta: 
    # geralmente temos muitos valores distribuidos em torno da média,
    # e alguns outros, muito distantes dela.


    # Curtose Baixa:
    # os dados tendem a estar distribuidos ao longo do conjunto.
    

    # Interpretação segundo Fisher: (OBS: No Pandas o padrão é Fisher)
    # Resultado da Curtose = 0 ----> (Mesocúrtica)/( Pearson = 3)
    # Distribuição Normal
    # Concentração moderada no centro
    # Outliers são raros


    # Resultado da Curtose < 1 ----> (Platicúrtica)/( Pearson < 3)
    # Pico achatado
    # Dados mais afastados "espalhados"
    # Poucos extremos. "Mas pode haver outliers"


    # Resultado da Curtose > 1 ----> (Leptocúrtica)/( Pearson > 3)
    # Pico mais Alto
    # Muitos valores próximos da média
    # Outliers mais fortes
    # Caldas mais pesadas

    #================================================================

    # Variância
    # É uma medida para verificar a dispersão dos dados
    # Observa-se em relação a média
    # É a média dos quadrados da diferença entre cada valor e a média 
    # OBS: O resultado da variância está elevado ao quadrado

    # Interpretação:
    # Quanto maior a variância, maior é o afastamento dos valores em relação a média,
    # Indicando alta dispersão

    #================================================================

    # Distancia entre Média e Variância
    # Até 10% -> Baixa dispersão em relação a média
    # Entre 10% e 25% -> dispersão moderada em relação a média
    # Mais que 25% -> Alta dispersão em relação a média

    #================================================================

    # Desvio Padrão 
    # É a raiz quadrada da variância
    # É a normalização da variância
    # Apresenta o quanto os dados podem estar afastados em relação a média 
    # (tanto para mais, quanto para menos)

    #================================================================

    # Coeficiente de variação
    # É a magnitude do desvio padrão em relação a média

print(f'''\nA média de recuperações foi de {media_recuperacao_veiculo:.2f} veículos, enquanto a mediana foi de {mediana_recuperacao_veiculo:.2f}.
A distância entre a média e a mediana é de {distancia:.2f}, apresentando uma assimetria forte.
A diferença significativa entre essas medidas indica que poucas delegacias registram quantidades muito elevadas de recuperações, elevando a média da distribuição. A média não representa adequadamente o comportamento da maioria das delegacias.
O coeficiente de variação foi de {coef_variacao:.2f}, indicando alta dispersão dos dados em relação à média.
Esse resultado demonstra que as recuperações variam bastante entre as delegacias, mostrando que não existe homogeneidade entre os valores observados.
A assimetria positiva elevada {assimetria} indica uma distribuição com cauda longa à direita, ou seja, poucas delegacias apresentam valores muito elevados de recuperação de veículos, enquanto a maior parte possui quantidades inferiores. Essa característica explica por que a média é muito superior à mediana.
O valor de {curtose} representa uma curtose alta, indicando forte concentração dos dados e presença de valores extremos. Isso reforça que existem delegacias com desempenho muito acima da maioria.
''')
print(f'\nPortanto, conclui-se que não existe um padrão médio representativo para todas as delegacias. Os dados apresentam elevada dispersão e uma distribuição fortemente assimétrica à direita, concentrando a maior parte das delegacias em baixos quantitativos de recuperação, enquanto poucas concentram valores muito elevados.')


print(f'''\nUtilizando dados matemáticos, cálculamos os limites que funcionam como marca de corte para a nossa distribuição.
Encontramos o limite inferior e superior de recuperações de veículos por delegacias, são considerados muito abaixo ou muito acima do comportamento analisado as delegacias que tiveram recuperações veículo fora desses valores limites!
Limite inferior: {limite_inferior}
Limite superior: {limite_superior}
''')

print(f'\nNão existem delegacias com recuperações muito menores que as demais, mas foram encontradas delegacias com muito mais recuperações que as demais.')
print(f'Delegacias com recuperações fora do padrão:\n{df_outliers_superiores}')

print(f'''\nAs delegacias com menos de {q1} recuperações de veículos, entram no gráfico como as delegacias com as menores recuperações, pois 75% dos registros estão acima desse valor.
Delegacias com as menores recuperações de veículos:\n{df_recuperacao_menores}
''')

print(f'''\nAs delegacias com mais de {q3} recuperações de veículos, entram no gráfico como as delegacias com as maiores recuperações, pois 75% dos registros estão abaixo desse valor.
Delegacias com as maiores recuperações de veículos:\n{df_recuperacao_maiores}
''')