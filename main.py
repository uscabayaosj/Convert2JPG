import logging
from google.cloud import tasks_v2
from google.protobuf import duration_pb2
import os
from PIL import Image
import glob

# Attempt to import pdf2image, but don't fail if it's not available
try:
    from pdf2image import convert_from_path
    pdf2image_available = True
except ImportError:
    pdf2image_available = False

def convert_webp_to_jpg(input_path, output_path, quality=85):
    """Convert WebP to optimized JPG."""
    with Image.open(input_path) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(output_path, 'JPEG', optimize=True, quality=quality)

def convert_pdf_to_jpg(input_path, output_path, quality=85):
    """Convert PDF to optimized JPG."""
    if not pdf2image_available:
        print(f"Skipping PDF conversion for {input_path}. pdf2image library not available.")
        return
    try:
        pages = convert_from_path(input_path, 300)
        for i, page in enumerate(pages):
            page.save(f"{output_path}_{i+1}.jpg", 'JPEG', optimize=True, quality=quality)
        print(f"Converted {input_path} to JPG")
    except Exception as e:
        print(f"Error converting PDF {input_path}: {str(e)}")

def convert_png_to_jpg(input_path, output_path, quality=85):
    """Convert PNG to optimized JPG."""
    with Image.open(input_path) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(output_path, 'JPEG', optimize=True, quality=quality)

def process_directory(input_dir, output_dir, quality=85):
    """Process all WebP, PDF, and PNG files in the input directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Process WebP files
    for webp_file in glob.glob(os.path.join(input_dir, '*.webp')):
        file_name = os.path.basename(webp_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.jpg")
        convert_webp_to_jpg(webp_file, output_path, quality)
        print(f"Converted {file_name} to JPG")
    
    # Process PDF files
    for pdf_file in glob.glob(os.path.join(input_dir, '*.pdf')):
        file_name = os.path.basename(pdf_file)
        output_path = os.path.join(output_dir, os.path.splitext(file_name)[0])
        convert_pdf_to_jpg(pdf_file, output_path, quality)

    # Process PNG files
    for png_file in glob.glob(os.path.join(input_dir, '*.png')):
        file_name = os.path.basename(png_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.jpg")
        convert_png_to_jpg(png_file, output_path, quality)
        print(f"Converted {file_name} to JPG")

def run_conversion():
    input_directory = "/tmp/input_files"  # Use a writable directory in App Engine
    output_directory = "/tmp/output_files"
    quality = 85  # Adjust this value to change the quality of the output JPGs

    process_directory(input_directory, output_directory, quality)
    logging.info("Conversion completed!")

if __name__ == "__main__":
    # For local testing
    input_directory = "/Users/ulyssescabayao/jpgcreator/input_files"
    output_directory = "output_files"
    quality = 85  # Adjust this value to change the quality of the output JPGs

    # Uncomment for local testing
    # process_directory(input_directory, output_directory, quality)

    run_conversion()