from openai import OpenAI
import webbrowser


client = OpenAI(
api_key="api_key",  # Replace with your API key
base_url="base_url"  
)

def generate_image(prompt):
        # Generate image
        response = client.images.generate(
            model="provider-1/FLUX.1-schnell",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        
        #print(response.data[0].url)
        webbrowser.open(response.data[0].url)

if __name__ == "__main__":
    print("uncomment it")
    prompt = input("Describe the image you want to generate: ")
    response = generate_image(prompt)

