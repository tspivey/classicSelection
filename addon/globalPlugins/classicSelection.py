#Copyright 2016 Tyler Spivey <tspivey@pcdesk.net>
#See the license in copying.txt.
#Originally taken from NVDA 2016.1.
import globalPluginHandler
import api
import ui
import textInfos

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Classic Selection")

	def script_review_markStartForCopy(self, gesture):
		self._copyStartMarker = api.getReviewPosition().copy()
		# Translators: Indicates start of review cursor text to be copied to clipboard.
		ui.message(_("Start marked"))
	# Translators: Input help mode message for mark review cursor position for copy command (that is, marks the current review cursor position as the starting point for text to be copied).
	script_review_markStartForCopy.__doc__ = _("Marks the current position of the review cursor as the start of text to be copied")

	def script_review_copy(self, gesture):
		if not getattr(self, "_copyStartMarker", None):
			# Translators: Presented when attempting to copy some review cursor text but there is no start marker.
			ui.message(_("No start marker set"))
			return
		pos = api.getReviewPosition().copy()
		if self._copyStartMarker.obj != pos.obj:
			# Translators: Presented when trying to copy text residing on a different object (that is, start marker is in object 1 but trying to copy text from object 2).
			ui.message(_("The start marker must reside within the same object"))
			return
		pos.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
		pos.setEndPoint(self._copyStartMarker, "startToStart")
		if pos.compareEndPoints(pos, "startToEnd") < 0 and pos.copyToClipboard():
			# Translators: Presented when some review text has been copied to clipboard.
			ui.message(_("Review selection copied to clipboard"))
		else:
			# Translators: Presented when there is no text selection to copy from review cursor.
			ui.message(_("No text to copy"))
			return
		self._copyStartMarker = None
	# Translators: Input help mode message for copy selected review cursor text to clipboard command.
	script_review_copy.__doc__ = _("Retrieves the text from the previously set start marker up to and including the current position of the review cursor and copies it to the clipboard")

	__gestures = {
		"kb:nvda+f9": "review_markStartForCopy",
		"kb:nvda+f10": "review_copy",
	}
