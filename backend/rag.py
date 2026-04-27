import io
import requests
import openpyxl
import pypdf


class RAGManager:
    def __init__(self, excel_path: str):
        self.articles: dict[str, str] = {}  # {article_name: full_text}
        self._load(excel_path)

    def _load(self, excel_path: str):
        wb = openpyxl.load_workbook(excel_path)
        ws = wb["Simulation - View Student List"]

        seen: set[str] = set()
        for row in ws.iter_rows(min_row=2):
            last = row[-1]
            if not last.hyperlink or not last.value:
                continue
            url = (last.hyperlink.target or last.hyperlink.display or "").strip()
            name = str(last.value).strip()
            if url and url not in seen:
                seen.add(url)
                text = self._fetch_pdf_text(url)
                if text:
                    self.articles[name] = text
                    print(f"[RAG] loaded '{name}' ({len(text)} chars)")

    def _fetch_pdf_text(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            reader = pypdf.PdfReader(io.BytesIO(resp.content))
            return "\n".join(p.extract_text() or "" for p in reader.pages).strip()
        except Exception as e:
            print(f"[RAG] failed to fetch {url}: {e}")
            return ""

    def get_context(self) -> str:
        return "\n\n---\n\n".join(
            f"[{name}]\n{text}" for name, text in self.articles.items()
        )
