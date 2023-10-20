import pypdfium2 as pdfium
from pytesseract import image_to_string
from io import BytesIO
from PIL import Image
import multiprocessing

def pdf2img(file_path,scale=300/72):
   pdf_file = pdfium.PdfDocument(file_path)
   pages_indices = [i for i in range(len(pdf_file))]
   renderer = pdf_file.render(
      pdfium.PdfBitmap.to_pil,
      page_indices=pages_indices,
      scale=scale
   )

   final_image = []
   for i,image in zip(pages_indices,renderer):
      
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        final_image.append(dict({i:image_byte_array}))
    
   return final_image

def img2str(list_dict_final_images):
    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []
    for index,image_bytes in enumerate(image_list):
        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)
    
    return '\n'.join(image_content)

def main():
    path= r'c:\Users\saish\Downloads\Resume_v3.pdf'
    f = pdf2img(path)
    print(img2str(f))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
    