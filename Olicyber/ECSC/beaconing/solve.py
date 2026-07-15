import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import re


if __name__ == '__main__':
    tree = ET.parse('logs.xml')
    root = tree.getroot()
    queries = []
    decrypted = b''
    
    ns = {
        "ev": "http://schemas.microsoft.com/win/2004/08/events/event"
    }

    for event in root:
        evid = event.find('.//ev:EventID', ns).text

        if evid is not None and evid == '22':
            qs = int(event.find('.//ev:Data[@Name="QueryStatus"]', ns).text)
            
            if qs == 9003:
                qn = event.find('.//ev:Data[@Name="QueryName"]', ns).text
                
                if '8BD45a6fed311339f9e9353e1f1f9f14e1b6A3F67' in qn:
                    queries.append(qn)

    queries = queries[::-1]
    
    key = bytes.fromhex(queries[1].split(".")[0])
    iv = bytes.fromhex(queries[2].split(".")[0])
    
    cp = AES.new(key, AES.MODE_CBC, iv=iv)
    
    for q in queries[3:]:
        decrypted += unpad(cp.decrypt(bytes.fromhex(q.split(".")[0])), AES.block_size)
    
    decrypted = decrypted.decode()
    decrypted = re.findall(r'ECSC{(.+)}', decrypted)[0]
    
    print('ECSC{%s}' % decrypted)