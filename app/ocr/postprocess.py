import re

class PostProcessor:
    def process(self, text: str) -> str:
        text = self.fix_hyphenation(text)
        text = self.remove_noise(text)
        text = self.correct_common_errors(text)
        text = self.normalize_whitespace(text)
        return text.strip()

    def fix_hyphenation(self, text):
        return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    def normalize_whitespace(self, text):
        text = re.sub(r'\n{3,}', '\n\n', text)
        lines = [re.sub(r'[ \t]+', ' ', l).strip()
                 for l in text.split('\n')]
        return "\n".join(lines)

    def remove_noise(self, text):
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'\b\S+@\S+\.\S+\b', '', text)
        return text

    def correct_common_errors(self, text):
        patterns = [
            (r'\bI\b(?=\d)', '1'),
            (r'\bl0\b', '10'),
            (r'\b0O\b', '00')
        ]
        for p, r in patterns:
            text = re.sub(p, r, text)
        return text
