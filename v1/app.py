# This is a Flask web application that calculates information about IP networks and their complementary ranges
from flask import Flask, render_template, request, jsonify
import ipaddress  # Python's built-in IP address manipulation library
from typing import List, Set

# Initialize Flask web application
app = Flask(__name__)

# Calculate details about a single subnet (IP network range)
def calculate_subnet(cidr):
    try:
        # Convert CIDR notation (like "192.168.1.0/24") to a network object
        network = ipaddress.ip_network(cidr, strict=False)
        
        # Special handling for /32 networks (single IP)
        if network.prefixlen == 32:
            return {
                'firstIP': str(network.network_address),
                'lastIP': str(network.network_address),
                'totalHosts': 1
            }
        # Special handling for /31 networks (two IPs)
        elif network.prefixlen == 31:
            return {
                'firstIP': str(network[0]),
                'lastIP': str(network[1]),
                'totalHosts': 2
            }
        # For all other networks
        else:
            return {
                'firstIP': str(network[1]),  # First usable IP (after network address)
                'lastIP': str(network[-2]),  # Last usable IP (before broadcast address)
                'totalHosts': network.num_addresses - 2  # Total usable IPs
            }
    except ValueError as e:
        print(f"Subnet calculation error: {str(e)}")
        return None

# Convert list of CIDR strings to set of network objects
def get_all_networks(cidrs: List[str]) -> Set[ipaddress.IPv4Network]:
    networks = set()
    for cidr in cidrs:
        try:
            network = ipaddress.ip_network(cidr.strip(), strict=False)
            networks.add(network)
        except ValueError as e:
            print(f"Error parsing CIDR {cidr}: {str(e)}")
    return networks

# Find all IP ranges that are NOT covered by the input networks
def calculate_combined_complementary_ranges(cidrs: List[str]) -> List[str]:
    try:
        if not cidrs:
            return []

        # Convert CIDR strings to network objects
        networks = get_all_networks(cidrs)
        if not networks:
            return []

        # Convert networks to integer ranges for easier manipulation
        covered_ranges = [(int(network.network_address), int(network.broadcast_address))
                         for network in networks]
        covered_ranges.sort()

        # Combine overlapping ranges into continuous blocks
        merged_ranges = []
        current_start, current_end = covered_ranges[0]
        
        for start, end in covered_ranges[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start, end
        merged_ranges.append((current_start, current_end))

        # Find gaps between the merged ranges - these are the complementary ranges
        complementary = []
        current_ip = 0
        
        for start, end in merged_ranges:
            if current_ip < start:
                # Convert the gap to CIDR notation
                range_networks = ipaddress.summarize_address_range(
                    ipaddress.IPv4Address(current_ip),
                    ipaddress.IPv4Address(start - 1)
                )
                complementary.extend([str(net) for net in range_networks])
            current_ip = end + 1

        # Handle any remaining range after the last merged range
        if current_ip < int(ipaddress.IPv4Address('255.255.255.255')):
            range_networks = ipaddress.summarize_address_range(
                ipaddress.IPv4Address(current_ip),
                ipaddress.IPv4Address('255.255.255.255')
            )
            complementary.extend([str(net) for net in range_networks])

        return complementary

    except Exception as e:
        print(f"Error calculating complementary ranges: {str(e)}")
        return []

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route that handles the calculation request
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get CIDR notations from the form and clean them up
    cidrs = request.form.get('cidr', '').split('\n')
    cidrs = [cidr.strip() for cidr in cidrs if cidr.strip()]
    
    if not cidrs:
        return jsonify({'error': 'At least one CIDR notation required'}), 400
    
    try:
        # Calculate information for each subnet
        subnets = []
        for cidr in cidrs:
            subnet_info = calculate_subnet(cidr)
            if subnet_info is None:
                return jsonify({'error': f'Invalid CIDR notation: {cidr}'}), 400
            subnets.append({'cidr': cidr, **subnet_info})
        
        # Calculate the complementary ranges
        complementary = calculate_combined_complementary_ranges(cidrs)
        
        # Return all results as JSON
        return jsonify({
            'subnets': subnets,
            'complementary': [{'cidr': cidr} for cidr in complementary]
        })
    except Exception as e:
        print(f"Calculation error: {str(e)}")
        return jsonify({'error': 'An error occurred during calculation'}), 500

# Start the application if running directly
if __name__ == '__main__':
    app.run(debug=True) 
