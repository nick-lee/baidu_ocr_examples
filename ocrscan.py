#coding = utf-8
from aip import AipOcr
import sys
import os
import click

# fixme : replace it with user's key
#APP_ID = 'USER APP ID'
#API_KEY = 'USER API KEY'
#SECRET_KEY = 'USER SECRET KEY'

aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

options = {
  'detect_direction': 'true',
  'language_type': 'CHN_ENG',
}

def handle_table_ocr(f):
	pass

def handle_word_ocr(f):
	pass

def handle_ocr(c,path):
    if c in ['table']:
    	print("==>scan as table")
        handle_table_ocr(path)
    else:
    	print("==>scan as word")
        handle_word_ocr(path)  
    print "=>processing %s" % (path)    

    print("=>end.")


@click.command()
@click.option('-c', type=click.Choice(['table', 'word']))
@click.option('-f',help='image file path')
@click.option('-d',help='directory for batch file processing')
def main(c,f,d):
    print "c=%s f=%s d=%s" % (c,f,d)	
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

