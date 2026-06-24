"""Базовое сканирование портов"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.utils import section, ok, err, info, warn


class PortScanModule:
    """Сканирование топовых портов"""

    TOP_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 8080, 8443, 9200, 27017]

    def scan_port(self, ip, port):
        """Скан одного порта"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            sock.close()
            return port, result == 0
        except:
            return port, False

    def run(self, ip, ports=None):
        section(f"Скан портов: {ip}")

        if not ports:
            ports = self.TOP_PORTS
            info(f"Сканируем {len(ports)} топовых портов")

        open_ports = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.scan_port, ip, p): p for p in ports}
            for future in as_completed(futures):
                port, is_open = future.result()
                if is_open:
                    open_ports.append(port)
                    ok(f"Порт {port} открыт")

        if open_ports:
            info(f"Открыто портов: {len(open_ports)}")
            for p in sorted(open_ports):
                service = self._get_service(p)
                info(f"  {p}/tcp — {service}")
        else:
            warn("Открытых портов не найдено (или фильтруются)")

        return {"ip": ip, "open_ports": sorted(open_ports), "total_scanned": len(ports)}

    def _get_service(self, port):
        """Название сервиса по порту"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy", 
            8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB"
        }
        return services.get(port, "Unknown")
