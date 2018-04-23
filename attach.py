# -*- coding:utf-8 -*-
import re 
import os 
import time
import multiprocessing
import ConfigParser

# global variable


process_name=''
process_path=''
windbg_path=''
sleep_time = 0
command_list=[]


# write commands to command_tmp.txt
def write_to_commandScript():
	global command_list
	rr = ''
	for item in command_list:
		rr = rr + item + ';'
	rr = rr[:-1]
	with open('command_tmp.txt','wb') as fp:
		fp.write(rr)
	fp.close()


# use tasklist to get the process_id
def get_process_id():
	global process_name
	result = os.popen('tasklist|findstr %s'%(process_name.strip("\"")))
	res = result.read()

	if len(res)==0:
		print '%s not found...'%(process_name)
		exit(0)
	else:
		pattern = '\d{3,4}'   
		match = re.search(pattern,res)	
		pid  = match.group(0)
	return pid

# make windbg attach to the process. When windbg runs over, delete tmp files automatic
def attach(pid):
	global windbg_path,command_file
	write_to_commandScript()
	command = "\"%s\" -p %s -c \"$$><command_tmp.txt\""%(windbg_path.strip("\""),pid)
	with open('execute.bat','wb') as f:
		f.write(command)
	f.close()
	os.system('execute.bat')
	clear_file()

# delete tmp files
def clear_file():
	os.system('del execute.bat')
	os.system('del command_tmp.txt')


def run_process(process_path):
	os.system('"'+process_path+'"')

def init_config():
	global windbg_path
	global process_name
	global process_path
	global sleep_time
	cf = ConfigParser.ConfigParser()
	cf.read('config.txt')
	selected_session = cf.get("selected_session","session")
	windbg_path = cf.get('windbg_info','windbg_path')
	process_name = cf.get(selected_session,'process_name')
	process_path = cf.get(selected_session,'process_path')
	sleep_time = cf.getint("common_config","sleep_time")
	f = open('command.txt','rb')
	while 1:
		line = f.readline()
		if not line:
			break 
		command_list.append(line)
	f.close()

if __name__=='__main__':
	# get config info from config.txt
	init_config()

	# start multiprocessing to start process
	p = multiprocessing.Process(target=run_process,args=(process_path,))
	p.start()
	time.sleep(sleep_time)
	pid = get_process_id()
	print 'attach to process %s'%(pid)
	attach(pid)