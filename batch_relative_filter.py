import statistics as stats


def z_normalize(scores):
    mean = stats.mean(scores)
    std = stats.pstdev(scores) or 1e-6
    return [(s - mean) / std for s in scores]


def find_max_gap_z(z_scores):
    sorted_z = sorted(z_scores, reverse=True)

    max_gap = 0.0
    split_index = 1

    for i in range(len(sorted_z) - 1):
        gap = sorted_z[i] - sorted_z[i + 1]
        if gap > max_gap:
            max_gap = gap
            split_index = i + 1

    threshold_z = (sorted_z[split_index - 1] + sorted_z[split_index]) / 2
    return threshold_z, split_index


def batch_relative_filter(scores, min_keep=1):
    """
    Args:
        scores (List[float]): Raw confidence scores (logits or probabilities)
        min_keep (int): Minimum number of documents to keep

    Returns:
        List[bool]: Keep/Discard mask for each document
    """
    n = len(scores)
    keep_mask = [False] * n

    max_s = max(scores)
    min_s = min(scores)
    score_range = max_s - min_s

    sorted_indices = sorted(range(n), key=lambda i: scores[i], reverse=True)

    # CASE 1: Flat distribution
    if score_range < 0.12:
        max_keep = min(3, n)
        for i in sorted_indices[:max_keep]:
            keep_mask[i] = True

    else:
        z_scores = z_normalize(scores)

        # CASE 2: Strong cluster
        if min_s >= 0.8:
            max_keep = min(5, n)
            for i in sorted_indices:
                if z_scores[i] >= 0:
                    keep_mask[i] = True

            kept = [i for i in sorted_indices if keep_mask[i]]
            for i in kept[max_keep:]:
                keep_mask[i] = False

        # CASE 3: Weak cluster
        elif max_s <= 0.55:
            max_keep = min(2, n)
            for i in sorted_indices[:max_keep]:
                keep_mask[i] = True

        # CASE 4: Mixed distribution
        else:
            threshold_z, max_keep = find_max_gap_z(z_scores)
            kept = 0

            for i in sorted_indices:
                if z_scores[i] >= threshold_z:
                    keep_mask[i] = True
                    kept += 1
                if kept == max_keep:
                    break

    # Safety net
    if sum(keep_mask) < min_keep:
        for i in sorted_indices[:min_keep]:
            keep_mask[i] = True

    return keep_mask
