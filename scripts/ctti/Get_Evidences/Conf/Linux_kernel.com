echo "date;hostname;uptime;cat /etc/*release;uname -a;rpm -qa | grep -i kernel"
date;hostname;uptime;cat /etc/*release;uname -a;rpm -qa | grep -i kernel; 

