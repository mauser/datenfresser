import os

def pushUdevNotification( notification ):
	print "enter push"
	#udevNotificationLock.acquire()
	udevNotificationList.append( notification )
	#udevNotificationLock.release()
	print "leave push"

def getNextUdevNotification():
	print "calling getNextUdev"
	element = []
	#udevNotificationLock.acquire()
	if len(udevNotificationList) > 0:
		element = udevNotificationList.pop( )
	#udevNotificationLock.release()
	print "after get"
	return [element]

class UdevListener():
	
	def run(self):

		main_pid = os.getpid()

		pid = os.fork()
		if pid > 0:
			return
		else:
			print "dbus process has pid: " + str(os.getpid())	
			#code taken from http://stackoverflow.com/questions/5109879/usb-devices-udev-and-d-bus 
			import dbus
			import gobject
			from dbus.mainloop.glib import DBusGMainLoop


			#ignore our own signal
			signal.signal(signal.SIGUSR1, signal.SIG_IGN)

			def device_added_callback(device):
			    print 'Device %s was added' % (device)
			    print "sending to %s " % main_pid
			    #os.kill( main_pid , signal.SIGUSR1 ) 
			    #pushUdevNotification(device)
			
			    bus = dbus.SystemBus()
			    ud_manager_obj = bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
			    ud_manager = dbus.Interface(ud_manager_obj, 'org.freedesktop.UDisks')

			    for dev in ud_manager.EnumerateDevices():
				
				device_obj = bus.get_object("org.freedesktop.UDisks", dev)
				device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
				
				interface = device_props.Get('org.freedesktop.UDisks.Device', "DriveConnectionInterface")
				if interface == "usb" or interface == "firewire":
					print "usb found"
					device_file = device_props.Get('org.freedesktop.UDisks.Device', "DeviceFile")
					device_file = device_file[device_file.rfind("/")+1:]
					device = device[device.rfind("/")+1:]
					if device == device_file:
						
						#let the udev mount it..
						sleep(1)
						print device_props.Get('org.freedesktop.UDisks.Device', "DeviceMountPaths")


			def device_changed_callback(device):
				pass
				
			#must be done before connecting to DBus
			DBusGMainLoop(set_as_default=True)

			bus = dbus.SystemBus()

			proxy = bus.get_object("org.freedesktop.UDisks", 
					       "/org/freedesktop/UDisks")
			iface = dbus.Interface(proxy, "org.freedesktop.UDisks")

			devices = iface.get_dbus_method('EnumerateDevices')()
			
			


			#print '%s' % (devices)

			#addes two signal listeners
			iface.connect_to_signal('DeviceAdded', device_added_callback)
			iface.connect_to_signal('DeviceChanged', device_changed_callback)

			#start the main loop
			mainloop = gobject.MainLoop()
			mainloop.run()

