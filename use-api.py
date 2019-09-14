'''
Author: Chengen Liu
This file utilises the commonwealth bank public api, retrieves data and formats it.
This program is an assistant program for the research purpose of the subject Financial Markets and Instruments FNCE90047.
'''
import requests
import json
import csv


'''
Main class holds the sending request/ format data functionality
'''
class CommonWealth:
    def __init__(self, host_url, headers_):
        self.host_url = host_url
        self.headers_ = headers_

    def comwealth_products(self):
        """
        Send request to retrieve full description of products
        :return: the unicode string of retrieved results that are in json format
        """
        # Retrieve JSON from Com Bank
        r = requests.get(url=self.host_url, headers=self.headers_)
        # print(r.text)
        return r.text
    def output_file(self,json_file):
        """
        Output the json format input
        :param json_file: Json format input
        """
        with open('comwealth_origin_products.json', 'w') as f:
            json.dump(json_file, f) # Export the file in json format.
    def format_data(self, json_file):
        """
        Format the data and output in csv format
        :param json_file: a file in json format
        """
        with open("comwealth.csv", 'a') as comwealth:
            csv_writer = csv.writer(comwealth, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for i in range(0, json_file["meta"]["totalRecords"]-1):
                try:
                    csv_writer.writerow([json_file["data"]["products"][i]["name"], json_file["data"]["products"][i]["effectiveFrom"],
                                         json_file["data"]["products"][i]["effectiveTo"], json_file["data"]["products"][i]["description"],
                                         json_file["data"]["products"][i]["productId"], json_file["data"]["products"][i]["additionalInformation"]["feesAndPricingUri"]])
                except:
                    print(json_file["data"]["products"][i]["name"])
            csv_writer.close()

    # Retrieve details about one product
    def fetch_product(self, product_id):
        """
        Retrieve details about one specific product, provided its product id.
        :param product_id: A specific product id, as required in com wealth bank api description.
        :return: A json format string
        """
        r = requests.get(url=self.host_url+"/"+product_id, headers=self.headers_)
        return  r.text


    def format_product_details(self,product_content, product_name):
        """
        Format and ouput the specific product content.
        :param product_content: The dictionary (after loading the json string) of the specific product
        :param product_name: The name of the products
        """
        with open ('comwealth_products_indetail.txt', 'a') as f:
            f.write(product_name)
            f.write("\n")
            my_print_dict(product_content, f)
            f.write("\n")
        f.close()
        print("ok")


    # Fetch the products details (all products)
    # Receive the argument that is a python object.
    def fetch_product_all_details(self, json_file):
        """
        Retrieve all products, using prductId
        :param json_file: The summary of all products.
        """
        for i in range(0,json_file["meta"]["totalRecords"]-1):
            product = self.fetch_product(json_file["data"]["products"][i]["productId"])   # one product
            dict_product = json.loads(product)
            self.format_product_details(dict_product, dict_product["data"]["name"])
            # self.format_test(product)

            #Format the data
            # self.format_product_details(product, json.loads(product)["data"]["name"])

    def format_test(self):
        full_content = self.comwealth_products()
        content_id= (json.loads(full_content))["data"]["products"][0]["productId"]
        # print(content["data"]["products"][0]["productId"])
        print(content_id)
        one_product = self.fetch_product(content_id)  # Return a json format string.
        print(one_product)
        dic_json = json.loads(one_product)
        with open ('test.txt', 'w') as f:
            my_print_dict(dic_json, f)
            f.write("\n")
        f.close()
        print("ok")



'''
This function receieves a dictionary and formats its output by recursion. 
However, this function will not be able to deal with list in dictionary. 
d: dictionary that needs to iterate
f: the file-writer
'''
def my_print_dict(d, f):
    for k, v in d.items():
        if isinstance(v, dict):
            my_print_dict(v,f)
            f.write("\n")
        else:
            f.write("{0}: {1} \n".format(k,v))




def main():
    comwealth_host_url = "https://api.commbank.com.au/cds-au/v1/banking/products"
    comwealth_headers = {'Accept': "application/json"}
    comwealth = CommonWealth(comwealth_host_url, comwealth_headers)
    content_json = json.loads(comwealth.comwealth_products())  # Content returned as unicode and loaded as a python object.

    # Store original products json 
    comwealth.output_file(content_json)
    # Format the json and output json. No use once finised.
    # comwealth.format_data(content_json)

    comwealth.fetch_product_all_details(content_json)


if __name__ == '__main__':
    main()



