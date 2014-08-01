import sublime, sublime_plugin
import re

class SelectBarCommand(sublime_plugin.TextCommand):
	# select each line of the selected bars
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		new_sels = []
		units = 16

		for sel in sels:
			regions = helper.getBarSelection(self.view, sel, units)

			for reg in regions:
				new_sels.append(reg)

		sels.clear()
		for reg in new_sels:
			sels.add(reg)


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

			# insert the empty bar after the selected one
			for reg in regions:
				self.view.insert(edit, reg.end() + offset, "-" * units + "|")
				offset += units + 1

			# save the begining of the new bar as the curser position after insertion
			final_pos.append(sublime.Region(regions[0].end(), regions[len(regions) - 1].begin() + offset))

		# set the cursor to the saved positions
		sels.clear()
		for pos in final_pos:
			sels.add(pos)


class DublicateBarCommand(sublime_plugin.TextCommand):
	# dublicate the bars and insert them after the selected ones
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		final_pos = []
		units = 16

		for sel in sels:
			offset = 0
			new_sels = []
			regions = helper.getBarSelection(self.view, sel, units)

			# to avoid weird offset calculations, we create the insertions before inserting
			dublicates = []
			for reg in regions:
				dublicates.append(self.view.substr(reg))

			# insert the appropriate strings after the selected bar
			i = 0
			for reg in regions:
				insert_string = dublicates[i]
				self.view.insert(edit, reg.end() + offset, insert_string)
				offset += len(insert_string)
				i += 1

			# save the begining of the new bar as the curser position after insertion
			final_pos.append(sublime.Region(regions[0].end(), regions[len(regions) - 1].begin() + offset))

		# set the cursor to the saved positions
		sels.clear()
		for pos in final_pos:
			sels.add(pos)


class NewLineAfterBarCommand(sublime_plugin.TextCommand):
	# break the whole tab-line after the selected bar
	def run(self, edit):
		pass
		

class Helper(object):
	# return the regions of each line of the selected bar
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

		# add last line
		if len(lines) > 1:
			sel_to_end = sublime.Region(lines[len(lines) - 1].end(), lines[len(lines) - 1].end() + length)
			match_len = len(re.match('.*?\|', view.substr(sel_to_end)).group(0))
			end_pos = sel_to_end.begin() + match_len
			begin_pos = end_pos - units - 1
			bar_regions.append(sublime.Region(begin_pos, end_pos))

		return bar_regions