echo "date;hostname;uptime;uname -a;cat /etc/*release;/home/y9deap/lssecfixesSeptiembre22_Linux_21/lssecfixes -n;rpm -qa --last|sort;"
date;hostname;uptime;uname -a;cat /etc/*release;
echo "========================================================================================="
/home/y9deap/lssecfixesSeptiembre22_Linux_21/lssecfixes -n;
echo "========================================================================================="
rpm -qa --last|sort;
echo "========================================== end =========================================="
