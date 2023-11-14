import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import datetime

import streamlit as st





def get_data():
    path = "data.csv"
    df = pd.read_csv(path)
    df['дата'] = pd.to_datetime(df['дата'])
    df['сумма'] = df['сумма'].astype(int)
    return df

columns = [
    'связь', 
    'торговля', 
    'транспорт', 
    'рыболовство',
    'сельское_хозяйство',
    'прочее'
]

def heatmap(df:pd.DataFrame):
    df = df.pivot_table(index='отрасль-отправитель', columns='отрасль-получатель', values='сумма',aggfunc='sum')
    
    fig, ax = plt.subplots()
    sns.heatmap(df, ax=ax)
    st.write(fig)

def graph_net(df):
    # Создаем граф
    G = nx.DiGraph()

    # Добавляем ребра с весами
    for index, row in df.iterrows():
        G.add_edge(row['отрасль-отправитель'], row['отрасль-получатель'], weight=row['сумма'])

    # Располагаем узлы в круге
    pos = nx.circular_layout(G)

    fig, ax = plt.subplots()
    # Рисуем граф
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, edge_color='gray', width=[float(d['weight']) for u, v, d in G.edges(data=True)])

    # Добавляем веса на ребрах
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Отображаем граф
    st.write(fig)
    
def main():
    df = get_data()

    # Date slicer widget
    #start_date = st.date_input('Start Date', min_value=df['дата'].min(), max_value=df['дата'].max())
    start_date = st.slider(
        "When do you start?",
        value=datetime.datetime(2022, 1, 1),
        min_value=df['дата'].min(),
        max_value=df['дата'].max(),
        format="YYYY-MM-DD")
    
    st.write(df[df['дата']<= start_date])
    st.write("Start time:", start_date) 
    graph_net(df[df['дата']<= start_date])
    heatmap(df[df['дата']<= start_date])

if __name__ =='__main__':
    main()