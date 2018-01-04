#coding = utf-8
from aip import AipOcr
import sys
import os
import click
import io,json
import datetime
from pprint import pprint

# fixme : replace it with user's key
APP_ID = 'USER APP ID'
API_KEY = 'USER API KEY'
SECRET_KEY = 'USER SECRET KEY'

aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

options = {
  'detect_direction': 'true',
  'language_type': 'CHN_ENG',
}

class ConfNotExistErr(Exception):
    '''raise this error when configuration file not exist'''
    pass

class LogData(object):
    def __init__(self,imgname,time):
        self.imgname = imgname
        self.time = time
        self.url = 'NOT DEFINE'
        self.result = 'NOT DEFINE'

def load_img_file(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def load_conf():
    try:
        data = json.load(open('./aip.conf'))
        pprint(data)
        APP_ID = data["aip"]["app_id"]
        API_KEY = data["aip"]["api_key"]
        SECRET_KEY = data["aip"]["secret_key"]
        print("Connect Server with APP_ID[%s] API_KEY[%s] SECRET_KEY[%s] " % (APP_ID,API_KEY ,SECRET_KEY) )
    except Exception as err:
        raise ConfNotExistErr('Configuration not be handled well!')


def handle_table_ocr(f):
    # 1. make a request ; 2. get the result
    # image size < 4M and width|height > 15px , max widht/height < 4096px
 
    msg_back = {}
    try:
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        logdata = LogData(f,datetime.datetime.now())
        content = load_img_file(f)
        msb_back = client.tableRecognitionAsync(content)
    except Exception as err:
        print err
    try:
        print msg_back["result"]["result_id"] 
        print msg_back["log_id"]
    except Exception as err:
        print err
        print("AIP return error , LOG_ID[%s] ERROR_MSG[%s]" % (msg_back["log_id"], msg_back["error_msg"]))
        logdata.result='Request Error'
        return 
     
    try:
        options = {}
        ocr_back = {}
        # type could be json | excel
        options["result_type"] = "excel"
        ocr_back = client.getTableRecognitionResult(msg_back['result']['result_id'])
	logdata.result = ocr_back["ret_msg"]
        if (options["result_type"] == "excel"):
            logdata.url = ocr_back['result']['result_data']['file_rul']
        else:
            logdata.url = 'JSON NOT DEFINE'
        logdata.result='Success'
        pprint(ocr_back)
    except Exception as err:
        print err
        print("AIP return error , LOG_ID[%s] ERROR_MSG[%s]" % (msb_back['log_id'],msg_back['error_msg']) )
        logdata.result='Result Error'
        return 

    

def handle_word_ocr(f):
    pass

def handle_ocr(c,path):
    try:
        load_conf()
    except ConfNotExistErr:
        print "Configuration file not correct!"
        return

    if c in ['table']:
    	print("=>scan as table")
        handle_table_ocr(path)
    else:
    	print("=>scan as word")
        handle_word_ocr(path)  
    print "=>processing %s" % (path)    

    print("=>end.")


@click.command()
@click.option('-c',type=click.Choice(['table', 'word']))
@click.option('-f',help='image file path')
@click.option('-o',default="./output",help='output file path')
@click.option('-d',help='directory for batch file processing')
def main(c,f,o,d):
    print "c=%s f=%s o=%s d=%s" % (c,f,o,d)	
    if (not c):
        print "Please select -c [table|word] as input"
        return

    if (not f) and (not d):
        print "Please choose the file or directory, use --help for detail" 
        return

    if (d):
        file_count = 0
        for filename in os.listdir(d):
    	    if filename.endswith(".png") or filename.endswith(".jpg"): 
    	        file_count=file_count+1
                print(os.path.join(d, filename))
                filepath = os.path.join(d, filename)
                handle_ocr(c,filepath)
    	    else:
        	    continue
        if file_count == 0:
            print "Doesn't find any valid files under %s " % d
        else:
            print "%d files are processed!" % file_count
    else:
        handle_ocr(c,f)

 

    
if __name__ == '__main__':
    main()

