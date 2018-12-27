import sys


def main():
    assert len(sys.argv) >= 2
    which_version = sys.argv[1]
    assert which_version in ('patch', 'minor')
    version_path = 'awe/resources/VERSION'
    with open(version_path) as f:
        version = f.read()
    major, minor, patch = version.split('.')
    if which_version == 'patch':
        patch = str(int(patch) + 1)
    else:
        patch = 0
        minor = str(int(minor) + 1)
    with open(version_path, 'w') as f:
        f.write('{}.{}.{}'.format(major, minor, patch))


if __name__ == '__main__':
    main()
