import xml.etree.ElementTree as ET
from argparse import ArgumentParser

argp = ArgumentParser('EVTX dumper')
argp.add_argument('-p', '--proc', action='store_true', help='Dump procs')
argp.add_argument('-v', '--values', action='store_true', help='Dump SetValue')
argp.add_argument('-f', '--files', action='store_true', help='Dump FileCreate')
argp.add_argument('-d', '--dns', action='store_true', help='Dump DNS query')
args = argp.parse_args()

ns = {
    "ev": "http://schemas.microsoft.com/win/2004/08/events/event"
}


def dump_procs(root: ET.Element):
    print("\n------------ PROCS DUMP ------------\n")
    for event in root:
        evid = event.find('.//ev:EventID', ns).text
        
        if evid is not None and evid == '1':
            pid = int(event.find('.//ev:Data[@Name="ProcessId"]', ns).text)
            cmd = event.find('.//ev:Data[@Name="CommandLine"]', ns).text
            img = event.find('.//ev:Data[@Name="Image"]', ns).text
            parent = event.find('.//ev:Data[@Name="ParentProcessId"]', ns)
            
            parent = parent.text if parent is not None else "None"
            
            print(f'------ Process ------\nProc ID: {pid}\nParent ID: {parent}\nImage: {img}\nCMD: {cmd}\n')


def dump_values(root: ET.Element):
    print("\n------------ SET-VALUES DUMP ------------\n\n")
    for event in root:
        evid = event.find('.//ev:EventID', ns).text
        
        if evid is not None and evid == '13':
            pid = int(event.find('.//ev:Data[@Name="ProcessId"]', ns).text)
            dt = event.find('.//ev:Data[@Name="Details"]', ns).text
            target = event.find('.//ev:Data[@Name="TargetObject"]', ns).text
            img = event.find('.//ev:Data[@Name="Image"]', ns).text
                        
            print(f'------ Value ------\nProc ID: {pid}\nImage: {img}\nTarget: {target}\nDetails: {dt}\n')


def dump_files(root: ET.Element):
    print("\n------------ FILE-CREATE DUMP ------------\n\n")
    for event in root:
        evid = event.find('.//ev:EventID', ns).text
        
        if evid is not None and evid == '11':
            pid = int(event.find('.//ev:Data[@Name="ProcessId"]', ns).text)
            img = event.find('.//ev:Data[@Name="Image"]', ns).text
            tf = event.find('.//ev:Data[@Name="TargetFilename"]', ns).text
                        
            print(f'------ File ------\nProc ID: {pid}\nImage: {img}\nTarget: {tf}\n')
            
            
def dump_dns(root: ET.Element):
    print("\n------------ DNS QUERY DUMP ------------\n\n")
    for event in root:
        evid = event.find('.//ev:EventID', ns).text
        
        if evid is not None and evid == '22':
            pid = int(event.find('.//ev:Data[@Name="ProcessId"]', ns).text)
            img = event.find('.//ev:Data[@Name="Image"]', ns).text
            qn = event.find('.//ev:Data[@Name="QueryName"]', ns).text
            qs = event.find('.//ev:Data[@Name="QueryStatus"]', ns).text
            qr = event.find('.//ev:Data[@Name="QueryResults"]', ns).text
                        
            print(f'------ Dns ------\nProc ID: {pid}\nImage: {img}\nQuery Name: {qn}\nQuery Status: {qs}\nQuery Results: {qr}\n')


if __name__ == '__main__':
    tree = ET.parse('logs.xml')
    root = tree.getroot()
    
    if not args.proc and not args.values and not args.files and not args.dns:
        argp.print_help()
    
    else:
        if args.proc:
            dump_procs(root)
        
        if args.values:
            dump_values(root)
            
        if args.files:
            dump_files(root)
            
        if args.dns:
            dump_dns(root)