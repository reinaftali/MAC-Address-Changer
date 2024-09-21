#!/usr/bin/env python

import re
import subprocess
import optparse

def get_arguments():
    parser = optparse. OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to" + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

ascii_art = '''

  __  __          _____               _     _                   
 |  \/  |   /\   / ____|     /\      | |   | |                  
 | \  / |  /  \ | |         /  \   __| | __| |_ __ ___  ___ ___ 
 | |\/| | / /\ \| |        / /\ \ / _` |/ _` | '__/ _ \/ __/ __|
 | |  | |/ ____ \ |____   / ____ \ (_| | (_| | | |  __/\__ \__ \\
 |_|  |_/_/ ___\_\_____| /_/    \_\__,_|\__,_|_|  \___||___/___/
           / ____| |                                            
          | |    | |__   __ _ _ __   __ _  ___ _ __             
          | |    | '_ \ / _` | '_ \ / _` |/ _ \ '__|            
          | |____| | | | (_| | | | | (_| |  __/ |               
           \_____|_| |_|\__,_|_| |_|\__, |\___|_|               
                                     __/ |                      
                                    |___/                       

'''
print("\033[92m" + ascii_art + "\033[0m")
options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to "+ current_mac)
else:
    print("[-] MAC address did not get changed.")