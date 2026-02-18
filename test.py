from batch_relative_filter import batch_relative_filter


def test_batch(name, scores):
    print()
    print(name)

    mask = batch_relative_filter(scores)

    print("Scores:", scores)
    print("Keep mask:", mask)

    for i, s in enumerate(scores):
        print(f"Doc {i}: score={s:.2f} -> {'KEEP' if mask[i] else 'DISCARD'}")


if __name__ == "__main__":

    test_batch(
        "ALL STRONG (TIGHT)",
        [0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.91, 0.90, 0.89, 0.88]
    )

    test_batch(
        "STRONG WITH WEAK TAIL",
        [0.95, 0.94, 0.93, 0.92, 0.90, 0.89, 0.88, 0.70, 0.68, 0.65]
    )

    test_batch(
        "MIXED WITH CLEAR GAP",
        [0.94, 0.92, 0.90, 0.89, 0.87, 0.55, 0.52, 0.50, 0.48, 0.30]
    )

    test_batch(
        "ONE STRONG REST WEAK",
        [0.96, 0.55, 0.54, 0.53, 0.52, 0.51, 0.50, 0.48, 0.45, 0.40]
    )
    test_batch(
        "TWO PEAKS",
        [0.95, 0.94, 0.80, 0.79, 0.78, 0.55, 0.53, 0.50, 0.48, 0.45]
    )

    test_batch(
        "FLAT MID RANGE",
        [0.62, 0.61, 0.60, 0.60, 0.59, 0.58, 0.57, 0.56, 0.55, 0.54]
    )

    test_batch(
        "GRADUAL DECAY",
        [0.95, 0.98, 0.90, 0.88, 0.82, 0.80, 0.78, 0.76, 0.74, 0.72]
    )

    test_batch(
        "ADVERSARIAL",
        [0.91, 0.89, 0.88, 0.87, 0.86, 0.85, 0.50, 0.49, 0.48, 0.47]
    )
