import ollama
import base64
from io import BytesIO
from PIL import Image

def get_llm_response_text_only(prompt):
    conditional = 'if this is innapropriate for a 14 year old boy/girl to read return 1 if not return 0. I only want a binary response, either 0 or 1'
    try:
        response = ollama.generate(
            model="gemma3:4b",
            prompt=prompt + conditional,
        )
        return response['response'][0]
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_llm_response(prompt, post_images):
    conditional = 'if this is innapropriate for a 14 year old boy/girl to read return 1 if not return 0. I only want a binary response, either 0 or 1'
    try:
        response = ollama.generate(
            model="gemma3:4b",
            prompt=prompt + conditional,
            images=post_images
        )
        return response['response'][0]
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def encode_images(images):
    result = []
    for img in images:
        # image = Image.open(img)
        buffered = BytesIO()
        img.save(buffered, format='JPEG')
        result.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))

    return result

if __name__ == '__main__':
    # test_prompt = "I am a needy little fox today that wants to be 'fked" \
    # "if this is innapropriate for a 14 year old boy/girl to read return 0 if not return 1. I only want a binary response, either 0 or 1"
    # response = get_llm_response(test_prompt)
    # print(response)
    pass