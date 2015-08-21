try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

def config_gen():
	# SECRET_KEY = 'qweR'
	config = ConfigParser()
	config['DEFAULT']['logfile'] = 'shadowsocks.logs'
	# config['DEFAULT']['logfile'] = '/var/log/shadowsocks.log'  
	config['DEFAULT']['IP'] = '127.0.0.1'   
	
	with open('logviewer.ini', 'w') as configfile:    # save
	    config.write(configfile)
