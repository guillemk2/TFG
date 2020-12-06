#!/bin/bash

# Obtenir última versió del codi
git --work-tree=/home/pi/TFG/ --git-dir=/home/pi/TFG/.git pull origin dev

# Posar en marxa servidor des d'ubicació remota
npm --prefix ~/TFG/server/ run start &

# Posar en marxa prometheus
/usr/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

# Posar en marxa prototip:
python3 /home/pi/TFG/prototip/main.py