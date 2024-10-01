import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in str(scapy_packet[scapy.Raw].load):
                print("EXE Request")
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            print(scapy_packet.show())

    packet.accept()



queue = netfilterqueue.NetfilterQueue()

#0 is the queue number mentionned in iptables command
queue.bind(0, process_packet)

queue.run()