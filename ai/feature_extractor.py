def normalize_findings(findings):
    merged = {}
    for f in findings:
        key = f["issue"]
        if key not in merged:
            merged[key] = {
                "issue": key,
                "confidence": f["confidence"],
                "evidence": list(f["evidence"]),
                "seen_in_images": 1,
            }
        else:
            m = merged[key]
            m["confidence"] = max(m["confidence"], f["confidence"])
            for e in f["evidence"]:
                if e not in m["evidence"]:
                    m["evidence"].append(e)
            m["seen_in_images"] += 1
    return sorted(merged.values(), key=lambda x: x["confidence"], reverse=True)
