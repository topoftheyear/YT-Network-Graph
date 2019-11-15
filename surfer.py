import os

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
    
    # Create queue of channels
    queue = ["UC_x5XG1OV2P6uZZ5FSM9Ttw"]
    explored_channels = list()
    
    # Go through everything 
    try:
        while len(queue) > 0:
            # Get next channel
            current_channel = queue.pop(0)
            # Add it to the list of traversed channels
            explored_channels.append(current_channel)
            
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
        
            for c in all_channels[current_channel]['connected_channels']:
                # Verify we haven't already explored the channel
                if c in explored_channels:
                    continue
                    
                # Verify the channel isn't already in the queue
                if c in queue:
                    continue
                    
                queue.append(c)

    except KeyboardInterrupt:
        print('Stopping')
    except Exception:
        print('Broke')

    for key,item in all_channels.items():
        print(key)
        print(item)

if __name__ == "__main__":
    main()