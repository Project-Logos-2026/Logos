"""
Semantic_Extractor
Deterministic semantic ingestion engine.

Ingests text blocks and produces semantic nuggets with natural language,
semantic tags, lambda expressions, and PXL formalisms.
"""


class SemanticExtractor:

    def __init__(self):
        self.tick_counter = 0

    def extract(self, text_block: str, source_path: str):
        sentences = self._split_sentences(text_block)
        nuggets = []

        for i in range(0, len(sentences) - 1):
            window = sentences[i:i + 2]
            nugget = {
                "nugget_id": f"NUG_{self.tick_counter}_{i}",
                "source_path": source_path,
                "natural_language": " ".join(window),
                "semantic_tag": self._derive_tag(window),
                "lambda_expression": self._lambda(window),
                "pxl_formalism": self._pxl(window),
            }
            nuggets.append(nugget)

        self.tick_counter += 1
        return nuggets

    def _split_sentences(self, text: str):
        return [s.strip() for s in text.split(".") if s.strip()]

    def _derive_tag(self, window):
        if "therefore" in " ".join(window).lower():
            return "inference"
        return "semantic_statement"

    def _lambda(self, window):
        return f"λx. {window[0]}"

    def _pxl(self, window):
        return f"{window[0]} ⟹ {window[-1]}"
