echo "date;hostname;cat /etc/*release;uname -a;"
date;hostname;cat /etc/*release;uname -a;rpm -qa| grep -i openssh;
