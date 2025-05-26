#!/bin/bash

# Load .env
source .env

echo "🌐 Choose network:"
select OPTION in "WiFi" "LAN"; do
    case $OPTION in
        WiFi ) JETSON_HOST=$JETSON_IP_WIFI; break;;
        LAN ) JETSON_HOST=$JETSON_IP_LAN; break;;
        * ) echo "Invalid option";;
    esac
done

# Sync
echo "🔄 Syncing project to $JETSON_HOST..."
rsync -avz --exclude-from=.rsync-exclude ./ "$JETSON_USER@$JETSON_HOST:$JETSON_PATH"