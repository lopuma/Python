echo "date;hostname;uptime;oslevel -s;/home/y9deap/lssecfixesSeptiembre03_Aix_21/lssecfixes -n;"
date;hostname;uptime;oslevel -s;
echo "========================================================================================="
/home/y9deap/lssecfixesSeptiembre03_Aix_21/lssecfixes -n;
echo "========================================================================================="
lslpp -L;emgr -P;
echo "========================================== end =========================================="
