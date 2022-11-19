echo "date;hostname;cat /etc/*release;uname -a;uptime;/home/ESY9DEAP/lssecfixes_20210409/lssecfixes"
date;hostname;cat /etc/*release;uname -a;uptime;/home/ESY9DEAP/lssecfixes_20210409/lssecfixes -n; 
