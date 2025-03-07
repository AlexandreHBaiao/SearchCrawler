import os

# Crawler for Azure Devops Wiki

# # %%
# !pip install azure-identity

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
base_url = f"https://msdata.visualstudio.com/{project}/_apis/wiki/wikis/{wiki_id}/pages"
main_url = f"{base_url}?recursionLevel={recursionLevel}&path=/&includeContent=True&api-version={api_version}"

response = requests.get(main_url, headers=headers)
response.raise_for_status()
wiki_pages = response.json()

contents = []
def get_page_recursively(page):
    if 'subPages' in page:
        for sub_page in page['subPages']:
            get_page_recursively(sub_page)
    url = f"{base_url}/?path={urllib.parse.quote(page['path'])}&recursionLevel=OneLevel&includeContent=True&api-version={api_version}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    page_content = response.json()
    if response.status_code == 200 and page_content['content'] is not None:
        contents.append(page_content['content'])

get_page_recursively(wiki_pages)

print(contents[0])






# %%
