import enum
from collections import namedtuple


class Room(object):

    def __init__(self, rows, slots):
        self.rows = [Row(self, y, slots) for y in range(rows)]

    def __getitem__(self, pos):
        y = pos
        x = None

        if isinstance(pos, (tuple)):
            (y, x) = pos

        row = self.rows[y]
        if x is None:
            return row

        slot = row[x]
        return slot

    def __setitem__(self, pos, item):
        (y, x) = pos

        row = self.rows[y]
        row[x] = item

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def dump(self):
        s = ''

        return s


class Row(object):
    MultiSlot = namedtuple('MultiSlot', ['slot', 'size'])

    def __init__(self, room, y, size):
        self.room = room
        self.y = y

        self.slots = [Slot(self.room, self.y, x) for x in range(size)]

    def find_slot(self, item):
        _filter = lambda slot: not slot.slot.occupied
        for slot in filter(_filter, self.slots_iter()):
            if slot.size >= item.size:
                return slot.slot

        return None

    def add(self, item):
        slot = self.find_slot(item)

        if slot is not None:
            slot.put(item)
            return True

        return False

    def slots_iter(self, merged=True):
        i = 0
        while i < len(self.slots):
            slot = self.slots[i]

            if slot.occupied:
                size = slot.content.size

                yield Row.MultiSlot(slot, size)
            else:
                size = 1

                if merged:
                    for j in range(i + 1, len(self.slots)):
                        other = self.slots[j]
                        if other.occupied:
                            break
                        size += 1

                yield Row.MultiSlot(slot, size)

            i += size

    @property
    def capacity(self):
        _filter = lambda slot: slot.slot.occupied and isinstance(slot.slot.content, Machine)
        slots = [slot.slot for slot in filter(_filter, self.slots_iter())]
        return sum(slot.content.capacity for slot in slots)

    def __getitem__(self, pos):
        return self.slots[pos]

    def __setitem__(self, pos, item):
        start = pos
        end = pos + item.size

        slots = self.slots[start:end]
        for slot in slots:
            slot.content = item

        item.slot = slots[0]

    def __len__(self):
        return sum(1 for slot in self.slots if not slot.occupied)

    def __iter__(self):
        return iter(self.slots)


class Slot(object):

    def __init__(self, room, y, x):
        self.room = room
        self.y = y
        self.x = x

        self.content = None

    def put(self, item):
        self.row[self.x] = item

    @property
    def pos(self):
        return (self.y, self.x)

    @property
    def row(self):
        return self.room[self.y]

    @property
    def occupied(self):
        return self.content is not None

    def __repr__(self):
        return '<Slot (%d, %d) = %r>' % (self.y, self.x, self.content)


class Content(object):

    def __init__(self, slot=None):
        self.slot = slot


class UnknownContent(Content):
    size = 1


class Machine(Content):

    def __init__(self, spec, slot=None):
        super().__init__(slot)
        self.spec = spec

        self.pool = None

    def dump(self):
        if self.slot is None:
            return 'x'

        assert self.pool is not None
        return '%d %d %d' % (self.slot.y, self.slot.x, self.pool)

    @property
    def size(self):
        return self.spec.size

    @property
    def capacity(self):
        return self.spec.capacity

    def __repr__(self):
        return '<%r %r>' % (self.spec, self.pool)
