from datetime import (
    datetime,
    timedelta,
    timezone,
)
from decimal import Decimal
from typing import (
    Iterable,
    Mapping,
)


_unix_epoch_start = datetime(1970, 1, 1, tzinfo=timezone.utc)


def appearance(
    intervals: Mapping[str, Iterable[int | float | Decimal | bool | str | datetime]],
) -> Decimal:
    validated_intervals: dict[str, list[Decimal]] = {k: [] for k in intervals}
    for entity, timestamps in intervals.items():
        for i, timestamp_ in enumerate(timestamps):
            if isinstance(timestamp_, datetime):
                validated_timestamp = Decimal(timestamp_.timestamp())
            elif isinstance(timestamp_, (int, float, Decimal, bool, str)):
                # To correctly handle negative `timestamp_` values
                # (dates before the Unix epoch),
                # we avoid using `datetime.fromtimestamp()`,
                # as it does not support negative timestamps.
                # Instead, compute the date by adding the specified number of seconds
                # to the epoch start:
                _unix_epoch_start + timedelta(seconds=float(timestamp_))

                validated_timestamp = Decimal(timestamp_)
            else:
                raise ValueError(
                    f"Item '{timestamp_}' for entity '{entity}'"
                    "is not timestamp-serializable"
                )
            validated_intervals[entity].append(validated_timestamp)

        else:
            if timestamps and ((timestamps_lenght := (i + 1)) >= 2):
                if timestamps_lenght % 2:
                    raise ValueError(f"Odd number of timestamps for entity '{entity}'")
            else:
                raise ValueError(
                    f"Not enough timestamps for entity '{entity}': "
                    f"({timestamps_lenght if timestamps else 0}"
                )

    enters_or_exits = list(
        (timestamp_, 1 - 2 * (i % 2), k)
        for k in validated_intervals
        for i, timestamp_ in enumerate(validated_intervals[k])
    )
    enters_or_exits.sort()

    appearance_counts = dict.fromkeys(validated_intervals, 0)
    total_overlap_time = Decimal(0)
    start_time = Decimal(-1)
    for enter_or_exit in enters_or_exits:
        appearance_counts[enter_or_exit[2]] += enter_or_exit[1]
        if all(appearance_counts.values()):
            if start_time == -1:
                start_time = enter_or_exit[0]
        elif start_time > -1:
            total_overlap_time += enter_or_exit[0] - start_time
            start_time = Decimal(-1)

    return total_overlap_time


if __name__ == "__main__":
    tests = [
        {
            "intervals": {
                "lesson": [1594663200, 1594666800],
                "pupil": [
                    1594663340,
                    1594663389,
                    1594663390,
                    1594663395,
                    1594663396,
                    1594666472,
                ],
                "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
            },
            "answer": 3117,
        },
        {
            "intervals": {
                "lesson": [1594702800, 1594706400],
                "pupil": [
                    1594702789,
                    1594704500,
                    1594702807,
                    1594704542,
                    1594704512,
                    1594704513,
                    1594704564,
                    1594705150,
                    1594704581,
                    1594704582,
                    1594704734,
                    1594705009,
                    1594705095,
                    1594705096,
                    1594705106,
                    1594706480,
                    1594705158,
                    1594705773,
                    1594705849,
                    1594706480,
                    1594706500,
                    1594706875,
                    1594706502,
                    1594706503,
                    1594706524,
                    1594706524,
                    1594706579,
                    1594706641,
                ],
                "tutor": [
                    1594700035,
                    1594700364,
                    1594702749,
                    1594705148,
                    1594705149,
                    1594706463,
                ],
            },
            "answer": 3577,
        },
        {
            "intervals": {
                "lesson": [1594692000, 1594695600],
                "pupil": [1594692033, 1594696347],
                "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
            },
            "answer": 3565,
        },
    ]
    for i, test in enumerate(tests):
        test_answer = appearance(test["intervals"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
