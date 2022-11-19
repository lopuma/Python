echo "date;hostname;uptime;uname -a;cat /etc/*release;/home/y9djay/LssecfixesLinux_Sept2021/lssecfixes -n;rpm -qa --last|sort;"
date;hostname;uptime;uname -a;cat /etc/*release;
echo "========================================================================================="
/home/y9djay/LssecfixesLinux_Sept2021/lssecfixes -n;
echo "========================================================================================="
rpm -qa --last|sort;
echo "========================================== end =========================================="
