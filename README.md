
# HTTP EXE Interceptor

This Python script is designed to intercept HTTP requests and responses, specifically targeting `.exe` file downloads. The script uses `netfilterqueue` to intercept packets, while `scapy` is used to manipulate the packet data.

## How It Works

- The script intercepts HTTP packets using `netfilterqueue`.
- It inspects the intercepted packets for `.exe` download requests.
- When an `.exe` download request is detected, it modifies the HTTP response, redirecting it to a different URL (`http://localIP/test.exe`).
- This allows an attacker to serve a malicious file instead of the requested executable.

## Prerequisites

- **Kali Linux** or any Linux distribution with root access.
- Python 3.x installed.
- `iptables` for creating packet queues.
- `netfilterqueue` and `scapy` Python libraries.

### Installing Dependencies

1. **Install `scapy`**:
   ```bash
   sudo pip install scapy
   ```

2. **Install `netfilterqueue`** (ensure the required system libraries are installed):
   ```bash
   sudo apt-get install libnetfilter-queue-dev
   sudo pip install netfilterqueue --break-system-packages
   ```

## Running the Script

### Step 1: Set up iptables

Use `iptables` to forward HTTP packets to a queue (queue number `0` in this example). This allows the script to intercept the packets.

```bash
sudo iptables -I FORWARD -p tcp --dport 80 -j NFQUEUE --queue-num 0
```

If you're testing on your local machine, use:
```bash
sudo iptables -I OUTPUT -p tcp --dport 80 -j NFQUEUE --queue-num 0
sudo iptables -I INPUT -p tcp --sport 80 -j NFQUEUE --queue-num 0
```

### Step 2: Run the Python Script

```bash
sudo python3 exe_interceptor.py
```

### Step 3: Clean Up iptables Rules (Optional)

After running the script, reset your iptables rules to their original state:

```bash
sudo iptables --flush
```

## Script Breakdown

- **set_payload(packet)**: This function modifies the HTTP response to redirect the download to `http://localIP/test.exe`.
- **process_packet(packet)**: This function processes each packet intercepted by `netfilterqueue`. It checks if the packet contains an `.exe` download request, and if so, it modifies the response to redirect the download.
- **queue.bind(0, process_packet)**: Binds the script to iptables' queue `0`.

## Warning

This script is for educational purposes only. Performing packet interception and manipulation on networks without permission is illegal and unethical.

## License

0x1tsjusthicham
