# metric_base.py - Basic classes for Text representations. 
# 
# Based on Coh-Metrix-Port's functionalities from
# Andre Luiz Verucci da Cunha [Copyright (C) 2014] published
# under GNU General Public License as published by the Free
# Software Foundation.
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

class Metric(object):
    """A metric is a textual characteristic.
    """

    def __init__(self, text, name="", column_name="", desc=""):
        """Form a metric.

        Keyword arguments:
        text -- Text for which the textual characteristic is computed for.
        name -- A succint name of the metric (e.g., 'Flesch index'). If
            no name is provided, the class name is used. (default "")
        table_name -- The name of the column in the table corresponding to
            the category of this metric in coh_user_data. If no value is
            specified, Coh-Metrix-Port will check whether 'name' is a valid
            table name; if so, 'name' is used as the table name. (default "")
        desc -- A longer description of the metric. Used for UI purposes.
            (default "")
        """
        if name:
            self.name = name
        else:
            name = self.__class__.__name__
        self.column_name = column_name
        self.desc = desc

        self.text = text

    # Metrics

    def value(self):
        """Calculate the value of the metric in the text.

        Returns: an appropriate data structure for the corresponding to the metric.
        """
        raise NotImplementedError()
