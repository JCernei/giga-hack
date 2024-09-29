import ollama

ml_model = 'llama3.1'

# Function to call the main prompt
def set_main_prompt():
    return """
Analyze the following contract and extract the following information categorized into the specified sections. Do not translate the fields or terms—retain them in the original language of the contract. If any important information that doesn’t fit into these categories is detected, create a new category and add it accordingly:

1. Contract Information:
Contract Dates: What are the start and end dates of the contract (e.g., contract period from [start date] to [end date])?
Service Periods: What are the specific periods for service delivery or recurring services?
Referenced Contracts or Agreements: Are there any contract numbers, annexes, or additional agreements referenced?

2. Billing and Payment Terms:
Billing Rates: What are the daily, monthly, or other specified billing rates? Include details on total contract value, if applicable. If the contract specifies payments in installments (e.g., monthly payments over time), indicate both the **total contract value** and the **individual installment amount**.
Pro Rata Billing: Are there any conditions for partial or pro rata billing?
Penalties and Fees: Are there penalties for late payments (e.g., interest rates, fees)?
Payment Schedules: What are the payment due dates (e.g., initial, interim, final)? Are there invoicing stages (e.g., advance, interim, and final payments)? If installments are specified, indicate how frequently payments are due (e.g., monthly, quarterly).
Payment Instructions: What are the bank details (IBAN, SWIFT) or other payment instructions? Are there any special conditions for payment (e.g., currencies or documentation required for payments)?

3. Customer Information:
Customer Details: Who is the customer (name, company, address)?
Customer Contact Information: Provide the customer’s phone number, email, and any other relevant contact details.
Special Instructions: Are there any customer-specific billing or payment preferences?

4. Service or Product Descriptions:
Services Provided: What are the services or products being provided under this contract? Include any clear descriptions tied to deliverables or milestones.
Service Period: What are the specific timeframes for each service or product (if applicable)?

5. Tax and Legal Requirements:
Tax Information: Are there any VAT details, tax codes, or specific tax-related clauses?
Currency Exchange Rates: If applicable, what are the currency exchange rates or conversion guidelines?
Legal Terms: Are there any specific legal clauses or compliance requirements related to payments or tax obligations?

6. Additional Conditions:
Billing Models: Is there any mention of blended rate models, multipliers, or staged payments? Specify if the contract involves **installments** or **recurring payments** and how often they are billed (e.g., monthly, quarterly).
Required Documentation: What documentation (e.g., timesheets, receipts, summaries) is required for invoicing or payments?
Special Clauses: Are there any unusual or custom clauses related to billing, payments, or contract obligations (e.g., termination conditions, service-specific clauses)?

7. Additional Detected Information:
If you detect any important details that do not fit into the categories above, please create a new category and provide the relevant information.
Important: Keep all extracted information in its original language and format. Do not translate any terms or field names. Think carefully about how to handle contracts that specify **recurring or installment payments**.
Think carefully.
    """

# Function to generate a response based on the provided data
def generate_ai_response(data, prompt):
    global ml_model
    complete_prompt = f"{prompt}\n\nContract Data:\n{data}\n"
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': complete_prompt}])
    return response['message']['content']

# Secondary prompt 1: Invoice Information & Client Data
def extract_invoice_info(main_result):
    global ml_model
    prompt = """
    1. Invoice Information & Client Data

Prompt: Based on the extracted invoice information, please provide detailed data for the following fields in JSON format. If the contract specifies **recurring payments** or **installments**, make sure the invoice reflects only the amount for the current billing period, not the total contract value.

{
  "invoice_number": "Identify the invoice number.",
  "invoice_date": "Specify the date the invoice was issued. If the info is missing or is unclear, use the current day.",
  "due_date": "Extract the payment due date. If the info is missing, but the invoice date is clearly specified as a date of the month, select the last day of the month of the invoice_date.",
  "bill_to": {
    "client_name": "Client’s full name.",
    "company_name": "Company name.",
    "address": "Full address.",
    "contact_information": {
      "email": "Email address.",
      "phone": "Phone number."
    },
    "banking_information": {
      "bank_name": "Bank name (if provided).",
      "account_name": "Account name (if provided).",
      "iban": "IBAN (if provided).",
      "swift_bic": "SWIFT/BIC code (if provided)."
    }
  },
  "bill_from": {
    "provider_name": "Provider’s full name.",
    "company_name": "Company name.",
    "address": "Full address.",
    "contact_information": {
      "email": "Email address.",
      "phone": "Phone number."
    },
    "banking_information": {
      "bank_name": "Bank name (if provided).",
      "account_name": "Account name (if provided).",
      "iban": "IBAN (if provided).",
      "swift_bic": "SWIFT/BIC code (if provided)."
    }
  },
  "payment_terms": "Identify any payment terms (e.g., Net 30, early payment discounts, penalties for late payment)."
}
If the contract specifies **installments** or **recurring payments**, ensure that the **total amount due** reflects only the amount for the current period (e.g., the monthly payment), not the total contract value.
Return Only JSON, and nothing else
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Secondary prompt 2: Description or Details of Products/Services
def extract_service_details(main_result):
    global ml_model
    prompt = """
    2. Description or Details of Products/Services

Prompt: Please extract detailed information about the products or services provided, and format the data in JSON in a table-like structure as follows. If the contract involves **installments** or **recurring services**, ensure the **quantity** reflects the current billing period (e.g., one month) and the **total amount** corresponds to the installment amount.

{
  "service_details": [
    {
      "description": "Provide a description of the product or service listed on the invoice.",
      "unit_of_measure": "Identify the unit of measurement (e.g., days, hours, service, month).",
      "quantity": "How many units or services were provided (e.g., number of days, number of products).",
      "rate_per_unit": "Extract the rate per unit (e.g., rate per day, service, hour).",
      "total_amount": "Calculate and extract the total amount for each service or product for this billing period (e.g., monthly installment)."
    }
  ]
}
If the contract specifies **installments** or **recurring services**, make sure the **total amount** reflects only the current billing period and not the total contract value.
Return Only JSON, and nothing else
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Secondary prompt 3: Calculation Details
def extract_calculation_details(main_result):
    global ml_model
    prompt = """
    3. Calculation Details

Prompt:
Please extract detailed calculations from the invoice and format the data in JSON as follows:

{
  "calculation_details": {
    "subtotal": "What is the subtotal before taxes or additional fees?",
    "taxes": {
      "tax_rate": "Identify the tax rate applied (if any, e.g., VAT, sales tax).",
      "tax_amount": "Provide the calculated tax amount."
    },
    "total_amount_due": "What is the final total amount due after applying all fees, taxes, and discounts?",
    "currency": "Specify the currency in which the invoice is issued (e.g., EUR, USD, MDL).",
    "exchange_rate": {
      "rate": "If a currency conversion is involved, extract the exchange rate used.",
      "from_currency": "Identify the original currency (if applicable).",
      "to_currency": "Identify the converted currency (if applicable)."
    }
  }
}

If the contract specifies **installments** or **recurring services**, make sure the **total amount** reflects only the current billing period and not the total contract value.
Return Only JSON, and nothing else
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Secondary prompt 4: Payment Instructions
def extract_payment_instructions(main_result):
    global ml_model
    prompt = """
    4. Payment Instructions

Prompt:
Please extract the payment instructions from the invoice and format the data in JSON as follows:

{
  "payment_instructions": {
    "bank_name": "What is the name of the bank where the payment should be sent?",
    "account_name": "What is the account holder's name for the payment?",
    "iban": "Extract the IBAN if provided.",
    "swift_bic": "Extract the SWIFT/BIC code for international payments.",
    "payment_due_date": "Reinforce when the payment is due.",
    "late_payment_penalties": "Identify any penalties for late payment (e.g., interest rates)."
  }
}Return Only JSON, and nothing else.
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Secondary prompt 5: Special Conditions or Clauses
def extract_special_conditions(main_result):
    global ml_model
    prompt = """
    5. Special Conditions or Clauses

Prompt:
Please extract any special conditions or clauses related to this invoice and format the data in JSON as follows:

{
  "special_conditions": {
    "pro_rata_billing": "Is there any mention of pro rata billing? If so, provide details.",
    "early_payment_discounts": "Are there any discounts or incentives for early payment? Provide details.",
    "late_payment_penalties": "What are the penalties for late payments (e.g., interest rates, fees)?",
    "contract_references": "Identify any references to other contracts, agreements, or annexes that are important for this invoice."
  }
}
Return Only JSON, and nothing else.
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Secondary prompt 6: Customer Information
def extract_customer_info(main_result):
    global ml_model
    prompt = """
    6. Customer Information

Prompt:
Please extract the detailed customer (Bill To) information from the invoice and format the data in JSON as follows:

{
  "customer_information": {
    "customer_name": "Full name of the customer or business entity.",
    "customer_address": "Full address of the customer.",
    "customer_contact": {
      "phone": "Phone number, if available.",
      "email": "Email address, if available."
    },
    "vat_or_tax_id": "Extract the VAT or tax ID if applicable."
  }
}
Return Only JSON, and nothing else.
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Secondary prompt 7: Additional Detected Information
def extract_additional_info(main_result):
    global ml_model
    prompt = """
    7. Additional Detected Information

Prompt:
Please review the main extracted data and provide any additional important information not covered in the above sections. If you identify new categories or unusual details, create a new category and explain its relevance. Format the additional information in JSON as follows:

{
  "additional_information": {
    "category_name": "Provide the name of the newly identified category, if applicable.",
    "details": "Provide detailed information about the newly identified category or unusual detail.",
    "relevance": "Explain why this information is relevant or important for the invoice."
  }
}
Return Only JSON, and nothing else.
Think carefully.
    """
    response = ollama.chat(model=ml_model, messages=[{'role': 'user', 'content': f"{prompt}\n{main_result}"}], format='json')
    return response['message']['content']

# Main function to organize the flow and read contract data from a file
def process_contract(contract_data):
    # Set main prompt
    main_prompt = set_main_prompt()
    
    # Step 1: Call main prompt and get response
    main_result = generate_ai_response(contract_data, main_prompt)
    
    # Step 2: Process main result through each secondary prompt
    invoice_info = extract_invoice_info(main_result)
    service_details = extract_service_details(main_result)
    calculation_details = extract_calculation_details(main_result)
    payment_instructions = extract_payment_instructions(main_result)
    special_conditions = extract_special_conditions(main_result)
    customer_info = extract_customer_info(main_result)
    additional_info = extract_additional_info(main_result)
    
    # Combine the results into a dictionary
    result = {
        "main_result": main_result,
        "invoice_information": invoice_info,
        "service_details": service_details,
        "calculation_details": calculation_details,
        "payment_instructions": payment_instructions,
        "special_conditions": special_conditions,
        "customer_information": customer_info,
        "additional_information": additional_info
    }
    
    # Return the result as a JSON string
    return result
