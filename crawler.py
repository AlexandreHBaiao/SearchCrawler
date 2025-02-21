import os

# Crawler for Azure Devops Wiki

# %%
!pip install azure-identity

# %% Import libraries
import requests
import json
import urllib.parse
from azure.identity import DefaultAzureCredential

# %% Credentials

credential = DefaultAzureCredential()
# token_response = credential.get_token("https://dev.azure.com/.default")
# ba
token_response = credential.get_token("499b84ac-1321-427f-aa17-267ca6975798/.default")
access_token = token_response.token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# %% List wiki pages

# base url: https://msdata.visualstudio.com/Azure%20Search/_wiki/wikis/Azure-Search.wiki/193/Azure-Search-Wiki
project = 'Azure%20Search'
wiki_id = 'Azure-Search.wiki'
api_version = '7.1-preview.1'
recursionLevel = 'full'
base_url = f"https://msdata.visualstudio.com/{project}/_apis/wiki/wikis/{wiki_id}/pages?recursionLevel={recursionLevel}&path=/&includeContent=True&api-version={api_version}"

response = requests.get(base_url, headers=headers)
response.raise_for_status()
wiki_pages = response.json()


def get_page_recurively(page):
    if 'subPages' in page:
        for sub_page in page['subPages']:
            get_page_recurively(sub_page)
    print(page['path'])
    url = page['url'] + f"?recursionLevel=OneLevel&path=/&includeContent=True&api-version={api_version}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    page_content = response.json()
    if page_content['content'] is not None:
        print(page_content['content'])


list = []
def print_content_of_subpages(page):
    if 'subPages' in page:
        for sub_page in page['subPages']:
            if (':' in sub_page['path']) or ('?' in sub_page['path']) or ('+' in sub_page['path']):
                continue
            print_content_of_subpages(sub_page)

    print(page['path'])
    git_item_url= page['url']
    parsed_url = urllib.parse.urlparse(git_item_url)
    response = requests.get(parsed_url.geturl(), headers=headers)
    response.raise_for_status()
    page_content = response.json()
    print(page_content)
    if 'content' in page_content:
        list = page_content['content']

print_content_of_subpages(wiki_pages)

print(list[0])

    






# %%
