# netpro
Something like psuedo Wireshark or tcpdump

It locates the packet senders' vague address by sniffing their IPs, and we use Geoip2 to do that.
It also analyses upper protocol by its IP header, and recognizes TCP FLAGs when received/sent TCP header.
