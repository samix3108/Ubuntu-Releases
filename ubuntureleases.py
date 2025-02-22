import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

ascii_art = r"""

              .-.
        .-'``(|||)
     ,`\ \    `-`.               88                         88
    /   \ '``-.   `              88                         88
  .-.  ,       `___:    88   88  88,888,  88   88  ,88888, 88888  88   88
 (:::) :        ___     88   88  88   88  88   88  88   88  88    88   88
  `-`  `       ,   :    88   88  88   88  88   88  88   88  88    88   88
    \   / ,..-`   ,     88   88  88   88  88   88  88   88  88    88   88
     `./ /    .-.`      '88888'  '88888'  '88888'  88   88  '8888 '88888'
 LGB    `-..-(   )
              `-`

------------------------------------------------
This ASCII pic can be found at
https://asciiart.website/index.php?art=logos%20and%20insignias/linux
"""

base_url = 'https://releases.ubuntu.com/'

def fetch_versions(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        versions = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.endswith('/') and href[:-1].replace('.', '').isdigit():  
                versions.append(href.strip('/'))
        return versions
    else:
        print("Error accessing the page.")
        return []

def download_iso(version):
    url = f"{base_url}{version}/ubuntu-{version}-desktop-amd64.iso"
    file_name = url.split('/')[-1]

    response = requests.head(url)
    total_size = int(response.headers.get('content-length', 0))

    with requests.get(url, stream=True) as response, open(file_name, 'wb') as file, tqdm(
        desc=file_name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            bar.update(len(chunk))

    print(f"{file_name} successfully downloaded!")

if __name__ == '__main__':
    print(ascii_art)
    print("Ubuntu Releases")
    print("=" * 50)
    
    versions = fetch_versions(base_url)
    if versions:
        print("Available Versions:")
        for idx, version in enumerate(versions):
            print(f"{idx + 1}. {version}")

        try:
            choice = int(input("Enter the number of the version you want to download: ")) - 1
            if 0 <= choice < len(versions):
                selected_version = versions[choice]
                print(f"Starting download of version: {selected_version}")
                download_iso(selected_version)
            else:
                print("Invalid version number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        print("No versions found.")
