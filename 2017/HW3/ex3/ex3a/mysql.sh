echo "launching mysql ..."
mysqld_safe --user=root 2>&1 &
sleep 2
mysqladmin -u root password "$ROOT_PWD" 2>&1
tfile=`mktemp`

cat > $tfile <<HERE
SET @@SESSION.SQL_LOG_BIN=0;
DROP DATABASE IF EXISTS test;

CREATE DATABASE IF NOT EXISTS $DATABASE1;
CREATE USER IF NOT EXISTS '$USERNAME1'@'localhost' IDENTIFIED BY '$USER_PWD1';
FLUSH PRIVILEGES;
GRANT ALL ON $DATABASE1.* TO '$USERNAME1'@'localhost' IDENTIFIED BY '$USER_PWD1';

CREATE DATABASE IF NOT EXISTS $DATABASE2;
CREATE USER IF NOT EXISTS '$USERNAME2'@'localhost' IDENTIFIED BY '$USER_PWD2';
FLUSH PRIVILEGES;
GRANT ALL ON $DATABASE2.* TO '$USERNAME2'@'localhost' IDENTIFIED BY '$USER_PWD2';
FLUSH PRIVILEGES;
HERE


echo "creating users ..."
mysql -uroot -p$ROOT_PWD < $tfile 2>&1

## EXERCISE 1
echo "creating table 1"
cat > $tfile <<HERE
USE $DATABASE1;
CREATE TABLE personalities(id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                         name varchar(100) not null);

CREATE TABLE contact_messages(name varchar(100) not null,
                      mail varchar(100) not null,
                      message varchar(200) not null);
HERE
mysql -uroot -p$ROOT_PWD < $tfile 2>&1
                                               
