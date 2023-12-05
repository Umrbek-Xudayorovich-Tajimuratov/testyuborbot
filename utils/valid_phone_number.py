# Program to check whether a phone number is 
# valid or not 
import phonenumbers 
  

async def valid_phone(phone_number):
    
    try:
        # Parsing String to Phone number 
        phone_number = phonenumbers.parse(phone_number) 
        # Validating a phone number 
        valid = phonenumbers.is_valid_number(phone_number) 
        # Checking possibility of a number 
        # possible = phonenumbers.is_possible_number(phone_number) 
    except:
        valid=False
    
    print("VALID: ",valid)
    return valid


  

# def valid_phone(phone_number):
    
#     try:
#         # Parsing String to Phone number 
#         phone_number = phonenumbers.parse(phone_number) 

#         # Validating a phone number 
#         valid = phonenumbers.is_valid_number(phone_number) 
#         # Checking possibility of a number 
#         # possible = phonenumbers.is_possible_number(phone_number) 
#     except:
#         valid=False
#     print(valid)
#     # return (valid)

# valid_phone("afssf")