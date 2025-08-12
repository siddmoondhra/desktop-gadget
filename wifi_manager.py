import os
import subprocess
import time
import re

class EnhancedWiFiManager:
    def __init__(self, display, buttons):
        self.name = "WiFi Manager"
        self.display = display
        self.buttons = buttons
        
        # New networks to add (your girlfriend's WiFi, etc.)
        self.new_networks = {
            "TheCrib_5g": "22224444"
        }
        
        self.mode = "main"  # main, add, delete, saved
        self.current_selection = 0
        self.saved_networks = []
        self.new_network_names = list(self.new_networks.keys())
        
    def run(self):
        self._load_saved_networks()
        
        while True:
            if self.mode == "main":
                self._show_main_menu()
            elif self.mode == "add":
                self._show_add_menu()
            elif self.mode == "delete":
                self._show_delete_menu()
            elif self.mode == "saved":
                self._show_saved_networks()
                
            button = self.buttons.get_pressed()
            self._handle_input(button)
            time.sleep(0.1)
    
    def _show_main_menu(self):
        options = ["Add Networks", "Delete Networks", "View Saved", "Current Status"]
        current_option = options[self.current_selection % len(options)]
        
        current_wifi = self._get_current_wifi()
        display_text = f"WiFi Manager\n{current_option}\nNow: {current_wifi}"
        self.display.draw_centered_text(display_text)
    
    def _show_add_menu(self):
        if not self.new_network_names:
            self.display.draw_centered_text("No new networks\nto add")
            return
            
        network_name = self.new_network_names[self.current_selection % len(self.new_network_names)]
        self.display.draw_centered_text(f"Add Network\n{network_name}\nSelect to add")
    
    def _show_delete_menu(self):
        if not self.saved_networks:
            self.display.draw_centered_text("No saved networks\nto delete")
            return
            
        network_name = self.saved_networks[self.current_selection % len(self.saved_networks)]
        self.display.draw_centered_text(f"Delete Network\n{network_name}\nSelect to delete")
    
    def _show_saved_networks(self):
        if not self.saved_networks:
            self.display.draw_centered_text("No saved\nnetworks found")
            return
            
        network_name = self.saved_networks[self.current_selection % len(self.saved_networks)]
        status = "CONNECTED" if network_name == self._get_current_wifi() else "SAVED"
        self.display.draw_centered_text(f"{status}\n{network_name}")
    
    def _handle_input(self, button):
        if button == 'back':
            if self.mode == "main":
                return  # Exit app
            else:
                self.mode = "main"
                self.current_selection = 0
                
        elif button == 'up':
            self.current_selection -= 1
            time.sleep(0.2)
            
        elif button == 'down':
            self.current_selection += 1
            time.sleep(0.2)
            
        elif button == 'select':
            self._handle_select()
    
    def _handle_select(self):
        if self.mode == "main":
            options = ["add", "delete", "saved", "status"]
            selected = options[self.current_selection % len(options)]
            
            if selected == "status":
                self._show_status()
            else:
                self.mode = selected
                self.current_selection = 0
                
        elif self.mode == "add":
            if self.new_network_names:
                network_name = self.new_network_names[self.current_selection % len(self.new_network_names)]
                self._add_network(network_name)
                
        elif self.mode == "delete":
            if self.saved_networks:
                network_name = self.saved_networks[self.current_selection % len(self.saved_networks)]
                self._delete_network(network_name)
        
        elif self.mode == "saved":
            if self.saved_networks:
                network_name = self.saved_networks[self.current_selection % len(self.saved_networks)]
                self._connect_to_network(network_name)
    
    def _load_saved_networks(self):
        """Load list of saved WiFi networks from wpa_supplicant"""
        try:
            with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
                content = f.read()
            
            # Find all SSID entries
            ssid_matches = re.findall(r'ssid="([^"]+)"', content)
            self.saved_networks = list(set(ssid_matches))  # Remove duplicates
            
        except Exception as e:
            print(f"Error loading saved networks: {e}")
            self.saved_networks = []
    
    def _get_current_wifi(self):
        """Get currently connected WiFi SSID"""
        try:
            result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except:
            pass
        return "None"
    
    def _show_status(self):
        """Show detailed WiFi status"""
        current_wifi = self._get_current_wifi()
        total_saved = len(self.saved_networks)
        
        self.display.draw_centered_text(f"WiFi Status\nConnected: {current_wifi}\nSaved: {total_saved} networks")
        time.sleep(3)
    
    def _add_network(self, network_name):
        """Add a new network to wpa_supplicant"""
        password = self.new_networks[network_name]
        
        self.display.draw_centered_text(f"Adding\n{network_name}...")
        
        try:
            self._add_network_to_config(network_name, password)
            self.display.draw_centered_text(f"Added!\n{network_name}")
            
            # Remove from new networks list
            del self.new_networks[network_name]
            self.new_network_names = list(self.new_networks.keys())
            
            # Refresh saved networks
            self._load_saved_networks()
            
        except Exception as e:
            self.display.draw_centered_text(f"Error adding\n{network_name}")
            
        time.sleep(2)
    
    def _delete_network(self, network_name):
        """Delete a network from wpa_supplicant"""
        self.display.draw_centered_text(f"Deleting\n{network_name}...")
        
        try:
            self._remove_network_from_config(network_name)
            self.display.draw_centered_text(f"Deleted!\n{network_name}")
            
            # Refresh saved networks
            self._load_saved_networks()
            
            # Reset selection if needed
            if self.current_selection >= len(self.saved_networks):
                self.current_selection = max(0, len(self.saved_networks) - 1)
                
        except Exception as e:
            self.display.draw_centered_text(f"Error deleting\n{network_name}")
            
        time.sleep(2)
    
    def _connect_to_network(self, network_name):
        """Force connection to a specific network"""
        self.display.draw_centered_text(f"Connecting to\n{network_name}...")
        
        try:
            # Restart WiFi to trigger reconnection
            subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], check=True)
            time.sleep(5)
            
            current = self._get_current_wifi()
            if current == network_name:
                self.display.draw_centered_text(f"Connected!\n{network_name}")
            else:
                self.display.draw_centered_text(f"Connection failed\nTrying: {network_name}")
                
        except Exception as e:
            self.display.draw_centered_text(f"Error connecting\n{network_name}")
            
        time.sleep(3)
    
    def _add_network_to_config(self, ssid, password):
        """Add network to wpa_supplicant configuration"""
        config_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
        
        # Read existing config
        with open(config_path, 'r') as f:
            config_content = f.read()
        
        # Check if network already exists
        if f'ssid="{ssid}"' in config_content:
            raise Exception("Network already exists")
        
        # Add new network block
        network_block = f"""
network={{
    ssid="{ssid}"
    psk="{password}"
    priority=5
}}
"""
        config_content += network_block
        
        # Write back to config
        temp_file = '/tmp/wpa_temp.conf'
        with open(temp_file, 'w') as f:
            f.write(config_content)
            
        subprocess.run(['sudo', 'cp', temp_file, config_path], check=True)
        os.remove(temp_file)
    
    def _remove_network_from_config(self, ssid):
        """Remove network from wpa_supplicant configuration"""
        config_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
        
        # Read existing config
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Find and remove the network block
        # Look for the network block that contains this SSID
        lines = content.split('\n')
        new_lines = []
        in_network_block = False
        skip_network = False
        
        for line in lines:
            if line.strip().startswith('network={'):
                in_network_block = True
                skip_network = False
                current_block = [line]
            elif in_network_block and line.strip() == '}':
                current_block.append(line)
                in_network_block = False
                
                # Check if this block contains our SSID
                block_content = '\n'.join(current_block)
                if f'ssid="{ssid}"' not in block_content:
                    # Keep this block
                    new_lines.extend(current_block)
                # If it contains our SSID, we skip it (delete it)
                
            elif in_network_block:
                current_block.append(line)
            else:
                new_lines.append(line)
        
        # Write back to config
        new_content = '\n'.join(new_lines)
        temp_file = '/tmp/wpa_temp.conf'
        with open(temp_file, 'w') as f:
            f.write(new_content)
            
        subprocess.run(['sudo', 'cp', temp_file, config_path], check=True)
        os.remove(temp_file)