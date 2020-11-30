import hpmiko
import getpass

password = getpass.getpass()

myswitch = hpmiko.HP("172.16.1.62", "manager", password)
myswitch.connect()

hostname = myswitch.get_hostname()
print(f"hostname: {hostname}")
