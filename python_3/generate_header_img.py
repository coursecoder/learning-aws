import os
import openai

# to use DALL-E openAI you will need to create account and generate key
# set environment variable named OPENAI_API_KEY
# if this is not setup the script will automatically use the header image on file
openai.api_key = "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"
openai.Model.list()
 
def get_header_img():
        """
        Use DALL-E Images API.

        """
        response = openai.Image.create(
        prompt="balls of red yellow green blue playdough on dark gray surface, Sigma 85mm f/1.4",
        n=1,
        size="1024x1024"
        )
        img_url = response['data'][0]['url']
        return img_url

if __name__ == '__main__':
        img_url = get_header_img()
        print(img_url)