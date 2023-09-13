import os
import requests
import base64
import random
import string
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("API_KEY")

# Ensure the API key is not empty
if api_key is None:
    raise ValueError("API_KEY not found in the .env file")

# Define the base URL for the API
base_url = 'https://api.getimg.ai/v1'

# Endpoint for generating images
generation_endpoint = '/stable-diffusion/text-to-image'

# Endpoint for upscaling images
upscale_endpoint = '/enhacements/upscale'

# Define the headers with authentication
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# Define the JSON data for generating the image
generation_data = {
    "model": "dark-sushi-mix-v2-25",  # Replace with your desired model
    "prompt": "Side view of a cat with vibrant neon neural network veins, representing futuristic technology and artificial intelligence. ",  # Your prompt for generating the image
    "output_format": "jpeg",  # Specify JPEG format
    "width": 1024,  # Your desired width
    "height": 1024,  # Your desired height
}

# Make a POST request to generate the image
try:
    response_generation = requests.post(f'{base_url}{generation_endpoint}', headers=headers, json=generation_data)

    # Check if the generation request was successful (status code 200)
    if response_generation.status_code == 200:
        # Parse the response JSON for the generated image
        generated_data = response_generation.json()
        
        # Decode the base64 image string
        generated_image_data = base64.b64decode(generated_data['image'])
        
        # Extract the first three words from the prompt
        prompt_words = generation_data['prompt'].split()[:3]
        
        # Generate a random string for uniqueness
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        # Construct the filename with the first three words and random string
        filename = '-'.join(prompt_words) + '-' + random_string + '-generated.jpg'
        
        # Specify the file path for saving the generated image
        generated_file_path = os.path.join('generated', filename)
        

        print(f"Image generated successfully and saved as '{generated_file_path}'")

        # Upscale the generated image
        # Encode the generated image data as base64 for upscaling
        encoded_generated_image = base64.b64encode(generated_image_data).decode('utf-8')

        upscale_data = {
            "model": "real-esrgan-4x",  # Replace with your desired upscale model
            "image": encoded_generated_image,  # Base64 encoded generated image
            "scale": 4,  # Upscale factor
            "output_format": "jpeg",  # Specify JPEG format
        }


        print(f'Upscale API URL: {base_url}{upscale_endpoint}')

        # Make a POST request to upscale the image
        response_upscale = requests.post(f'{base_url}{upscale_endpoint}', headers=headers, json=upscale_data)

        # Check if the upscale request was successful (status code 200)
        if response_upscale.status_code == 200:
            # Parse the response JSON for the upscaled image
            upscaled_data = response_upscale.json()
            
            # Decode the base64 upscaled image string
            upscaled_image_data = base64.b64decode(upscaled_data['image'])
            
            # Construct the filename for the upscaled image
            upscale_filename = '-'.join(prompt_words) + '-' + random_string + '-upscaled.jpg'
            
            # Specify the file path for saving the upscaled image
            upscale_file_path = os.path.join('generated', upscale_filename)
            
            # Save the upscaled image to the specified file path
            with open(upscale_file_path, 'wb') as upscale_image_file:
                upscale_image_file.write(upscaled_image_data)
            
            print(f"Image upscaled successfully and saved as '{upscale_file_path}'")
        else:
            # Handle error cases for upscaling
            print(f'Error upscaling image: {response_upscale.status_code}')
            print(response_upscale.text)
    else:
        # Handle error cases for generation
        print(f'Error generating image: {response_generation.status_code}')
        print(response_generation.text)
except requests.exceptions.RequestException as e:
    # Handle connection errors or other exceptions here
    print(f'Error: {e}')
