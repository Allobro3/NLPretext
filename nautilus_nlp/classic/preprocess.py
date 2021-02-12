# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import re
import unicodedata
from ftfy import fix_text as _fix_text
from nautilus_nlp._config import constants
from nautilus_nlp.token.tokenizer import tokenize
from nautilus_nlp._utils.phone_number import extract_phone_numbers as _extract_phone_numbers
from nautilus_nlp._utils.stopwords import get_stopwords


def normalize_whitespace(text) -> str:
    """
    Given ``text`` str, replace one or more spacings with a single space, and
    one or more linebreaks with a single newline. Also strip leading/trailing
    whitespace.
    eg. "   foo  bar  " -> "foo bar"

    Parameters
    ----------
    text : string

    Returns
    -------
    string
    """
    text = constants.NONBREAKING_SPACE_REGEX.sub(
        " ", constants.LINEBREAK_REGEX.sub(r"\n", text)
    ).strip()
    return text


def remove_stopwords(text: str, lang: str, custom_stopwords: list = None) -> str:
    """
    Given ``text`` str, remove classic stopwords for a given language and
    custom stopwords given as a list.

    Parameters
    ----------
    text : string
    lang : string
    custom_stopwords : list of strings

    Returns
    -------
    string
    """
    stopwords = get_stopwords(lang)
    if custom_stopwords:
        stopwords += custom_stopwords
    if lang in ["fr", "en"]:
        lang_module = {
            "fr" : "fr_spacy",
            "en" : "en_spacy"
        }[lang]
        return ' '.join(
            [x for x in tokenize(text, lang_module) if x not in stopwords])
    return ' '.join([x for x in text.split() if x not in stopwords])


def remove_eol_characters(text) -> str:
    """
    Remove end of line (\n) char.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """
    text = text.replace("\n", " ")
    return text


def fix_bad_unicode(text, normalization: str = "NFC") -> str:
    """
    Fix unicode text that's "broken" using `ftfy
    <http://ftfy.readthedocs.org/>`_;
    this includes mojibake, HTML entities and other code cruft,
    and non-standard forms for display purposes.

    Parameters
    ----------
    text : string

    normalization ({'NFC', 'NFKC', 'NFD', 'NFKD'}):
        if 'NFC', combines characters and diacritics written using separate
        code points, e.g. converting "e" plus an acute accent modifier into
        "é"; unicode
        can be converted to NFC form without any change in its meaning!
        if 'NFKC', additional normalizations are applied that can change
        the meanings of characters, e.g. ellipsis characters will be replaced
        with three periods
    Returns
    -------
    string
    """
    text = _fix_text(text, normalization=normalization)
    return text


def unpack_english_contractions(text) -> str:
    """
    Replace *English* contractions in ``text`` str with their unshortened
    forms.
    N.B. The "'d" and "'s" forms are ambiguous (had/would, is/has/possessive),
    so are left as-is.
    eg. "You're fired. She's nice." -> "You are fired. She's nice."

    Parameters
    ----------
    text : string

    Returns
    -------
    string
    """

    # standard
    text = constants.CONTRACTION_NT_NOT.sub(
        r"\1\2 not",
        text,
    )
    text = constants.CONTRACTION_LL_WILL.sub(
        r"\1\2 will",
        text,
    )
    text = constants.CONTRACTION_RE_ARE.sub(r"\1\2 are", text)
    text = constants.CONTRACTION_VE_HAVE.sub(
        r"\1\2 have",
        text,
    )
    text = constants.CONTRACTION_CANT_CANNOT.sub(r"\1\2n not", text)
    text = constants.CONTRACTION_M_AM.sub(r"\1\2 am", text)
    text = constants.CONTRACTION_LET_LETUS.sub(r"\1\2 us", text)
    text = constants.CONTRACTION_WONT_WILLNOT.sub(r"\1\2ill not", text)
    text = constants.CONTRACTION_SHANT_SHALLNOT.sub(r"\1\2hall not", text)
    text = constants.CONTRACTION_YALL_YOUALL.sub(r"\1\2ou all", text)
    return text


def replace_urls(text, replace_with: str = "*URL*") -> str:
    """
    Replace all URLs in ``text`` str with ``replace_with`` str.

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the URL to be replaced with.

    Returns
    -------
    string
    """
    text = constants.URL_REGEX.sub(
        replace_with, constants.SHORT_URL_REGEX.sub(replace_with, text)
    )
    return text


def replace_emails(text, replace_with="*EMAIL*") -> str:
    """
    Replace all emails in ``text`` str with ``replace_with`` str

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the email address to be replaced with.

    Returns
    -------
    string
    """
    text = constants.EMAIL_REGEX.sub(replace_with, text)
    return text


def replace_phone_numbers(text, country_to_detect: list,
                          replace_with: str = "*PHONE*",
                          method: str = "regex") -> str:
    """
    Replace all phone numbers in ``text`` str with ``replace_with`` str

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the phone number to be replaced with.
    method : ['regex','detection']
        regex is faster but will omit a lot of numbers, while detection will
        catch every numbers, but takes a while.
    country_to_detect : list
        If a list of country code is specified, will catch every number
        formatted.
        Only when method = 'detection'.
    Returns
    -------
    string
    """
    if method == 'regex':
        text = constants.PHONE_REGEX.sub(replace_with, text)
    elif method == 'detection':
        found_nums = _extract_phone_numbers(text,
                                            countrylist=country_to_detect)

        # order by lenght to avoid truncated numbers to be removed first.
        found_nums.sort(key=len, reverse=True)
        for phone_number in found_nums:
            text = text.replace(phone_number, replace_with)
    else:
        raise ValueError('Please input a valid method between "regex" or \
            "detection"')
    return text


def replace_numbers(text, replace_with="*NUMBER*") -> str:
    """
    Replace all numbers in ``text`` str with ``replace_with`` str.

    Parameters
    ----------
    text : string
    replace_with : string
        the string you want the number to be replaced with.

    Returns
    -------
    string
    """
    text = constants.NUMBERS_REGEX.sub(replace_with, text)
    return text


def replace_currency_symbols(text, replace_with=None) -> str:
    """
    Replace all currency symbols in ``text`` str with string specified by
    ``replace_with`` str.

    Parameters
    ----------
    text : str
        raw text
    replace_with : None or string
        if None (default), replace symbols with
            their standard 3-letter abbreviations (e.g. '$' with 'USD', '£'
            with 'GBP'); otherwise, pass in a string with which to replace all
            symbols (e.g. "*CURRENCY*")

    Returns
    -------
    string
    """
    if replace_with is None:
        for k, v in constants.CURRENCIES.items():
            text = text.replace(k, v)
    else:
        text = constants.CURRENCY_REGEX.sub(replace_with, text)
    return text


def remove_punct(text, marks=None) -> str:
    """
    Remove punctuation from ``text`` by replacing all instances of ``marks``
    with whitespace.

    Parameters
    ----------
    text : str
        raw text

    marks : str or None
        If specified, remove only the characters in this string,
        e.g. ``marks=',;:'`` removes commas, semi-colons, and colons.
        Otherwise, all punctuation marks are removed.

    Returns
    -------
    string

    Note
    -------
    When ``marks=None``, Python's built-in :meth:`str.translate()` is
    used to remove punctuation; otherwise, a regular expression is used
    instead. The former's performance is about 5-10x faster.
    """
    if marks:
        text = re.sub("[{}]+".format(re.escape(marks)), " ", text,
                      flags=re.UNICODE)
    else:
        text = text.translate(constants.PUNCT_TRANSLATE_UNICODE)
    return text


def remove_accents(text, method: str = "unicode") -> str:
    """
    Remove accents from any accented unicode characters in ``text`` str,
    either by transforming them into ascii equivalents or removing them
    entirely.

    Parameters
    ----------
    text : str
        raw text

    method : ({'unicode', 'ascii'})
        if 'unicode', remove accented
        char for any unicode symbol with a direct ASCII equivalent; if 'ascii',
        remove accented char for any unicode symbol

        NB: the 'ascii' method is notably faster than 'unicode', but less good

    Returns
    -------
    string

    Raises
    -------
    ValueError
        if ``method`` is not in {'unicode', 'ascii'}
    """
    if method == "unicode":
        text = "".join(
            c
            for c in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(c)
        )
    elif method == "ascii":
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", errors="ignore")
            .decode("ascii")
        )
    else:
        msg = '`method` must be either "unicode" and "ascii", not {}' \
               .format(method)
        raise ValueError(msg)
    return text


def remove_multiple_spaces_and_strip_text(text) -> str:
    """
    Remove multiple spaces, strip text, and remove '-', '*' characters.

    Parameters
    ----------
    text : str
        the text to be processed

    Returns
    -------
    string
        the text with removed multiple spaces and strip text
    """
    regex_remove_multiple_spaces_list = ["\\t", "[\\s\\-\\*]{2,}"]
    for regex_remove_multiple_spaces in regex_remove_multiple_spaces_list:
        text = re.sub(regex_remove_multiple_spaces, " ", text)
        text = text.strip()
    return text


def filter_non_latin_characters(text) -> str:
    """
    Function that filters non latin characters of a text

    Parameters
    ----------
    text : string

    Returns
    -------
    string
    """
    text = constants.LATIN_CHARACTERS_RE.sub(' ', text)
    text = normalize_whitespace(text)
    return text
