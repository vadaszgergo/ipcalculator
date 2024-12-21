from flask import Flask, render_template, request, jsonify, Response
import ipaddress
from typing import List, Set, Union
import traceback

app = Flask(__name__)

# Import all functions from both original applications
def calculate_subnet(cidr):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        
        if network.prefixlen == 32:
            return {
                'firstIP': str(network.network_address),
                'lastIP': str(network.network_address),
                'totalHosts': 1
            }
        elif network.prefixlen == 31:
            return {
                'firstIP': str(network[0]),
                'lastIP': str(network[1]),
                'totalHosts': 2
            }
        else:
            return {
                'firstIP': str(network[1]),
                'lastIP': str(network[-2]),
                'totalHosts': network.num_addresses - 2
            }
    except ValueError as e:
        print(f"Subnet calculation error: {str(e)}")
        return None

def get_all_networks(cidrs: List[str]) -> Set[ipaddress.IPv4Network]:
    networks = set()
    for cidr in cidrs:
        try:
            network = ipaddress.ip_network(cidr.strip(), strict=False)
            networks.add(network)
        except ValueError as e:
            print(f"Error parsing CIDR {cidr}: {str(e)}")
    return networks

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

def consolidate_ips(ip_list: List[str]) -> List[str]:
    """Consolidate IP addresses into CIDR ranges using ipaddress module."""
    try:
        # Convert IPs to integers and remove duplicates
        ip_integers = set()
        for ip_str in ip_list:
            try:
                ip = ipaddress.ip_address(ip_str.strip())
                ip_integers.add(int(ip))
            except ValueError:
                continue

        if not ip_integers:
            return []

        # Sort the IP integers
        sorted_ips = sorted(list(ip_integers))
        
        # Consolidate ranges
        consolidated = []
        current_start = sorted_ips[0]
        current_end = sorted_ips[0]

        for ip in sorted_ips[1:]:
            if ip == current_end + 1:
                # Consecutive IP, extend the current range
                current_end = ip
            else:
                # Gap found, add previous range or individual IP
                consolidated.append((current_start, current_end))
                current_start = current_end = ip

        # Add the last range or IP
        consolidated.append((current_start, current_end))

        # Convert ranges to CIDR notation
        cidr_ranges = []
        for start, end in consolidated:
            start_ip = ipaddress.ip_address(start)
            end_ip = ipaddress.ip_address(end)
            
            # Try to create the most compact CIDR representation
            try:
                range_networks = ipaddress.summarize_address_range(start_ip, end_ip)
                cidr_ranges.extend(str(network) for network in range_networks)
            except Exception:
                # Fallback to individual IPs if summarization fails
                cidr_ranges.append(f"{start_ip}/32")

        return cidr_ranges

    except Exception:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate-complement', methods=['POST'])
def calculate_complement():
    cidrs = request.form.get('cidr', '').split('\n')
    cidrs = [cidr.strip() for cidr in cidrs if cidr.strip()]
    
    if not cidrs:
        return jsonify({'error': 'At least one CIDR notation required'}), 400
    
    try:
        subnets = []
        for cidr in cidrs:
            subnet_info = calculate_subnet(cidr)
            if subnet_info is None:
                return jsonify({'error': f'Invalid CIDR notation: {cidr}'}), 400
            subnets.append({'cidr': cidr, **subnet_info})
        
        complementary = calculate_combined_complementary_ranges(cidrs)
        
        return jsonify({
            'subnets': subnets,
            'complementary': [{'cidr': cidr} for cidr in complementary]
        })
    except Exception as e:
        print(f"Calculation error: {str(e)}")
        return jsonify({'error': 'An error occurred during calculation'}), 500

@app.route('/consolidate', methods=['POST'])
def consolidate():
    try:
        ip_list = []
        
        # Handle manual input
        if 'ip-list' in request.form:
            content = request.form['ip-list']
            ip_list = [line.strip() for line in content.splitlines() if line.strip()]
        
        # Handle file upload
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            content = file.read().decode('utf-8')
            ip_list = [line.strip() for line in content.splitlines() if line.strip()]
        
        else:
            return jsonify({'error': 'No input provided'}), 400

        if not ip_list:
            return jsonify({'error': 'No valid IP addresses found in file'}), 400

        ranges = consolidate_ips(ip_list)
        
        response_data = {
            'original_count': len(ip_list),
            'ranges': ranges,
            'ranges_count': len(ranges)
        }

        if request.form.get('download') == 'true':
            output = '\n'.join(ranges)
            return Response(
                output,
                mimetype='text/plain',
                headers={'Content-Disposition': 'attachment; filename=consolidated_ranges.txt'}
            )
        
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 