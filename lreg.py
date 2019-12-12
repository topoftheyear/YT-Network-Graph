import json

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

def main():
    predicting_key = 'subscribers'

    all_channels = dict()
    with open('all_channels.json', 'r') as f:
        all_channels = json.load(f)
    
    print('Creating dataset')
    workable_channels = dict()
    for id, info in tqdm(all_channels.items()):
        if 'statistics' not in info:
            continue
        
        weight = 0
        
        for other_id, other_info in all_channels.items():
            if other_id == id:
                continue
                
            if id in other_info['connected_channels']:
                weight += 1
        
        workable_channels[id] = {
            'name': info['name'],
            'subscribers': int(info['statistics']['subscriberCount']),
            'views': int(info['statistics']['viewCount']),
            'videos': int(info['statistics']['videoCount']),
            'outbound_connections': len(info['connected_channels']),
            'inbound_connections': weight,
        }
        
    print('Plotting points')
    for key, item in tqdm(workable_channels.items()):
        plt.scatter(x=item['inbound_connections'], y=item[predicting_key], c='b')
        
    plt.xlabel('outbound connections')
    plt.ylabel(predicting_key)
    
    print('Creating X and Y dimensions for linear regression')
    x = list()
    for id, data in tqdm(workable_channels.items()):
        x.append([data['outbound_connections']])
        
    y = list()
    for id, data in tqdm(workable_channels.items()):
        y.append(data[predicting_key])
        
    x = np.array(x)
    y = np.array(y)
    
    print('Creating and fitting the model')
    model = LinearRegression().fit(x, y)
    
    print(f'Score: {model.score(x, y)}')
    print(f'Coefficient: {model.coef_}')
    print(f'Intercept: {model.intercept_}')
    
    plt.plot(x, model.predict(x), c='red', linewidth=3)
    plt.show()
    plt.savefig('figure.png')

    
if __name__ == "__main__":
    main()
