#!/bin/bash

# replace <domain> with yours
# replace <sub> with yours
# replace <path> with a path to your authorised ssh key

declare -i att=0
if pidof -o %PPID -x "checker.sh">/dev/null; then
	echo "$(date) Process already running" >> /home/pi/Programs/dynv6-updtr/logg.txt
	exit 0
fi
declare got="0"
while [ "$got" != "1" ];do
	sleep 1
	got=$(ssh -q -o "StrictHostKeyChecking no" -i <path> api@dynv6.com hosts <domain> records | grep -c "<sub>")
	if [[ "$got" != "1" ]]; then
		ssh -q -o "StrictHostKeyChecking no" -i <path> api@dynv6.com hosts <domain> records del <sub> a
		sleep 2
		ssh -q -o "StrictHostKeyChecking no" -i <path> api@dynv6.com hosts <domain> records set <sub> a
    		echo "$(date) Ran replace, attempt: $att" >> /home/pi/Programs/dynv6-updtr/logg.txt
	fi
	att+=1
done
