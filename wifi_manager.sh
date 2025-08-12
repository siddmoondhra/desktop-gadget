#!/bin/bash

# hotspot_fallback.sh - Create WiFi hotspot when no internet connection
# This allows you to connect directly to the Pi when it can't reach WiFi

HOTSPOT_SSID="PiDevice_Setup"
HOTSPOT_PASS="raspberry123"

check_internet() {
    ping -c 1 8.8.8.8 >/dev/null 2>&1
    return $?
}

setup_hotspot() {
    echo "No internet detected, setting up access point..."
    
    # Install required packages
    sudo apt-get update
    sudo apt-get install -y hostapd dnsmasq
    
    # Stop services
    sudo systemctl stop hostapd
    sudo systemctl stop dnsmasq
    
    # Configure hostapd
    sudo tee /etc/hostapd/hostapd.conf > /dev/null <<EOF
interface=wlan0
driver=nl80211
ssid=${HOTSPOT_SSID}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=${HOTSPOT_PASS}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

    # Configure dnsmasq
    sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup
    sudo tee /etc/dnsmasq.conf > /dev/null <<EOF
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF

    # Configure static IP
    sudo tee -a /etc/dhcpcd.conf > /dev/null <<EOF

# Hotspot configuration
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
EOF

    # Enable and start services
    sudo systemctl enable hostapd
    sudo systemctl enable dnsmasq
    
    # Restart networking
    sudo systemctl restart dhcpcd
    sudo systemctl start hostapd
    sudo systemctl start dnsmasq
    
    echo "Hotspot active!"
    echo "Network: ${HOTSPOT_SSID}"
    echo "Password: ${HOTSPOT_PASS}"
    echo "Pi IP: 192.168.4.1"
    echo "SSH: ssh pi@192.168.4.1"
}

restore_wifi() {
    echo "Internet detected, restoring normal WiFi..."
    sudo systemctl stop hostapd
    sudo systemctl stop dnsmasq
    sudo systemctl disable hostapd
    sudo systemctl disable dnsmasq
    
    # Restore dhcpcd config
    sudo sed -i '/# Hotspot configuration/,$d' /etc/dhcpcd.conf
    
    sudo systemctl restart dhcpcd
}

# Main logic
if check_internet; then
    echo "Internet connection OK"
    # Make sure hotspot is disabled
    if systemctl is-active --quiet hostapd; then
        restore_wifi
    fi
else
    echo "No internet connection"
    sleep 30  # Wait a bit for WiFi to connect
    
    if ! check_internet; then
        echo "Still no internet, creating hotspot"
        setup_hotspot
    fi
fi