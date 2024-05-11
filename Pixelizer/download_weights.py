# import requests
# import os

# # Replace 'YOUR_GOOGLE_DRIVE_URL' with the URL of the file you want to download


# # Function to download a file from Google Drive using its shareable link
# def download_file_from_google_drive(google_drive_url, destination):
#     response = requests.get(google_drive_url)
#     with open(destination, 'wb') as f:
#         f.write(response.content)

# # pixelart_vgg19.pth   https://drive.google.com/file/d/1b2AdjBlr30QPQI6WExxIcZ_SwPCaPt1C/view?usp=drive_link
# # alias_net.pth        https://drive.google.com/file/d/1cCeZsfwL2WiHYGv84ICWzNRkYAjtXeA2/view?usp=drive_link
# # 160_net_G_B.pth      https://drive.google.com/file/d/1eDdz_psOT6DXMfWboojSXKvUc9nXl9WW/view?usp=drive_link
# # 160_net_G_A.pth      https://drive.google.com/file/d/1T7exWZsPafqgBjY5DpsHKHhjPFXvAHjx/view?usp=drive_link

# pixelart_vgg19 = 'https://drive.google.com/file/d/1b2AdjBlr30QPQI6WExxIcZ_SwPCaPt1C/view?usp=drive_link'
# alias_net = 'https://drive.google.com/file/d/1cCeZsfwL2WiHYGv84ICWzNRkYAjtXeA2/view?usp=drive_link'
# net_G_B =      'https://drive.google.com/file/d/1eDdz_psOT6DXMfWboojSXKvUc9nXl9WW/view?usp=drive_link'
# net_G_A =       'https://drive.google.com/file/d/1T7exWZsPafqgBjY5DpsHKHhjPFXvAHjx/view?usp=drive_link'

# os.makedirs('./checkpoints/AdGenture', exist_ok=True)
# os.makedirs('./dataset/TEST_DATA/Input', exist_ok=True)
# download_file_from_google_drive(pixelart_vgg19, 'pixelart_vgg19.pth')
# download_file_from_google_drive(alias_net, 'alias_net.pth')
# download_file_from_google_drive(net_G_B, './checkpoints/AdGenture/160_net_G_A.pth')
# download_file_from_google_drive(net_G_A, './checkpoints/AdGenture/160_net_G_B.pth')

import requests

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    



def main():
    
    pixelart_vgg19 = '1b2AdjBlr30QPQI6WExxIcZ_SwPCaPt1'
    alias_net = '1cCeZsfwL2WiHYGv84ICWzNRkYAjtXeA2'
    net_G_B = '1eDdz_psOT6DXMfWboojSXKvUc9nXl9WW'
    net_G_A = '1T7exWZsPafqgBjY5DpsHKHhjPFXvAHjx'

   
    print(f"dowload {pixelart_vgg19} to {'pixelart_vgg19.pth'}")
    download_file_from_google_drive(pixelart_vgg19, 'pixelart_vgg19.pth')

    print(f"dowload {alias_net} to {'alias_net.pth'}")
    download_file_from_google_drive(alias_net, 'alias_net.pth')

    print(f"dowload {net_G_A} to {'./checkpoints/AdGenture/160_net_G_A.pth'}")
    download_file_from_google_drive(net_G_A, './checkpoints/AdGenture/160_net_G_A.pth')

    print(f"dowload {net_G_B} to {'./checkpoints/AdGenture/160_net_G_B.pth'}")
    download_file_from_google_drive(net_G_B, './checkpoints/AdGenture/160_net_G_B.pth')


if __name__ == "__main__":
    main()
