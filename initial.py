from configparser import ConfigParser

def config_gen():
	# SECRET_KEY = 'qweR'
	config = ConfigParser()
	config['DEFAULT']['logfile'] = 'shadowsocks.logs'    
	config['DEFAULT']['IP'] = '188.154.76.109'   
	
	with open('logviewer.ini', 'w') as configfile:    # save
	    config.write(configfile)
