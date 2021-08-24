import sys, os
import subprocess


def check_args(args):
    if len(args) == 2:
        name_device = args[1]
        name_file = '20-local.rules'
    elif len(sys.argv) == 3:
        name_device = args[1]
        name_file = args[2]
        if not name_file.endswith('.rules'):
            raise AttributeError('Invalid name file of rules')
    else:
        raise AttributeError('Invalid count arguments')
    if not name_device.startswith('ttyUSB') and name_device[6:].isnumeric():
        raise AttributeError('Invalid name for mapping')
    return name_device, name_file


def get_condition_unique(output):
    i_first_kernels_attr = output.index(b'KERNELS=="1')
    i_second_kernels_attr = i_first_kernels_attr + 11 + output[i_first_kernels_attr + 10:].index(b'"')
    return output[i_first_kernels_attr: i_second_kernels_attr]


def build_rules(kernels_attr, name_file):
    port_was_setup = False
    num_line = 0
    with open(f'/etc/udev/rules.d/{name_file}', 'r') as file_r:
        for row in file_r.readlines():
            if kernels_attr.decode('utf8') in row:
                port_was_setup = True
                break
            num_line += 1
    with open(f'/etc/udev/rules.d/{name_file}', 'a') as file_w:
        if not port_was_setup:
            line_kernels_attr = kernels_attr.decode('utf8')
            file_w.write(line_kernels_attr + ', SYMLINK+=\"tgw' + str(num_line) + '"\n')


if __name__ == "__main__":
    name_device, name_file = check_args(sys.argv)
    output = subprocess.run(['udevadm', 'info', f'--name=/dev/{name_device}', '--attribute-walk'], stdin=None, stdout=subprocess.PIPE).stdout
    kernels_attr = get_condition_unique(output)
    build_rules(kernels_attr, name_file)
    os.system('udevadm trigger')
