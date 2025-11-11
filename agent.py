import dspy
from typing import Dict, List, Tuple
import wikipedia
from signature import (
    CulturalEtiquette,
    ReligionAndSpiritualSites,
    FestivalsAndHolidays,
    LanguageAndCommunication,
    FoodAndDiningNorms,
    HeritageAndMonuments,
    ConversationStarters,
)
import config  # ensures dspy.configure runs on import

CATEGORY_SECTION_MAP: Dict[str, List[str]] = {
    "cultural_etiquette": [
        "Culture",
        "Customs",
        "Etiquette",
        "Social customs",
        "Culture and society",
    ],
    "religion_and_spiritual_sites": [
        "Religion",
        "Religious sites",
        "Spirituality",
        "Religious tourism",
    ],
    "festivals_and_holidays": [
        "Festivals",
        "Holidays",
        "Public holidays",
        "Celebrations",
    ],
    "language_and_communication": [
        "Language",
        "Languages",
        "Demographics",
        "Communication",
        "People",
    ],
    "food_and_dining_norms": [
        "Cuisine",
        "Food",
        "Dining",
        "Food and drink",
    ],
    "heritage_and_monuments": [
        "Heritage",
        "Monuments",
        "Landmarks",
        "Architecture",
        "Tourism",
    ],
}

FALLBACK_MESSAGES: Dict[str, str] = {
    "cultural_etiquette": "No specific cultural etiquette information available.",
    "religion_and_spiritual_sites": "No notable religious or spiritual sites found.",
    "festivals_and_holidays": "No festivals or holidays information available.",
    "language_and_communication": "No language or communication details available.",
    "food_and_dining_norms": "No food or dining information available.",
    "heritage_and_monuments": "No heritage or monuments information available.",
}

CATEGORY_SIGNATURES: Dict[str, Tuple[type, str]] = {
    "cultural_etiquette": (CulturalEtiquette, "Cultural Etiquette: "),
    "religion_and_spiritual_sites": (
        ReligionAndSpiritualSites,
        "Religion & Spiritual Sites: ",
    ),
    "festivals_and_holidays": (FestivalsAndHolidays, "Festivals & Holidays: "),
    "language_and_communication": (
        LanguageAndCommunication,
        "Language & Communication: ",
    ),
    "food_and_dining_norms": (FoodAndDiningNorms, "Food & Dining Norms: "),
    "heritage_and_monuments": (HeritageAndMonuments, "Heritage & Monuments: "),
}

CONVERSATION_STARTER_GUIDANCE = (
    "Create concise, friendly conversation starters a respectful traveler can use when visiting the destination. "
    "Reference the insights provided. Avoid stereotypes and stay positive."
)


class WikipediaAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictors: Dict[str, dspy.Predict] = {
            key: dspy.Predict(signature)
            for key, (signature, _) in CATEGORY_SIGNATURES.items()
        }
        self.conversation_predictor = dspy.Predict(ConversationStarters)

    def _select_page(self, query: str):
        try:
            candidates = wikipedia.search(query, results=5)
        except Exception as exc:
            raise RuntimeError(f"Error retrieving search results: {exc}") from exc

        for title in candidates:
            try:
                return wikipedia.page(title, auto_suggest=False)
            except wikipedia.DisambiguationError:
                continue
            except Exception:
                continue
        raise RuntimeError("No suitable Wikipedia page found for the destination.")

    def _match_section(self, page, candidates: List[str]) -> str:
        sections_lookup = {section.lower(): section for section in page.sections}
        for candidate in candidates:
            for lowered, actual in sections_lookup.items():
                if candidate.lower() in lowered:
                    content = page.section(actual)
                    if content:
                        return content
        return ""

    def retrieve_info(self, question: str) -> Dict[str, str]:
        try:
            page = self._select_page(question)
        except RuntimeError as exc:
            return {"error": str(exc)}

        structured_info: Dict[str, str] = {}
        summary = getattr(page, "summary", "")

        for category, section_candidates in CATEGORY_SECTION_MAP.items():
            section_text = self._match_section(page, section_candidates)
            if not section_text and summary:
                section_text = summary
            structured_info[category] = section_text or FALLBACK_MESSAGES[category]

        structured_info["page_title"] = page.title
        structured_info["page_url"] = getattr(page, "url", "")
        return structured_info

    def forward(self, question: str) -> str:
        destination = question
        info_sections = self.retrieve_info(destination)
        if "error" in info_sections:
            return info_sections["error"]

        insights: Dict[str, str] = {}
        conversation_context_lines: List[str] = []
        for key, (_, display_title) in CATEGORY_SIGNATURES.items():
            predictor = self.predictors[key]
            section_info = info_sections.get(key, FALLBACK_MESSAGES[key])
            result = predictor(question=destination, info=section_info)
            answer_text = getattr(result, "answer", str(result))
            cleaned_answer = answer_text.strip()
            insights[display_title] = cleaned_answer
            conversation_context_lines.append(f"{display_title}: {cleaned_answer}")

        conversation_context = "\n".join(conversation_context_lines)
        starters_prompt = (
            f"{CONVERSATION_STARTER_GUIDANCE}\n\n"
            f"Destination: {destination}\n"
            f"Insights by topic:\n{conversation_context}"
        )
        starters_result = self.conversation_predictor(
            question=destination,
            info=starters_prompt,
        )
        starters_answer = getattr(starters_result, "answer", str(starters_result)).strip()

        lines = []
        page_title = info_sections.get("page_title")
        if page_title:
            lines.append(f"Destination: {page_title}")
        lines.append("")

        for display_title, answer in insights.items():
            lines.append(f"{display_title}")
            lines.append(f"{answer if answer else 'No details available.'}")
            lines.append("")

        if starters_answer:
            lines.append("Conversation Starters")
            lines.append(starters_answer)
            lines.append("")

        page_url = info_sections.get("page_url")
        if page_url:
            lines.append(f"Source: {page_url}")

        return "\n".join(lines).strip()



