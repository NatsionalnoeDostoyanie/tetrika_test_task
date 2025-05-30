from typing import (
    Any,
    Iterable,
)

import aiohttp
import wikipediaapi


def _extend_letters_to_animals_count(
    letters_to_animals_count: dict[str, int], animal_names: Iterable[str]
) -> None:
    for animal_name in animal_names:
        if animal_name:
            if (first_letter := animal_name[0]) in letters_to_animals_count:
                letters_to_animals_count[first_letter] += 1


def get_animals_count_for_each_letter(
    wiki_page: wikipediaapi.WikipediaPage, letters: str
) -> dict[str, int]:
    letters_to_animals_count = dict.fromkeys(letters, 0)
    _extend_letters_to_animals_count(
        letters_to_animals_count, wiki_page.categorymembers
    )
    return letters_to_animals_count


async def async_get_animals_count_for_each_letter(
    wiki_page_title: str,
    letters: str,
    user_agent: str,
    wiki_page_language: str,
    **query_params: Any,
) -> dict[str, int]:
    default_params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": wiki_page_title,
        "cmlimit": 500,
    }

    _used_params = query_params
    _used_params.setdefault("timeout", 10.0)
    _used_params.setdefault("format", "json")
    _used_params.setdefault("redirects", 1)
    _used_params.update(default_params)

    headers = {"User-Agent": user_agent}

    url = "https://" + wiki_page_language + ".wikipedia.org/w/api.php"

    letters_to_animals_count = dict.fromkeys(letters, 0)
    _do_while_flag = True
    async with aiohttp.ClientSession(
        headers=headers, timeout=aiohttp.ClientTimeout(_used_params["timeout"])
    ) as session:
        # Do-While Loop Emulating
        while _do_while_flag:
            async with session.get(url, params=_used_params) as response:
                raw = await response.json()
            animal_names = (
                categorymember["title"]
                for categorymember in raw["query"]["categorymembers"]
            )
            _extend_letters_to_animals_count(letters_to_animals_count, animal_names)
            if "continue" in raw:
                _used_params["cmcontinue"] = raw["continue"]["cmcontinue"]
            else:
                _do_while_flag = False
    return letters_to_animals_count


if __name__ == "__main__":
    import asyncio
    import csv
    import os
    from pathlib import Path

    from dotenv import load_dotenv

    load_dotenv()

    RUSSIAN_LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    ENGLISH_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    WIKI_PAGE_TITLE = "Категория:Животные_по_алфавиту"
    WIKI_PAGE_LANGUAGE = "ru"
    USER_AGENT = os.environ["WIKIPEDIA_USER_AGENT"]

    # wiki_wiki = wikipediaapi.Wikipedia(USER_AGENT, WIKI_PAGE_LANGUAGE)
    # wiki_page = wiki_wiki.page(WIKI_PAGE_TITLE)
    # animal_names = get_animals_count_for_each_letter(wiki_page, RUSSIAN_LETTERS)

    animal_names = asyncio.run(
        async_get_animals_count_for_each_letter(
            WIKI_PAGE_TITLE,
            RUSSIAN_LETTERS + ENGLISH_LETTERS,
            USER_AGENT,
            WIKI_PAGE_LANGUAGE,
        )
    )

    module_dir = Path(__file__).parent.resolve()
    result_file_path = module_dir / "beasts.csv"

    with open(result_file_path, "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows(animal_names.items())
