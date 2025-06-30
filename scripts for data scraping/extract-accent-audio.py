import os
import requests
import tarfile
from bs4 import BeautifulSoup

# URL for VoxForge 16kHz audio files
BASE_URL = 'https://repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/'
DOWNLOAD_DIR = 'voxforge_data'

#get all .tgz file links from the URL
def get_tgz_links(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tgz_links = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.tgz')]
    return tgz_links

#Download and extract a .tgz file into the specified directory
def download_and_extract_tgz(tgz_url, download_path):

    filename = tgz_url.split('/')[-1]
    file_path = os.path.join(download_path, filename)

    print(f'Downloading {filename}...')
    response = requests.get(tgz_url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f'Extracting {filename}...')
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=download_path)

    os.remove(file_path)
#parse README file and extract key value metadata pairs
def parse_readme(readme_path):
    metadata = {}
    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                metadata[key.strip()] = value.strip()
    return metadata

#Traverse all subdirectories and get metadata from README files
def collect_metadata(data_dir):
    metadata_list = []
    for root, dirs, files in os.walk(data_dir):
        if 'README' in files:
            readme_path = os.path.join(root, 'README')
            metadata = parse_readme(readme_path)
            metadata['path'] = root
            metadata_list.append(metadata)
    return metadata_list

def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    tgz_links = get_tgz_links(BASE_URL)
    for link in tgz_links:
        full_url = BASE_URL + link
        download_and_extract_tgz(full_url, DOWNLOAD_DIR)

    print('complete.')

    print('parsing metadata from README files')
    metadata_entries = collect_metadata(DOWNLOAD_DIR)
    for entry in metadata_entries:
        print(entry)

if __name__ == '__main__':
    main()
