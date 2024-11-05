'''
Project Overview: Language Detection with Azure AI Services

This project demonstrates two methods for implementing a language detection model using Azure AI Services: a REST client and an SDK client. Both methods use
environment variables for secure access to Azure AI resources, specifically utilizing the Text Analytics Language Detection API.

REST Client (rest-client.py): The REST client method utilizes HTTP. client to make direct HTTP POST requests to the Azure Text Analytics API.
In this script, the GetLanguage function constructs a JSON request with the user-provided text and sends it to the API endpoint specified in .env variables.
The response returns the detected language, displayed in the console. This method is more flexible, providing insights into the request and response structure, and is
suitable for environments where a lower-level API interaction is preferred.

SDK Client (sdk-client.py): The SDK client method leverages Azure's TextAnalyticsClient for simpler and more secure access to the language detection service. 
This script also gathers input text from the user but uses Azure’s TextAnalyticsClient.detect_language function for direct language detection. 
The SDK simplifies authentication and API calls,
requiring minimal configuration and error handling, making it suitable for rapid development and environments where Azure's Python SDK is supported.

Both approaches offer flexibility based on application needs, allowing developers to interact with Azure AI Services through different methods 
while achieving consistent results.
This repository serves as a foundation for experimenting with Azure AI’s language detection capabilities and can be adapted to include additional 
NLP functionalities or integrated into larger projects

for example-
input: 
Enter some text ("quit" to stop)
hello
output :
Language: English
'''


# Language detection model using Azure AI services
 

# Using Rest_Client

#.env variables for rest-client

AI_SERVICE_ENDPOINT="XXXXXXXXXXX.cognitive-services"
AI_SERVICE_KEY="XXXXXXXXXXXXXXXXXXX"

# rest-client.py code

from dotenv import load_dotenv
import os
import http.client, base64, json, urllib
from urllib import request, parse, error

def main():
    global ai_endpoint
    global ai_key

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('Enter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                GetLanguage(userText)


    except Exception as ex:
        print(ex)

def GetLanguage(text):
    try:
        # Construct the JSON request body (a collection of documents, each with an ID and text)
        jsonBody = {
            "documents":[
                {"id": 1,
                 "text": text}
            ]
        }

        # Let's take a look at the JSON we'll send to the service
        print(json.dumps(jsonBody, indent=2))

        # Make an HTTP request to the REST interface
        uri = ai_endpoint.rstrip('/').replace('https://', '')
        conn = http.client.HTTPSConnection(uri)

        # Add the authentication key to the request header
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ai_key
        }

        # Use the Text Analytics language API
        conn.request("POST", "/text/analytics/v3.1/languages?", str(jsonBody).encode('utf-8'), headers)

        # Send the request
        response = conn.getresponse()
        data = response.read().decode("UTF-8")

        # If the call was successful, get the response
        if response.status == 200:

            # Display the JSON response in full (just so we can see it)
            results = json.loads(data)
            print(json.dumps(results, indent=2))

            # Extract the detected language name for each document
            for document in results["documents"]:
                print("\nLanguage:", document["detectedLanguage"]["name"])

        else:
            # Something went wrong, write the whole response
            print(data)

        conn.close()


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()



# using sdk-client 

#.env variables for sdk-client

AI_SERVICE_ENDPOINT="XXXXXXXXXX.cognitive-services"
AI_SERVICE_KEY="XXXXXXXXXXXXXXXXXXX"



# sdk-client.py code

from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    global ai_endpoint
    global ai_key

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('\nEnter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                language = GetLanguage(userText)
                print('Language:', language)

    except Exception as ex:
        print(ex)

def GetLanguage(text):

    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    # Call the service to get the detected language
    detectedLanguage = client.detect_language(documents = [text])[0]
    return detectedLanguage.primary_language.name


if __name__ == "__main__":
    main()
