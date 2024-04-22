import tkinter as tk
from tkinter import Text, filedialog, scrolledtext, messagebox
from mindee import Client, PredictResponse, product
import os
from PIL import Image
import re
import subprocess  # For opening file explorer

# Global variables
image_folder_path = None
image_paths = []
image_index = 0
output_folder_path = "output"  # Folder to save the images with invoice numbers

def select_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    if output_folder_path:
        output_folder_label.config(text=f"Output Folder: {output_folder_path}")

def select_folder():
    global image_folder_path, image_paths
    # Prompt user to select a folder containing images
    image_folder_path = filedialog.askdirectory()
    if image_folder_path:
        # Get a list of image files in the selected folder
        image_paths = [os.path.join(image_folder_path, file) for file in os.listdir(image_folder_path) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # Display the list of image names
        display_image_names()

def display_image_names():
    # Clear previous content in the scrolled text widget
    image_list_text.delete(1.0, tk.END)
    # Display image names in the scrolled text widget
    for img_path in image_paths:
        image_list_text.insert(tk.END, os.path.basename(img_path) + "\n")

def extract_text_and_display():
    global image_index
    try:
        # Initialize Mindee client
        mindee_client = Client(api_key="2d7fd6d2118262d2a5d674448ad17930")
        
        if image_index < len(image_paths):
            # Extract text from the current image
            input_doc = mindee_client.source_from_path(image_paths[image_index])
            result: PredictResponse = mindee_client.parse(product.InvoiceV4, input_doc)
            extracted_text = str(result.document)

            # Display extracted text in the prediction textbox
            prediction_text = ""
            invoice_number_found = False
            for line in extracted_text.split("\n"):
                if line.startswith(":Invoice Number:") and not invoice_number_found:
                    prediction_text += line + "\n"
                    invoice_number_found = True

            prediction_box.delete(1.0, tk.END)  # Clear previous content
            prediction_box.insert(tk.END, prediction_text)

            if invoice_number_found:
                save_image_with_invoice_number(image_paths[image_index], extracted_text)

            image_index += 1
            if image_index < len(image_paths):
                # Schedule the next extraction after 1 second
                root.after(1000, extract_text_and_display)
        else:
            messagebox.showinfo("Extraction Complete", "Text extracted from all images!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def save_image_with_invoice_number(image_path, extracted_text):
    # Extract invoice number from the extracted text
    invoice_number = None
    for line in extracted_text.split("\n"):
        if line.startswith(":Invoice Number:"):
            invoice_number = line.split(":Invoice Number:")[1].strip()
            break

    if invoice_number:
        # Sanitize the invoice number to remove invalid characters
        sanitized_invoice_number = re.sub(r'[\\/*?:"<>|]', '_', invoice_number)

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Open the image
        image = Image.open(image_path)

        # Create the filename for the PDF using the sanitized invoice number
        filename = f"{sanitized_invoice_number}.pdf"
        output_path = os.path.join(output_folder_path, filename)

        # Save the image as PDF
        image.save(output_path, "PDF")

# Create the main window
root = tk.Tk()
root.title("Text Extraction GUI")

# Create a label
label = tk.Label(root, text="Select a folder containing images and click the button to extract text from them.", font=("Helvetica", 12))
label.pack(pady=20)

# Create a button to select the folder
folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.pack(pady=5)

# Create a button to select the output folder
output_folder_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
output_folder_button.pack(pady=5)

# Label to display the selected output folder
output_folder_label = tk.Label(root, text="")
output_folder_label.pack(pady=5)

# Create a scrolled text widget to display image names
image_list_text = scrolledtext.ScrolledText(root, height=10, width=50)
image_list_text.pack(pady=10)

# Create a button to trigger text extraction
button = tk.Button(root, text="Extract Text", command=extract_text_and_display)
button.pack(pady=10)

# Create a textbox to display prediction (invoice number and purchase date)
prediction_box = Text(root, height=10, width=80)
prediction_box.pack(pady=10)

# Run the GUI
root.mainloop()
