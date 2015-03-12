from collections import namedtuple

Slot = namedtuple('Slot', ['x', 'y'])
Machine = namedtuple('Machine', ['no', 'size', 'capacity'])


spec_fields = ['rows', 'slots', 'unavailables', 'pools', 'machines']


class Specification(namedtuple('Specification', spec_fields)):

    @staticmethod
    def parse(f):
        def read_numbers(f):
            return [int(part) for part in f.readline().split()]

        # Parse header
        [rows, slots, unavailables_count, pools,
            machines_count] = read_numbers(f)

        assert 1 <= rows <= 1000
        assert 1 <= slots <= 1000
        assert 0 <= unavailables_count <= rows * slots
        assert 1 <= pools <= 1000
        assert 1 <= machines_count <= rows * slots

        # Parse unavailable slots
        unavailables = []
        for _ in range(unavailables_count):
            [x, y] = read_numbers(f)
            unavailables.append(Slot(x, y))

        # Parse machines
        machines = []
        for no in range(machines_count):
            [size, capacity] = read_numbers(f)
            machines.append(Machine(no, size, capacity))

        return Specification(rows, slots, unavailables, pools, machines)
