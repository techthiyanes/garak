#!/usr/bin/env python3

import logging
from colorama import Fore, Style

from garak.harness.base import Harness

import garak._plugins as _plugins


class PxD(Harness):
    def __init__(self):
        super().__init__()

    def run(self, model, probe_names, detector_names, evaluator):
        probe_names = sorted(probe_names)
        detector_names = sorted(detector_names)
        print(
            f"🕵️  queue of {Style.BRIGHT}{Fore.LIGHTYELLOW_EX}probes:{Style.RESET_ALL} "
            + ", ".join([name.replace("probes.", "") for name in probe_names])
        )
        print(
            f"🔎 queue of {Style.RESET_ALL}{Fore.LIGHTBLUE_EX}detectors:{Style.RESET_ALL} "
            + ", ".join([name.replace("detectors.", "") for name in detector_names])
        )
        logging.info("probe queue: " + " ".join(probe_names))
        for probename in probe_names:
            try:
                probe = _plugins.load_plugin(probename)
            except Exception as e:
                message = f"{probename} load exception 🛑, skipping >>"
                print(message)
                logging.error(message + " " + str(e))
                continue
            if not probe:
                message = f"{probename} load failed ⚠️, skipping >>"
                print(message)
                logging.warning(message)
                continue
            detectors = []
            for detector_name in detector_names:
                detector = _plugins.load_plugin(detector_name, break_on_fail=False)
                if detector:
                    detectors.append(detector)
                else:
                    print(f" detector load failed: {detector_name}, skipping >>")
                    logging.error(
                        f" detector load failed: {detector_name}, skipping >>"
                    )
            h = Harness()
            h.run(model, [probe], detectors, evaluator, announce_probe=False)
            # del probe, h, detectors
