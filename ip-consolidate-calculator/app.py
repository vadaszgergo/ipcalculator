from flask import Flask, render_template, request, jsonify, Response
import ipaddress
from typing import List, Union
import traceback

app = Flask(__name__)

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

@app.route('/consolidate', methods=['POST'])
def consolidate():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read IP addresses from the uploaded file
        content = file.read().decode('utf-8')
        ip_list = [line.strip() for line in content.splitlines() if line.strip()]
        
        if not ip_list:
            return jsonify({'error': 'No valid IP addresses found in file'}), 400

        # Consolidate IPs into ranges
        ranges = consolidate_ips(ip_list)
        
        # Create the response content
        response_data = {
            'original_count': len(ip_list),
            'ranges': ranges,
            'ranges_count': len(ranges)
        }

        # If download parameter is present, return as file
        if request.form.get('download') == 'true':
            output = '\n'.join(ranges)
            return Response(
                output,
                mimetype='text/plain',
                headers={'Content-Disposition': 'attachment; filename=consolidated_ranges.txt'}
            )
        
        # Otherwise return JSON response
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 