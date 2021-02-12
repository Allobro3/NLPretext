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
#!/usr/local/bin/python3
import os
import phonenumbers as _phonenumbers


ROOT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Country config
COUNTRY_MAPPING_ISO = {
    'af': 'Afghanistan', 'ax': 'Åland Islands', 'al': 'Albania', 'dz': 'Algeria', 'as': 'American Samoa', 'ad':
    'Andorra', 'ao': 'Angola', 'ai': 'Anguilla', 'aq': 'Antarctica', 'ag': 'Antigua and Barbuda', 'ar': 'Argentina',
    'am': 'Armenia', 'aw': 'Aruba', 'au': 'Australia', 'at': 'Austria', 'az': 'Azerbaijan', 'bs': 'Bahamas',
    'bh': 'Bahrain', 'bd': 'Bangladesh', 'bb': 'Barbados', 'by': 'Belarus', 'be': 'Belgium', 'bz': 'Belize',
    'bj': 'Benin', 'bm': 'Bermuda', 'bt': 'Bhutan', 'bo': 'Bolivia (Plurinational State of)',
    'bq': 'Bonaire, Sint Eustatius and Saba', 'ba': 'Bosnia and Herzegovina', 'bw': 'Botswana', 'bv': 'Bouvet Island',
    'br': 'Brazil', 'io': 'British Indian Ocean Territory', 'bn': 'Brunei Darussalam', 'bg': 'Bulgaria',
    'bf': 'Burkina Faso', 'bi': 'Burundi', 'cv': 'Cabo Verde', 'kh': 'Cambodia', 'cm': 'Cameroon', 'ca': 'Canada',
    'ky': 'Cayman Islands', 'cf': 'Central African Republic', 'td': 'Chad', 'cl': 'Chile', 'cn': 'China',
    'cx': 'Christmas Island', 'cc': 'Cocos (Keeling) Islands', 'co': 'Colombia', 'km': 'Comoros', 'cg': 'Congo',
    'cd': 'Congo, Democratic Republic of the', 'ck': 'Cook Islands', 'cr': 'Costa Rica', 'ci': "Côte d'Ivoire",
    'hr': 'Croatia', 'cu': 'Cuba', 'cw': 'Curaçao', 'cy': 'Cyprus', 'cz': 'Czechia', 'dk': 'Denmark', 'dj': 'Djibouti',
    'dm': 'Dominica', 'do': 'Dominican Republic', 'ec': 'Ecuador', 'eg': 'Egypt', 'sv': 'El Salvador',
    'gq': 'Equatorial Guinea', 'er': 'Eritrea', 'ee': 'Estonia', 'sz': 'Eswatini', 'et': 'Ethiopia',
    'fk': 'Falkland Islands (Malvinas)', 'fo': 'Faroe Islands', 'fj': 'Fiji', 'fi': 'Finland', 'fr': 'France',
    'gf': 'French Guiana', 'pf': 'French Polynesia', 'tf': 'French Southern Territories', 'ga': 'Gabon', 'gm': 'Gambia',
    'ge': 'Georgia', 'de': 'Germany', 'gh': 'Ghana', 'gi': 'Gibraltar', 'gr': 'Greece', 'gl': 'Greenland',
    'gd': 'Grenada', 'gp': 'Guadeloupe', 'gu': 'Guam', 'gt': 'Guatemala', 'gg': 'Guernsey', 'gn': 'Guinea',
    'gw': 'Guinea-Bissau', 'gy': 'Guyana', 'ht': 'Haiti', 'hm': 'Heard Island and McDonald Islands', 'va': 'Holy See',
    'hn': 'Honduras', 'hk': 'Hong Kong', 'hu': 'Hungary', 'is': 'Iceland', 'in': 'India', 'id': 'Indonesia',
    'ir': 'Iran (Islamic Republic of)', 'iq': 'Iraq', 'ie': 'Ireland', 'im': 'Isle of Man', 'il': 'Israel', 'it':
    'Italy', 'jm': 'Jamaica', 'jp': 'Japan', 'je': 'Jersey', 'jo': 'Jordan', 'kz': 'Kazakhstan', 'ke': 'Kenya',
    'ki': 'Kiribati', 'kp': "Korea (Democratic People's Republic of)", 'kr': 'Korea, Republic of', 'kw': 'Kuwait',
    'kg': 'Kyrgyzstan', 'la': "Lao People's Democratic Republic", 'lv': 'Latvia', 'lb': 'Lebanon', 'ls': 'Lesotho',
    'lr': 'Liberia', 'ly': 'Libya', 'li': 'Liechtenstein', 'lt': 'Lithuania', 'lu': 'Luxembourg', 'mo': 'Macao',
    'mg': 'Madagascar', 'mw': 'Malawi', 'my': 'Malaysia', 'mv': 'Maldives', 'ml': 'Mali', 'mt': 'Malta',
    'mh': 'Marshall Islands', 'mq': 'Martinique', 'mr': 'Mauritania', 'mu': 'Mauritius', 'yt': 'Mayotte',
    'mx': 'Mexico', 'fm': 'Micronesia (Federated States of)', 'md': 'Moldova, Republic of', 'mc': 'Monaco',
    'mn': 'Mongolia', 'me': 'Montenegro', 'ms': 'Montserrat', 'ma': 'Morocco', 'mz': 'Mozambique', 'mm': 'Myanmar',
    'na': 'Namibia', 'nr': 'Nauru', 'np': 'Nepal', 'nl': 'Netherlands', 'nc': 'New Caledonia', 'nz': 'New Zealand',
    'ni': 'Nicaragua', 'ne': 'Niger', 'ng': 'Nigeria', 'nu': 'Niue', 'nf': 'Norfolk Island', 'mk': 'North Macedonia',
    'mp': 'Northern Mariana Islands', 'no': 'Norway', 'om': 'Oman', 'pk': 'Pakistan', 'pw': 'Palau',
    'ps': 'Palestine, State of', 'pa': 'Panama', 'pg': 'Papua New Guinea', 'py': 'Paraguay', 'pe': 'Peru',
    'ph': 'Philippines', 'pn': 'Pitcairn', 'pl': 'Poland', 'pt': 'Portugal', 'pr': 'Puerto Rico', 'qa': 'Qatar',
    're': 'Réunion', 'ro': 'Romania', 'ru': 'Russian Federation', 'rw': 'Rwanda', 'bl': 'Saint Barthélemy',
    'sh': 'Saint Helena, Ascension and Tristan da Cunha', 'kn': 'Saint Kitts and Nevis', 'lc': 'Saint Lucia',
    'mf': 'Saint Martin (French part)', 'pm': 'Saint Pierre and Miquelon', 'vc': 'Saint Vincent and the Grenadines',
    'ws': 'Samoa', 'sm': 'San Marino', 'st': 'Sao Tome and Principe', 'sa': 'Saudi Arabia', 'sn': 'Senegal',
    'rs': 'Serbia', 'sc': 'Seychelles', 'sl': 'Sierra Leone', 'sg': 'Singapore', 'sx': 'Sint Maarten (Dutch part)',
    'sk': 'Slovakia', 'si': 'Slovenia', 'sb': 'Solomon Islands', 'so': 'Somalia', 'za': 'South Africa',
    'gs': 'South Georgia and the South Sandwich Islands', 'ss': 'South Sudan', 'es': 'Spain', 'lk': 'Sri Lanka',
    'sd': 'Sudan', 'sr': 'Suriname', 'sj': 'Svalbard and Jan Mayen', 'se': 'Sweden', 'ch': 'Switzerland',
    'sy': 'Syrian Arab Republic', 'tw': 'Taiwan, Province of China', 'tj': 'Tajikistan',
    'tz': 'Tanzania, United Republic of', 'th': 'Thailand', 'tl': 'Timor-Leste', 'tg': 'Togo', 'tk': 'Tokelau',
    'to': 'Tonga', 'tt': 'Trinidad and Tobago', 'tn': 'Tunisia', 'tr': 'Turkey', 'tm': 'Turkmenistan',
    'tc': 'Turks and Caicos Islands', 'tv': 'Tuvalu', 'ug': 'Uganda', 'ua': 'Ukraine', 'ae': 'United Arab Emirates',
    'gb': 'United Kingdom of Great Britain and Northern Ireland', 'us': 'United States of America',
    'um': 'United States Minor Outlying Islands', 'uy': 'Uruguay', 'uz': 'Uzbekistan', 'vu': 'Vanuatu',
    've': 'Venezuela (Bolivarian Republic of)', 'vn': 'Viet Nam', 'vg': 'Virgin Islands (British)',
    'vi': 'Virgin Islands (U.S.)', 'wf': 'Wallis and Futuna', 'eh': 'Western Sahara', 'ye': 'Yemen', 'zm': 'Zambia',
    'zw': 'Zimbabwe'}

# Phone numbers config
SUPPORTED_COUNTRY = [None, 'US', 'AG', 'AI', 'AS', 'BB', 'BM', 'BS', 'CA', 'DM',
                     'GD', 'GU', 'JM', 'KN', 'KY', 'LC', 'MP', 'MS', 'PR', 'SX', 'TC', 'TT',
                     'VC', 'VG', 'VI', 'RU', 'KZ', 'EG', 'ZA', 'GR', 'NL', 'BE', 'FR', 'ES',
                     'HU', 'IT', 'VA', 'RO', 'CH', 'AT', 'GB', 'GG', 'IM', 'JE', 'DK', 'SE',
                     'NO', 'SJ', 'PL', 'DE', 'PE', 'MX', 'CU', 'AR', 'BR', 'CL', 'CO', 'VE',
                     'MY', 'AU', 'CC', 'CX', 'ID', 'PH', 'NZ', 'SG', 'TH', 'JP', 'KR', 'VN',
                     'CN', 'TR', 'IN', 'PK', 'AF', 'LK', 'MM', 'IR', 'SS', 'MA', 'EH', 'DZ',
                     'TN', 'LY', 'GM', 'SN', 'MR', 'ML', 'GN', 'CI', 'BF', 'NE', 'TG', 'BJ',
                     'MU', 'LR', 'SL', 'GH', 'NG', 'TD', 'CF', 'CM', 'CV', 'ST', 'GQ', 'GA',
                     'CG', 'CD', 'AO', 'GW', 'IO', 'AC', 'SC', 'SD', 'RW', 'ET', 'SO', 'DJ',
                     'KE', 'TZ', 'UG', 'BI', 'MZ', 'ZM', 'MG', 'RE', 'YT', 'ZW', 'NA', 'MW',
                     'LS', 'BW', 'SZ', 'KM', 'SH', 'TA', 'ER', 'AW', 'FO', 'GL', 'GI', 'PT',
                     'LU', 'IE', 'IS', 'AL', 'MT', 'CY', 'FI', 'AX', 'BG', 'LT', 'LV', 'EE',
                     'MD', 'AM', 'BY', 'AD', 'MC', 'SM', 'UA', 'RS', 'ME', 'XK', 'HR', 'SI',
                     'BA', 'MK', 'CZ', 'SK', 'LI', 'FK', 'BZ', 'GT', 'SV', 'HN', 'NI', 'CR',
                     'PA', 'PM', 'HT', 'GP', 'BL', 'MF', 'BO', 'GY', 'EC', 'GF', 'PY', 'MQ',
                     'SR', 'UY', 'CW', 'BQ', 'TL', 'NF', 'BN', 'NR', 'PG', 'TO', 'SB', 'VU',
                     'FJ', 'PW', 'WF', 'CK', 'NU', 'WS', 'KI', 'NC', 'TV', 'PF', 'TK', 'FM',
                     'MH', 'KP', 'HK', 'MO', 'KH', 'LA', 'BD', 'TW', 'MV', 'LB', 'JO', 'SY',
                     'IQ', 'KW', 'SA', 'YE', 'OM', 'PS', 'AE', 'IL', 'BH', 'QA', 'BT', 'MN',
                     'NP', 'TJ', 'TM', 'AZ', 'GE', 'KG', 'UZ', 'DO']

FORMAT_NUMBERS = {
    "E164": _phonenumbers.PhoneNumberFormat.E164,
    "INTERNATIONAL": _phonenumbers.PhoneNumberFormat.INTERNATIONAL,
    "NATIONAL": _phonenumbers.PhoneNumberFormat.NATIONAL,
    "RFC3966": _phonenumbers.PhoneNumberFormat.RFC3966
}
