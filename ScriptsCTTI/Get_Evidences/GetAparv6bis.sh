#!/bin/bash

############################################################################################################################
#
#	Fecha:	 08/06/2014
#
#	Autor:   Juan Extreme
#	Empresa: Iru Ederra XXI
#
#	Descripción: Se connecta por plink, lanza comandos almacenados en un fichero y obtiene evidencias en formato Imagen.
#	Requisitos:  Completar archivos de configuracion
#		     Aplicacion plink para automatización de las conexiones
#		     Aplicacion Shutter para captura de imagenes.
#
#	Ejecución:  ./GetApar.sh
#
############################################################################################################################

clear
salir=n

#Pedir los datos para validarnos en los servidores

GetUserInfo(){
	echo
	echo
	echo " ===================================================="
	echo "|                INTRODUCE TUS DATOS                 |"
	echo " ===================================================="
	echo
	echo 
	read -p "Teclea tu usuario: " User
	read -s -p "Teclea tu password: " Password
	echo
	echo 
	echo

	HomeDir=/home/$User
	FileServers=$(ls ./Conf/*.server)

	echo -e "\033[0;34m Ficheros de servidores disponibles: \033[0m"
	echo " ===================================================="
	echo 
	i=0
	for item in ${FileServers[*]};do
		echo $i")	"$item
		ArrFiles[$i]=$item
		((i++))
	done

	echo 
	echo " ===================================================="
	echo
	echo -e "\033[0;34m Selecciona una opcion: \033[0m";read File

	Servers=${ArrFiles[$File]} 
	echo -e $Servers

}

#Pedir los datos necesarios para la ejecucion de comandos en remoto con plink y generar la carpeta local para las evidencias

GetPlinkInfo(){

	read -p "Teclea el número de Apar: " Apar

	mkdir ./Evidences/$Apar
	mkdir ./Evidences/$Apar/Resultado
	mkdir ./Evidences/$Apar/Afectadas 

	echo
	echo
	echo
	for item in ${ArrServers[*]};do
		echo -e $item >>./Evidences/$Apar/ListaMaquinas
	done

	FALLIDOS=./Evidences/$Apar/Fallidos_$Apar.txt 

	FileCommands=$(ls ./Conf/*.com)

	i=0
	for item in ${FileCommands[*]};do
		echo $i "	"$item
		ArrCommands[$i]=$item
		((i++))
	done

	echo -e "\033[0;34m Escriba una opcion: \033[0m";read Command

	Commands=${ArrCommands[$Command]} 
	echo -e $Commands

}

#Pedir los datos necesarios para la carpeta a crear/borrar en los servidores

GetFolderInfo(){

	echo
	read -p "Teclea el nombre de la carpeta: " Folder

	FolderPath=$HomeDir/$Folder
	echo -e "La ruta es: " $FolderPath

}

#Recogemos los nombres e ips en Arrays 

GetServersInfo(){

	i=0
	while read line; do
		IFS=';' read -a ArrResultado <<< "$line"
		ArrIps[$i]=${ArrResultado[0]}
		ArrServers[$i]=${ArrResultado[1]} 
		((i++))
	done < $Servers
}

GetPscpInfo(){

	UploadFolders=$(ls ./Upload)

	echo -e "\033[0;34m Elige la  carpeta a subir al servidor: \033[0m"
	echo " ===================================================="
	echo 
	i=0
	for item in ${UploadFolders[*]};do
		echo $i")	"$item
		ArrFolders[$i]=$item
		((i++))
	done

	echo
	echo " ===================================================="
	echo
	echo -e "\033[0;34m Selecciona una opcion: \033[0m";read Folder

	UFolder=${ArrFolders[$Folder]} 

	UFolder="./Upload/"$UFolder

}

#Verificamos si los servidores están registrados en nuestro equipo
#Pendiente de verificar ssh-keyscan -H <ip-address> >> ~/.ssh/known_hosts
#ssh-keyscan -H <hostname> >> ~/.ssh/known_hosts
#ssh-keyscan -t rsa <ip-address> >> ~/.ssh/known_hosts
#cat ~/.ssh/known_hosts | grep <ip-address>

#GetCheckServers{

#echo y | plink -ssh user@ip exit

#}

#Lanzamos los comandos con plink

PlinkCommand(){

	Fallidos=./Evidences/$Apar/Fallidos_$Apar.txt
	i=0

	for item in ${ArrIps[*]};do

		clear
		#echo y | plink -ssh -pw $Password $User@$item < ./$Commands
		echo y | plink -ssh -pw $Password $User@$item -m ./$Commands

		if [ "$?" = "0" ]; then
#			shutter --window=Terminal -d 1 -C -o ./Evidences/$Apar/Resultado/${ArrServers[$i]}.jpg -n -e --disable_systray &>/dev/null
			shutter -a -d 1 -C -o ./Evidences/$Apar/Resultado/${ArrServers[$i]}.jpg -n -e --disable_systray &>/dev/null
#			shutter -a -d 1 -C -o "${VarExportPath}/$aparNumber/$aparNumber"_"${ArrResultado[1]}.png" -n -e --disable_systray &>/dev/null

		else
			echo -e $item >>$Fallidos
		fi

		((i++))
	done
	ProcesoTerminado;

}

PlinkCommandFile(){

	Fallidos=./Evidences/$Apar/Fallidos_$Apar.txt
	# Result=./Evidences/$Apar/Resultado_$Apar.txt
	i=0

	for item in ${ArrIps[*]};do

		clear
		#echo y | plink -ssh -pw $Password $User@$item < ./$Commands > ./Evidences/$Apar/Resultado/${ArrServers[$i]}.txt
		echo y | plink -ssh -pw $Password $User@$item -m ./$Commands > ./Evidences/$Apar/Resultado/${ArrServers[$i]}.txt

		((i++))
	done
	ProcesoTerminado;

}

PscpCommand(){

	Fallidos=./Evidences/$Apar/Servidores_Fallidos.txt

	i=0
	for item in ${ArrIps[*]};do

		sshpass -p $Password scp -r $UFolder $User@$item:$HomeDir


		if [ "$?" = "0" ]; then
			echo -e upload ok
		else
			echo -e $item "  " No se han podido subir los ficheros >>$Fallidos
		fi

	done
	ProcesoTerminado;

}

Finalizar (){

	echo -e "\033[0;31m ¿Seguro que desea salir del programa? (y/n) \033[0m"
	read salir

}

PlinkDeleteFolder(){

	Fallidos=./Evidences/$Apar/Servidores_Fallidos_DeleteFolder.txt

	i=0
	for item in ${ArrIps[*]};do
		plink -pw $Password $User@$item rm -R $FolderPath

		if [ "$?" = "0" ]; then
			echo
		else 
			echo -e $item >>$Fallidos
		fi
	done
	ProcesoTerminado;

}

# Mensaje de proceso terminado con formato

ProcesoTerminado (){

	echo
	echo
	echo " ===================================================="
	echo "|                                                    |"
	echo "|                PROCESO FINALIZADO                  |"
	echo "|                                                    |"
	echo " ===================================================="
	echo
	echo "Revisa el fichero de Fallidos"
	echo
	echo "Pulse una tecla para continuar....."
	read pausa

}

# Main

GetUserInfo;

GetServersInfo

while [ $salir != y ]
do
	clear
	echo
	echo
	echo " ===================================================="
	echo -e "\033[0;34m Elige una opcion: \033[0m"
	echo " ===================================================="
	echo
	echo
	echo -e "a) Sacar Pantallazos de Evidencias"
	echo -e "b) Sacar Evidencias a fichero"
	echo -e "c) Subir carpeta por scp"
	echo -e "d) Borrar una carpeta"
	echo -e "e) Listar carpetas de nuestro perfil en el servidor"
	echo -e "q) Salir"
	echo
	echo -e "\033[0;34m Escriba una opcion: \033[0m";read Opcion

	case $Opcion in
		a)	GetPlinkInfo
			PlinkCommand;;
		b)	GetPlinkInfo
			PlinkCommandFile;;
		c)	GetPscpInfo
			PscpCommand;;
		d)	GetFolderInfo
			PlinkDeleteFolder;;
		e)	echo -e En proceso;;	
		q)	Finalizar;;

	esac
done
