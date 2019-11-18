import os
import json
import time

import googleapiclient.discovery
import googleapiclient.errors

def main():
    # Establish connection
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "API_key"
    api_key = open(client_secrets_file, 'r').read()

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    
    # All channels
    all_channels = dict()
    if os.path.isfile('all_channels.json'):
        all_channels = get_channels()
    
    # Create queue of channels
    queue = list()
    if os.path.isfile('existing_queue.txt'):
        queue = get_queue()
    else:
        queue = ["UC_x5XG1OV2P6uZZ5FSM9Ttw"]
    
    # Go through everything 
    try:
        while len(queue) > 0:
            # Get next channel
            current_channel = queue.pop(0)
            
            # Form and make request
            request = youtube.channels().list(
                part='snippet,brandingSettings',
                id=current_channel
            )
            response = request.execute()
            
            # If there are no items, continue
            if len(response['items']) <= 0:
                continue
            
            result = response['items'][0]
            
            # If keys don't exist in the result, continue
            if 'featuredChannelsUrls' not in result['brandingSettings']['channel'] or 'title' not in result['snippet']:
                continue
            
            # Otherwise, add to list of channels
            print(result['snippet']['title'])
            all_channels[current_channel] = {'name': result['snippet']['title'], 'connected_channels': result['brandingSettings']['channel']['featuredChannelsUrls']}
        
            # Add all those channels to the queue
            for c in all_channels[current_channel]['connected_channels']:
                # Verify we haven't already explored the channel
                if c in all_channels.keys():
                    continue
                    
                # Verify the channel isn't already in the queue
                if c in queue:
                    continue
                    
                queue.append(c)
                
            # Artificial waiting time
            time.sleep(0.7)

    except KeyboardInterrupt:
        print('Stopping')
    except googleapiclient.errors.HttpError:
        print('Quota exceeded')
    except Exception:
        print('Broke')
        
    # Save everything
    with open('all_channels.json', 'w') as f:
        json.dump(all_channels, f)
    
    with open('existing_queue.txt', 'w') as f:
        for thing in queue:
            f.write(f'{thing}\n')
        
def get_channels():
    d = dict()
    with open('all_channels.json', 'r') as f:
        d = json.load(f)
        
    return d

def get_queue():
    q = list()
    with open('existing_queue.txt', 'r') as f:
        line = f.readline().strip('\n')
        while line:
            q.append(line)
            line = f.readline().strip('\n')
    print(f'loaded_queue \n{q}')
    
    return q

if __name__ == "__main__":
    main()