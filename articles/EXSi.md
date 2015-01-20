EXSi5.5.ISO 添加Intel i218-v网卡驱动
===
ESXi5.5 本身并为支持最新Intel 9系芯片网卡驱动程序。为了让EXSi5.5在ASUS z97上正常运行，需要自行倒入相关驱动程序。

### 环境准备
* PowerShell 2.0或更高版本（Windows 7/8/8.1)
* [VMware vSphere PowerCLI](https://communities.vmware.com/community/vmtn/automationtools/powercli)
* [ESXi-Customizer-PS](http://vibsdepot.v-front.de/tools/ESXi-Customizer-PS-v2.3.ps1)
* [ESXi 5.5 Update 2 Offline Bundle](https://my.vmware.com/group/vmware/details?downloadGroup=ESXI55U2&productId=353&rPId=6656#) (替代EXSi5.5 ISO镜像)

### 驱动和链接

* [sata-xahci-1.24-1-offline_bundle.zip](http://vibsdepot.v-front.de/wiki/index.php/Sata-xahci) – addonboard SATA AHCI controller mappings
* [igb-5.2.7-1331820-offline_bundle-2157967.zip](https://my.vmware.com/group/vmware/details?downloadGroup=DT-ESXI55-INTEL-IGB-527&productId=353) – Intel igb 5.2.7 NIC driver
* [net-e1000e-3.1.0.2-glr-offline_bundle.zip](http://vibsdepot.v-front.de/wiki/index.php/Net-e1000e) – Intel e1000e 3.1.0.2 NIC driver


### 执行ESXi-Customizer-PS 批处理

第一次运行VMware vSphere PowerCLI 时可能会遇到无法加载 `*.ps1`的错误，这是因为操作系统默认禁止执行脚本，可以打开在管理员用下打开**powershell**，并执行：

```bash
Set-ExecutionPolicy remotesigned
```
新建离线驱动程序文件夹 **offline_bundles** 并将下载好的驱动文件拖至此文件夹。导航至ESXi-Customizer-PS目录，并在**PowerCLI**中运行如下命令：

```bash
.\ESXi-Customizer-PS-v2.3.ps1 
-pkgDir .\offline_bundles
-izip .\update-from-esxi5.5-5.5_update02-2068190.zip 
-nsc
```

如果编译成功，则由如下输出:

```bash
PowerCLI D:\> .\ESXi-Customizer-PS-v2.3.ps1 -pkgDir .\offline_bundles -iZip .\update-from-esxi5.5-5.5_update02-2068190.z
ip -nsc

Script to build a customized ESXi installation ISO or Offline bundle using the VMware PowerCLI ImageBuilder snapin
(Call with -help for instructions)

Logging to C:\Users\ADMINI~1\AppData\Local\Temp\ESXi-Customizer-PS.log ...

Running with PowerShell version 2.0 and VMware vSphere PowerCLI 5.8 Release 1 build 2057893

Adding base Offline bundle .\update-from-esxi5.5-5.5_update02-2068190.zip ... [OK]

Getting ImageProfiles, please wait ... [OK]

Using ImageProfile ESXi-5.5.0-20140902001-standard ...
(dated 08/23/2014 06:46:46, AcceptanceLevel: PartnerSupported,
For more information, see http://kb.vmware.com/kb/2079732.)

Loading Offline bundles and VIB files from .\offline_bundles ...
   Loading D:\offline_bundles\igb-5.2.7-1331820-offline_bundle-2157967.zip ... [OK]
      Add VIB net-igb 5.2.7-1OEM.550.0.0.1331820 [OK, replaced 5.0.5.1.1-1vmw.550.1.15.1623387]
   Loading D:\offline_bundles\net-e1000e-3.1.0.2-glr2-offline_bundle.zip ... [OK]
      Add VIB net-e1000e 3.1.0.2-glr2 [New AcceptanceLevel: CommunitySupported] [OK, replaced 1.1.2-4vmw.550.1.15.162338
7]
   Loading D:\offline_bundles\sata-xahci-1.27-1-offline_bundle.zip ... [OK]
      Add VIB sata-xahci 1.27-1 [OK, added]

Exporting the ImageProfile to 'D:\\ESXi-5.5.0-20140902001-standard-customized.iso'. Please be patient ...


All done.

PowerCLI D:\>
```
### 参考链接

[Adding multiple drivers to an ESXi 5.5 u2 ISO](http://blog.kihltech.com/2014/10/adding-multiple-drivers-to-an-esxi-5-5-u2-iso/)
[ESXi-Customizer-PS Instructions](http://www.v-front.de/p/esxi-customizer-ps.html#download)
