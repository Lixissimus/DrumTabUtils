import sublime, sublime_plugin
import re

class SelectBarCommand(sublime_plugin.TextCommand):
	# select each line of the selected bars
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		new_sels = []

		for sel in sels:
			regions = helper.getBarSelection(self.view, sel)

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

		for sel in sels:
			offset = 0
			new_sels = []
			regions = helper.getBarSelection(self.view, sel)
			units = len(self.view.substr(regions[0])) - 1

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

		for sel in sels:
			offset = 0
			new_sels = []
			regions = helper.getBarSelection(self.view, sel)

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


class RemoveBarCommand(sublime_plugin.TextCommand):
	# remove the selected bar
	def run(self, edit):
		sels = self.view.sel()
		helper = Helper()

		for sel in sels:
			offset = 0
			regions = helper.getBarSelection(self.view, sel)

			# remove the selcted bar
			for reg in regions:
				length = len(self.view.substr(reg))
				self.view.erase(edit, sublime.Region(reg.begin() + offset, reg.end() + offset))
				offset -= length


class NewLineAfterBarCommand(sublime_plugin.TextCommand):
	# break the whole tab-line after the selected bar
	def run(self, edit):
		pass
		

class Helper(object):
	# return the regions of each line of the selected bar
	def getBarSelection(self, view, sel):
		lines = view.split_by_newlines(sel)

		bar_regions = []

		# save the selection's start column, since this defines the bar that will be selected
		(first_row, first_col) = view.rowcol(sel.begin())

		for line in lines:
			# get the line's row
			(cur_row, cur_col) = view.rowcol(line.begin())
			# calculate a point (selection point) defined by the line's row and the selction's column
			# this is always a point, that is in the current line and the selected bar
			sel_point = view.text_point(cur_row, first_col)
			# get the beginning and the end point of the current line
			line_start_point = view.line(sel_point).begin()
			line_end_point = view.line(sel_point).end()
			# get the (l)ast (p)art of the line, beginning at the line's selection point
			lp_line = view.substr(sublime.Region(sel_point, line_end_point))
			# detect the (l)ast (p)art of the bar, the end is defines by the closing |
			# 'match' just finds a match at the beginning of the string
			lp_bar = re.match('.*?\|', lp_line).group(0)
			# this defines the end point of the bar
			end_point = sel_point + len(lp_bar)
			# get the string from the line's beginning to the bar's end point
			line_to_bar_end = view.substr(sublime.Region(line_start_point, end_point))
			# detect a full bar at the end of previously extracted string
			# this string contains the selected bar (one line of it)
			bar_string = re.search('\|[^|]*\|$', line_to_bar_end).group(0)
			# the + 1 is needed to exclude the opening | from the selection
			start_point = end_point - len(bar_string) + 1
			# create a new region and save it
			bar_regions.append(sublime.Region(start_point, end_point))

		return bar_regions