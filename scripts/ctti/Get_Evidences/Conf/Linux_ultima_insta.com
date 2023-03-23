hostname;cat /etc/*release|grep -i release;rpm -qa --last|head -n 1
