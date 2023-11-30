import argparse
import base64
import mimetypes
import os


def convert_image_to_base64(image_path, mime_type=None):
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        if not mime_type:
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                raise ValueError("Não foi possível determinar o tipo MIME da imagem.")

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{image_base64}"
    except Exception as e:
        print(f"Ocorreu um erro ao converter a imagem para base64: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Converte uma imagem para base64")
    parser.add_argument("image_path", help="Caminho para a imagem")
    parser.add_argument("-t", "--mime_type", help="Tipo MIME da imagem (opcional)")

    args = parser.parse_args()
    image_path = args.image_path
    mime_type = args.mime_type

    if not os.path.exists(image_path):
        print("O arquivo da imagem não existe.")
        return

    image_base64 = convert_image_to_base64(image_path, mime_type)

    if image_base64:
        print(image_base64)


if __name__ == "__main__":
    main()
