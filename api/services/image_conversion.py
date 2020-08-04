import img2pdf
from PIL import Image


class ImageConversionService:
    def convert(self, img_path, pdf_path):

        image = Image.open(img_path)
        pdf_bytes = img2pdf.convert(image.filename)

        with open(pdf_path, "wb") as pdf_file:

            pdf_file.write(pdf_bytes)
            image.close()
