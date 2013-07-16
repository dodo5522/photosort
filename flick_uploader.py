#!/usr/bin/python

'''
Upload media files to flickr.

 arg1 : Local directory path including media files
 arg2 : none
'''

import os,sys,string,re
import flickr_api as flickr

argvs = sys.argv
argc = len(argvs)
path_conf = re.sub(r'(.*).py', r'\1.conf', argvs[0])
path_auth_file = re.sub(r'(.*).py', r'\1.token', argvs[0])

###################
# sub routine
###################
def LoadConfiguration():
	# conf file is based on py script name	
	fp_conf = open(path_conf, 'r')
	
	# read configuration	
	conf = dict()
	for read_line in fp_conf:
		line = string.strip(read_line)
		if line[0:len('API_KEY')] == 'API_KEY':
			conf['API_KEY'] = re.sub(r'API_KEY=([0-9a-z]+)', r'\1', line)
		elif line[0:len('API_SEC')] == 'API_SEC':
			conf['API_SEC'] = re.sub(r'API_SEC=([0-9a-z]+)', r'\1', line)
		elif line[0:len('URL_CALLBACK')] == 'URL_CALLBACK':
			conf['URL_CALLBACK'] = re.sub(r'URL_CALLBACK=(http://.+)', r'\1', line)
	fp_conf.close()
	
	# dump the configuration
	for key in conf.keys():
		print key + ' : ' + conf[key]
	
	return (conf['API_KEY'], conf['API_SEC'], conf['URL_CALLBACK'])

def LoadTokenFileOrGenerateItIfNotExists(api_key=None, api_sec=None, url_callback=None):
	if api_key == None or api_sec == None or url_callback == None:
		print 'Error: api_key(%s) or another is not specified.' % (api_key)
		return None
	
	# create object to authenticate
	flickr.set_keys(api_key, api_sec)
	
	if os.path.exists(path_auth_file):
		print '%s already exists so load it.' % (path_auth_file)
		auth = flickr.auth.AuthHandler.load(path_auth_file)
	else:
		print '%s does not exist.' % (path_auth_file)
		
		# set URL to get the query of oauth_token & oauth_verifier
		auth = flickr.auth.AuthHandler(callback=url_callback)
		
		# get URL for oauth
		url = auth.get_authorization_url('write')
		print url
		
		# store the token already verified
		verifier = raw_input('Enter the verifier:')
		auth.set_verifier(verifier)
		auth.save(path_auth_file)
	
	# set the AuthHandler for the session
	flickr.set_auth_handler(auth)
	
	return flickr

###################
# main routine
###################

# load configuration file and get some parameters
(API_KEY, API_SEC, URL_CALLBACK) = LoadConfiguration()

# initialize flickr_api object
obj = LoadTokenFileOrGenerateItIfNotExists(api_key=API_KEY,
                                           api_sec=API_SEC,
                                           url_callback=URL_CALLBACK)

if obj != None:
        # upload file
        obj.upload(photo_file='/home/takashi/tools_private/python/DSC_0593.jpg')
else:
        print 'Error: auth is empty.'
        sys.exit()


