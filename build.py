#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0+
#
# Author: Herman Semenov <GermanAizek@yandex.ru>
#

from pick import pick
import os

title = 'Choose your building variant linux kernel for Orange Pi 3: '
options = ['U-boot without eMMC', 'U-boot with eMMC']
option, index = pick(options, title, indicator='=>', default_index=0)

# install packages
os.system('sudo apt install build-essential gcc-aarch64-linux-gnu flex bison libssl-dev python3 swig rsync device-tree-compiler')

# building arm-trusted-firmware
os.chdir('arm-trusted-firmware')
os.system('make -j$(nproc) CROSS_COMPILE=aarch64-linux-gnu- PLAT=sun50i_h6 PRELOADED_BL33_BASE=0x40010000')
os.chdir('..')

# building aw-el2-barebone
os.chdir('aw-el2-barebone')
os.system('make -j$(nproc) ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-')
os.chdir('..')

# building u-boot-el1-hyp
if option == 'U-boot without eMMC':
	os.system('cp arm-trusted-firmware/build/sun50i_h6/release/bl31.bin u-boot-el1-hyp/bl31.bin')
	os.system('cp aw-el2-barebone/el2-bb.bin u-boot-el1-hyp/hyp.bin')
	os.system('cp configs/u-boot-el1-hyp-config u-boot-el1-hyp/.config')
	os.chdir('u-boot-el1-hyp')	
else:
	os.system('cp arm-trusted-firmware/build/sun50i_h6/release/bl31.bin u-boot-el1-hyp-emmc/bl31.bin')
	os.system('cp aw-el2-barebone/el2-bb.bin u-boot-el1-hyp-emmc/hyp.bin')
	os.system('cp configs/u-boot-el1-hyp-config u-boot-el1-hyp-emmc/.config')
	os.chdir('u-boot-el1-hyp-emmc')
	
os.system('make -j$(nproc) CROSS_COMPILE=aarch64-linux-gnu-')
os.chdir('..')


	
