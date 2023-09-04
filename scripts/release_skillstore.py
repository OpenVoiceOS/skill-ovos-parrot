import json
from os.path import join, dirname

base_dir = dirname(dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version_file = join(base_dir, 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


desktop_dir = join(base_dir, "res", "desktop")

jsonf = join(desktop_dir, "skill.json")

with open(jsonf) as f:
    data = json.load(f)

data["branch"] = "v" + get_version()

with open(jsonf, "w") as f:
    json.dump(data, f, indent=4)
