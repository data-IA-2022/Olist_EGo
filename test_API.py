import requests, uuid, json

# Copier coller exemple Azure translate

# Add your key and endpoint
key = "ee55f77145dc4e62b3d480efbdec7589"
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "francecentral"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['fr', 'zu']
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.
body = [{
    'text': 'I would really like to drive your car around the block a few times!'
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

#print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

base_url="http://localhost:5099/"
print('OK')

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['fr']
}


# API OLIST, récupération des info catégories
r = requests.get(base_url+"/api/categories", headers={'Subscription-Key': key})
print(r.status_code)
print(r.text)

#print(r.json())
for cat in r.json():
	print(cat)
	pk=cat['product_category_name']
	if cat['product_category_name_french'] is None:
	    # Si pas de version FR
		txt=cat['product_category_name_english'].replace('_', ' ')
		# Requète API Azure
		body = [{'text': txt}]
		request = requests.post(constructed_url, params=params, headers=headers, json=body)
		response = request.json()
		print(response)
		traduc=response[0]['translations'][0]['text']

		print(f"TRADUCTION de '{txt}' -> '{traduc}'")

		# Requete API OLIST pour update
		r2 = requests.post(base_url+"/api/category", data={'cat':pk, 'fr': traduc}, headers={'Subscription-Key': key})
		print(r2.status_code)
		#print(r2.text)

		quit()
	