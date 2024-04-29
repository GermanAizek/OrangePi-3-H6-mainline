#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0+
#
# Author: Herman Semenov <GermanAizek@yandex.ru>
#

from pick import pick
import os, subprocess
import psutil

title = 'Choose your building variant linux kernel for Orange Pi 3: '
options = ['U-boot without eMMC', 'U-boot with eMMC']
option, index = pick(options, title, indicator='=>', default_index=0)

title = 'Choose destination disk for create image: '
devices = subprocess.getoutput('lsblk -o NAME -nl').splitlines()
option_sdcard, index_sdcard = pick(devices, title, indicator='=>', default_index=0)

# install packages
print('[INFO] Installing packages...')
os.system('sudo apt install build-essential gcc-aarch64-linux-gnu flex bison libssl-dev python3 swig rsync device-tree-compiler')

# building arm-trusted-firmware
print('[INFO] Building arm-trusted-firmware...')
os.chdir('arm-trusted-firmware')
os.system('make clean')
os.system('CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 make -j$(nproc --all) PLAT=sun50i_h6 PRELOADED_BL33_BASE=0x40010000')
os.chdir('..')

# building aw-el2-barebone
print('[INFO] Building aw-el2-barebone...')
os.chdir('aw-el2-barebone')
os.system('make clean')
os.system('CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 make -j$(nproc --all) ')
os.chdir('..')

# building u-boot-el1-hyp
print('[INFO] Building u-boot-el1-hyp...')
if option == 'U-boot without eMMC':
	os.chdir('u-boot-el1-hyp')
	os.system('make clean')
	os.system('cp ../arm-trusted-firmware/build/sun50i_h6/release/bl31.bin bl31.bin')
	os.system('cp ../aw-el2-barebone/el2-bb.bin hyp.bin')
	os.system('cp ../configs/u-boot-el1-hyp-config .config')
else:
	os.chdir('u-boot-el1-hyp-emmc')
	os.system('make clean')
	os.system('cp ../arm-trusted-firmware/build/sun50i_h6/release/bl31.bin bl31.bin')
	os.system('cp ../aw-el2-barebone/el2-bb.bin hyp.bin')
	os.system('cp ../configs/u-boot-el1-hyp-config .config')
	
os.system('CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64 make -j$(nproc --all)')
os.system('dd if=u-boot-sunxi-with-spl.bin of={0} bs=1024 seek=8'.format(option_sdcard))
os.chdir('..')

# compiling linux kernel
os.system('cp configs/linux-5.7.4-config linux-5.7.4/.config')
os.system('make -j$(nproc --all) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs modules')
os.system('make -j$(nproc --all) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-')
os.system('make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=output modules_install')
os.system('make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- INSTALL_MOD_PATH=output headers_install INSTALL_HDR_PATH=output/usr')

# copying binaries
os.system('cp -R linux-5.7.4/arch/arm64/boot/Image /media/debian/armbi_root/boot/')
os.system('cp -R linux-5.7.4/arch/arm64/boot/dts/* /media/debian/armbi_root/boot/dtbs/')
os.system('cp -R linux-5.7.4/output/lib/ /media/debian/armbi_root/usr/')
os.system('cp -R linux-5.7.4/output/usr/ /media/debian/armbi_root/')