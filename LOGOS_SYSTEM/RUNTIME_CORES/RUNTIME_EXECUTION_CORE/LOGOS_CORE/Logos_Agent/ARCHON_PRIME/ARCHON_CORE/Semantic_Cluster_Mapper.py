"""
Semantic_Cluster_Mapper
Builds cluster topology using similarity metrics.

Groups semantic artifacts by tag and computes per-cluster density.
"""

import math


class SemanticClusterMapper:

    def cluster(self, artifacts):
        clusters = {}

        for artifact in artifacts:
            tag = artifact.get("semantic_tag", "unknown")
            clusters.setdefault(tag, []).append(artifact)

        results = []
        for tag, members in clusters.items():
            results.append({
                "cluster_id": tag,
                "member_count": len(members),
                "density": self._density(members),
                "members": members,
            })

        return results

    def _density(self, members):
        if len(members) < 2:
            return 0.1
        return math.log(len(members) + 1)
