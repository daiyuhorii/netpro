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

static void print_ipheader(char *p)
{
    struct ip *ip;
    
    ip = (struct ip *)p;
    
    printf("ip_v = 0x%x\n", ip->ip_v);
    printf("ip_hl = 0x%x\n", ip->ip_hl);
    printf("ip_tos = 0x%.2x\n", ip->ip_tos);
    printf("ip_len = %d bytes\n", ntohs(ip->ip_len));
    printf("ip_id = 0x%.4x\n", ntohs(ip->ip_id));
    printf("ip_off = 0x%.4x\n", ntohs(ip->ip_off));
    printf("ip_ttl = 0x%.2x\n", ip->ip_ttl);
    printf("ip_p = 0x%.2x\n", ip->ip_p);
    printf("ip_sum = 0x%.4x\n", ntohs(ip->ip_sum));
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

int main(){
    pcap_if_t *alldevs;
    pcap_if_t *dev;
    pcap_t *handle;
    struct bpf_program fp;
    char filter_exp[] = "port 80";
    bpf_u_int32 mask;
    bpf_u_int32 net;
    struct pcap_pkthdr header;
    const __u_char *packet;
    int inum;
    char errbuf[PCAP_ERRBUF_SIZE];

    // retrieve devices, or exit(1) if there is none
    if(pcap_findalldevs(&alldevs, errbuf) == -1) {
        fprintf(stderr, "err in pcap_findalldevs: %s\n", errbuf);
        exit(1);
    }

    // print the list of devices
    int devNum=0;
    for(dev=alldevs; dev; dev=dev->next)
    {
        printf("%d %s", devNum++, dev->name);
        if(dev->description)
            printf("    (%s)\n", dev->description);
        else
            printf("(No description available)\n");
    }

    if(devNum == 0){
        printf("No interfaces found. Check out if pcap is properly installed.");
        return -1;
    }
    // choose which device is to be sniffed
    printf("Choose the device which you want to sniff: ");
    scanf("%d", &inum);
    if(inum < 0 || devNum < inum){
        printf("--- Invalid number ---");
        pcap_freealldevs(alldevs);
        return -1;
    }

    for(inum=0, dev=alldevs; inum<inum; inum++){
        dev = dev->next;
    }
    printf("device name = %s\n", dev->name);
    
    // open the chosen device
    handle = pcap_open_live(dev->name, BUFSIZ, 1, 1000, errbuf);
    if(handle == NULL){
        fprintf(stderr, "Couldn't open device: %s\n", errbuf);
        exit(1);
    }
    if(pcap_compile(handle, &fp, "ip and tcp", 0, net) == -1){
        fprintf(stderr, "Couldn't analyze the filter\n");
        exit(1);
    }
    if(pcap_setfilter(handle, &fp) == -1){
        fprintf(stderr, "Couldn't set filter\n");
        exit(1);
    }
    /* ループでパケットを受信 */
    while (1) {
        time_t t = header.ts.tv_sec;
        if ((packet = pcap_next(handle, &header)) == NULL)
            continue;
        
        printf("Fetched packet length[%d] at %s", header.len, ctime(&t));    
        print_ipheader((char *)(packet+sizeof(struct ether_header)));
    }
    pcap_close(handle);
    return 0;
}
