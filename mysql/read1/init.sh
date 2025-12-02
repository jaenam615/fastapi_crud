#!/bin/bash
set -e

echo "===> Configuring REPLICA 1"

mysql -u root -ppassword <<EOF
STOP SLAVE;

CHANGE MASTER TO
  MASTER_HOST='mysql_write',
  MASTER_USER='repl',
  MASTER_PASSWORD='repl_password',
  MASTER_PORT=3306,
  MASTER_AUTO_POSITION=1;

START SLAVE;
EOF

echo "===> Replica 1 replication started"
