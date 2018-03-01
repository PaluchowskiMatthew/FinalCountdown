#!/bin/bash 
#cd /root

if [ $# -eq 0 ]; then
    echo "must provide address email as first argument"
    exit 1
fi

EMAIL=$1

if [ ! -f credentials.cfg ]; then
    echo "credentials.cfg not found. exit"
    exit 1
fi

. credentials.cfg

if [ ! -v ROOT_PWD ]; then
    echo "provide ROOT_PWD variable"
    exit 1
fi

if [ ! -v USERNAME1 ]; then
    echo "provide USERNAME1 variable"
    exit 1
fi

if [ ! -v USER_PWD1 ]; then
    echo "provide USER_PWD1 variable"
    exit 1
fi

if [ ! -v DATABASE1 ]; then 
    echo "provide DATABASE1 variable"
    exit 1
fi

if [ ! -v USERNAME2 ]; then
    echo "provide USERNAME2 variable"
    exit 1
fi

if [ ! -v USER_PWD2 ]; then
    echo "provide USER_PWD2 variable"
    exit 1
fi

if [ ! -v DATABASE2 ]; then 
    echo "provide DATABASE2 variable"
    exit 1
fi

#echo "launching mysql ..."
#mysqld_safe --user=root --password=Tqkmwgyi2 2>&1 &
#sleep 2
#mysqladmin -uroot -pTqkmwgyi2 2>&1
#tfile=`mktemp`

#cat > $tfile <<HERE
#SET @@SESSION.SQL_LOG_BIN=0;
#DROP DATABASE IF EXISTS test;

#CREATE DATABASE IF NOT EXISTS $DATABASE1;
#CREATE USER IF NOT EXISTS '$USERNAME1'@'localhost' IDENTIFIED BY '$USER_PWD1';
#FLUSH PRIVILEGES;
#GRANT ALL ON $DATABASE1.* TO '$USERNAME1'@'localhost' IDENTIFIED BY '$USER_PWD1';

#CREATE DATABASE IF NOT EXISTS $DATABASE2;
#CREATE USER IF NOT EXISTS '$USERNAME2'@'localhost' IDENTIFIED BY '$USER_PWD2';
#FLUSH PRIVILEGES;
#GRANT ALL ON $DATABASE2.* TO '$USERNAME2'@'localhost' IDENTIFIED BY '$USER_PWD2';
#FLUSH PRIVILEGES;
#HERE


#echo "creating users ..."
#mysql -uroot -p$ROOT_PWD < $tfile 2>&1

## EXERCISE 1
#echo "creating table 1"
#cat > $tfile <<HERE
#USE $DATABASE1;
#CREATE TABLE personalities(id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#                         name varchar(100) not null);

#CREATE TABLE contact_messages(name varchar(100) not null,
#                      mail varchar(100) not null,
#                      message varchar(200) not null);
#HERE
#mysql -uroot -p$ROOT_PWD < $tfile 2>&1


## EXERCISE 2
#echo "creating table 2"
#cat > $tfile <<HERE
#USE $DATABASE2;
#CREATE TABLE users(name varchar(100) not null,
#                   password varchar(40) not null);

#CREATE TABLE contact_messages(name varchar(100) not null,
#                      mail varchar(100) not null,
#                      message varchar(200) not null);
#HERE

#mysql -uroot -p$ROOT_PWD < $tfile 2>&1
#rm $tfile

if [ $# -eq 1 ]; then
    echo "launching flask web app in foreground"
    python3 site.pyc $EMAIL 2>&1
    exit
fi

echo "launching flask web app in background"
python3 site.pyc $EMAIL 2>&1 &
sleep 1


shift
chown com402:com402 $1 

TIMEOUT=10
echo "launching user script $1 with timeout $TIMEOUT"
su com402 -c "timeout -t $TIMEOUT python3 $1 2>&1" 2>&1
