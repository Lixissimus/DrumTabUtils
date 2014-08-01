import sublime, sublime_plugin
import re

class NewBarCommand(sublime_plugin.TextCommand):

	# insert an empty bar after the selected ones
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		final_pos = []
		new_sels = []
		units = 16
		offset = 0

		for sel in sels:
			regions = helper.getBarSelection(self.view, sel, units)
			for reg in regions:
				new_sels.append(reg)

			final_pos.append(regions[0].end())

		for new_sel in new_sels:
			self.view.insert(edit, new_sel.end() + offset, "-" * units + "|")
			offset += units + 1

		sels.clear()
		for pos in final_pos:
			sels.add(pos)


class DublicateBarCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "dublicate")

class Helper(object):
	def __init__(self):
		super(Helper, self).__init__()

	def getBarSelection(self, view, sel, units):
		lines = view.split_by_newlines(sel)

		bar_regions = []

		# add first line
		length = len(view.substr(lines[0]))
		match = re.match('.*?\|', view.substr(lines[0])).group(0)
		match_len = len(match)
		end_pos = lines[0].begin() + match_len
		begin_pos = end_pos - units - 1
		print(begin_pos, end_pos)
		bar_regions.append(sublime.Region(begin_pos, end_pos))

		# add second to n-1 lines
		for i in range(1, len(lines) - 1):
			sel_to_end = sublime.Region(lines[i].end() - length, lines[i].end())
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			end_pos = sel_to_end.begin() + match_len
			begin_pos = end_pos - units - 1
			print(begin_pos, end_pos)
			bar_regions.append(sublime.Region(begin_pos, end_pos))

		if len(lines) > 1:
			# add last line
			sel_to_end = sublime.Region(lines[len(lines) - 1].end(), lines[len(lines) - 1].end() + length)
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			end_pos = sel_to_end.begin() + match_len
			begin_pos = end_pos - units - 1
			print(begin_pos, end_pos)
			bar_regions.append(sublime.Region(begin_pos, end_pos))

		return bar_regions