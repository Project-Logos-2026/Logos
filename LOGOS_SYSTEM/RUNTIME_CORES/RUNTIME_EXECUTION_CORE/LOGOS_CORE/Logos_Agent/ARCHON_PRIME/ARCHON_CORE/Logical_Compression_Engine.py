"""
Logical_Compression_Engine
Compresses semantic fragments into reusable formal artifacts.

Groups nuggets by semantic tag and merges them into compressed logical
statements for downstream principle discovery.
"""


class LogicalCompressionEngine:

    def compress(self, nuggets):
        groups = {}

        for nugget in nuggets:
            key = nugget["semantic_tag"]
            groups.setdefault(key, []).append(nugget)

        compressed = []
        for tag, items in groups.items():
            compressed.append({
                "logic_family": tag,
                "source_count": len(items),
                "compressed_statement": self._merge(items),
            })

        return compressed

    def _merge(self, items):
        statements = [i["natural_language"] for i in items]
        return " | ".join(statements[:3])
