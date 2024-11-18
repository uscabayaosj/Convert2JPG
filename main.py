import logging
from PIL import Image
import os
import glob

# Attempt to import pdf2image, but don't fail if it's not available
try:
    from pdf2image import convert_from_path
    pdf2image_available = True
except ImportError:
    pdf2image_available = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_webp_to_jpg(input_path, output_path, quality=85):
    """Convert WebP to optimized JPG."""
    try:
        with Image.open(input_path) as img:
            rgb_img = img.convert('RGB')
            rgb_img.save(output_path, 'JPEG', optimize=True, quality=quality)
            logging.info(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        logging.error(f"Error converting WebP to JPG: {str(e)}")

def convert_pdf_to_jpg(input_path, output_path, quality=85):
    """Convert PDF to optimized JPG."""
    if not pdf2image_available:
        logging.error("pdf2image library not installed. Cannot convert PDF files.")
        raise ImportError("pdf2image library is required for PDF conversion")
    
    try:
        # Convert first page of PDF to image
        pages = convert_from_path(input_path, first_page=1, last_page=1)
        if not pages:
            raise ValueError("No pages found in PDF")
        
        # Append .jpg to output path
        output_path = f"{output_path}.jpg"
        pages[0].save(output_path, 'JPEG', optimize=True, quality=quality)
        logging.info(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        logging.error(f"Error converting PDF to JPG: {str(e)}")

def convert_png_to_jpg(input_path, output_path, quality=85):
    """Convert PNG to optimized JPG."""
    try:
        with Image.open(input_path) as img:
            rgb_img = img.convert('RGB')
            rgb_img.save(output_path, 'JPEG', optimize=True, quality=quality)
            logging.info(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        logging.error(f"Error converting PNG to JPG: {str(e)}")

def process_directory(input_dir, output_dir, quality=85):
    """Process all WebP, PDF, and PNG files in the input directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Process WebP files
    for webp_file in glob.glob(os.path.join(input_dir, '*.webp')):
        file_name = os.path.basename(webp_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.jpg")
        convert_webp_to_jpg(webp_file, output_path, quality)
    
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

def run_conversion(input_directory, output_directory, quality=85):
    """Run conversion process for specified directories."""
    if not os.path.exists(input_directory):
        logging.error(f"Input directory does not exist: {input_directory}")
        return

    os.makedirs(output_directory, exist_ok=True)
    process_directory(input_directory, output_directory, quality)
    logging.info("Conversion completed!")

if __name__ == "__main__":
    # For local testing
    input_directory = "/Users/ulyssescabayao/jpgcreator/input_files"
    output_directory = "/Users/ulyssescabayao/jpgcreator/output_files"
    quality = 85  # Adjust this value to change the quality of the output JPGs

    run_conversion(input_directory, output_directory, quality)