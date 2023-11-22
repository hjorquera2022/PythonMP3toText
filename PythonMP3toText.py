import os
from pydub import AudioSegment
import librosa
import speech_recognition as sr

def extract_voice_from_mp3(mp3_file):
    # Cargar el archivo MP3 utilizando pydub y convertirlo a formato WAV
    #audio = AudioSegment.from_mp3(mp3_file)

    # Esto especificará explícitamente el códec de audio y los parámetros al cargar el archivo 
    # audio = AudioSegment.from_mp3(mp3_file, codec="mp3", parameters=["-acodec", "mp3", "-ar", "16000"]).set_frame_rate(16000).set_channels(1)
    audio = AudioSegment.from_mp3(mp3_file).set_frame_rate(16000).set_channels(1)

    wav_file = "temp.wav"
    audio.export(wav_file, format="wav")

    # Cargar el archivo WAV utilizando librosa
    audio, sr = librosa.load(wav_file)

    # Extraer características del audio utilizando librosa
    audio_features = librosa.feature.mfcc(audio, sr)

    # Convertir las características de audio en un archivo de texto utilizando SpeechRecognition
    recognizer = sr.Recognizer()
    audio_text = ""
    
    for feature in audio_features.T:
        # Convertir las características en una cadena de audio utilizando librosa
        audio_segment = librosa.feature.inverse.mfcc(feature)
        
        # Guardar el segmento de audio en un archivo temporal
        librosa.output.write_wav('temp.wav', audio_segment, sr)
        
        # Utilizar SpeechRecognition para transcribir el audio
        with sr.AudioFile('temp.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-ES")
            audio_text += text + " "

    # Eliminar el archivo temporal
    os.remove('temp.wav')
    
    return audio_text

# Ruta del archivo MP3 de entrada
mp3_file = "C:\\temp\\MUSICATXT\\archivo.mp3"

# Extraer la voz humana y generar el archivo de texto
extracted_text = extract_voice_from_mp3(mp3_file)
print(extracted_text)
