import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = os.path.join("Data")
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError as e:
            print(f"Unable to open {image_path}: {e}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error in API request: {e}")
        return None

async def generate_image(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High Details, high resolution, seed = {randint(0, 1000000)}",
        }

        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes is None:
            print(f"Failed to generate image {i+1}")
            continue
            
        try:
            output_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i+1}.jpg")
            with open(output_path, "wb") as f:
                f.write(image_bytes)
        except IOError as e:
            print(f"Error saving image {i+1}: {e}")

def GenerateImages(prompt: str):
    try:
        asyncio.run(generate_image(prompt))
        open_images(prompt)
        return True
    except Exception as e:
        print(f"Error in GenerateImages: {e}")
        return False

def main():
    while True:
        try:
            data_file = os.path.join("Frontend", "Files", "ImageGeneration.data")
            with open(data_file, "r") as f:
                data = f.read().strip()

            if not data:
                sleep(1)
                continue

            Prompt, Status = data.split(",")

            if Status == "True":
                print("Generating Images..")
                GenerateImages(prompt=Prompt)

            with open(data_file, "w") as f:
                f.write("False,False")
        except Exception as e:
            print(f"Error in main loop: {e}")
            sleep(1)

if __name__ == "__main__":
    main()