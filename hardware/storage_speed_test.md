# 存储测速

测试移动存储的读写速率。线缆都是 USB 3.0 Micro-B 接头。使用的测速软件为 macOS 上的 Disk Speed Test.

## 移动硬盘

第一个出场的是 Elements 25A2 移动硬盘，控制器与机械硬盘一体。控制器是 Elements 25A2:

:生产企业: Western Digital
:链接速度: 5 Gb/s
:USB 供应商 ID: x1058
:USB 产品 ID: 0x25a2
:USB 产品版本: 0x1014

再看硬盘：

:容量: 2 TB（2,000,301,457,408字节）
:文件系统: ExFAT
:设备名称: Elements 25A2
:介质名称: WD Elements 25A2 Media
:分区图类型: MBR（主引导记录）

测速结果：

![dst_elements_25a2.png](/_images/hardware/dst_elements_25a2.png)

第二个是一块 5400rpm 机械硬盘，使用一个移动硬盘盒。控制器是 HE-V300(NS1066 2.45):

:生产企业: SSK
:链接速度: 5 Gb/s
:USB 供应商 ID: 0x2537
:USB 产品 ID: 0x1066
:USB 产品版本: 0x0100

硬盘：

:容量: 1 TB（1,000,170,717,184字节）
:文件系统: ExFAT
:设备名称: HGST HTS541010A7
:介质名称: ATA HGST HTS541010A7 Media
:分区图类型: MBR（主引导记录）

测速结果：

![dst_hgst_hts541010a7.png](/_images/hardware/dst_hgst_hts541010a7.png)

第三个是另一块 5400rpm 机械硬盘，使用同一个移动硬盘盒。硬盘信息：

:容量: 160.04 GB（160,035,635,200字节）
:文件系统: ExFAT
:设备名称: Hitachi HTS54251
:介质名称: ATA Hitachi HTS54251 Media
:分区图类型: MBR（主引导记录）

测速结果：

![dst_hitachi_hts54251.png](/_images/hardware/dst_hitachi_hts54251.png)

都是 5400rpm, 差距咋还这么大呢。

第四个是一块 SSD 硬盘，使用同一个移动硬盘盒。硬盘信息：

:容量: 125.03 GB（125,033,381,888字节）
:文件系统: ExFAT
:设备名称: KINGSHARE E20012
:介质名称: ATA KINGSHARE E20012 Media
:分区图类型: MBR（主引导记录）

测速结果：

![dst_kingshare_e20012.png](/_images/hardware/dst_kingshare_e20012.png)

这 SSD 貌似也没快多少。

## 优盘

一个优盘。控制器：

:生产企业: VERBATIM
:链接速度: 480 Mb/s
:USB供应商ID: 0x0ed1
:USB产品ID: 0x6981
:USB产品版本: 0x0101

盘：

:容量: 16.83 GB（16,833,118,208字节）
:文件系统: MS-DOS FAT32
:设备名称: Store'N'Go
:介质名称: VERBATIM Store'N'Go Media
:分区图类型: MBR（主引导记录）

测速结果：

![dst_verbatim_16g.png](/_images/hardware/dst_verbatim_16g.png)

这优盘年纪有点大了。

## TF 卡

意犹未尽，又搬出了一堆老硬件，首先是品胜 USB 3.0 读卡器：

:生产企业: Generic
:链接速度: 5 Gb/s
:USB供应商ID: 0x05e3
:USB产品ID: 0x0748
:USB产品版本: 0x1201

这个用的是公版驱动，名称显示不出来。

一张 TF 卡：

![tf_banq_joy_hc1_32g.jpg](/_images/hardware/tf_banq_joy_hc1_32g.jpg)

:容量: 31.29 GB（31,293,095,936字节）
:文件系统: MS-DOS FAT32
:设备名称: STORAGE DEVICE
:介质名称: Generic STORAGE DEVICE Media
:分区图类型: MBR（主引导记录）

测速结果：

![dst_banq_joy_hc1_32g.png](/_images/hardware/dst_banq_joy_hc1_32g.png)

这个被行车记录仪用了好多年，估计磨得差不多了。

## SD 卡

然后是一堆老旧 SD 卡。第一张：

![sd_kingston_sda10_128g.jpg](/_images/hardware/sd_kingston_sda10_128g.jpg)

:容量: 125.1 GB（125,101,539,328字节）
:文件系统: ExFAT
:设备名称: STORAGE DEVICE
:介质名称: Generic STORAGE DEVICE Media
:分区图类型: MBR（主引导记录）

不同的卡系统读到的信息是一样的，只是容量不同，故不再赘述。

测速结果：

![dst_kingston_sda10_128g.png](/_images/hardware/dst_kingston_sda10_128g.png)

第二张：

![sd_kingston_sd10vg2_16g.jpg](/_images/hardware/sd_kingston_sd10vg2_16g.jpg)

:容量: 15.52 GB（15,518,957,568字节）

测速结果：

![dst_kingston_sd10vg2_16g.png](/_images/hardware/dst_kingston_sd10vg2_16g.png)

同是 Class 10, 这差别也够大的。

第三张：

![sd_kingston_sd4_4g.jpg](/_images/hardware/sd_kingston_sd4_4g.jpg)

:容量: 3.95 GB（3,950,645,248字节）
:文件系统: MS-DOS FAT32

这里文件系统换成了 FAT32, 因为这么大的容量实在没有必要上 ExFAT.

测速结果：

![dst_kingston_sd4_4g.png](/_images/hardware/dst_kingston_sd4_4g.png)

## CF 卡

还有更老的 CF 卡。这时上面这个测速软件已经不能用了，因为它最小要写一个 1G 的文件，实在是太太太大了，只能换成 Magic Disk Benchmark.

第一张：

![cf_pqi_hs_128m.jpg](/_images/hardware/cf_pqi_hs_128m.jpg)

:容量: 129.9 MB（129,867,776字节）
:文件系统: MS-DOS FAT16

这个容量只能 FAT16 了。

测速结果：

![mdb_pqi_hs_128m.png](/_images/hardware/mdb_pqi_hs_128m.png)

第二张：

![cf_pqi_f1_40x_128m.jpg](/_images/hardware/cf_pqi_f1_40x_128m.jpg)

:容量: 129.9 MB（129,867,776字节）

测速结果：

![mdb_pqi_f1_40x_128m.png](/_images/hardware/mdb_pqi_f1_40x_128m.png)

第三张：

![cf_sandisk_128m.jpg](/_images/hardware/cf_sandisk_128m.jpg)

:容量: 128 MB（128,036,864字节）

注意看，同是标称 128M 的三张卡，实际大小还是有一点点的区别。

测速结果：

![mdb_sandisk_128m.png](/_images/hardware/mdb_sandisk_128m.png)

第四张：

![cf_canon_fc_8m.jpg](/_images/hardware/cf_canon_fc_8m.jpg)

:容量: 7.9 MB（7,919,616字节）

测速结果：

![mdb_canon_fc_8m.png](/_images/hardware/mdb_canon_fc_8m.png)

最后这个是最早的一张 CF 卡，购佳能便携相机所赠。本以为是性能最差的一张，没想到这写入速度相当能打。

最后补一个本地硬盘的，科幻啊：

![dst_mac1_local.png](/_images/hardware/dst_mac1_local.png)
