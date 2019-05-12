import json

## Test json file
def validateJsonContent(json_filename):
	with open(json_filename, mode="r", encoding="UTF-8") as json_file:
		data = json.loads(json_file.read())

if __name__ == '__main__':
   validateJsonContent("modules-part.json")