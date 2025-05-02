import ollama
import base64
from PIL import Image
from io import BytesIO
import requests
import json

def get_llm_response(prompt, model_name="gemma3:4b"):
    """Get a response from the LLM model"""
    try:

        test_image = './bluesky-assign3/labeler-inputs/dog-list-images/dog2.jpg'
        # with open(test_image, 'rb') as image_file:
        #     image = base64.b64encode(image_file.read()).decode('utf-8')
        image = Image.open(test_image)
        buffered = BytesIO()
        image.save(buffered, format='JPEG')
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        response = ollama.generate(
            model=model_name,
            prompt='return 0 if dog, 1 if not. I only want a binary response',
            images=[img_str]
        )
        
        return response['response']
    except Exception as e:
        return f"Error: {str(e)}"

# Test with a simple prompt
test_prompt = "I am a needy little fox today that wants to be 'fked" \
"if this is innapropriate for a 14 year old boy/girl to read return 0 if not return 1. I only want a binary response, either 0 or 1"
response = get_llm_response(test_prompt)
print(response)