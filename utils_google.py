import httplib2
import json
import sys
from googleapiclient import discovery
from oauth2client import tools, file, client
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials

# limited preview only (sorry!)
API_DISCOVERY_FILE = 'vision_discovery_v1alpha1.json'
SERVICE_ACCOUNT_FILE = 'service-account.json'

# [START get_vision_service]
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
##DISCOVERY_URL='https://vision.googleapis.com/$discovery/rest?version=v1'

""" Google Authentication Utilities """

def get_vision_api():
    ## def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)

## def get_vision_api():
##	credentials = get_api_credentials('https://www.googleapis.com/auth/cloud-platform')
##	with open(API_DISCOVERY_FILE, 'r') as f:
##		doc = f.read()	
##	return discovery.build_from_document(doc, credentials=credentials, http=httplib2.Http())


def get_api_credentials(scope, service_account=True):
	""" Build API client based on oAuth2 authentication """
	STORAGE = file.Storage('oAuth2.json') #local storage of oAuth tokens
	credentials = STORAGE.get()
	if credentials is None or credentials.invalid: #check if new oAuth flow is needed
		if service_account: #server 2 server flow
##			with open(SERVICE_ACCOUNT_FILE) as f:
##				account = json.loads(f.read())
##				email = account['client_email']
##				key = account['private_key']
			credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
##			credentials = client.SignedJwtAssertionCredentials(email, key, scope=scope)
			STORAGE.put(credentials)
		else: #Application Default Credentials (ADC)
			credentials = GoogleCredentials.get_application_default()
			return discovery.build('vision', 'v1', credentials=credentials,
                          discoveryServiceUrl=DISCOVERY_URL)	    
##		else: #normal oAuth2 flow
##			CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
##			FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS, scope=scope)
##			PARSER = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser])
##			FLAGS = PARSER.parse_args(sys.argv[1:])
##			credentials = tools.run_flow(FLOW, STORAGE, FLAGS)
		
	return credentials