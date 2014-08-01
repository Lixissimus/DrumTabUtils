import sublime, sublime_plugin
import re

class NewBarCommand(sublime_plugin.TextCommand):

	# insert an empty bar after the selected ones
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		lines = []
		new_sels = []
		units = 16

		for sel in sels:
			insert_positions = helper.getInsertionPositions(self.view, sel)
			new_sels.append(insert_positions[0])

			offset = 0
			for insert_position in insert_positions:
				self.view.insert(edit, insert_position + offset, "-" * units + "|")
				offset += units + 1

		sels.clear()
		for sel in new_sels:
			sels.add(sel)


class DublicateBarCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "dublicate")

class Helper(object):
	def __init__(self):
		super(Helper, self).__init__()

	def getInsertionPositions(self, view, sel):
		lines = view.split_by_newlines(sel)

		insert_positions = []

		# add first line
		length = len(view.substr(lines[0]))
		match = re.match('.*?\|', view.substr(lines[0])).group(0)
		match_len = len(match)
		insert_positions.append(lines[0].begin() + match_len)

		# add second to n-1 lines
		for i in range(1, len(lines) - 1):
			sel_to_end = sublime.Region(lines[i].end() - length, lines[i].end())
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			insert_positions.append(sel_to_end.begin() + match_len)

		if len(lines) > 1:
			# add last line
			sel_to_end = sublime.Region(lines[len(lines) - 1].end(), lines[len(lines) - 1].end() + length)
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			insert_positions.append(sel_to_end.begin() + match_len)

		return insert_positions		