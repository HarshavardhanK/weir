"""
Class for the image agent

It takes in an image and returns a detailed description of the image.

Combined with the location of the image and the detailed description, we can then feed this information to the next agent.


"""

import os
import base64
from dotenv import load_dotenv

from openai import OpenAI

class ImageAgent:
    
    def __init__(self):
        
        load_dotenv()
        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def _encode_image(self, image_path: str) -> str:
        """Encode the image into a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
    def __call__(self, image_path: str) -> str:
        """Return a detailed description of the image."""
        SYSTEM_PROMPT = """
        You are an expert at describing images. 
        The user will provide you with an image and you will return a detailed description of the image.
        Describe the image in full detail, including the objects, colors, textures, and any other relevant features.
        """
        
        image_base64 = self._encode_image(image_path)
        
        messages = [
            
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", 
             "content": [
                 {
                     "type": "text",
                     "text": "Here is the image",
                 },
                 {
                     "type": "image_url",
                     "image_url": {
                         "url": f"data:image/jpeg;base64,{image_base64}"
                     }
                 }
             ]}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
        )
        
        return response.choices[0].message.content


if __name__ == "__main__":
    image_agent = ImageAgent()
    print(image_agent("/Users/harshavardhank/Desktop/Screenshot 2024-11-11 at 00.01.51.png"))