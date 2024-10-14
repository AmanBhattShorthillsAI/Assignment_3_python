import os
import json
import pandas as pd  # For saving tables as CSV
from io import BytesIO
from PIL import Image as PILImage
from data_extractor.storage.storage import Storage  # For handling PPTX images

class FileStorage(Storage):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def store(self, data, filename: str, data_type: str):
        """Save data based on type: 'text', 'image', 'url', or 'table'."""
        if data_type == 'text':
            self.save_text(data, filename)
        elif data_type == 'image':
            self.save_images(data, filename)
        elif data_type == 'url':
            self.save_urls(data, filename)
        elif data_type == 'table':
            self.save_tables(data, filename)
        else:
            raise ValueError("Unsupported data type. Use 'text', 'image', 'url', or 'table'.")

    def save_text(self, data, filename: str):
        """Save text data as a .txt file."""
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(self.output_dir, txt_filename)
        with open(output_path, 'w') as f:
            f.write(data)

    def save_images(self, images, filename: str):
        """Save image data to image files and metadata."""
        images_dir = os.path.join(self.output_dir, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        metadata = []
        for idx, image in enumerate(images):
            # Check if the image is a PIL Image object (PPTX case)
            if isinstance(image, PILImage.Image):  
                # Convert the image to bytes (PNG format)
                image_bytes = BytesIO()
                image.save(image_bytes, format='PNG')  # Save as PNG
                image_bytes = image_bytes.getvalue()
                image_filename = f"image_{idx + 1}.png"
                image_ext = 'png'
            # Otherwise, assume it's a dictionary (PDF/DOCX case)
            elif isinstance(image, dict):
                # Check if it's a dictionary and has the necessary keys
                image_filename = f"image_{idx + 1}.{image.get('ext', 'jpg')}"
                image_bytes = image.get('image_data', b"")
                image_ext = image.get('ext', 'jpg')  # noqa: F841
            else:
                # If the image is neither a PIL Image nor a dictionary, skip it
                continue

            # Save the image data to file
            image_path = os.path.join(images_dir, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            metadata.append({
                "file_name": image_filename,
                "page_number": image.get("page", "N/A"),
                "dimensions": image.get("dimensions", "N/A")
            })

        metadata_file = os.path.join(images_dir, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)

    def save_urls(self, urls, filename: str):
        urls_dir = os.path.join(self.output_dir, "urls")
        if not os.path.exists(urls_dir):
            os.makedirs(urls_dir)

        url_filename = os.path.join(urls_dir, "urls.txt")
        metadata = []

        with open(url_filename, "w") as url_file:
            for url_info in urls:
                url_file.write(f"{url_info['url']}\n")
                metadata.append({
                    "linked_text": url_info["linked_text"],
                    "url": url_info["url"],
                    "page_number": url_info["page_number"]
                })

        metadata_file = os.path.join(urls_dir, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)

    def save_tables(self, tables, filename: str):
        """Save extracted tables as CSV files and generate metadata."""
        tables_dir = os.path.join(self.output_dir, "tables")
        if not os.path.exists(tables_dir):
            os.makedirs(tables_dir)

        metadata = []
        for idx, table in enumerate(tables):
            csv_filename = f"table_{idx + 1}.csv"
            csv_path = os.path.join(tables_dir, csv_filename)
            
            # Save table data to CSV file
            if isinstance(table, pd.DataFrame):
                table.to_csv(csv_path, index=False)
            elif isinstance(table, list):
                with open(csv_path, 'w', newline='') as f:
                    for row in table:
                        f.write(",".join(row) + "\n")
            
            # Add metadata for the current table
            metadata.append({
                "table_filename": csv_filename,
                "row_count": len(table) if isinstance(table, list) else table.shape[0],
                "column_count": len(table[0]) if isinstance(table, list) and table else table.shape[1]
            })

        # Save the metadata for all tables in a JSON file
        metadata_file = os.path.join(tables_dir, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
                        
    def close(self):
        pass

