import argparse
import re
import os

try:
    from docx import Document
except ImportError:
    print("Biblioteca 'python-docx' não encontrada. Instalando...")
    os.system("pip install python-docx")
    from docx import Document


def identify_abbreviations(file_path):
    abbreviations = set()

    try:
        # Abra o arquivo .docx
        doc = Document(file_path)

        for paragraph in doc.paragraphs:
            text = paragraph.text

            # Use uma expressão regular mais específica para encontrar as siglas no formato "significado (SIGLA)"
            matches = re.findall(r'([^(),:;"\'\.\d]+)\s*\(([A-Z]+)\)', text)

            for match in matches:
                meaning = match[0].strip()
                abbreviation = match[1].strip()
                abbreviations.add((abbreviation, meaning))

    except Exception as e:
        print(f"Ocorreu um erro ao abrir o arquivo: {e}")
        return None

    return abbreviations


def save_abbreviations_to_file(abbreviations):
    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define o caminho completo para o arquivo "siglas.txt" no mesmo diretório do script
    output_file = os.path.join(script_dir, 'siglas.txt')

    # Escreve as abreviações no arquivo
    with open(output_file, 'w', encoding='utf-8') as file:
        for abbreviation, meaning in abbreviations:
            file.write(f"{abbreviation}: {meaning}\n")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Identificar abreviações em um arquivo .docx e salvar em um arquivo de saída")
    parser.add_argument("file_path", help="Caminho para o arquivo .docx")
    parser.add_argument("-o", "--output_file", help="Caminho para o arquivo de saída (txt) onde as siglas serão salvas")
    return parser.parse_args()


def main():
    args = parse_arguments()
    file_path = args.file_path

    abbreviations = identify_abbreviations(file_path)

    if abbreviations:
        for abbreviation, meaning in abbreviations:
            print(f"{abbreviation}: {meaning}")

        save_abbreviations_to_file(abbreviations)

    else:
        print("Nenhuma abreviação encontrada no arquivo.")


if __name__ == "__main__":
    main()
