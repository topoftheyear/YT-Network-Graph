import json

from tqdm import tqdm

def main():
    channels = dict()
    with open('all_channels.json', 'r') as f:
        channels = json.load(f)
        
    table_format = ['channel_id\tname\tweight\tdirected\ttarget\tinteraction']
    
    print('Building nodes list')
    for channel_id, info in tqdm(channels.items()):
        name = str(info['name'].encode('utf-8'))
        name = name[2:len(name) - 1]
        weight = 0
        for other_id, other_info in channels.items():
            if other_id == channel_id:
                continue
                
            if channel_id in other_info['connected_channels']:
                weight += 1
        for connected_channel in info['connected_channels']:
            if connected_channel not in channels.keys():
                continue
            table_format.append(f'{channel_id}\t{name}\t{weight}\tfalse\t{connected_channel}\tpp')
        
    with open('nodes.txt', 'w') as f:
        for element in table_format:
            f.write(element)
            f.write('\n')
        
    
if __name__ == "__main__":
    main()
