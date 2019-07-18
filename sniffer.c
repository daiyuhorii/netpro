#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <net/ethernet.h>
#include <arpa/inet.h>
#include <time.h>
#include <sys/time.h>
#include <string.h>

char *ctime(const time_t *timep);

static void print_udpheader(struct ip *ip){
    struct udphdr *udp;

    udp = (struct udphdr *)((char *)ip + (ip->ip_hl<<2));
    printf("protocol: UDP\n");
    printf("%d bytes received\n", ntohs(udp->uh_ulen));
    printf("\n\n");
}

static void print_tcpheader(struct ip *ip){
    struct tcphdr *tcp;

    tcp = (struct tcphdr *)((char *)ip + (ip->ip_hl<<2));
    printf("protocol: TCP\n");
    // flags to detect syn, ack, etc...
    // if true, flags will be u_int16_t 1 
    printf("FLAGS: ");
    if(tcp->urg){
        printf("URG ");
    }
    if(tcp->ack){
        printf("ACK ");
    }
    if(tcp->psh){
        printf("PSH ");
    }
    if (tcp->rst){
        printf("RST ");
    }
    if(tcp->syn){
        printf("SYN ");
    }
    if (tcp->fin){
        printf("FIN");
    }
    printf("\n");
}

static void print_ipheader(__u_char *args, const struct pcap_pkthdr *hdr, const __u_char *packet)
{
    struct ip *ip;
    
    ip = (struct ip *) (char *)(packet+sizeof(struct ether_header));
    
    printf("ip_v = 0x%x\n", ip->ip_v);
    printf("ip_len = %d bytes\n", ntohs(ip->ip_len));
    printf("ip_id = 0x%.4x\n", ntohs(ip->ip_id));
    printf("ip_off = 0x%.4x\n", ntohs(ip->ip_off));
    printf("ip_ttl = 0x%.2x\n", ip->ip_ttl);
    printf("ip_src = %s\n", inet_ntoa(ip->ip_src));
    printf("ip_dst = %s\n", inet_ntoa(ip->ip_dst));

    switch (ip->ip_p)
    {
    case IPPROTO_UDP:
        print_udpheader(ip);
        break;
    case IPPROTO_TCP:
        print_tcpheader(ip);
        break;
    default:
        break;
    }
    printf("\n");
}

int main(int argc, char *argv[]){
    pcap_if_t *alldevs;
    pcap_if_t *dev;
    pcap_t *handle;
    struct bpf_program fp;
    char filter_exp[] = "ip";
    bpf_u_int32 mask;
    bpf_u_int32 net;
    struct pcap_pkthdr header;
    const __u_char *packet;
    int inum;
    char errbuf[PCAP_ERRBUF_SIZE];

    // retrieve devices, or exit(1) if there is none
    char *device = pcap_lookupdev(errbuf);
    if(device == NULL) {
        printf("No device found. Abort: %s\n", errbuf);
    }
    printf("DEVICE: %s\n", device);
    // open the chosen device
    handle = pcap_open_live(device, BUFSIZ, 1, 1000, errbuf);

    // Error handlers. Abort when one or more of them is true.
    if(handle == NULL){
        fprintf(stderr, "Couldn't open device: %s\n", errbuf);
        exit(1);
    }
    if(pcap_compile(handle, &fp, filter_exp, 0, net) == -1){
        fprintf(stderr, "Couldn't analyze the filter\n");
        exit(1);
    }
    if(pcap_setfilter(handle, &fp) == -1){
        fprintf(stderr, "Couldn't set filter\n");
        exit(1);
    }
    /* Get packets within loops.
       pcap_loop returns 0 when it ends successfully,
       otherwise it returns something else to handle errors.*/
    pcap_loop(handle, 100, print_ipheader, NULL);
    printf("successfully completed.\n");    
    pcap_close(handle);
    return 0;
}