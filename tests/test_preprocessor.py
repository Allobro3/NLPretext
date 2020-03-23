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
import pytest
import numpy as np
from nautilus_nlp.preprocessing.preprocess import (
    remove_multiple_spaces_and_strip_text,
    remove_accents,
    fix_bad_unicode,
    remove_EOL_characters,
    remove_tokens_with_nonletters,
    remove_special_caracters_from_tokenslist,
    get_stopwords,
    remove_stopwords,
    normalize_whitespace,
    unpack_english_contractions,
    replace_urls,
    replace_emails,
    replace_phone_numbers,
    replace_numbers,
    replace_currency_symbols,
    remove_punct,
    remove_emoji,
    convert_emoji_to_text,
    extract_emojis,
    remove_mentions,
    extract_mentions,
    remove_html_tags,
    remove_smallwords,
    extract_hashtags,
    remove_hashtag,
    filter_non_latin_characters
)
import nautilus_nlp.utils.phone_number as phone

@pytest.mark.parametrize("text, expected_result",
                         [("ACV water + cinnamon + turmeric + cucumber + lemon. 👍🏻",
                           [":thumbs_up_light_skin_tone:"]),
                          ("This is a text without emojis",
                           [])])
def test_extract_emojis(text, expected_result):
    result = extract_emojis(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("I take care of my skin with @hellobody",
                           "I take care of my skin with"),
                          ("This is a text without mentions",
                           "This is a text without mentions")])
def test_remove_mentions(text, expected_result):
    result = remove_mentions(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("I take care of my skin with @hellobody",
                           ["@hellobody"]),
                          ("This is a text without mentions",
                           [])])
def test_extract_mentions(text, expected_result):
    result = extract_mentions(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("This is a text with <html> content of html tag </html>",
                           "This is a text with content of html tag"),
                          ("This is a text without html tags",
                           "This is a text without html tags")])
def test_remove_html_tags(text, expected_result):
    result = remove_html_tags(text)
    assert expected_result == result


@pytest.mark.parametrize("tokens_list, smallwords_threshold, expected_result",
                         [(["I", "take", "care", "of", "my", "skin"],
                           2,
                           ["take", "care", "skin"]),
                          (["This", "text", "contains", "only", "long", "words"],
                           2,
                           ["This", "text", "contains", "only", "long", "words"])])
def test_remove_smallwords(tokens_list, smallwords_threshold, expected_result):
    result = remove_smallwords(tokens_list, smallwords_threshold)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("this is a #hashtag in the middle of the text",
                           ["#hashtag"]),
                          ("#this is a hashtag in the beginning of the text",
                           ["#this"]),
                          ("this is a hashtag in the end of the #text",
                           ["#text"]),
                          ("this is a text with no hashtag",
                           []),
                          ("this is a text with #many #hashtags",
                           ["#many", "#hashtags"])]
                         )
def test_extract_hashtags(text, expected_result):
    result = extract_hashtags(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_result",
                         [("this is a #hashtag in the middle of the text",
                           "this is a in the middle of the text"),
                          ("#this is a hashtag in the beginning of the text",
                           "is a hashtag in the beginning of the text"),
                          ("this is a hashtag in the end of the #text",
                           "this is a hashtag in the end of the"),
                          ("this is a text with no hashtag",
                           "this is a text with no hashtag"),
                          ("this is a text with #many #hashtags",
                           "this is a text with")]
                         )
def test_remove_hashtag(text, expected_result):
    result = remove_hashtag(text)
    assert expected_result == result


@pytest.mark.parametrize("text, expected_filtered_text",
                         [("كلمات Learn 3 Arabic كلمات words EASILY- Vocabulary #1 تعلم ٣ جديدة",
                           "Learn 3 Arabic words EASILY Vocabulary 1")])
def test_filter_non_latin_characters(text, expected_filtered_text):
    filtered_text = filter_non_latin_characters(text)
    assert expected_filtered_text == filtered_text


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("hello   world", "hello world"),
        ("\n   hello world    ", "hello world"),
        ("----- hello\tworld *****", "hello world"),
        ("hello-world", "hello-world"),
        ("hello - world", "hello world"),
    ],
)
def test_remove_multiple_spaces_and_strip_text(input_str, expected_str):
    result = remove_multiple_spaces_and_strip_text(input_str)
    np.testing.assert_string_equal(result, expected_str)

@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("\nhello world", " hello world"),
        ("hello\nworld", "hello world"),
        ("hello world\n", "hello world ")
    ],
)
def test_remove_EOL_characters(input_str, expected_str):
    result = remove_EOL_characters(input_str)
    np.testing.assert_string_equal(result, expected_str)    


def test_remove_tokens_with_nonletters():
    input_tokens = ['foo','bar','124','34euros']
    expected_output = ['foo','bar']
    result = remove_tokens_with_nonletters(input_tokens)
    np.testing.assert_array_equal(result,expected_output)


def test_remove_special_caracters_from_tokenslist():
    input_tokens = ['foo','bar','---',"'s",'#']
    expected_output = ['foo','bar',"'s"]
    result = remove_special_caracters_from_tokenslist(input_tokens)
    np.testing.assert_array_equal(result, expected_output)


def test_get_stopwords():
    languages_to_test = ['fr','en','ga','zh']
    for lang in languages_to_test:
        result = get_stopwords(lang)
        assert len(result) > 0 and type(result) == list


@pytest.mark.parametrize(
    "input_tokens, expected_output",
    [
        (['I','like','when','you','move','your','body','!'], ['I', 'move', 'body', '!']),
        ('I like when you move your body !', ['I', 'move', 'body', '!']),
    ],
)    
def test_remove_stopwords(input_tokens, expected_output):
    stopwords = get_stopwords('en')
    result = remove_stopwords(input_tokens, stopwords)
    np.testing.assert_array_equal(result, expected_output)


def test_remove_accents():
    input_str = "éèëêàù"
    expected_str = "eeeeau"

    result = remove_accents(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
    ('Les augmentations de rÃ©munÃ©rations',
  'Les augmentations de rémunérations'),
 ("rÃ©nover l'enquÃªte publique pour en faire un vrai outil  d'amÃ©nagement du territoire et de dialogue social",
  "rénover l'enquête publique pour en faire un vrai outil  d'aménagement du territoire et de dialogue social"),
 ('Limitations de vitesse et sÃ©curitÃ© routiÃ¨re',
  'Limitations de vitesse et sécurité routière'),
 ('Pour un nouveau contrat citoyen', 'Pour un nouveau contrat citoyen'),
 ('DÃ©velopper les dÃ©marches de budget participatif dans les collectivitÃ©s et associer les citoyens dans la rÃ©alisation des projets',
  'Développer les démarches de budget participatif dans les collectivités et associer les citoyens dans la réalisation des projets'),
 ('proportienelle', 'proportienelle'),
 ('Pour plus de dÃ©mocratie participative',
  'Pour plus de démocratie participative'),
 ('Transparence de la vie public', 'Transparence de la vie public'),
 ('18 mois de trop....ca suffit macron',
  '18 mois de trop....ca suffit macron'),
 ('EgalitÃ© devant les infractions routiÃ¨res',
  'Egalité devant les infractions routières')
    ],
)
def test_fix_bad_unicode(input_str, expected_str):
    result = fix_bad_unicode(input_str)
    np.testing.assert_string_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ('  foo  ', 'foo'),
        ('  foo   bar  ', 'foo bar')
    ],
)
def test_normalize_whitespace(input_str, expected_str):
    result = normalize_whitespace(input_str)
    np.testing.assert_equal(result, expected_str)

@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("I can't tell how we've done.", 'I can not tell how we have done.'),
        ("You're fired. She's nice.", "You are fired. She's nice."),
        ("Let's go!",'Let us go!'),
        ("You've been missing",'You have been missing'),
        ("I'm sure you're leaving",'I am sure you are leaving'),
        ("We'll survive.","We will survive.")
    ]
    )
def test_unpack_english_contractions(input_str, expected_str):
    result = unpack_english_contractions(input_str)
    np.testing.assert_equal(result, expected_str)

@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("Wan't to contribute to Nautilus? read https://github.com/artefactory/nautilus-nlp/blob/docs/CONTRIBUTING.md first",
         "Wan't to contribute to Nautilus? read *URL* first"),
        ("The ip address of my VM is http://34.76.182.5:8888", "The ip address of my VM is *URL*"),
        ("If you go to http://internet.org, you will find a website hosted by FB.",
         "If you go to *URL*, you will find a website hosted by FB."),
        ("Ishttps://waaaou.com/ available?",'Is*URL* available?'),
        ("mailto:hugo.vasselin@artefact.com",'*URL*')
    ]
    )
def test_replace_urls(input_str, expected_str):
    result = replace_urls(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("my email:hugo.vasselin@artefact.com","my email:*EMAIL*"),
        ("v543143@nwytg.net is a temporary email", "*EMAIL* is a temporary email"),
        ("our emails used to be name.surname@artefact.is","our emails used to be *EMAIL*"),
        ("chaudasse_du_13@hotmail.fr,C ton email bb?",'*EMAIL*,C ton email bb?')
    ]
    )
def test_replace_emails(input_str, expected_str):
    result = replace_emails(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("mon 06 bb: 0625093267","mon 06 bb: *PHONE*"),
        ("mon 06 bb: 06.25.09.32.67","mon 06 bb: *PHONE*"),
        ("call me at +33625093267","call me at *PHONE*"),
        ("call me at +33 6 25 09 32 67","call me at *PHONE*"),
        ("call me at +33 625 093 267","call me at *PHONE*"),
        ("if this unit test doesn't work, call 3615 and says 'ROBIN'",
         "if this unit test doesn't work, call *PHONE* and says 'ROBIN'"),
        ('(541) 754-3010 is a US. Phone','*PHONE* is a US. Phone'),
        ('+1-541-754-3010 is an international Phone','*PHONE* is an international Phone'),
        ('+1-541-754-3010 Dialed in the US','*PHONE* Dialed in the US'),
        ('+1-541-754-3010 Dialed from Germany','*PHONE* Dialed from Germany')
    ]
    )
def test_replace_phone_numbers(input_str, expected_str):
    result = replace_phone_numbers(input_str,   replace_with="*PHONE*", 
                                                method="detection",
                                                country_format_to_detect=phone.SUPPORTED_COUNTRY
                                                )
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("123, 3 petits chats","*NUMBER*, *NUMBER* petits chats"),
        ("l0ve 2 twa <3","l0ve *NUMBER* twa <*NUMBER*"),
        ("Give me 45bucks!","Give me *NUMBER*bucks!"),
        ("call me at +33625093267","call me at *NUMBER*")
    ]
    )
def test_replace_numbers(input_str, expected_str):
    result = replace_numbers(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, param, expected_str",
    [
        ("Give me 23$",None,"Give me 23USD"),
        ("Give me 23£",None,"Give me 23GBP"),
        ("Give me 23 £",None,"Give me 23 GBP"),
        ("Give me 23 €",None,"Give me 23 EUR"),
        ("¥ is both japanese yen and Chinese Renminbi","*CUR*","*CUR* is both japanese yen and Chinese Renminbi")
    ]
    )
def test_replace_currency_symbols(input_str, param, expected_str):
    result = replace_currency_symbols(input_str, replace_with=param)
    np.testing.assert_equal(result, expected_str)

@pytest.mark.parametrize(
    "input_str, param, expected_str",
    [
        ("Seriously...",None,"Seriously   "),
        ("Seriously?",None,"Seriously "),
        ("Seriously ?",None,"Seriously  "),
        ("Seriously???",None,"Seriously   "),
        ("Seriously?!",None,"Seriously  "),
        ('"Seriously"',None," Seriously "),
        ('Seriously:',None,"Seriously "),
        ('Seriously;',None,"Seriously "),
        ("'Seriously'",None," Seriously "),
        ("'Seriously'",'.,;',"'Seriously'"),
        ("Seriously.,.",'.,;',"Seriously "),
        ("Seriously...",'.,;',"Seriously "),
        ("Seriously.!.",'.,;',"Seriously ! "),
        ("hugo.vasselin@artefact.com",'.,;',"hugo vasselin@artefact com"),
        ("hugo.vasselin@artefact.com",None,"hugo vasselin artefact com"),
        ("hugo-vasselin@artefact.com",None,"hugo vasselin artefact com")
    ]
    )
def test_remove_punct(input_str, param, expected_str):
    result = remove_punct(input_str, marks=param)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("👉👌",""),
        ("🎅🏿⌚",""),
        ("🥖✊💦",""),
        ("✊",""),
        ("J'espère que les 🚓 vont pas lire ce test",
        "J'espère que les  vont pas lire ce test"),
        ("J'espère que les vont pas lire ce test🚓",
        "J'espère que les vont pas lire ce test")
    ]
    )
def test_remove_emoji(input_str, expected_str):
    result = remove_emoji(input_str)
    np.testing.assert_equal(result, expected_str)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("👉👌",":backhand_index_pointing_right::OK_hand:"),
        ("🎅🏿⌚",":Santa_Claus_dark_skin_tone::watch:"),
        ("🥖✊💦",":baguette_bread::raised_fist::sweat_droplets:"),
        ("✊",":raised_fist:")
    ]
    )
def test_convert_emoji_to_text(input_str, expected_str):
    result = convert_emoji_to_text(input_str)
    np.testing.assert_equal(result, expected_str)    