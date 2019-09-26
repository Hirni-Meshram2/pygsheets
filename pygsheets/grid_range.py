from pygsheets.datarange import DataRange
from pygsheets.worksheet import Worksheet
from pygsheets import utils
from pygsheets import exceptions


class GridRange(object):
    """ A range on a sheet. All indexes are zero-based.
    Indexes are half open, e.g the start index is inclusive and the end index is exclusive -- [startIndex, endIndex).
    Missing indexes indicate the range is unbounded on that side. """

    def __init__(self, label=None, worksheet_id=None, start=None, end=None, spreadsheet=None):
        self._label = label
        self._worksheet_name = None
        self._worksheet_id = worksheet_id
        self._start = start
        self._end = end
        self.spreadsheet = spreadsheet

        if label:
            self._update_values()
        else:
            self._update_label()

    @property
    def start(self):
        """ address of top left cell (index) """
        return self._start

    @start.setter
    def start(self, value):
        value = utils.format_addr(value, 'tuple')
        self._start = value
        self._update_label()

    @property
    def end(self):
        """ address of bottom right cell (index) """
        return self._end

    @end.setter
    def end(self, value):
        value = utils.format_addr(value, 'tuple')
        self._end = value
        self._update_label()

    @property
    def label(self):
        """ Label in grid range format """
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self._update_values()

    @property
    def worksheet_id(self):
        return self._worksheet_id

    @worksheet_id.setter
    def worksheet_id(self, value):
        if isinstance(value, Worksheet):
            self.set_worksheet(value)
        else:
            self._worksheet_id = value
            self._update_label()

    def set_worksheet(self, value):
        """ set the worksheet of this grid range. """
        if isinstance(value, Worksheet):
            self.spreadsheet = value.spreadsheet
            self._worksheet_id = value.id
            self._update_label()
        else:
            raise exceptions.InvalidArgumentValue()

    def _update_label(self):
        """update label from values """
        pass

    def _update_values(self):
        """ update values from label """
        label = self._label
        self._worksheet_name = label.split('!')
        if len(label.split('!')) > 1:
            pass
            self._worksheet_name = label.split('!')[1]

    def to_json(self):
        self._update_values()
        return {
            "sheetId": self._worksheet_id,
            "startRowIndex": self._start[0]-1,
            "endRowIndex": self._end[0],
            "startColumnIndex": self._start[1]-1,
            "endColumnIndex": self._end[1],
        }

    def to_range(self, worksheet):
        return DataRange()