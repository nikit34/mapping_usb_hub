import sys
import subprocess


if __name__ == "__main__":
    name_device = sys.argv[1]
    if not name_device.startswith('ttyUSB') and name_device[6:].isnumeric():
        raise AttributeError('Invalid name for mapping')
    output = subprocess.run(['udevadm', 'info', f'--name=/dev/{name_device}', '--attribute-walk'], stdin=None, stdout=subprocess.PIPE).stdout
    i_first_kernels_attr = output.index(b'KERNELS=="1')
    i_second_kernels_attr = i_first_kernels_attr + 11 + output[i_first_kernels_attr+10:].index(b'"')
    kernels_attr = output[i_first_kernels_attr: i_second_kernels_attr]
    port_was_setup = False
    num_line = 0
    with open('/etc/udev/rules.d/10-local.rules', 'a+') as file:
        for row in file.readlines():
            if kernels_attr in row:
                port_was_setup = True
                break
            num_line += 1
    if not port_was_setup:
        file.write(kernels_attr + ', SYMLINK+="tgw' + str(num_line) + '"')
    subprocess.run(['sudo udevadm trigger'], stdin=None, stdout=None)