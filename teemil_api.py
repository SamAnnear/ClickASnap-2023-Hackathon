import requests
import urllib
import base64
import os




class TeemilAPI():

    def __init__(self):

        self.publicSafeKey = 'elCp6zR3XcWXOE49c2EIoLc0yJleaJdJ3LMrBRrX'
        
    def createImageTshirt(self, img_url, local):

        if not local:
            img = self.encodeImageBase64(img_url)

        else:
            img = self.encodeImageLocal(img_url)

        url = 'https://teemill.com/omnis/v3/product/create'

        payload = {
            "image_url": f"data:image/png;base64, {str(img)[2:]}"
            }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer Bearer {self.publicSafeKey}"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()

    
    def encodeImageBase64(self, img_url):

        r = requests.get(img_url)

        return base64.b64encode(r.content)
    
    def decodeImageBase64(self, base64_):

        '''with open('trash/temp.png', 'wb') as tempImgFile:
            tempImgFile.write(base64.b64decode(base64_))'''

        return base64.b64decode(base64_)

    def encodeImageLocal (self, img_path):

        # flask web feature
        with open(f".{img_path.split('5000')[1]}", 'rb') as file:
            img_data = file.read()

            b64 = base64.b64encode(img_data)

        '''print(img_path)

        with open(img_path, 'rb') as file:
            img_data = file.read()

            b64 = base64.b64encode(img_data)'''

        return b64
    
    def createMultipleImageLocal (self):

        filesdir = './static/images_tshirts'
        for imagerepo in os.listdir(filesdir):

            path = filesdir + f'/{imagerepo}'

            for repo in os.listdir(path):

                if repo.endswith('.png'):
                    
                    data = self.createImageTshirt(f'{path}/{repo}', 1)
                    image_url = data['url']

                    b64 = self.encodeImageBase64(image_url)
                    content = self.decodeImageBase64(b64)

                    with open(f'{path}/{repo}', 'wb') as image_file:
                        image_file.write(content)

                else:

                    path = filesdir + f'/{imagerepo}' + f'/{repo}'

                    for repo2 in os.listdir(path):
                        
                        data = self.createImageTshirt(f'{path}/{repo2}', 1)
                        image_url = data['url']

                        b64 = self.encodeImageBase64(image_url)
                        content = self.decodeImageBase64(b64)

                        with open(f'{path}/{repo2}', 'wb') as image_file:
                            image_file.write(content)

    

if __name__ == '__main__':
    api = TeemilAPI()
    #api.decodeImageBase64(api.encodeImageBase64('https://avatars.githubusercontent.com/u/43704805?s=80&v=4'))
    #print(api.createImageTshirt('https://d1unuvan7ts7ur.cloudfront.net/0x600/filters:strip_exif()/4be698c3-af97-46b4-b98f-280af75b8da7/01GTWDTCEB3K9TEXY1B5YXQGZH', 0))
    #print(str(api.encodeImageBase64('https://avatars.githubusercontent.com/u/43704805?s=80&v=4'))[2:])
    #api.createMultipleImageLocal()
    print(api.createImageTshirt('./static/images/image_one/cartoon/image-1-cartoon-1.png', 1))
