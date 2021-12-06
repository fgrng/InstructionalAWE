# autocerrected.py - Text representation class with autocorrection for misspelled words.
#
# 
# 
# Copyright (C) 2021 Fabian Grünig <gruenig@posteo.de>
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from classes.text import Text

import hunspell as hs

class AutocorrectedText(Text):
    """Represents a autocorrectet text: its autocorrected content and metadata.
    """

    def __init__(self, filepath="", plaintext="", encoding='utf-8', title='', author='',
                 source=''):
        """Form class of Text representation from plaintext argument or file
        and autocorrect misspelled words.
        One of the following two arguments is required:
        filepath -- a path to the file containing the text. The text is
            supposed to be formatted as one paragraph per line, with
            multiple sentences per paragraph. Blank lines are ignored.
        plaintext -- a string containing the telt. The text is
            supposed to be formatted as one paragraph per line, with
            multiple sentences per paragraph. Blank lines are ignored.
        
        Keyword arguments:
        encoding -- The encoding of the input file (default "utf-8")
        title -- The title of the text (default "").
        author -- The author of the text (default "").
        source -- Where the text came from, usually a URL (default "").
        """
        self.autocorrected = False

        # Call parent constructor with same arguments.
        super().__init__(filepath, plaintext, encoding, title, author, source)


    # Change the paragraphs property. All other porperties rely on 
    # the paragraph property.
    @property
    def paragraphs(self):
        # Perform autocorrection unless already corrected.
        if not self.autocorrected:
            self.autocorrect()
        return self._paragraphs

    def autocorret(self):
        spellchecker = hunspell.HunSpell(
            '/usr/share/hunspell/de_DE.dic',
            '/usr/share/hunspell/de_DE.aff')
        


