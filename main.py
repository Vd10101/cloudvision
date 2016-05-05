import argparse
import json
from utils_google import get_vision_api
from utils_image import (read_image, read_image_base64, save_image, draw_face, draw_box, draw_text)

## inputfile  = "pic.jpg"
## outputfile = "output.jpg"

def main(inputfile, outputfile, max_results):
##def main():

	vision = get_vision_api()
	
	body = make_request(inputfile)
	response = vision.images().annotate(body=body).execute()
	
	show_results(inputfile, response, outputfile)
	
def make_request(inputfile):
	""" Create a request batch (one file at a time) """
	return {
		"requests":[
			{
				"image":{
	    				"content": read_image_base64(inputfile)
	    			},
				"features": [
					{
						"type":"LABEL_DETECTION",
      						"maxResults": 10
      					},
      					{
      						"type":"TEXT_DETECTION",
      						"maxResults": 10
      					},
      					{
      						"type":"FACE_DETECTION",
      						"maxResults": 20
      					}
      				]
			}
		]
	}

def show_results(inputfile, data, outputfile):

	#read original file
	im = read_image(inputfile)

	#draw face, boxes and text for each response
	for r in data['responses']:

		if 'faceAnnotations' in r:
			draw_face(im, r['faceAnnotations'])

		if 'labelAnnotations' in r:
			strs = map(lambda a: a['description'], r['labelAnnotations'])
			im = draw_text(im, ", ".join(strs))

		for field in ['textAnnotations', 'logoAnnotations']:
			if field in r:
				for a in r[field]:
					draw_box(im, a['boundingPoly']['vertices'])

	#save to output file
	save_image(outputfile, im)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects faces in the given image.')
    parser.add_argument(
        'input_image', help='the image you\'d like to detect faces in.')
    parser.add_argument(
        '--out', dest='output', default='output.jpg',
        help='the name of the output file.')
    parser.add_argument(
        '--max-results', dest='max_results', default=10,
        help='the max results of face detection.')
    args = parser.parse_args()

    main(args.input_image, args.output, args.max_results)