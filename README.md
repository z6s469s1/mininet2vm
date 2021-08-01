# mininet2vm


2 vlan & bridge internet  & 2 NAT
---
![](https://i.imgur.com/hnJAUjs.png)



要記得同internal mode的vm mac要不同 不然會ping不到
不知為何r1 想要有三張網卡 各別傳不同LAN 在第三個LAN(綁實際bridge IP的router)就要用NAT



2 vlan & bridge internet  & 1 NAT
---

中間router改用switch串 就沒有問題了
![](https://i.imgur.com/rYQbm6l.png)
