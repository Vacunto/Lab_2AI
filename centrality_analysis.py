import networkx as nx
from networkx.algorithms import centrality
import matplotlib.pyplot as plt
import json
from vk_data import get_friends, save_to_json


def create_graph(friends_data):
    G = nx.Graph()

    for user_id, friends in friends_data.items():
        G.add_node(user_id)
        for friend_id in friends:
            G.add_node(friend_id)
            G.add_edge(user_id, friend_id)

    return G

def calculate_centrality(G):
    centrality_measures = {
        'closeness_centrality': centrality.closeness_centrality(G),
        'betweenness_centrality': centrality.betweenness_centrality(G),
        'eigenvector_centrality': centrality.eigenvector_centrality(G, max_iter=500)
    }
    return centrality_measures

def main():
    token = ''  
    user_id = '351652267'  

    friends_data = get_friends(token, user_id)

    save_to_json(friends_data)
    
    with open('friends_data.json', 'r') as json_file:
        friends_data = json.load(json_file)

    G = create_graph(friends_data)

    centrality_measures = calculate_centrality(G)
    
    for measure, values in centrality_measures.items():
        print(f"{measure}: {values}")
    
    print('Максимальное значение Центральность по близости')
    mx = max(centrality_measures['closeness_centrality'], key=centrality_measures['closeness_centrality'].get)
    print(f"ID узла: {mx}, Значение: {centrality_measures['closeness_centrality'][mx]}")

    print('Максимальное значение Центральность по посредничиству')
    mx = max(centrality_measures['betweenness_centrality'], key=centrality_measures['betweenness_centrality'].get)
    print(f"ID узла: {mx}, Значение: {centrality_measures['betweenness_centrality'][mx]}")

    print('Максимальное значение Центральность по собственному значению')
    mx = max(centrality_measures['eigenvector_centrality'], key=centrality_measures['eigenvector_centrality'].get)
    print(f"ID узла: {mx}, Значение: {centrality_measures['eigenvector_centrality'][mx]}")

    nx.draw(G, with_labels=False, node_color='lightblue', node_size=20)
    plt.show()


if __name__ == "__main__":
    main() 