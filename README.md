# Automated Invoice Management API

This API is designed to automate the process of invoice management. It provides functionalities to manage invoices, customers, and products.

## Setting up Mindee API Trial Version

To use the automated data extraction feature for invoices, you need to sign up for a trial version of Mindee API. Follow the steps below to create a Mindee API trial version:

1. Go to the [Mindee website](https://www.mindee.com/) and sign up for an account.
2. Once you're signed in, navigate to the [Mindee API Dashboard](https://my.mindee.net/api/dashboard).
3. Click on "New API Key" to generate a new API key.
4. Copy the API key generated. You'll need this API key to authenticate your requests.

## How to Use

### Input Folder

The input folder is where you should place the images of invoices that you want to process. Follow the steps below to use the input folder:

1. Create a folder named `input` in the root directory of the project.
2. Place the images of the invoices that you want to process inside the `input` folder.

### Output Folder

The output folder is where the processed invoices will be saved after extraction. Follow the steps below to specify the output folder:

1. Create a folder named `output` in the root directory of the project.
2. After processing, the extracted data will be saved as JSON files in the `output` folder.

## Running the API

To run the API, follow these steps:

1. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt


**1. Set up the Mindee API key in the .env file:**
plaintext
Copy code
MINDEE_API_KEY=your_mindee_api_key_here
Start the Flask server by running the following command:
bash
Copy code
python app.py
The API will start running at http://localhost:5000.

**2. API Endpoints**
POST /invoices/upload - Upload an invoice image for data extraction.
GET /invoices/{invoice_id} - Get the extracted data for a specific invoice.
GET /invoices - Get a list of all processed invoices.
Sample Usage
Uploading an Invoice Image
bash
Copy code
curl -X POST -F "invoice_image=@/path/to/your/invoice.jpg" http://localhost:5000/invoices/upload
Getting Extracted Data for a Specific Invoice
bash
Copy code
curl http://localhost:5000/invoices/{invoice_id}
Getting a List of All Processed Invoices
bash
Copy code
curl http://localhost:5000/invoices
css
Copy code

This should give users a clear idea of how to set up the Mindee API trial version and how to use the input and output folders. Let me know if you need further assistance!
