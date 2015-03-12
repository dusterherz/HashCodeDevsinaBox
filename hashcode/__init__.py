from argparse import ArgumentParser
from pathlib import Path
from .dispatch import dispatch
from .room import Room, UnknownContent, Machine
from .spec import Specification

parser = ArgumentParser()
parser.add_argument('input_file')


def main(args):
    # Parse specs
    with Path(args.input_file).open('r') as f:
        spec = Specification.parse(f)

    # Create room and fill it
    room = Room(spec.rows, spec.slots)

    for (y, x) in spec.unavailables:
        room[y, x] = UnknownContent()

    machines = [Machine(m_spec) for m_spec in spec.machines]

    # Do the magic here.
    dispatch(room, machines, spec.pools)

    # Print result.
    for m in machines:
        print(m.dump())
