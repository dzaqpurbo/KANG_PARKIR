!pip install -q -U google-generativeai

import google.generativeai as genai
from IPython.display import Markdown

from google.colab import userdata
GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

!pip install python-dotenv

import google.generativeai as genai
from google.colab import userdata
import PIL.Image
from datetime import datetime
import json

api_key = userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

file = PIL.Image.open("mobil.jpg")

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
prompt = [
    file,
    f"You are a parking gate that receives picture input and recognizes the plate number. Recognize the plate number from the input picture and generate the output in the following JSON format: {{'plat_no': '<plate_number>', 'vehicle': '<vehicle_type>', 'vehicle_type': '<specific_vehicle_type>', 'color': '<color>', 'gate_open': '{current_time}', 'gate_closed': 'N/A'}}"
]

try:
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    cleaned_response = response.text.strip("```json").strip("```").strip()
    valid_json_text = cleaned_response.replace("'", '"')

    json_data = json.loads(valid_json_text)

    formatted_json = json.dumps(json_data, indent=4)
    print(formatted_json)

    output_filename = "KANG_PARKIR.json"
    with open(output_filename, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"JSON output saved to {output_filename}")

except json.JSONDecodeError as json_error:
    print(f"JSON Decode Error: {json_error}")
    print("Response text might not be in valid JSON format.")
except Exception as e:
    print(f"Error: {e}")
