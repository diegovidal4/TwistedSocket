import re

global commands
commands=['ER','XANS','SI','XAIM','XART','XAID','XAEF','XADP','XAGR','VR','TD','ST','SS','RT','PV','ID','GS','GC','EV','ED','DA']

def as_dict(config):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict
    
def get_data(data):
	data=data.rstrip("\n\r") #Clear new line character
	resp={}
	regexp = re.compile("(?<=[;>])([^&>]+)(?=[;<])")
	if regexp.search(data) is not None: #If data has syrus format
		resp["format"]="Syrus"
		clean_data=data[1:len(data)-1] #Remove > and <
		resp['qualifier']=clean_data[0] #Get qualifier
		resp['data']=data
		try:
			resp['command']=filter((lambda x: x in clean_data), commands)[0] #Get the command
		except IndexError: #if command not found in list
			return {}

		header=resp['qualifier']+resp['command']

		if resp['qualifier']=='S':
			pass
		elif resp['qualifier']=='R':
			div=clean_data.split(';')
			sections=len(div)-1
			if "ID" in clean_data: #if string has IMEI
				resp['imei']=div[sections].replace("ID=","")
			if resp['command']=="ER": #if command is an error response
				r=div[0].split(':')
				try:
					resp['err_number']=r[0].replace(header,"")
					resp['command_error']=r[1]
					return resp
				except IndexError:
					return {}
			resp['response']=div[0].replace(resp['qualifier']+resp['command'],"") #Get response from command
			resp['misc']=div[1]
				# resp['response']=get_digit_string(header)
				# resp['command']=clear_digit(header[1:])
	return resp

def clean_data(data):
	return data.replace("\n","")
def clear_digit(data):
	return ''.join(i for i in data if not i.isdigit())

def get_digit_string(data):
	return ''.join(i for i in data if i.isdigit())



if __name__=="__main__":
	p=raw_input()
	print get_data(p)
