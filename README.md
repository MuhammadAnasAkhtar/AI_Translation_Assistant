# AI_Translation_Assistant

This is an AI-powered translation assistant that allows you to translate text or audio into your desired language with professional accuracy. The application leverages Hugging Face's models to provide translation services in multiple languages.

# Key Features:
Text Translation: Input text and select a target language for translation.
Audio Translation: Upload an audio file, and the app will transcribe the speech and translate it into the selected language.
Multilingual Support: Supports many languages, with automatic language detection and translation via FLORES-200 codes.
# Requirements
The following libraries are required to run this application:

torch: PyTorch library for model inference.
gradio: To build the user interface and handle user input.
transformers: For loading pre-trained models like the translation and speech-to-text models.
json: For parsing language codes from a JSON file.
# How to Use
Launch the Application: Run the script, and the Gradio web interface will open automatically. If it doesn't, follow the link provided in the terminal output.

Text Translation:

Input your text in the "Input Text" field.
Select the language you want to translate to from the "Select Destination Language" dropdown.
Click Translate, and the translated text will appear in the output box.
Audio Translation:

Upload an audio file using the Upload Audio File button.
Select the language you want to translate the transcribed audio to.
Click Transcribe and Translate to transcribe and translate the audio.
# Explanation of Code
Translation Pipeline: The app uses Hugging Face's facebook/nllb-200-distilled-600M model for translation. This model supports a wide variety of languages and is configured to use the FLORES-200 language codes.

Language Handling:

The available languages are stored in the language.json file, which includes language names and their corresponding FLORES-200 code.
The code extracts unique language names and sorts them alphabetically, removing duplicate entries with different scripts.
Speech-to-Text: The app uses the openai/whisper-small model to transcribe the audio into text. Once transcribed, the text is passed to the translation pipeline to generate the translated output.

# Gradio Interface:

The user interface is built using Gradio's Blocks and Tabs components.
There are two tabs: one for text translation and one for audio translation. Each tab has its own input fields and output boxes.
# Example
Text Translation:
Input: "Hello, how are you?"
Selected Language: Spanish
Output: "Hola, ¿cómo estás?"
Audio Translation:
Input: An uploaded audio file of someone speaking English.
Selected Language: French
Output: The transcribed and translated text of the audio in French.
# Error Handling
If an invalid language is selected or if the language code cannot be found in the JSON data, the app will return an error message: Error: Could not find FLORES code for language [language_name].
If the audio cannot be transcribed, the app will display: Error: Unable to transcribe audio..
Any issues during the translation or transcription process will be caught and displayed as error messages.
# Future Improvements
Speech Recognition Enhancement: Improve accuracy by using larger Whisper models for better transcription quality.
Batch Translation: Allow users to translate multiple texts or audio files in one go.
Extended Language Support: Add support for more languages by improving the language.json file.
Customizable Models: Allow users to upload their own models for translation or transcription.
# License
This project is licensed under the MIT License - see the LICENSE file for details.
