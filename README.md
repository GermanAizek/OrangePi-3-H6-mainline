# Orange Pi 3 H6 mainline
Mainline kernel Orange Pi 3 (Allwinner H6) with USB3, WiFi, Ethernet, PCI-E patches. EL2 Hypervisor for quirky PCI-E controller.

*Warning!* Its not tested on LTS version.

### Content
* arm-trusted-firmware: ARM Trusted Firmware-A
* aw-el2-barebone: Allwinner SoCs' 64-bit EL2 barebone hypervisor for PCI-E quirky controller.
* u-boot-2022.10: Mainline u-boot with native eMMC support.
* u-boot-2019.04: Mainline u-boot. (not needed)
* u-boot-el1-hyp: Patched u-boot with BL31 and hypervisor support for PCI-Eb quirky controller.
* u-boot-el1-hyp-emmc: Patched u-boot with BL31 and hypervisor support for PCI-Eb quirky controller. Support for boot from EMMC 8GB.
* linux-5.7.4: Mainline kernel + out of tree patches for USB3, WiFi Ethernet, PCI-E controller.
* configs: u-boot-2019.04 and linux-5.7.4 configuration files.
* dts: custom dts for the Orange Pi 3 (adds emac support to mainline dts as of 11/16/2022)

* **the experimental/ folder contains a new PCIe sunxi module, gmac patches and a dts for newer kernels.**

### Instructions

#### Build environment
* Debian 12 (Bookworm)

#### building from sources

```bash
sudo python ./build.py
```

**Copying to SD card is hardcoded in build.py, edit your media path**

### Booting from eMMC

Before you follow these instructions you must have prepared the partition on the eMMC. Create a single partition and format it (mkfs.ext4 -O ^64bit /dev/mmcblk1p1).

```bash
echo 0 > /sys/block/mmcblk1boot0/force_ro
echo 0 > /sys/block/mmcblk1boot1/force_ro
mmc bootbus set single_hs x1 x4 /dev/mmcblk1
mmc bootpart enable 1 1 /dev/mmcblk1
dd if=u-boot-sunxi-with-spl.bin of=/dev/mmcblk1boot0 bs=4k
dd if=u-boot-sunxi-with-spl.bin of=/dev/dev/mmcblk1 bs=1k seek=8
```

### Addendum for mainline kernel 5.19.8 or later (no PCIe support)

To get the Orange Pi 3 to boot on mainline kernel with u-boot-2022.10. The mainline kernel now includes support for ethernet, USB3, eMMC (but no PCIe support):
* compile arm-trusted-firmware v2.2, move bl31.bin to the u-boot-2022.10 directory.
* copy dts/sun50i-h6-orangepi-3.dts to u-boot-2022.10/arch/arm/dts/sun50i-h6-orangepi-3.dts
* compile u-boot-2022.10.
* extract ArchLinuxARM-aarch64-latest.tar.gz on the SD card.
* copy u-boot-2022.10/arch/arm/dts/sun50i-h6-orangepi-3.dtb to the SD card at /boot/dtbs/allwinner/sun50i-h6-orangepi-3.dtb

### References

* https://lkml.org/lkml/2019/4/5/863
* https://github.com/megous/linux/tree/opi3-5.1
* http://linux-sunxi.org/Xunlong_Orange_Pi_3
* https://notsyncing.net/?p=blog&b=2016.orangepi-pc-custom-kernel
* https://forum.armbian.com/topic/13529-a-try-on-utilizing-h6-pcie-with-virtualization/
* https://megous.com/git/linux/commit/?h=orange-pi-5.7&id=9607a07062fdae6e410d32d4807365c5e542b18d
* https://linux-sunxi.org/Bootable_eMMC
* https://oftc.irclog.whitequark.org/linux-sunxi/2022-03-16
* https://patchwork.kernel.org/project/linux-arm-kernel/patch/20190411101951.30223-6-megous@megous.com/


