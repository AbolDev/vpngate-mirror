#!/usr/bin/env python3
"""Downloads the public server list of VPN Gate (https://www.vpngate.net) and writes it here in
several forms. Nothing is filtered: every server that is in the list is kept as it was given.

  vpngate.csv     the list as vpngate.net gives it (with the OpenVPN configurations inside)
  servers.json    the same, without the configurations: one object per server
  servers.txt     one `openvpn://` link per server, for Kumo (https://github.com/AbolDev/kumo-client)
  ovpn/*.ovpn     each server's OpenVPN configuration file, as it was given

Usage: python scripts/build.py [folder]
"""
import base64
import csv
import io
import json
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request

API = "https://www.vpngate.net/api/iphone/"


def fetch():
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


def flag(code):
    code = (code or "").upper()
    if len(code) != 2 or not code.isalpha():
        return ""
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in code) + " "


def protocol_and_port(config, default_ip):
    proto, port = "udp", ""
    for line in config.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] == "proto":
            proto = parts[1].split("-")[0]
        if len(parts) >= 3 and parts[0] == "remote":
            port = parts[2]
    return proto, port


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    raw = fetch()
    lines = [l for l in raw.splitlines() if l and not l.startswith("*")]
    if not lines:
        sys.exit("empty answer; nothing changed")
    lines[0] = lines[0].lstrip("#")
    rows = list(csv.DictReader(io.StringIO("\n".join(lines))))
    rows = [r for r in rows if r.get("IP") and r.get("OpenVPN_ConfigData_Base64")]
    if not rows:
        sys.exit("no server in the answer; nothing changed")

    folder = os.path.join(out, "ovpn")
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    meta, links = [], []
    for r in rows:
        config = base64.b64decode(r["OpenVPN_ConfigData_Base64"]).decode("utf-8", "replace")
        proto, port = protocol_and_port(config, r["IP"])
        country = r.get("CountryShort", "")
        name = "%s_%s_%s_%s" % (country or "XX", r["IP"], proto, port or "0")
        name = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
        with open(os.path.join(folder, name + ".ovpn"), "w", encoding="utf-8", newline="\n") as f:
            f.write(config)
        info = {k: v for k, v in r.items() if k != "OpenVPN_ConfigData_Base64"}
        info["file"] = "ovpn/%s.ovpn" % name
        info["protocol"], info["port"] = proto, port
        meta.append(info)
        mbps = int(r.get("Speed") or 0) / 1e6
        title = "%sVPN Gate %s %d Mbps" % (flag(country), country, round(mbps))
        body = base64.urlsafe_b64encode(config.encode()).decode().rstrip("=")
        links.append("openvpn://%s#%s" % (body, urllib.parse.quote(title)))

    with open(os.path.join(out, "vpngate.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write(raw.replace("\r\n", "\n"))
    with open(os.path.join(out, "servers.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(out, "servers.txt"), "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(links) + "\n")
    print("%d servers" % len(rows))


if __name__ == "__main__":
    main()
