import sys
import subprocess


if __name__ == "__main__":
    name_device = sys.argv[1]
    if not name_device.startswith('ttyUSB') and name_device[6:].isnumeric():
        raise AttributeError('Invalid name for mapping')
    output = subprocess.run(['udevadm', 'info', f'--name=/dev/{name_device}', '--attribute-walk'], stdout=subprocess.PIPE).stdout
    i_first_kernels_attr = output.index(b'KERNELS=="1')
    i_second_kernels_attr = i_first_kernels_attr + 11 + output[i_first_kernels_attr+10:].index(b'"')
    kernels_attr = output[i_first_kernels_attr: i_second_kernels_attr]
