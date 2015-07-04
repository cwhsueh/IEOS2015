[System Configurations]

Host:
	Platform: Raspberry Pi 2 Model B
	OS: Raspbian (release date: 2015-05-05)
	Kernel version: 3.18

Client:
	Platform: PC
	OS: Ubuntu 14.04.2
	Kernel version: 3.16


[Host Setup Steps]

1. Download and install the newest Raspbian.

2. Load usbip kernel modules.

	-sudo insmod usbip-core
	-sudo insmod usbip-host

   If corresponding kernel modules cannot be found,
   you will need to compile linux kernel with built-in usbip support by yourself,
   or, alternatively, you can compile it into seperate kernel modules if your kernel supports.

   The source code of usbip kernel modules for raspbian can be found at:

   https://github.com/raspberrypi/linux/tree/rpi-3.18.y/drivers/usb/usbip
   

3. Compile usbip user programs. You can find the source in the archive,
   though it's recommended to download from the newest source tree,
   which can be found here:

   https://github.com/raspberrypi/linux/tree/rpi-3.18.y/tools/usb/usbip

4. Run usbip host daemon.

	-sudo ./usbipd -D

5. List all the exportable usb devices.

	-sudo ./usbip list -l

6. Bind usb devices found on host

	-sudo ./usbip bind -b <device-bus-id>



[Client Setup Steps]

1. Load usbip kernel modules.

	-sudo insmod usbip-core
	-sudo insmod vhci-hcd

   If corresponding kernel modules cannot be found,
   you will need to compile linux kernel with built-in usbip support by yourself,
   or, alternatively, you can compile it into seperate kernel modules if your kernel supports.
   
   The source code of usbip kernel modules for linux can be found at:

   https://github.com/torvalds/linux/tree/master/drivers/usb/usbip

2. Compile usbip user programs. You can find the source in the archive,
   though it's recommended to download from the newest source tree,
   which can be found here:

   https://github.com/torvalds/linux/tree/master/tools/usb/usbip

5. List all the importable usb devices on host.

	-sudo ./usbip list -r <host-ip-address>

6. Attach usb devices found on host

	-sudo ./usbip attach -r <host-ip-address> -b <device-bus-id>