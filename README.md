# vpngate-mirror

A copy of the public server list of [VPN Gate](https://www.vpngate.net) (a research project of the
University of Tsukuba, Japan), updated every 3 hours.

`vpngate.net` cannot be opened from some countries (Iran, for one). GitHub, and the mirrors of it
such as jsDelivr, usually can. Nothing is filtered or changed: every server in the list is here.

## Files

| File | What it is |
| --- | --- |
| `vpngate.csv` | The list as `vpngate.net/api/iphone/` gives it, with the OpenVPN configurations inside (base64). |
| `servers.json` | The same list without the configurations: one object per server (country, speed, ping, sessions, ...), with the `file` of its configuration. |
| `servers.txt` | One `openvpn://` link per server, for [Kumo](https://github.com/AbolDev/kumo-client). |
| `ovpn/` | The OpenVPN configuration file of each server, as it was given. Open it with any OpenVPN client. |

Direct addresses (they work even when `raw.githubusercontent.com` is slow):

```
https://cdn.jsdelivr.net/gh/AbolDev/vpngate-mirror@main/servers.txt
https://raw.githubusercontent.com/AbolDev/vpngate-mirror/main/servers.txt
```

(jsDelivr keeps a branch for up to 12 hours, so GitHub's own address is the newest.)

## Please know

- The servers are run by volunteers you do not know. **VPN Gate says they may keep logs.** Use them to
  test, or for things that are not private. Do not log in to anything important through them.
- A server in the list may be gone already, and the list changes all the time.
- This is not an official copy and has no connection with the VPN Gate project. The data belongs to
  its authors; see the [VPN Gate site](https://www.vpngate.net) for its terms.

## Build it yourself

```
python scripts/build.py .
```
