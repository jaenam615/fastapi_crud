#!/bin/bash
set -e

echo "===> Creating replication user on MASTER"

mysql -u root -ppassword <<EOF
CREATE USER IF NOT EXISTS 'repl'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;

-- Required for replicas to connect cleanly
FLUSH TABLES WITH READ LOCK;
EOF

echo "===> Master initialization done"
