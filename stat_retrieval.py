import os
import json

import googleapiclient.discovery
import googleapiclient.errors

def main():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "API_key"
    api_key = open(client_secrets_file, 'r').read()

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    all_channels = dict()
    with open('all_channels.json', 'r') as f:
        all_channels = json.load(f)
        
    try:
        pass
        for channel in all_channels.keys():
            print(channel)
            #if 'statistics' in all_channels[channel]:
            #    print(f'Skipping {all_channels[channel]["name"]}')
            #    continue
        
            request = youtube.channels().list(
                part="statistics",
                id=channel,
            )
            response = request.execute()
            print(response)

            # If there are no items, continue
            if len(response['items']) <= 0:
                continue
            
            result = response['items'][0]
            
            all_channels[channel]['statistics'] = result['statistics']
            
    except googleapiclient.errors.HttpError:
        print('Quota exceeded')
        
    # Save everything
    with open('all_channels.json', 'w') as f:
        json.dump(all_channels, f)

if __name__ == "__main__":
    main()