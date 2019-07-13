// files //
sniffer.c : 低レイヤのスニッファープログラム
sniff.py  : スニッファを動かすためのpython3プログラム
sniff     : sniffer.cをコンパイルした実行ファイル

sniffer.c : A low-level sniffer program
sniff.py  : a python3 program to run sniffer program
sniff     : An executable compiled from sniffer.c

// usage //
execute sudo ./sniff to run.
sniffer.cをテスト/デバッグするにはlibpcapライブラリが必要(Linux).
debian系なら、sudo apt install libpcap-devでインストールできる.
ヘッダファイルは/usr/includeに格納されているので、cプログラムをいじりたいならpcap.h pcapディレクトリがそこにあることを確認すること.
You need libpcap library(on Linux) to debug sniffer.c
On debian distros, run 'sudo apt install libpcap-dev' to install it.
Header files are stored in /usr/inlcude. Make sure you have 'pcap.h' and 'pcap' directory there if you want to debug the c program.

// update schedule //
.pcapファイルにdumpする機能はまだついてないので後日アップデートしたい
A function to dump .pcap file is still not be implemented, we need an update.
