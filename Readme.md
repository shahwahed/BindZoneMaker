bindZoneMaker
=============

An [RFC1035 compliant](http://www.ietf.org/rfc/rfc1035.txt) DNS zone file parser and generator in python using jinja template

# Usage

## Zone Information

_bindZoneMaker_ use data expressed as a JSON object.
 It supports `SOA`, `NS`, `A`, `AAAA`, `CNAME`, `MX`, `PTR`, `SRV` and `TXT` record types
as well as the `$ORIGIN` keyword (for zone-wide use only). Each record type
(and the `$ORIGIN` keyword) is optional, though _bind_ expects to find at least
an `SOA` record in a valid zone file.

### Examples

#### Forward DNS Zone

The following JSON produces a zone file for a forward DNS zone:

```json
{
    "origin": "MYDOMAIN.COM.",
    "ttl": 3600,
    "soa": {
        "mname": "NS1.NAMESERVER.NET.",
        "rname": "HOSTMASTER.MYDOMAIN.COM.",
        "serial": "2019010301",
        "refresh": 3600,
        "retry": 600,
        "expire": 604800,
        "minimum": 86400
    },
    "ns": [
        { "host": "NS1.NAMESERVER.NET." },
        { "host": "NS2.NAMESERVER.NET." }
    ],
    "a": [
        { "name": "@", "ip": "127.0.0.1" },
        { "name": "www", "ip": "127.0.0.1" },
        { "name": "mail", "ip": "127.0.0.1" }
    ],
    "aaaa": [
        { "ip": "::1" },
        { "name": "mail", "ip": "2001:db8::1" }
    ],
    "cname":[
        { "name": "mail1", "alias": "mail" },
        { "name": "mail2", "alias": "mail" }
    ],
    "mx":[
        { "preference": 0, "host": "mail1" },
        { "preference": 10, "host": "mail2" }
    ],
    "spf":[
        { "domain": "mail1", "record": "v=spf1 ~all" }
    ],
    "txt":[
        { "name": "txt1", "txt": "hello" },
        { "name": "txt2", "txt": "world" }
    ],
    "srv":[
        { "name": "_xmpp-client._tcp", "target": "jabber", "priority": 10, "weight": 0, "port": 5222 },
        { "name": "_xmpp-server._tcp", "target": "jabber", "priority": 10, "weight": 0, "port": 5269 }
    ]
}
```
_bindZoneMaker_ will produce the following zone file from the above information:

```
; Zone: MYDOMAIN.COM.
; Exported  (yyyy-mm-ddThh:mm:ss.sssZ): 2019-01-05T21:35:46.429035+00:00
$ORIGIN MYDOMAIN.COM.
$TTL 3600

; SOA Record
@	IN	SOA	NS1.NAMESERVER.NET. HOSTMASTER.MYDOMAIN.COM.(
2019010301 ;serial
3600 ;refresh
600 ;retry
604800 ;expire
86400 ;minimum ttl
)

; NS Records
@   IN  NS  NS1.NAMESERVER.NET.
@   IN  NS  NS2.NAMESERVER.NET.

; MX Records
@	IN	MX	0    mail1
@	IN	MX	10    mail2

; SPF Records
mail1	IN	TXT	"v=spf1 ~all"

; A Records
@	IN	A	127.0.0.1
www	IN	A	127.0.0.1
mail	IN	A	127.0.0.1

; AAAA Records	IN	A	::1
mail	IN	A	2001:db8::1

; CNAME Records
mail1	IN	CNAME	mail
mail2	IN	CNAME	mail

; TXT Records
txt1	IN	TXT	"hello"
txt2	IN	TXT	"world"

; SRV Records
_xmpp-client._tcp	IN	SRV	10   0 5222   jabber
_xmpp-server._tcp	IN	SRV	10   0 5269   jabber

; End of Zone
```

### Reverse DNS Zone

This JSON will produce a zone file for a reverse DNS zone (the `ORIGIN`
keyword is recommended for reverse DNS zones):

```json
{
	"origin": "0.168.192.IN-ADDR.ARPA.",
	"ttl": 3600,
	"soa": {
		"mname": "NS1.NAMESERVER.NET.",
		"rname": "HOSTMASTER.MYDOMAIN.COM.",
		"serial": "2019010301",
		"refresh": 3600,
		"retry": 600,
		"expire": 604800,
		"minimum": 86400
	},
  "ns": [
      { "host": "NS1.NAMESERVER.NET." },
      { "host": "NS2.NAMESERVER.NET." }
  ],
  "ptr":[
      { "name": 1, "host": "HOST1.MYDOMAIN.COM." },
      { "name": 2, "host": "HOST2.MYDOMAIN.COM." }
  ]
}
```

_bindZoneMaker_ will produce the following zone file from the above information:

```
; Zone: 0.168.192.IN-ADDR.ARPA.
; Exported  (yyyy-mm-ddThh:mm:ss.sssZ): 2019-01-05T21:46:24.828344+00:00
$ORIGIN 0.168.192.IN-ADDR.ARPA.
$TTL 3600

; SOA Record
@	IN	SOA	NS1.NAMESERVER.NET. HOSTMASTER.MYDOMAIN.COM.(
2019010301 ;serial
3600 ;refresh
600 ;retry
604800 ;expire
86400 ;minimum ttl
)

; NS Records
@   IN  NS  NS1.NAMESERVER.NET.
@   IN  NS  NS2.NAMESERVER.NET.

; PTR Records
1	IN	PTR	"HOST1.MYDOMAIN.COM."
2	IN	PTR	"HOST2.MYDOMAIN.COM."


; End of Zone
```

## Standalone Usage

To use _bindZoneMaker_ to generate a zone file from JSON from the command line,
place the desired JSON data in a file (`dns_example.json` in this example)
and run the following command. Note that the resulting zone file will be
printed to the console; to save the zone file to disk (`db.mydomain.com` in this
example), use redirection as in this example:

```
bindZoneMaker.py -z dns_example.json > db.mydomain.com
```


# License
MIT License

Copyright (c) 2019 WAHED Shah Mohsin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.