import json
from rapidfuzz import fuzz, process
import os

# Get the directory where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(BASE_DIR, "Bank_Data.json"), "r", encoding="utf-8") as f:

    bank_data = json.load(f)



def get_id_by_name(name: str) -> int:
    customer_data = bank_data.get("customers", [])
    for customer in customer_data:
        customer_name = customer.get("customer_name", "")
        if customer_name.lower() == name.lower():
            customer_id = customer.get("customer_id", 0)
            return customer_id
    return 0



def get_transactions_by_name(name: str):
    customer_data = bank_data.get("customers", [])

    if len(name.strip()) < 3:
        return {
            "message": "Customer name atleast 3 characters long"
        }

    customer_names = [customer.get("customer_name", "") for customer in customer_data]

    result = process.extractOne(name.strip(), customer_names, scorer=fuzz.WRatio)

    if result is not None:
        matched_name, score, index = result
        if score >= 80:
            name = matched_name

    for customer in customer_data:
        customer_name = customer.get("customer_name", 0)
        if customer_name.lower() == name.lower():
            return customer.get("transactions", [])
    return {
        "message": "Transactions not found"
    }


def get_information_by_name(name: str) -> dict:
    customer_information = bank_data.get("customers", [])

    if len(name.strip()) < 3:
        return {
            "message": "Customer name atleast 3 characters long"
        }

    customer_names = [customer.get("customer_name", "") for customer in customer_information]

    result = process.extractOne(name.strip(), customer_names, scorer=fuzz.WRatio)

    if result is not None:
        matched_name, score, index = result
        if score >= 80:
            name = matched_name



    for customer in customer_information:
        customer_name = customer.get("customer_name", "")
        if customer_name.lower() == name.lower():
            customer_name = customer.get("customer_name", "")
            customer_account_type = customer.get("customer_account_type", "")
            customer_account_number = customer.get("customer_account_number", "")
            customer_ifsc_code = customer.get("customer_ifsc_code", "")
            customer_ph_number = customer.get("customer_ph_number", "")
            return {
                "customer_name": customer_name,
                "customer_account_type": customer_account_type,
                "customer_account_number": customer_account_number,
                "customer_ifsc_code": customer_ifsc_code,
                "customer_ph_number": customer_ph_number,
            }

    return {
        "message" : "Account not found"
    }


def get_branch_details_by_name(b_name: str) ->  dict:
    branch_details = bank_data.get("bank_details", [])

    if len(b_name.strip()) < 3:
        return {
            "message": "Branch name atleast 3 characters long"
        }

    branch_names = [branch.get("bank_name", "") for branch in branch_details]

    result = process.extractOne(b_name.strip(), branch_names, scorer=fuzz.WRatio)

    if result is not None:
        matched_name, score, index = result
        if score >= 80:
            b_name = matched_name

    for branch in branch_details:
        branch_name = branch.get("bank_name", "")
        if branch_name.lower() == b_name.lower():
            bank_name = branch.get("bank_name", "")
            bank_branch = branch.get("bank_branch", "")
            bank_ifsc = branch.get("bank_ifsc", "")
            bank_address = branch.get("bank_address", "")
            return {
                    "bank_name": bank_name,
                    "bank_branch": bank_branch,
                    "bank_ifsc": bank_ifsc,
                    "bank_address": bank_address
            }
    return {
        "message": "Details not found"
    }














# def get_customer_name_by_id(id: int) -> str:
#     customer_data = bank_data.get("customers", [])
#
#     for customer in customer_data:
#         customer_id = customer.get("customer_id", 0)
#         if(customer_id == id):
#             account_name = customer.get("customer_name", "")
#             return account_name
#
#     return ""
#
#
#
#
#
#
# def get_customer_account_type_by_id(id: int) -> str:
#     customer_data = bank_data.get("customers", [])
#
#     for customer in customer_data:
#         customer_id = customer.get("customer_id", 0)
#         if customer_id == id:
#             account_type = customer.get("customer_account_type", "")
#             return account_type
#     return ""
#
#
#
#
#
#
# def get_account_number_by_id(id: int) -> str:
#     customer_data = bank_data.get("customers", [])
#
#     for customer in customer_data:
#         customer_id = customer.get("customer_id", 0)
#         if(customer_id == id):
#             account_number = customer.get("customer_account_number", "")
#             return account_number
#     return ""
#
#
#
#
# def get_customer_ifsc_code_by_id(id: int) -> str:
#     customer_data = bank_data.get("customers", [])
#
#     for customer in customer_data:
#         customer_id = customer.get("customer_id", 0)
#         if customer_id == id:
#             customer_ifsc_code = customer.get("customer_ifsc_code", "")
#             return customer_ifsc_code
#
#     return ""
#
#
#
#
#
# def get_customer_ph_number_by_id(id: int) -> str:
#     customer_data= bank_data.get("customers", [])
#
#     for customer in customer_data:
#         customer_id = customer.get("customer_id", 0)
#         if customer_id == id:
#             ph_number = customer.get("customer_ph_number", "")
#             return ph_number
#
#     return ""
