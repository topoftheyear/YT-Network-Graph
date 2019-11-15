# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery
import googleapiclient.errors

def main():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "API_key"
    api_key = open(client_secrets_file, 'r').read()

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    request = youtube.channels().list(
        part="brandingSettings",
        #id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
        forUsername="GoogleDevelopers"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()