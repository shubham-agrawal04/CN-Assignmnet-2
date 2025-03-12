#!/usr/bin/env python3
import subprocess
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

ENABLE_DEBUG = True

def decode_tcp_flags(flag_string):
    """
    Convert the TCP flag string into a set of meaningful flag names.
    Handles hex values correctly.
    """
    try:
        flag_value = int(flag_string, 0)
    except ValueError:
        return set()
    
    flags_identified = set()
    if flag_value & 0x02:
        flags_identified.add('SYN')
    if flag_value & 0x10:
        flags_identified.add('ACK')
    if flag_value & 0x01:
        flags_identified.add('FIN')
    if flag_value & 0x04:
        flags_identified.add('RST')
    
    return flags_identified

def analyze_tcp_data(csv_filename):
    connection_records = defaultdict(dict)
    
    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        
        for entry in csv_reader:
            if ENABLE_DEBUG:
                print("DEBUG: Entry read:", entry)
            if len(entry) < 6:
                if ENABLE_DEBUG:
                    print("DEBUG: Skipping invalid entry:", entry)
                continue
            
            timestamp, src_addr, dest_addr, src_prt, dest_prt, flag_data = entry
            flags_detected = decode_tcp_flags(flag_data)
            
            if ENABLE_DEBUG:
                print("DEBUG: Extracted flags from", flag_data, "->", flags_detected)
            
            connection_key = (src_addr, dest_addr, src_prt, dest_prt)
            try:
                timestamp = float(timestamp)
            except ValueError:
                if ENABLE_DEBUG:
                    print("DEBUG: Skipping malformed timestamp:", timestamp)
                continue
            
            if connection_key not in connection_records:
                connection_records[connection_key]['begin'] = timestamp
                if ENABLE_DEBUG:
                    print(f"DEBUG: Start time logged for {connection_key} at {timestamp}")
            
            if 'RST' in flags_detected and 'finish' not in connection_records[connection_key]:
                connection_records[connection_key]['finish'] = timestamp
                if ENABLE_DEBUG:
                    print(f"DEBUG: RST flag recorded finish for {connection_key} at {timestamp}")
            
            if 'FIN' in flags_detected and 'ACK' in flags_detected and 'finish' not in connection_records[connection_key]:
                connection_records[connection_key]['finish'] = timestamp
                if ENABLE_DEBUG:
                    print(f"DEBUG: FIN-ACK recorded finish for {connection_key} at {timestamp}")
    
    connection_durations = []
    for key, timings in connection_records.items():
        if 'begin' not in timings:
            continue
        start_time = timings['begin']
        end_time = timings.get('finish', start_time + 100)
        connection_durations.append((start_time, end_time - start_time))
    
    return connection_durations

def plot(connection_durations):
    if not connection_durations:
        print("No valid TCP connections found.")
        return

    connection_durations.sort(key=lambda x: x[0])
    start_timestamps, duration_list = zip(*connection_durations)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(start_timestamps, duration_list, c='blue', label='connection Duration')
    plt.xlabel('connection Start Time (epoch seconds)')
    plt.ylabel('Connection Duration (seconds)')
    plt.title('Connection Duration vs. Connection Start Time')
    
    initial_experiment_time = start_timestamps[0]
    plt.axvline(x=initial_experiment_time + 20, color='red', linestyle='--', label='Attack Start')
    plt.axvline(x=initial_experiment_time + 120, color='green', linestyle='--', label='Attack End')
    
    plt.legend()
    plt.show()

def extract_tcp_info_from_pcap(input_pcap, output_csv):
    tshark_command = [
        'tshark', '-r', input_pcap, '-T', 'fields',
        '-e', 'frame.time_epoch', '-e', 'ip.src', '-e', 'ip.dst',
        '-e', 'tcp.srcport', '-e', 'tcp.dstport', '-e', 'tcp.flags',
        '-E', 'header=y', '-E', 'separator=,', '-E', 'quote=d', '-E', 'occurrence=f'
    ]
    with open(output_csv, 'w') as output_file:
        subprocess.run(tshark_command, stdout=output_file)

if __name__ == '__main__':
    pcap_filename = 'q2.pcap'
    csv_output_filename = 'tcp_data.csv'
    
    extract_tcp_info_from_pcap(pcap_filename, csv_output_filename)
    
    connection_info = analyze_tcp_data(csv_output_filename)
    print(f"Processed {len(connection_info)} TCP connections.")
    
    plot(connection_info)
