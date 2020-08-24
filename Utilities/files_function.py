import json

def json_save(data, file_name, file_type = 'json'):
	try:
		with open(file_name+'.{}'.format(file_type), 'w') as outfile:
			json.dump(data, outfile)
	except Exception('Error') as e:
		print(e)

def load_json(file_name):
	data = None
	try:
		with open(('{}.json'.format(file_name)), 'r') as f:
			data = json.load(f)
			return data
	except:
		print('Error')
	finally:
		return data
