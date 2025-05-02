import ollama
import base64
from io import BytesIO
from PIL import Image
import os

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
    
def get_llm_response(prompt):
    conditional = """Analyze this content and return only "1" if the following are present, otherwise return "0":

1. Pornographic content or explicit sexual acts
2. Exposed genitalia shown in a sexualized context
3. Content primarily focused on sexual arousal or gratification (excluding foot content)
4. Sexual content involving minors (always flag regardless of context)
5. Explicit sexual text or descriptions of sexual acts

Do not flag:
- Artistic, educational, or non-sexualized nudity
- Historical or cultural depictions involving nudity
- Medical or educational content
- Partial nudity in non-sexual contexts (e.g., swimwear, fitness)
- Foot-focused content or foot fetish material
- Non-explicit suggestive content

Return ONLY the single digit "1" or "0" without explanation."""


    encoded_images = []

    folder = './temp'

    if os.path.exists(folder) and os.listdir(folder):
        image_files = [f for f in os.listdir(folder) if f.lower().endswith(('jpg'))]

        if image_files:
            for img in image_files:
                img_path = os.path.join(folder, img)
                image = Image.open(img_path)
                buffered = BytesIO()
                image.save(buffered, format='JPEG')
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                encoded_images.append(img_str)

    try:
        response = ollama.generate(
            model="gemma3:4b",
            prompt=prompt + conditional,
            images=encoded_images
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
    test_prompt = "Do u ever just" 
    response = get_llm_response(test_prompt)
    print(response)
    pass