#flow_duration, ip_proto, src_port, dstport, byte_count, packet_count, label

import csv
import subprocess
from Collect_ddos_attack import CollectTrainingStatsApp



def attack_generation():
    # Step 4: Generate DDoS attack and save data
    #CollectTrainingStatsApp()
    # Assuming the attack traffic has been generated and captured by ITGRecv
    capture_file = 'capture.txt'
    with open(capture_file, 'w') as f:
        subprocess.call(["./ITGRecv"], stdout=f)  # Run ITGRecv and capture output to file

    # Read the captured traffic data from the ITGRecv output file
    captured_data = []
    with open(capture_file, 'r') as f:
        for line in f:
            # Extract the required fields from each line and add them to the captured_data list
            fields = line.strip().split(',')  # Adjust the splitting logic based on the actual output format
            timestamp = fields[0]
            datapath_id = fields[1]
            flow_id = fields[2]
            ip_src = fields[3]
            tp_src = fields[4]
            ip_dst = fields[5]
            tp_dst = fields[6]
            ip_proto = fields[7]
            icmp_code = fields[8]
            icmp_type = fields[9]
            flow_duration_sec = fields[10]
            flow_duration_nsec = fields[11]
            idle_timeout = fields[12]
            hard_timeout = fields[13]
            flags = fields[14]
            packet_count = fields[15]
            byte_count = fields[16]
            packet_count_per_second = fields[17]
            packet_count_per_nsecond = fields[18]
            byte_count_per_second = fields[19]
            byte_count_per_nsecond = fields[20]
            label = fields[21]

            captured_data.append({
                'timestamp': timestamp,
                'datapath_id': datapath_id,
                'flow_id': flow_id,
                'ip_src': ip_src,
                'tp_src': tp_src,
                'ip_dst': ip_dst,
                'tp_dst': tp_dst,
                'ip_proto': ip_proto,
                'icmp_code': icmp_code,
                'icmp_type': icmp_type,
                'flow_duration_sec': flow_duration_sec,
                'flow_duration_nsec': flow_duration_nsec,
                'idle_timeout': idle_timeout,
                'hard_timeout': hard_timeout,
                'flags': flags,
                'packet_count': packet_count,
                'byte_count': byte_count,
                'packet_count_per_second': packet_count_per_second,
                'packet_count_per_nsecond': packet_count_per_nsecond,
                'byte_count_per_second': byte_count_per_second,
                'byte_count_per_nsecond': byte_count_per_nsecond,
                'label': label
            })

    # Save the captured data to a CSV file
    csv_file = 'captured_data.csv'
    fieldnames = ['timestamp', 'datapath_id', 'flow_id', 'ip_src', 'tp_src', 'ip_dst', 'tp_dst',
              'ip_proto', 'icmp_code', 'icmp_type', 'flow_duration_sec', 'flow_duration_nsec',
              'idle_timeout', 'hard_timeout', 'flags', 'packet_count', 'byte_count',
              'packet_count_per_second', 'packet_count_per_nsecond', 'byte_count_per_second',
              'byte_count_per_nsecond', 'label']

    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(captured_data)
