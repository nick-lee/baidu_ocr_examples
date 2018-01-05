# baidu_ocr_examples

### Introduction
examples code for Bai Du Ai SDK 
following examples are provided :
- scan image as a table 
- scan image as words

### Setup
to use these examples, please install BAI DU 
   run `pip install baidu-aip`
   run `pip install wget`
   run `pip install click`
   the API_KEY , APP_ID , SECRET_KEY should be provided in aip.conf under the folder with json format like :
   
```
{
  "aip":{
      "app_id" : "xxxxx",
      "api_key" : "xxxxxxxxxxxxxxxxx",
      "secret_key" : "xxxxxxxxxxxxxxxx"
  }
```

### Usage
```
Usage: ocrscan.py [OPTIONS]

Options:
  -c [table|word]
  -f TEXT          image file path
  -o TEXT          output file path
  -d TEXT          directory for batch file processing
  --help           Show this message and exit.
```
example:
python ocrscan.py -c table -f ./1.img


