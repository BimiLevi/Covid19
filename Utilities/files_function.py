import json

def json_save(data, file_name, file_type = 'json'):
	try:
		with open(file_name+'.{}'.format(file_type), 'w') as outfile:
			json.dump(data, outfile)

	except Exception as e:
		print("Couldn't save the data that you requested:\n{}".format(data))
		print('The error that occurred is: {}'.format(e))

def load_json(file_name):
	data = None
	try:
		with open(('{}.json'.format(file_name)), 'r') as f:
			data = json.load(f)
			return data

	except Exception as e:
		print("Couldn't load the file that you requested: {}".format(file_name + '.json'))
		print('The error that occurred is: {}'.format(e))

	finally:
		return data
