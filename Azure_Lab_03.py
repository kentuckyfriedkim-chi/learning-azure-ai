"""
Image Text Extraction and Annotation with Azure AI Vision

This script utilizes Azure's Computer Vision API to read and extract text from images, 
annotate the detected text, and save the results as a new image. It supports detecting both 
printed and handwritten text, making it ideal for applications requiring OCR (Optical Character Recognition). 
The extracted text, along with bounding polygons around each word, is displayed in the console and visualized on the image.

Key Features:
- Reads and extracts text (printed or handwritten) from an input image using Azure's Vision API.
- Draws bounding polygons around detected text on the image.
- Displays text and its bounding polygon coordinates in the console.
- Saves the annotated image for easy reference.

Requirements:
- Python 3.x
- Azure AI Vision SDK
- dotenv, Pillow, Matplotlib

Setup Instructions:
1. Install the required packages using pip:
   ```bash
   pip install azure-ai-vision Pillow matplotlib python-dotenv
2. Set up Azure AI Vision API:
Create a .env file in the project directory with the following variables:
makefile
Copy code
AI_SERVICE_ENDPOINT=your_endpoint_here
AI_SERVICE_KEY=your_key_here
3. Place the images you want to analyze in an images folder in the project directory.
Usage:

4. Run the script from the command line:
bash
Copy code
python your_script_name.py
5. Choose the option to analyze either the image with printed text (Lincoln.jpg) or an image with handwritten text (Note.jpg) as prompted.
This script is ideal for developers looking to incorporate OCR and image annotation into their projects. 
"""

# Image Text Extraction and Annotation with Azure AI Vision

#.env variables for the code 
AI_SERVICE_ENDPOINT="XXXXXXXXXXX.cognitive-services"
AI_SERVICE_KEY="XXXXXXXXXXXXXXXXXXX"

# script code

from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def main():
    global cv_client
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )

        # Menu for text reading functions
        print('\n1: Use Read API for image (Lincoln.jpg)\n2: Read handwriting (Note.jpg)\nAny other key to quit\n')
        command = input('Enter a number:')
        
        if command == '1':
            image_file = os.path.join('images', 'Lincoln.jpg')
            GetTextRead(image_file)
        elif command == '2':
            image_file = os.path.join('images', 'Note.jpg')
            GetTextRead(image_file)

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('\n')
    
    # Open image file
    with open(image_file, "rb") as f:
        image_data = f.read()

    # Use Analyze image function to read text in image
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    # Display the image and overlay it with the extracted text
    if result.read is not None:
        print("\nText:")

        # Prepare image for drawing
        image = Image.open(image_file)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'
        
        for line in result.read.blocks[0].lines:
            # Return the text detected in the image
            print(f"  {line.text}")

            drawLinePolygon = True
            r = line.bounding_polygon
            bounding_polygon = (
                (r[0].x, r[0].y), (r[1].x, r[1].y),
                (r[2].x, r[2].y), (r[3].x, r[3].y)
            )

            # Return the position bounding box around each line
            print("   Bounding Polygon: {}".format(bounding_polygon))
            
            # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
            for word in line.words:
                r = word.bounding_polygon
                bounding_polygon = (
                    (r[0].x, r[0].y), (r[1].x, r[1].y),
                    (r[2].x, r[2].y), (r[3].x, r[3].y)
                )
                print(f"    Word: '{word.text}', Bounding Polygon: {bounding_polygon}, Confidence: {word.confidence:.4f}")

            # Draw word bounding polygon
            drawLinePolygon = False
            draw.polygon(bounding_polygon, outline=color, width=3)

            # Draw line bounding polygon
            if drawLinePolygon:
                draw.polygon(bounding_polygon, outline=color, width=3)
        
        # Save image
        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'text.jpg'
        fig.savefig(outputfile)
        print('\n  Results saved in', outputfile)

if __name__ == "__main__":
    main()








