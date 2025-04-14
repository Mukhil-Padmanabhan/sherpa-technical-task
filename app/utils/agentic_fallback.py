import wikipedia
import requests

def wikipedia_fallback(query: str) -> str | None:
    try:
        results = wikipedia.search(query)
        if not results:
            return None
        summary = wikipedia.summary(results[0], sentences=5)
        return f"Wikipedia {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            summary = wikipedia.summary(e.options[0], sentences=5)
            return f"Wikipedia - Disambiguation {summary}"
        except:
            return None
    except wikipedia.exceptions.PageError:
        return None
    except Exception as e:
        print(f"Wikipedia Fallback Failed: {e}")
        return None


def duckduckgo_fallback(query: str) -> str | None:
    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_redirect": "1"},
            timeout=5,
        )
        data = resp.json()
        if data.get("AbstractText"):
            return f"(DuckDuckGo) {data['AbstractText']}"
        elif data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if "Text" in topic:
                    return f"(DuckDuckGo Related) {topic['Text']}"
        return None
    except Exception as e:
        print(f"[ DuckDuckGo Fallback Failed]: {e}")
        return None


def fallback_knowledge_search(query: str) -> str:
    wiki_summary = wikipedia_fallback(query)
    if wiki_summary:
        return wiki_summary

    ddg_result = duckduckgo_fallback(query)
    if ddg_result:
        return ddg_result

    return "No reliable fallback data found. Please rely on general assistant intelligence."
