#!/usr/bin/python3
# low effort script to get the job done

import requests
import sys
from systemd import journal

def main(zone, hostname, token, ip="", dryrun="False"):
    stream = journal.stream('dynv6-api2')
    stream.write(f"Dynv6 script running for: {zone} {hostname} {ip}\n")
    header = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    zoneurl = ""
    recordd = None

    response = requests.get("https://dynv6.com/api/v2/zones", headers=header)
    if response.status_code == 200:
        zones = response.json()
        for zonee in zones:
            if zonee["name"] == zone:
                idd = zonee["id"]
                zoneurl = f"https://dynv6.com/api/v2/zones/{idd}/records"
                del idd
                break
    else:
        stream.write("error\n")
        exit(1)
    
    del response
    del zones
    
    response = requests.get(zoneurl, headers=header)
    if response.status_code == 200:
        records = response.json()
        for record in records:
            if record["name"] == hostname:
                recordd = record
                break
    else:
        stream.write("error\n")
        exit(1)
    
    del records
    del response
    
    payload = {'type': 'A', 'name': hostname, 'data': ip, 'priority': None, 'flags': None, 'tag': None, 'weight': None, 'port': None}
    
    if recordd is not None:
        if recordd["data"] != ip:
            print("Record exists. Different ip, editing")
            if dryrun == "False":
                response = requests.patch(zoneurl, data=payload, headers=header)
                del response
            else:
                stream.write("dryrun\n")
        else:
            stream.write("Already up to date.\n")
    else:
        stream.write("Not found. Creating\n")
        if dryrun == "False":
            response = requests.post(zoneurl, data=payload, headers=header)
            del response
        else:
            stream.write("dryrun\n")
    del payload

if __name__ == "__main__":
    listt = sys.argv
    listt.remove(listt[0])
    if len(listt) == 3:
        main(listt[0], listt[1], listt[2])
    elif len(listt) == 4:
        if listt[3] == "True" or listt[3] == "False":
            main(listt[0], listt[1], listt[2], dryrun=listt[3])
        else:
            main(listt[0], listt[1], listt[2], ip=listt[3])
    elif len(listt) == 5:
        main(listt[0], listt[1], listt[2], ip=listt[3], dryrun=listt[4])
    else:
        print("No")
