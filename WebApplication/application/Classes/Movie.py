class Movie:
	def __init__(self, arguments):
		if 'id' in arguments:
			self._id = arguments['id']
		else:
			self._id = 0
		self._title = arguments['title']
		self._director = arguments['director']
		self._producers = arguments['producers']
		self._actors = arguments['actors']
		self._language = arguments['language']
		self._subtitles = arguments['subtitles']
		self._dubbed = arguments['dubbed']
		self._release_date = arguments['release_date']
		self._runtime = arguments['run_time']

	def get_id(self):
		"""Returns the id of the object"""
		return self._id

	def __str__(self):

		return "Movie | ID: " + str(self._id) + " TITLE: " + self._title +  " DIRECTOR: " + self._director + " PRODUCERS: " + self._producers + " ACTORS: " + self._actors + \
				" LANGUAGE: "  + self._language + " SUBTITLES: " + self._subtitles + " DUBBED: " + self._dubbed + " RELEASE_DATE: " + self._release_date + " RUNTIME: " + str(self._runtime)