echo "SPECTRE"
date;hostname;cat /etc/*release;uname -a;uptime;
rpm -qa | grep -i microcode | sort;
rpm -qa | grep -i python-paramiko | sort;
rpm -qa | grep -i patch | sort;
rpm -qa | egrep 'kernel|perf' | sort;
rpm -qa | grep -i perf | sort;
rpm -qa | grep -i dhc | sort;
rpm -qa | grep -i ghostscript | sort;
