import warnings
import dspy
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

# Import config to ensure LM is configured at module load time.
from config import lm  # noqa: F401

from signature import (
    CulturalEtiquette,
    SpiritualSites,
    FestivalsHolidays,
    LanguageCommunication,
    FoodDiningNorms,
    HeritageMonuments,
    ConversationStarters,
)

warnings.filterwarnings(
    "ignore",
    message="No parser was explicitly specified",
    module="wikipedia"
)

GUIDELINES = {
    "cultural_etiquette": (
        "Summarize key etiquette practices and social norms a respectful visitor should know in 3 to 4 sentences. "
        "Highlight concrete dos and don'ts, and note how locals perceive courteous behavior."
    ),
    "spiritual_sites": (
        "Describe notable religious or spiritual sites with brief context in 3 to 4 sentences. "
        "Mention respectful conduct or access requirements when appropriate."
    ),
    "festivals_holidays": (
        "Explain major annual festivals or holidays in 3 to 4 sentences, including timing and what travelers should expect or do."
    ),
    "language_communication": (
        "Provide language or communication tips in 3 to 4 sentences, covering greetings, key phrases, and interaction norms."
    ),
    "food_dining_norms": (
        "Outline dining etiquette, signature dishes, and guidance on ordering or tipping in 3 to 4 sentences. Mention any taboos."
    ),
    "heritage_monuments": (
        "Describe important heritage landmarks or monuments in 3 to 4 sentences, including historical context and visitor tips."
    ),
    "conversation_starters": (
        "Craft 5 to 10 thoughtful questions a well-prepared traveler might ask locals. "
        "Each question must explicitly reference a specific detail from the provided information (e.g., named festival, landmark, dish, etiquette point). "
        "Write in first-person perspective (\"I\") to show the traveler already learned something and wants to dive deeper. Avoid generic questions and stereotypes."
    ),
}


class WikipediaAgent(dspy.Module):
    SECTION_KEYWORDS = {
        "cultural_etiquette": ["culture", "custom", "etiquette", "society"],
        "spiritual_sites": ["religion", "spiritual", "temple", "church", "mosque"],
        "festivals_holidays": ["festival", "holiday", "celebration"],
        "language_communication": ["language", "communication", "phrase", "dialect"],
        "food_dining_norms": ["cuisine", "food", "dining", "gastronomy"],
        "heritage_monuments": ["heritage", "monument", "landmark", "architecture", "historic"],
    }

    def __init__(self):
        super().__init__()
        self.cultural_predictor = dspy.Predict(CulturalEtiquette)
        self.spiritual_predictor = dspy.Predict(SpiritualSites)
        self.festival_predictor = dspy.Predict(FestivalsHolidays)
        self.language_predictor = dspy.Predict(LanguageCommunication)
        self.food_predictor = dspy.Predict(FoodDiningNorms)
        self.heritage_predictor = dspy.Predict(HeritageMonuments)
        self.conversation_predictor = dspy.Predict(ConversationStarters)

    def _resolve_page(self, destination: str):
        try:
            return wikipedia.page(destination, auto_suggest=False)
        except DisambiguationError as exc:
            for option in exc.options[:5]:
                try:
                    return wikipedia.page(option, auto_suggest=False)
                except Exception:
                    continue
            raise

    def _extract_section(self, page, keywords):
        for section_title in page.sections:
            title_lc = section_title.lower()
            if any(keyword in title_lc for keyword in keywords):
                try:
                    section_text = page.section(section_title)
                    if section_text:
                        return section_text
                except Exception:
                    continue
        return ""

    def retrieve_info(self, destination: str) -> dict:
        try:
            page = self._resolve_page(destination)
        except (DisambiguationError, PageError) as exc:
            return {"error": f"Could not uniquely identify '{destination}': {exc}"}
        except Exception as exc:
            return {"error": f"Error retrieving information for '{destination}': {exc}"}

        try:
            overview = wikipedia.summary(page.title, sentences=5)
        except Exception:
            overview = page.summary if hasattr(page, "summary") else "Overview not available."

        info = {"destination": page.title, "overview": overview}
        for key, keywords in self.SECTION_KEYWORDS.items():
            section_text = self._extract_section(page, keywords)
            if not section_text:
                section_text = overview
            info[key] = section_text
        return info

    def _compose_context(self, info: dict, key: str) -> str:
        overview = info.get("overview", "")
        section = info.get(key, "")
        return (
            f"Overview:\n{overview}\n\n"
            f"Section focus ({key.replace('_', ' ')}):\n{section}"
        )

    def _compose_conversation_context(self, info: dict) -> str:
        sections = [
            info.get("overview", ""),
            info.get("cultural_etiquette", ""),
            info.get("festivals_holidays", ""),
            info.get("food_dining_norms", ""),
            info.get("language_communication", ""),
            info.get("spiritual_sites", ""),
            info.get("heritage_monuments", ""),
        ]
        joined = "\n\n".join(filter(None, sections))
        return f"Destination insights:\n{joined}"

    def forward(self, destination: str) -> dict:
        info = self.retrieve_info(destination)
        if "error" in info:
            return {"destination": destination, "error": info["error"]}

        responses = {
            "destination": info["destination"],
        }

        responses["cultural_etiquette"] = self.cultural_predictor(
            destination=destination,
            info=self._compose_context(info, "cultural_etiquette"),
            guidance=GUIDELINES["cultural_etiquette"],
        ).etiquette

        responses["spiritual_sites"] = self.spiritual_predictor(
            destination=destination,
            info=self._compose_context(info, "spiritual_sites"),
            guidance=GUIDELINES["spiritual_sites"],
        ).sites

        responses["festivals_holidays"] = self.festival_predictor(
            destination=destination,
            info=self._compose_context(info, "festivals_holidays"),
            guidance=GUIDELINES["festivals_holidays"],
        ).festivals

        responses["language_communication"] = self.language_predictor(
            destination=destination,
            info=self._compose_context(info, "language_communication"),
            guidance=GUIDELINES["language_communication"],
        ).guidance_output

        responses["food_dining_norms"] = self.food_predictor(
            destination=destination,
            info=self._compose_context(info, "food_dining_norms"),
            guidance=GUIDELINES["food_dining_norms"],
        ).dining

        responses["heritage_monuments"] = self.heritage_predictor(
            destination=destination,
            info=self._compose_context(info, "heritage_monuments"),
            guidance=GUIDELINES["heritage_monuments"],
        ).highlights

        responses["conversation_starters"] = self.conversation_predictor(
            destination=destination,
            info=self._compose_conversation_context(info),
            guidance=GUIDELINES["conversation_starters"],
        ).questions

        return responses



