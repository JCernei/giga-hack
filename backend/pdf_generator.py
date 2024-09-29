
import json
import os
import time
import textwrap
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


INVOICE_FOLDER = './invoices'

def clean_text(value):
    """Helper function to clean text for PDF output."""
    if isinstance(value, str):
        return value.strip()
    return str(value)


def clean_json_string(json_string):
    cleaned_string = json_string.replace('\"', '"')  
    cleaned_string = cleaned_string.replace("\n", "") 
    cleaned_string = cleaned_string.replace("\t", "")
    cleaned_string = cleaned_string.replace("ă", "a") 
    cleaned_string = cleaned_string.replace("î", "i")
    cleaned_string = cleaned_string.replace("â", "a")
    cleaned_string = cleaned_string.replace("ș", "s")
    cleaned_string = cleaned_string.replace("ț", "t")
    cleaned_string = cleaned_string.replace("Ă", "A")
    cleaned_string = cleaned_string.replace("Î", "I")
    cleaned_string = cleaned_string.replace("Â", "A")
    cleaned_string = cleaned_string.replace("Ș", "S")
    cleaned_string = cleaned_string.replace("Ț", "T")
    return cleaned_string


def generate_invoice_from_text(processed_data, original_filename):
    # Create a unique invoice filename based on timestamp and original filename
    timestamp = int(time.time())
    invoice_filename = f'invoice_{timestamp}_{original_filename}.pdf'
    invoice_path = os.path.join(INVOICE_FOLDER, invoice_filename)

    # Create a new PDF using ReportLab
    c = canvas.Canvas(invoice_path, pagesize=A4)
    page_width, page_height = A4

    # Set title
    c.setFont("Courier", 16)
    c.drawString(100, 800, "Invoice")
    c.setFont("Courier", 12)
    c.drawString(100, 780, f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    y = 750  # Initial Y position for text
    line_height = 14  # Line height (spacing between lines)
    left_margin = 100  # Left margin for text
    max_line_width = 170 * mm  # Max width for text area

    # Parse the JSON strings into dictionaries
    try:
        invoice_info = json.loads(clean_json_string(processed_data['invoice_information']))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

    def draw_wrapped_text(text, x, y, max_width, font_size=10):
        c.setFont("Courier", font_size)
        # Wrap text based on max width and font size
        lines = textwrap.wrap(text, width=int(max_width / (font_size * 0.6)))  # Approx chars per line
        for line in lines:
            if y < 40:  # Check if the text goes beyond the bottom margin
                c.showPage()  # Create a new page if needed
                y = 800  # Reset the y position
                c.setFont("Courier", font_size)  # Reset the font for the new page
            c.drawString(x, y, line)
            y -= line_height  # Move to the next line
        return y

    def draw_section_title(title, x, y):
        c.setFont("Times-Bold", 12)
        c.drawString(x, y, title)
        return y - line_height

    def draw_key_value(key, value, x, y, indent=0):
        if not value:
            value = "-"
        text = f"{key}: {value}"
        return draw_wrapped_text(text, x + indent, y, max_line_width)

    # Start populating the invoice info
    y = draw_section_title("Invoice Details", left_margin, y)
    
    y = draw_key_value("Invoice Number", invoice_info.get("invoice_number", ""), left_margin, y)
    y = draw_key_value("Invoice Date", invoice_info.get("invoice_date", ""), left_margin, y)
    y = draw_key_value("Due Date", invoice_info.get("due_date", ""), left_margin, y)
    
    # Billing Information
    y = draw_section_title("Bill To", left_margin, y)
    bill_to = invoice_info.get("bill_to", {})
    y = draw_key_value("Client Name", bill_to.get("client_name", ""), left_margin, y)
    y = draw_key_value("Company Name", bill_to.get("company_name", ""), left_margin, y)
    y = draw_key_value("Address", bill_to.get("address", ""), left_margin, y)

    y = draw_section_title("Contact Information", left_margin, y)
    contact_info_to = bill_to.get("contact_information", {})
    y = draw_key_value("Email", contact_info_to.get("email", ""), left_margin, y, indent=10)
    y = draw_key_value("Phone", contact_info_to.get("phone", ""), left_margin, y, indent=10)

    y = draw_section_title("Banking Information", left_margin, y)
    banking_info_to = bill_to.get("banking_information", {})
    y = draw_key_value("Bank Name", banking_info_to.get("bank_name", ""), left_margin, y, indent=10)
    y = draw_key_value("Account Name", banking_info_to.get("account_name", ""), left_margin, y, indent=10)
    y = draw_key_value("IBAN", banking_info_to.get("iban", ""), left_margin, y, indent=10)
    y = draw_key_value("SWIFT/BIC", banking_info_to.get("swift_bic", ""), left_margin, y, indent=10)

    # Bill From Information
    y = draw_section_title("Bill From", left_margin, y)
    bill_from = invoice_info.get("bill_from", {})
    y = draw_key_value("Provider Name", bill_from.get("provider_name", ""), left_margin, y)
    y = draw_key_value("Company Name", bill_from.get("company_name", ""), left_margin, y)
    y = draw_key_value("Address", bill_from.get("address", ""), left_margin, y)

    y = draw_section_title("Contact Information", left_margin, y)
    contact_info_from = bill_from.get("contact_information", {})
    y = draw_key_value("Email", contact_info_from.get("email", ""), left_margin, y, indent=10)
    y = draw_key_value("Phone", contact_info_from.get("phone", ""), left_margin, y, indent=10)

    y = draw_section_title("Banking Information", left_margin, y)
    banking_info_from = bill_from.get("banking_information", {})
    y = draw_key_value("Bank Name", banking_info_from.get("bank_name", ""), left_margin, y, indent=10)
    y = draw_key_value("Account Name", banking_info_from.get("account_name", ""), left_margin, y, indent=10)
    y = draw_key_value("IBAN", banking_info_from.get("iban", ""), left_margin, y, indent=10)
    y = draw_key_value("SWIFT/BIC", banking_info_from.get("swift_bic", ""), left_margin, y, indent=10)

    # Payment Terms
    y = draw_section_title("Payment Terms", left_margin, y)
    y = draw_key_value("Terms", invoice_info.get("payment_terms", ""), left_margin, y)

    # Save the PDF
    c.save()

    return invoice_path


def generate_invoice_json(processed_data):
    try:
        invoice_info = json.loads(clean_json_string(processed_data['invoice_information']))
        service_details = json.loads(clean_json_string(processed_data['service_details']))
        calculation_details = json.loads(clean_json_string(processed_data['calculation_details']))
        payment_instructions = json.loads(clean_json_string(processed_data['payment_instructions']))
        special_conditions = json.loads(clean_json_string(processed_data['special_conditions']))
        customer_info = json.loads(clean_json_string(processed_data['customer_information']))
        additional_info = json.loads(clean_json_string(processed_data['additional_information']))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

    invoice_json = {
        "invoice_information": {
            "invoice_number": invoice_info.get("invoice_number", "N/A"),
            "invoice_date": invoice_info.get("invoice_date", "N/A"),
            "due_date": invoice_info.get("due_date", "N/A"),
            "bill_to": {
                "client_name": invoice_info.get("bill_to", {}).get("client_name", "N/A"),
                "company_name": invoice_info.get("bill_to", {}).get("company_name", "N/A"),
                "address": invoice_info.get("bill_to", {}).get("address", "N/A"),
                "contact_information": {
                    "email": invoice_info.get("bill_to", {}).get("contact_information", {}).get("email", "N/A"),
                    "phone": invoice_info.get("bill_to", {}).get("contact_information", {}).get("phone", "N/A"),
                },
                "banking_information": {
                    "bank_name": invoice_info.get("bill_to", {}).get("banking_information", {}).get("bank_name", "N/A"),
                    "account_name": invoice_info.get("bill_to", {}).get("banking_information", {}).get("account_name", "N/A"),
                    "iban": invoice_info.get("bill_to", {}).get("banking_information", {}).get("iban", "N/A"),
                    "swift_bic": invoice_info.get("bill_to", {}).get("banking_information", {}).get("swift_bic", "N/A"),
                }
            },
            "bill_from": {
                "provider_name": invoice_info.get("bill_from", {}).get("provider_name", "N/A"),
                "company_name": invoice_info.get("bill_from", {}).get("company_name", "N/A"),
                "address": invoice_info.get("bill_from", {}).get("address", "N/A"),
                "contact_information": {
                    "email": invoice_info.get("bill_from", {}).get("contact_information", {}).get("email", "N/A"),
                    "phone": invoice_info.get("bill_from", {}).get("contact_information", {}).get("phone", "N/A"),
                },
                "banking_information": {
                    "bank_name": invoice_info.get("bill_from", {}).get("banking_information", {}).get("bank_name", "N/A"),
                    "account_name": invoice_info.get("bill_from", {}).get("banking_information", {}).get("account_name", "N/A"),
                    "iban": invoice_info.get("bill_from", {}).get("banking_information", {}).get("iban", "N/A"),
                    "swift_bic": invoice_info.get("bill_from", {}).get("banking_information", {}).get("swift_bic", "N/A"),
                }
            },
        },
        "service_details": service_details.get('service_details', []),
        "calculation_details": calculation_details,
        "payment_instructions": payment_instructions,
        "special_conditions": special_conditions,
        "customer_information": customer_info,
        "additional_information": additional_info,
    }
    return invoice_json


def generate_invoice_from_json(invoice_json, original_filename):
    # Create a unique invoice filename based on timestamp and original filename
    timestamp = int(time.time())
    invoice_filename = f'invoice_{timestamp}_{original_filename}.pdf'
    invoice_path = os.path.join(INVOICE_FOLDER, invoice_filename)

    # Create a new PDF using ReportLab
    c = canvas.Canvas(invoice_path, pagesize=A4)
    page_width, page_height = A4

    # Set some margins
    left_margin = 20 * mm
    right_margin = 20 * mm
    top_margin = 30 * mm
    bottom_margin = 20 * mm
    max_width = page_width - left_margin - right_margin

    # Set title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_margin, page_height - top_margin, "Invoice")

    # Add Date
    c.setFont("Helvetica", 12)
    c.drawString(left_margin, page_height - top_margin - 20, f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    y = page_height - top_margin - 50  # Initial Y position for text
    line_height = 14  # Line height (spacing between lines)

    # Helper to wrap and draw text
    def draw_wrapped_text(canvas, text, x, y, width, line_height):
        wrapped_lines = textwrap.wrap(text, width=80)
        for line in wrapped_lines:
            if y < bottom_margin:  # If we're running out of space, create a new page
                canvas.showPage()
                y = page_height - top_margin  # Reset Y position for new page
            canvas.drawString(x, y, line)
            y -= line_height
        return y

    # Helper to draw section headers
    def draw_section_header(canvas, text, x, y):
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(x, y, text)
        return y - line_height

    # Draw Invoice Information
    invoice_info = invoice_json["invoice_information"]
    y = draw_section_header(c, "Invoice Information", left_margin, y)
    invoice_text = f"Invoice Number: {invoice_info['invoice_number']}\nInvoice Date: {invoice_info['invoice_date']}\nDue Date: {invoice_info['due_date']}"
    y = draw_wrapped_text(c, invoice_text, left_margin, y, max_width, line_height)

    # Draw Bill To and Bill From
    y = draw_section_header(c, "Bill To", left_margin, y)
    bill_to_info = invoice_info['bill_to']
    bill_to_text = f"Client Name: {bill_to_info['client_name']}\nCompany Name: {bill_to_info['company_name']}\nAddress: {bill_to_info['address']}\nEmail: {bill_to_info['contact_information']['email']}\nPhone: {bill_to_info['contact_information']['phone']}"
    y = draw_wrapped_text(c, bill_to_text, left_margin, y, max_width, line_height)

    y = draw_section_header(c, "Bill From", left_margin, y)
    bill_from_info = invoice_info['bill_from']
    bill_from_text = f"Provider Name: {bill_from_info['provider_name']}\nCompany Name: {bill_from_info['company_name']}\nAddress: {bill_from_info['address']}\nEmail: {bill_from_info['contact_information']['email']}\nPhone: {bill_from_info['contact_information']['phone']}"
    y = draw_wrapped_text(c, bill_from_text, left_margin, y, max_width, line_height)

    # Draw Service Details
    y = draw_section_header(c, "Service Details", left_margin, y)
    for service in invoice_json["service_details"]:
        service_text = f"Service: {service['description']} - Amount: {service['total_amount']}"
        y = draw_wrapped_text(c, service_text, left_margin, y, max_width, line_height)

    # Draw Calculation Details
    y = draw_section_header(c, "Calculation Details", left_margin, y)
    for key, value in invoice_json["calculation_details"].items():
        calc_text = f"{key}: {value}"
        y = draw_wrapped_text(c, calc_text, left_margin, y, max_width, line_height)

    # Draw Payment Instructions
    y = draw_section_header(c, "Payment Instructions", left_margin, y)
    for key, value in invoice_json["payment_instructions"].items():
        payment_text = f"{key}: {value}"
        y = draw_wrapped_text(c, payment_text, left_margin, y, max_width, line_height)

    # Draw Special Conditions
    y = draw_section_header(c, "Special Conditions", left_margin, y)
    for key, value in invoice_json["special_conditions"].items():
        conditions_text = f"{key}: {value}"
        y = draw_wrapped_text(c, conditions_text, left_margin, y, max_width, line_height)

    # Draw Customer Information
    y = draw_section_header(c, "Customer Information", left_margin, y)
    for key, value in invoice_json["customer_information"].items():
        customer_text = f"{key}: {value}"
        y = draw_wrapped_text(c, customer_text, left_margin, y, max_width, line_height)

    # Draw Additional Information
    y = draw_section_header(c, "Additional Information", left_margin, y)
    for key, value in invoice_json["additional_information"].items():
        additional_text = f"{key}: {value}"
        y = draw_wrapped_text(c, additional_text, left_margin, y, max_width, line_height)

    # Add a footer with page number
    c.setFont("Helvetica", 10)
    c.drawString(left_margin, bottom_margin - 10, f"Page 1")

    # Save PDF
    c.save()

    return invoice_path
