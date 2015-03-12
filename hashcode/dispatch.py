from .room import Machine

def dispatch(room, machines, npools):
    pools = [0] * npools

    for m in sorted(machines, key=lambda m: m.capacity):
        added = False
        for row in sorted(room, key=lambda row: row.capacity):
            if row.add(m):
                added = True
                break

        if added:
            lowest_pool = next(iter(sorted(enumerate(pools), key=lambda entry: entry[1])))[0]
            m.pool = lowest_pool
            pools[lowest_pool] += m.capacity
