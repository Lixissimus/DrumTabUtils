import sublime, sublime_plugin
import re

class NewBarCommand(sublime_plugin.TextCommand):

	# insert an empty bar after the selected ones
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		final_pos = []
		units = 16

		for sel in sels:
			offset = 0
			new_sels = []
			regions = helper.getBarSelection(self.view, sel, units)

			final_pos.append(regions[0].end())

			for reg in regions:
				self.view.insert(edit, reg.end() + offset, "-" * units + "|")
				offset += units + 1

		sels.clear()
		for pos in final_pos:
			sels.add(pos)


class DublicateBarCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		final_pos = []
		units = 16

		for sel in sels:
			offset = 0
			new_sels = []
			regions = helper.getBarSelection(self.view, sel, units)

			final_pos.append(regions[0].end())

			# to avoid weird offset calculations, we create the insertions before inserting
			dublicates = []
			for reg in regions:
				dublicates.append(self.view.substr(reg))

			i = 0
			for reg in regions:
				insert_string = dublicates[i]
				self.view.insert(edit, reg.end() + offset, insert_string)
				offset += len(insert_string)
				i += 1

		sels.clear()
		for pos in final_pos:
			sels.add(pos)


class Helper(object):

	def getBarSelection(self, view, sel, units):
		lines = view.split_by_newlines(sel)

		bar_regions = []

		# add first line
		length = len(view.substr(lines[0]))
		match = re.match('.*?\|', view.substr(lines[0])).group(0)
		match_len = len(match)
		end_pos = lines[0].begin() + match_len
		begin_pos = end_pos - units - 1
		bar_regions.append(sublime.Region(begin_pos, end_pos))

		# add second to n-1 lines
		for i in range(1, len(lines) - 1):
			sel_to_end = sublime.Region(lines[i].end() - length, lines[i].end())
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			end_pos = sel_to_end.begin() + match_len
			begin_pos = end_pos - units - 1
			bar_regions.append(sublime.Region(begin_pos, end_pos))

		if len(lines) > 1:
			# add last line
			sel_to_end = sublime.Region(lines[len(lines) - 1].end(), lines[len(lines) - 1].end() + length)
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			end_pos = sel_to_end.begin() + match_len
			begin_pos = end_pos - units - 1
			bar_regions.append(sublime.Region(begin_pos, end_pos))

		return bar_regions