#coding = utf-8
from aip import AipOcr
import sys
import time
import os
import click
import io,json
import datetime
import wget
from pprint import pprint

# fixme : replace it with user's key

#aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

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

class AipConf(object):
    def __init__(self):
        self.app_id = None
        self.api_key = None
        self.secret_key = None

def load_img_file(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# support input parameter is base on seconds
def sleep_with_dots(s):
    sleeping_count = s * 2
    sys.stdout.write('  ')
    for count in range(0,sleeping_count):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.5)
    print(" ")

def get_file_by_url(url,outpath):
    sys.stdout.write('  ')
    return wget.download(url,outpath)

def load_conf(aip_conf):
    try:
        data = json.load(open('./aip.conf'))
        #pprint(data)
        aip_conf.app_id = data["aip"]["app_id"]
        aip_conf.api_key = data["aip"]["api_key"]
        aip_conf.secret_key = data["aip"]["secret_key"]
    except Exception as err:
        raise ConfNotExistErr('Configuration not be handled well!')


def handle_table_ocr(client,f):
    # 1. make a request ; 2. get the result
    # image size < 4M and width|height > 15px , max widht/height < 4096px
 
    msg_back = {}
    request = None
    try:
        logdata = LogData(f,datetime.datetime.now())
        print("  load content from %s and send request to server" % (os.path.basename(f)))
        content = load_img_file(f)
        msg_back = client.tableRecognitionAsync(content)
    except Exception as err:
        print "error!"
        print err

    try:
        #print(msg_back)
        print('  server processing , request_id = %s ' % (msg_back['result'][0]['request_id']))
    except Exception as err:
        print err
        print(msg_back)
        return 

    # timeout value request because if ask result so quickly, the server may not handle it in time!
    print("  wating server to process")
    sleep_with_dots(10)
    try:
        print("  get result request_id = %s " % (msg_back['result'][0]['request_id']))
        options = {}
        ocr_back = {}
        # type could be json | excel
        options["result_type"] = "excel"
        ocr_back = client.getTableRecognitionResult(msg_back['result'][0]['request_id'],{'result_type':'excel'})
        #print(ocr_back)
        print("  server return status : %s " % ocr_back['result']['ret_msg'])
        #print("url : %s " % ocr_back['result']['result_data'])
        filename = get_file_by_url(ocr_back['result']['result_data'], './output/table')
        print('\n  saving %s to output/table' % filename)
	#logdata.url = ocr_back['result']["result_data"]
        if (options["result_type"] == "excel"):
            logdata.url = ocr_back['result']['result_data']
        else:
            logdata.url = 'JSON NOT DEFINE'
        logdata.result='Success'
        #pprint(ocr_back)
    except Exception as err:
        print err
        print("AIP return error , REQUEST_ID[%s] ERROR_MSG[%s]" % (msb_back['result'][0]['request_id'],ocr_back['result']['error_msg']) )
        logdata.result='get the %s result error'
        return 

    

def handle_word_ocr(client,f):
    pass

def handle_ocr(client,c,path):
    if c in ['table']:
    	print("=>scan %s as table" % os.path.basename(path) )
        handle_table_ocr(client,path)
    else:
    	print("=>scan as word")
        handle_word_ocr(client,path)  
    print "=>processing %s end." % (os.path.basename(path))    



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


    aipconf = AipConf()
    try:
        load_conf(aipconf)
    except ConfNotExistErr:
        print "Configuration file not correct!"
        return

    client = AipOcr(aipconf.app_id, aipconf.api_key,aipconf.secret_key)
    pprint(client)
    print("Connect Server with APP_ID[%s] API_KEY[%s] SECRET_KEY[%s] " % (aipconf.app_id,aipconf.api_key ,aipconf.secret_key) )
    if (d):
        file_count = 0
        for filename in os.listdir(d):
            if filename.endswith(".png") or filename.endswith(".jpg"): 
                file_count=file_count+1
                print(os.path.join(d, filename))
                filepath = os.path.join(d, filename)
                handle_ocr(client,c,filepath)
    	    else:
                continue
        if file_count == 0:
            print "Doesn't find any valid files under %s " % d
        else:
            print "%d files are processed!" % file_count
    else:
        handle_ocr(client,c,f)

if __name__ == '__main__':
    main()

