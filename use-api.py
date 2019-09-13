import requests
import json
import csv

class CommonWealth:
    def __init__(self, host_url, headers_):
        self.host_url = host_url
        self.headers_ = headers_
    def comwealth_products(self):
        r = requests.get(url=self.host_url, headers=self.headers_)
        return r.text
    def output_file(self,json_file):
        with open('comwealth_origin_products.json', 'w') as f:
            json.dump(json_file, f) # Export the file in json format.
    def format_data(self, json_file):
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

    def fetch_product(self, product_id):
        r = requests.get(url=self.host_url+"/"+product_id, headers=self.headers_)
        return  r.text


    def format_product_details(self,product_content):
        with open('comwealth_prodcuts_indetail.txt', 'w') as f:


    def fetch_product_all_details(self, json_file):
        for i in range(0,json_file["meta"]["totalRecords"]-1):
            product_json_content =






      

def main():
    comwealth_host_url = "https://api.commbank.com.au/cds-au/v1/banking/products"
    comwealth_headers = {'Accept': "application/json"}
    comwealth = CommonWealth(comwealth_host_url, comwealth_headers)
    content_json = json.loads(comwealth.comwealth_products())  # Content returned as unicode.
    # print(comwealth.comwealth_products())
    # print(content_json)



    # Store original products json 
    comwealth.output_file(content_json)
    # Format the json and output json
    # comwealth.format_data(content_json)

    first_product = json.loads(comwealth.fetch_product(content_json["data"]["products"][0]["productId"]))
    with open ('first_product.json', 'w') as f:
        json.dump(first_product, f)
    f.close()

    # print(content_json["data"]["products"][0]["productId"])

    # for i in range(0,content_json["meta"]["totalRecords"]-1):
    #     print(content_json["data"]["products"][i]["name"], i)

if __name__ == '__main__':
    main()





# content_json = json.loads(comwealth_products())
# output_file(content_json)



# print(json.dumps(comwealth_products().decode("utf-8"), sort_keys=True, indent=4, separators=(',', ': ')))
# with open('data2.json','w') as f:
#     f.write(json.dumps(comwealth_products().decode("utf-8"), sort_keys=True, indent=4, separators=(',', ': ')))



