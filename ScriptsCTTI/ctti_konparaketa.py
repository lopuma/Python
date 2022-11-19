#! /usr/bin/env python3
import os
def fitxeroa_lerroka_irakurri(fitxeroa):
        lssecfix_rhsa = set()

        with open(fitxeroa) as file:
                line = file.readline()
                while line:                
                        if line[0] == "R":
                                lssecfix_rhsa.add(line[0:14])
                        line=file.readline()
        return(lssecfix_rhsa)

def fitxeroa_lerroka_irakurri_yum(fitxeroa):
        yum_rhsa = set()

        with open(fitxeroa) as file:
                line = file.readline()
                while line: 
                             
                        if line[0] == "0" or line[0] == "1" or line[0] == "2" or line[0] == "3":  
                                if line[35] == "R":
                                        yum_rhsa.add(line[35:49])
                                elif line[36] == "R":
                                        yum_rhsa.add(line[36:50])
                        line=file.readline()
        return(yum_rhsa)

def fitxategia_idatzi(test1,test2,zerb):
        with open("Emaitza.txt", 'a+') as f:
                print(zerb)
                f.write("ZERBITZARIA: " + zerb[:-4])
                f.write("\n")
                f.write("RHSA que no existe en yum: \n" )
                f.write(str(test1))
                f.write("\n")
                f.write("RHSA que instala de más: \n" )
                f.write(str(test2))
                f.write("\n")
                f.write(" \n")
        
        f.close()

def konparaketa(fitxategia_yum,fitxategia_lsfix):
        


        fitx2 = fitxeroa_lerroka_irakurri(fitxategia_yum)
        fitx1 = fitxeroa_lerroka_irakurri_yum(fitxategia_lsfix)
        f_izena = str(fitxategia_lsfix).split("/")
        zerbitzari_izena = f_izena[-1]       
        rhsa_yum_ez_emaitza = fitx1.difference(fitx2)
        rhsa_lsfix_ez_emaitza = fitx2.difference(fitx1)
        fitxategia_idatzi(rhsa_yum_ez_emaitza, rhsa_lsfix_ez_emaitza ,zerbitzari_izena)
        



yum_files=[]
lsfix_files=[]

direktorioa = os.getcwd()
if os.path.exists(direktorioa+"/Emaitza.txt"):
        os.remove(direktorioa+"/Emaitza.txt")
yum_direktorioa = direktorioa+"/yum/" 
lsfix_direktorioa = direktorioa +"/lssecfixes/"
yum_files = os.listdir(yum_direktorioa)
lsfix_files = os.listdir(lsfix_direktorioa)
yum_luz = len(yum_files)
lsfix_luzera = len(lsfix_files)
if lsfix_luzera > yum_luz:
        print("Falta algún fitxero de yum")
elif yum_luz > lsfix_luzera:
        print("Falta algún fitxero de lsfix")


for fitx_l in lsfix_files:
        for fitx_y in  yum_files:
                if str(fitx_l[:-4]) == str(fitx_y[:-8]):
                        konparaketa(yum_direktorioa+fitx_y,lsfix_direktorioa+fitx_l)              




