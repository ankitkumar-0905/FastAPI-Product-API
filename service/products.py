import json
from pathlib import Path
from typing import List ,Dict

DATA_FILE = Path(__file__).parent.parent / 'data' / 'dummy.json'

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,'r',encoding='utf-8') as file:
        return json.load(file)
    
def get_all_products() -> List[Dict]: #this function will return all the products from the json file
    return load_products()    

#this function will save the products to the json file
def save_products(products: List[Dict]) -> None:
    with open(DATA_FILE,'w',encoding='utf-8') as file: #open the file in write mode
        json.dump(products,file,indent=4,ensure_ascii=False) 

#this function will add a new product to the json file
def add_product(product: Dict) -> Dict:
    products = get_all_products()   #--->load existing products
    if any(p["sku"] == product["sku"] for p in products ):  #-->check if the sku already exists
        raise ValueError("SKU already exists" )   #-->if it exists raise an error
    products.append(product) #add the new product to the list
    save_products(products) #save the updated list back to the file
    return product

#this function will remove a product from the json file based on the product id
def remove_product(id:str) -> str:
    products = get_all_products()
    for idx ,p in enumerate(products): 
        if p.get("id")==str(id):
            deleted = products.pop(idx)
            save_products(products)
            return{"message":"products deleted successfully","data":deleted}


'''
-----------chatGPT code for deleting a product from the json file------------------

# def remove_product(id: str)->dict:
#     products = get_all_products()

#     for idx, p in enumerate(products):
#         if "id" not in p:
#             continue
#         if p["id"] == str(id):
#             deleted = products.pop(idx)
#             save_products(products)

#             return {
#                 "message": "product deleted successfully",
#                 "data": deleted
#             }

#     return {"message": "Product not found"}

'''

def change_product(product_id:str ,update_data:dict):
    products = get_all_products()
    for idx ,p in enumerate(products): 
        for key ,value in update_data.items():
            if value is None:
                continue
            if isinstance(value, dict) and isinstance(p.get(key), dict):
                p[key].update(value)
            else:
                p[key] = value    
        products[idx] = p
        save_products(products)
        return p
    raise ValueError("Product not found")        