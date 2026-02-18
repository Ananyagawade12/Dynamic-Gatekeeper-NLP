

def find_max_gap(scores):
    sorted_scores = sorted(scores, reverse=True)

    max_gap = 0.0
    split_index = 1

    for i in range(len(sorted_scores) - 1):
        gap = sorted_scores[i] - sorted_scores[i + 1]
        if gap > max_gap:
            max_gap = gap
            split_index = i + 1

    threshold = (sorted_scores[split_index - 1] + sorted_scores[split_index]) / 2
    return threshold, split_index


def batch_relative_filter(scores, min_keep=1):
    n = len(scores)
    max_s = max(scores)
    min_s = min(scores)
    score_range = max_s - min_s

    sorted_indices = sorted(range(n), key=lambda i: scores[i], reverse=True)
    keep_mask = [False] * n

    if min_s >= 0.8:
        max_keep = max(min(5, n), min_keep)

        # z-like relative filtering (mean based)
        mean = sum(scores) / n
        for i in sorted_indices:
            if scores[i] >= mean:
                keep_mask[i] = True

        # cap max_keep
        kept = [i for i in range(n) if keep_mask[i]]
        if len(kept) > max_keep:
            for i in kept[max_keep:]:
                keep_mask[i] = False

    elif max_s <= 0.55:
        max_keep = min(2, n)
        for i in sorted_indices[:max_keep]:
            keep_mask[i] = True

    else:
        threshold, max_keep = find_max_gap(scores)

        kept = 0
        for i in sorted_indices:
            if scores[i] >= threshold:
                keep_mask[i] = True
                kept += 1
            if kept == max_keep:
                break

    if sum(keep_mask) < min_keep:
        for i in sorted_indices[:min_keep]:
            keep_mask[i] = True

    return keep_mask




def test_batch(name, scores):
    print("\n" + "-" * 30)
    print(name)
    print("-" * 30)

    mask = batch_relative_filter(scores)

    print("Scores:", scores)
    print("Keep mask:", mask)

    for i, s in enumerate(scores):
        print(f"Doc {i}: score={s} -> {'KEEP' if mask[i] else 'DISCARD'}")


test_batch("EASY BATCH", [0.92, 0.95, 0.91, 0.93, 0.90])
test_batch("HARD BATCH", [0.45, 0.42, 0.48, 0.40, 0.44])
test_batch("MIXED BATCH", [0.91, 0.87, 0.52, 0.49, 0.30])
test_batch("MIXED BATCH 2", [0.95, 0.70, 0.52, 0.39, 0.30])
test_batch("FLAT LOW", [0.46, 0.45, 0.44, 0.43, 0.42])

test_batch(
    "ALL STRONG (TIGHT)",
    [0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.91, 0.90, 0.89, 0.88]
)

test_batch(
    "STRONG WITH WEAK TAIL",
    [0.95, 0.94, 0.93, 0.92, 0.90, 0.89, 0.88, 0.70, 0.68, 0.65]
)

test_batch(
    "ALL WEAK (FLAT)",
    [0.48, 0.47, 0.46, 0.45, 0.45, 0.44, 0.43, 0.42, 0.41, 0.40]
)

test_batch(
    "MIXED WITH CLEAR GAP",
    [0.94, 0.92, 0.90, 0.89, 0.87, 0.55, 0.52, 0.50, 0.48, 0.30]
)

test_batch(
    "MIXED NOISY MIDDLE",
    [0.93, 0.90, 0.87, 0.85, 0.83, 0.60, 0.58, 0.56, 0.40, 0.30]
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

