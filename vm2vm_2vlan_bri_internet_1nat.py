from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info


r1_nic='enp0s9' #internal1
r2_nic='enp0s10'#internal2
r3_nic='enp0s3' #bridge




def myNetwork():

    net = Mininet( topo=None, build=False)
    
    info( '*** Starting network\n')
    
    info( '*** Adding controller\n' )
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6653)

    info( '*** Add switches\n')
    s1=net.addSwitch( 's1' )

    info( '*** Add hosts\n')
    
    r1 = net.addHost('r1')
    Intf( r1_nic, node=r1 )
    
    r2 = net.addHost('r2')
    Intf( r2_nic, node=r2 )
    
    r3 = net.addHost('r3')
    Intf( r3_nic, node=r3 )
    

    info( '*** Add links\n')
    net.addLink(r1, s1)
    net.addLink(r2, s1)
    net.addLink(r3, s1)
    



    info( '*** Starting network\n')
    net.start()
    
    
    
    
    r1.cmd("ifconfig "+r1_nic+" 0")
    r1.cmd("ifconfig r1-eth1 0")
    r1.cmd("ip addr add 10.0.1.254/24 brd + dev "+r1_nic)
    r1.cmd("ip addr add 10.0.0.1/24 brd + dev r1-eth1")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r1.cmd("ip route add 10.0.2.0/24 via 10.0.0.2") 
    r1.cmd("ip route add 0.0.0.0/0 via 10.0.0.3")   
    
    
    
    r2.cmd("ifconfig "+r2_nic+" 0")
    r2.cmd("ifconfig r2-eth1 0")
    r2.cmd("ip addr add 10.0.2.254/24 brd + dev "+r2_nic)
    r2.cmd("ip addr add 10.0.0.2/24 brd + dev r2-eth1")
    r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r2.cmd("ip route add 10.0.1.0/24 via 10.0.0.1")
    r2.cmd("ip route add 0.0.0.0/0 via 10.0.0.3")   


    r3.cmd("ifconfig "+r3_nic+" 0")
    r3.cmd("ip addr add 192.168.50.200/24 brd + dev "+r3_nic)
    r3.cmd("route add default gw 192.168.50.1 "+r3_nic)
    r3.cmd("ifconfig r3-eth1 0")
    r3.cmd("ip addr add 10.0.0.3/24 brd + dev r3-eth1")
    r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r3.cmd("ip route add 10.0.1.0/24 via 10.0.0.1")
    r3.cmd("ip route add 10.0.2.0/24 via 10.0.0.2")
    r3.cmd("iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -d 192.168.50.0/24 -o "+r3_nic+" -j ACCEPT")
    r3.cmd("iptables -t nat -A POSTROUTING -s 10.0.2.0/24 -d 192.168.50.0/24 -o "+r3_nic+" -j ACCEPT")
    r3.cmd("iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -d 0.0.0.0/0 -o "+r3_nic+" -j MASQUERADE")
    r3.cmd("iptables -t nat -A POSTROUTING -s 10.0.2.0/24 -d 0.0.0.0/0 -o "+r3_nic+" -j MASQUERADE")
    
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
