"""
GRAVITYchat - Prompt Generator
--------------------------------
Generates user and system prompts for chat. It sets boundaries of the chat with
establishing factuality, references, handling input errors in prompting, etc for citizen
scientists.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import json
import pandas

DATA_DELIMITER = "~~~"

def alog_prompt(chat):
    """
    Constructs user and system prompts for LLM for chat.

    Args:
        chat (str): the text for chat response

    Returns:
        tuple:
            - user_prompt (str): Prompt provided to the language model that includes structured data.
            - sys_prompt (str): Instructional system message to guide GPT behavior and tone.

    Prompt Behavior:
        - Asks LLM to give factual responses to chat request with references.
        - Encourages simple, accessible language for citizen scientists.
        - Requests acronyms be expanded using the LIGO Abbreviations and Acronyms list.
        - Embeds formatted data using `format_data()` within a delimiter block.
    """

    user_prompt = chat


    sys_prompt = f"""
You are a LIGO scientist tasked with responding to with citizen scientists with factual,
accessible responses. These might be any questions about LIGO technology, scientific
results, or questions about citizen scientist tasks related to Zooniverse or Gravity Spy.
Your goal is to help citizen scientists with factual responses to their questions that
will enable them to interpret Gravity Spy Glitches and their oriigns. Use clear, simple
language and avoid technical jargon to ensure accessibility. Translate acronyms to full
words based upon LIGO Abbreviations and Acronyms whenever possible.

When generating summaries, Format all URLs without hashtags following this format:
[{template_link_text}]({template_link_url}).

Structure the summary logically, highlighting common or recent issues, and
maintain a neutral, informative tone. Phrase interpretations with rhetoric like
"an" (as opposed to "the") and "some" as opposed to "all" when referring to the
data. This will avoid extremes when there is a lack of clarity.
    """.strip()

    return user_prompt, sys_prompt

prompt = '!!!!!!! prompt testing !!!!!!!!'
