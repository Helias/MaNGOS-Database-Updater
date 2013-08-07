#Coded By Helias

try:
	import MySQLdb
except:
	print ("You must install python-mysqldb, type: apt-get install python-mysqldb or check the configuration")

import os
import commands

#Configuration
youruser="" #your home folder
username="" # username of your account mysql
password="" # password of your account mysql
database_mangos=""
database_characters=""
database_realmd=""
#End Configuration

t=0
while t<3:
	os.system("mkdir ~/updater_tmp")
	if t==0:
		DataBase=database_mangos
		sql=("SHOW COLUMNS FROM db_version FROM %s"% database_mangos)
	elif t==1:
		DataBase=database_characters
		sql=("SHOW COLUMNS FROM character_db_version FROM %s"% database_characters)
	elif t==2:
		DataBase=database_realmd
		sql=("SHOW COLUMNS FROM realmd_db_version FROM %s"% database_realmd)

	conn=MySQLdb.connect(host="localhost", user=username, passwd=password, db=DataBase)
	cursor=conn.cursor()
	sql+=" WHERE Field LIKE '%required%';"
	cursor.execute(sql)
	row=cursor.fetchone()
	file=row[0]
	file=file.replace("required_", "")
	cursor.close()
	conn.close()

	if(file.find(DataBase)>-1):
		m=0
		n=1
		while(m<20):
			try:
				x=int(file[m:n])
			except:
				x=0
				break
			m+=1
			n+=1
	v=len(file[0:n-1])
	a=""
	i=0
	while i<v:
		a+="*"
		i+=1

	a+=("_**_%s*.sql"% DataBase)
	os.system("cp ~/sources/mangos/sql/updates/%s ~/updater_tmp/"% a)

	x=commands.getoutput("ls ~/updater_tmp")
	list=x.split("\n")
	h=int(file[0:n-1])
	i=0
	for m in list:
		if int(list[i][0:5])<h:
			os.system("rm ~/updater_tmp/%s"% list[i])
		else:
			break
		i+=1
	os.system("rm ~/updater_tmp/%s.sql"% file)

	x=commands.getoutput("ls ~/updater_tmp")
	
	lenx=x.find("\n")
	j=len(x)
	x=x[lenx+1:j]
	
	list=x.split("\n")
	i=0
	mustup=1
	update=""
	for m in list:
		try:
			files=open("/home/%s/updater_tmp/%s"% (youruser, list[i]), "r").read()
			code=("-- %s \n\n %s \n\n"% (list[i], files))
			update+=code
			i+=1
		except:
			mustup=0
			print ("Your database %s is already updated"% DataBase)
			break
	os.system("rm -r ~/updater_tmp/")
	if mustup==1:
		print("I'm importing these files \n %s \n On %s"% (x, DataBase))
		conn=MySQLdb.connect(host="localhost", user=username, passwd=password, db=DataBase)
		cursor=conn.cursor()
		cursor.execute(update)
		cursor.close()
		conn.close()
	t+=1