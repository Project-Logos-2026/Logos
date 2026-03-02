
CLASSIFICATION_LADDER = {
    "rejected": 0,
    "conditional": 1,
    "provisional": 2,
    "canonical": 3,
}

class ClassificationError(Exception):
    pass

def validate_transition(current: str, target: str):
    if current not in CLASSIFICATION_LADDER or target not in CLASSIFICATION_LADDER:
        raise ClassificationError("Invalid classification state.")
    if CLASSIFICATION_LADDER[target] < CLASSIFICATION_LADDER[current]:
        raise ClassificationError("Classification regression not allowed.")
    if current == "canonical" and target != "canonical":
        raise ClassificationError("Cannot downgrade from canonical.")
    return True
