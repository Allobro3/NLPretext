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

from __future__ import absolute_import, division, print_function, unicode_literals

import re

class TokenPreprocessor():

    def __init__(self,tokens):
        if isinstance(tokens,list):
            self.tokens = tokens
        else:
            raise ValueError("Input must be a list")

    def remove_stopwords(self, stopwords: list) -> str:
        """ 
        Remove stopwords from a text.
        eg. 'I like when you move your body !' -> 'I move body !'

        Parameters
        ----------
        stopwords : list of stopwords to remove

        Returns
        -------
        list
            tokens without stopwords

        Raises
        ------
        ValueError
            When inputs is not a list
        """
        self.tokens = [word for word in self.tokens if word not in stopwords]
        return self.tokens

    def remove_tokens_with_nonletters(self) -> list:
        """
        Inputs a list of tokens, outputs a list of tokens without tokens that
        includes numbers of special caracters.
        ['foo','bar','124','34euros'] -> ['foo','bar']

        Parameters
        ----------
        tokens : list
            list of tokens to be cleaned

        Returns
        -------
        list
            list of tokens without tokens with numbers
        """
        self.tokens = [word for word in self.tokens if re.search("[^a-zA-Z]", word) is None]
        return self.tokens

    def remove_special_caracters_from_tokenslist(self) -> list:
        """ 
        Remove tokens that doesn't contains any number or letter. 
        eg. ['foo','bar','---',"'s",'#'] -> ['foo','bar',"'s"]

        Parameters
        ----------
        tokens : list
            list of tokens to be cleaned

        Returns
        -------
        list
            list of tokens without tokens that contains only special caracters
        
        """
        self.tokens = [word for word in self.tokens if re.search("[a-zA-Z0-9]", word)]
        return self.tokens

    def remove_smallwords(self, smallwords_threshold:int) -> list:
        """
        Function that removes words which length is below a threshold
        ["hello", "my", "name", "is", "John", "Doe"] --> ["hello","name","John","Doe"]

        Parameters
        ----------
        text : list
            list of strings
        smallwords_threshold: int
            threshold of small word

        Returns
        -------
        list
        """
        self.tokens = [word for word in self.tokens if len(word) > smallwords_threshold]
        return self.tokens