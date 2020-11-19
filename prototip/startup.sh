#! /bin/bash

# /etc/init.d/startup.sh
### BEGIN INIT INFO
# Provides:          startup.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

# Relés
gpio write 0 1
gpio write 1 1
gpio mode 0 out
gpio mode 1 out
#gpio write 0 1
#gpio write 1 1

# Botons
gpio mode 4 out
gpio mode 5 out
gpio write 4 1
gpio write 5 1

# Sensors humitat

# 1
gpio mode 21 out
gpio mode 22 in
gpio write 21 0

# 2
gpio mode 23 out
gpio mode 24 in
gpio write 23 0

# Fi
echo "GPIO config set"

