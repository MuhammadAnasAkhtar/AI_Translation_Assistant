import torch
import gradio as gr
import json
from transformers import pipeline

# Load the translation pipeline
text_translator = pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M",
    torch_dtype=torch.bfloat16
)

# Load the JSON data for language codes
with open('language.json', 'r') as file:
    language_data = json.load(file)

# Get all available languages (excluding duplicates with different scripts)
available_languages = []
seen_languages = set()
for entry in language_data:
    base_language = entry['Language'].split('(')[0].strip()
    if base_language not in seen_languages:
        available_languages.append(base_language)
        seen_languages.add(base_language)

# Sort languages alphabetically
available_languages.sort()

# Function to retrieve FLORES-200 code for a given language
def get_FLORES_code_from_language(language):
    # Try exact match first
    for entry in language_data:
        if entry['Language'].lower() == language.lower():
            return entry['FLORES-200 code']
    # Fallback to matching base language name
    for entry in language_data:
        if entry['Language'].lower().startswith(language.lower()):
            return entry['FLORES-200 code']
    return None

# Translation function
def translate_text(text, destination_language):
    dest_code = get_FLORES_code_from_language(destination_language)
    if dest_code is None:
        return f"Error: Could not find FLORES code for language {destination_language}"
    
    try:
        # Translation call
        translation = text_translator(text, src_lang="eng_Latn", tgt_lang=dest_code)
        return translation[0]["translation_text"]
    except Exception as e:
        return f"Error during translation: {str(e)}"

# Initialize the speech-to-text pipeline (Whisper model)
speech_to_text = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Function to transcribe audio to text
def transcribe_audio(audio_file, destination_language):
    try:
        transcription_result = speech_to_text(audio_file)
        print(f"Transcription result: {transcription_result}")  # Debugging output
        if "text" in transcription_result:
            transcription = transcription_result["text"]
        else:
            return "Error: Unable to transcribe audio."
        
        # Translate the transcribed text
        return translate_text(transcription, destination_language)
    except Exception as e:
        return f"Error during transcription: {str(e)}"

# Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown(
            """
            # 🌐 AI Translation Assistant  
            Translate **text or audio** into your desired language with professional accuracy.  
            """
        )

    with gr.Tabs():
        with gr.Tab("Text Translation"):
            text_input = gr.Textbox(label="Input Text", lines=6, placeholder="Enter your text here...")
            language_dropdown = gr.Dropdown(
                choices=available_languages, label="Select Destination Language"
            )
            translated_text_output = gr.Textbox(label="Translated Text", lines=4)
            translate_button = gr.Button("Translate")

            translate_button.click(
                translate_text, inputs=[text_input, language_dropdown], outputs=[translated_text_output]
            )

        with gr.Tab("Audio Translation"):
            audio_input = gr.Audio(label="Upload Audio File", type="filepath")
            audio_language_dropdown = gr.Dropdown(
                choices=available_languages, label="Select Destination Language"
            )
            audio_translated_text_output = gr.Textbox(label="Transcribed and Translated Text", lines=2)
            audio_translate_button = gr.Button("Transcribe and Translate")

            audio_translate_button.click(
                transcribe_audio,
                inputs=[audio_input, audio_language_dropdown],
                outputs=[audio_translated_text_output],
            )

if __name__ == "__main__":
    demo.launch()
