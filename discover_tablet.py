#!/usr/bin/env python3
from subprocess import run
from typing import Any

import yaml


def main():
    out = run(["libinput", "list-devices"], capture_output=True, text=True)
    out.check_returncode()
    for devicelines in out.stdout.split("\n\n"):
        device = dict()
        for line in devicelines.splitlines():
            split = line.split(":", maxsplit=1)
            if len(split) != 2:
                continue
            k = split[0].strip()
            v = split[1].strip()
            device[k] = v
        try:
            is_found = device['Capabilities'] == 'tablet-pad' and device['Device'] == 'HUION Huion Tablet_GS1331'
        except KeyError:
            continue
        if is_found:
            with open("config.yaml", "r+") as f:
                config: dict[str, Any] = yaml.safe_load(f)
                for i, dev_cfg in enumerate(config["devices"]):
                    if dev_cfg["input_name"] == 'HUION Huion Tablet_GS1331':
                        dev_cfg["input_fn"] = device["Kernel"]
                    config["devices"][i] = dev_cfg
                    f.seek(0)
                    yaml.dump(config, f)



if __name__ == "__main__":
    main()
