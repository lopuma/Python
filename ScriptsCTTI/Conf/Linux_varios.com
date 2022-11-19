echo "date;hostname;uptime;cat /etc/*release;uname -a;rpm -qa | grep -i ghostscript"
date;hostname;uptime;cat /etc/*release;uname -a;rpm -qa | grep -i ghostscript
#date;hostname;prtconf | grep "System Model"

