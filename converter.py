from pathlib import Path
from faster_whisper import WhisperModel
import argparse
import os

def get_in_minutes(sec):
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    seconds = int(sec % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def transcribe_video(file_path, output_directory, model_size="large-v3", language="pt"):
    # Run on GPU with FP16
    #model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")
    try:
        with open(file_path, 'rb') as file:
            file_path = Path(file_path)
            model = WhisperModel(model_size, device="cpu", compute_type="int8")

            output_file_path = Path(output_directory) / f"{file_path.stem}_output.txt"

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                segments, info = model.transcribe(
                    file, beam_size=5, language=language, best_of=2, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=2000))

                print(f"Detected language '{info.language}' with probability {info.language_probability}\n")

                for segment in segments:
                    output_file.write("[%s -> %s] %s \n" % (get_in_minutes(segment.start),
                                                            get_in_minutes(segment.end), segment.text))
                    print("[%s -> %s] %s \n" % (get_in_minutes(segment.start),
                                                get_in_minutes(segment.end), segment.text))

    except Exception as e:
        print(f"Ocorreu um erro ao transcrever o vídeo: {e}")

def main():
    parser = argparse.ArgumentParser(description="Transcreve um vídeo usando o modelo Whisper")
    parser.add_argument("file_path", help="Caminho para o vídeo")
    parser.add_argument("-o", "--output_directory", help="Caminho para o diretório de saída (opcional)")
    parser.add_argument("-m", "--model_size", default="large-v2", help="Tamanho do modelo (padrão: large-v2)")
    parser.add_argument("-l", "--language", default="pt", help="Idioma do vídeo (padrão: pt)")

    args = parser.parse_args()
    file_path = args.file_path
    output_directory = args.output_directory

    if not output_directory:
        output_directory = "./transcriptions"  # Diretório padrão se não especificado

    if not os.path.exists(file_path):
        print(f"O arquivo '{file_path}' não foi encontrado.")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # Cria o diretório de saída se não existir

    transcribe_video(file_path, output_directory, args.model_size, args.language)

if __name__ == "__main__":
    main()
