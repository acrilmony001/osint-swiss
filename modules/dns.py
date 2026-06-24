"""DNS разведка"""

import dns.resolver
import dns.reversename
from core.utils import section, ok, err, info, table


class DNSModule:
    """Сбор DNS-записей домена"""

    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5

    def query(self, domain, rtype):
        """Запрос записей указанного типа"""
        try:
            ans = self.resolver.resolve(domain, rtype)
            return [str(r) for r in ans]
        except Exception:
            return []

    def run(self, domain):
        """Полная DNS-разведка"""
        section(f"DNS: {domain}")

        types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
        result = {}

        for t in types:
            records = self.query(domain, t)
            if records:
                result[t] = records
                ok(f"{t}: {len(records)} записей")
            else:
                result[t] = None

        # PTR для первого A
        if result.get("A"):
            ip = result["A"][0]
            try:
                rev = dns.reversename.from_address(ip)
                ptr = self.resolver.resolve(rev, "PTR")
                result["PTR"] = [str(r) for r in ptr]
                info(f"PTR {ip} -> {result['PTR'][0]}")
            except Exception:
                result["PTR"] = None

        table(result, f"DNS записи: {domain}")
        return result
