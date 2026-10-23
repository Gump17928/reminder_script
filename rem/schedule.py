"""When a reminder fires."""


def minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def occurrences(r):
    """Minutes-since-midnight at which a reminder fires: its times, plus repeats.

    Repeats start at the first time and step by r["every"] (the last gap repeats)
    until r["until"].
    """
    times = [minutes(t) for t in r["time"]]
    out, gaps = set(times), r["every"]
    end, t = minutes(r["until"]), times[0]
    for i in range(1440 if gaps else 0):
        t += gaps[min(i, len(gaps) - 1)]
        if t > end:
            break
        out.add(t)
    return sorted(out)
