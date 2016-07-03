#!/usr/bin/env bash

echo "Decompressing...."
if unzip live_cricket_score.zip -d /opt/; then
    echo "Decompression done successfully."
else
    echo "Failed to decompress :("
    exit 1
fi

echo "Creating desktop entry...."
if sudo mv /opt/live_cricket_score/live-cricket-score.desktop /usr/share/applications/; then
    echo "Desktop entry created."
else
    echo "Failed to create desktop entry :("
    echo "Cleaning mess...."
    if rm -rf /opt/live_cricket_score; then
        echo "Mess cleaned. Try again."
        exit 1
    else
        echo "Failed to clean mess too >:( .Delete '/opt/live_cricket_score' folder manually."
    fi
    exit 1
fi

echo "Setting permissions.... Don't worry though :)"
if sudo chmod 775 /usr/share/applications/live-cricket-score.desktop; then
    sudo chmod 755 /opt/live_cricket_score
    sudo chmod 755 /opt/live_cricket_score/run.sh
    sudo chmod 755 /opt/live_cricket_score/core.py
    sudo chmod 755 /opt/live_cricket_score/icon.svg
else
    echo "Failed to set permissions :("
    echo "Cleaning mess...."
    if rm -rf /opt/live_cricket_score; then
        if rm /usr/share/applications/live-cricket-score.desktop; then
            echo "Mess cleaned. Try again."
            exit 1
        else
            echo "Failed to clean mess too >:( .Delete '/usr/share/applications/live-cricket-score.desktop' manually."
            exit 1
        fi
    else
        echo "Failed to clean mess too >:( .Delete '/opt/live_cricket_score' folder & '/usr/share/applications/live-cricket-score.desktop' manually."
    fi
    exit 1
fi