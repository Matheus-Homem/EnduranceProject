from src.env.helpers import Paths
from src.env.globals import Global

import polars as pl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

class WeightEngine:
	def __init__(self):
		
		# Instanciate Global
		self.global_instance = Global()

		# Instanciate Paths
		self.path = Paths()
		
		# Get global variables
		self.exec_date = self.global_instance.get_date()
		self.calendar = self.global_instance.get_calendar()
		
		# Set backgroud effects
		self.path_effect = [path_effects.withStroke(linewidth=2, foreground='white')]

		# Create plot path
		self.plot_path = self.calendar.get_partitioned_file_path(prefix="WM", fmt="png")
		
		# Create the variable that represents last 8 days data
		self._filter_last_week_data()
		
		# Start execution of engine
		self._run()

	def get_path(self):
		return self.plot_path
	
	def _filter_last_week_data(self):
		
		# Get refined data path
		self.weight_path = self.path.get_file_path("refined", "WM_WeightMeasurements.parquet")

		# Read refined data
		self.df_w = pl.read_parquet(self.weight_path)
		
		# Get last week date
		self.last_week_start = self.df_w['day_date'].max() - pl.duration(weeks=1)

		# Filter data to last 8 days
		self.last_week_data = self.df_w.filter(self.df_w['day_date'] >= self.last_week_start)

	def _decide_annotation_position(self, previous_value, current_value, next_value):
		if previous_value < current_value:
			if current_value < next_value:			# //
				return "bottom", "center", 0, -7
			elif current_value == next_value:		# /-
				return "bottom", "center", 0, 13
			elif current_value > next_value:		# /\
				return "bottom", "center", 0, -10
		elif previous_value == current_value:
			if current_value < next_value:			# -/
				return "top", "center", 0, -13
			elif current_value == next_value:		# --
				return "bottom", "center", 0, 0
			elif current_value > next_value:		# -\
				return "bottom", "center", 0, 15
		elif previous_value > current_value:
			if current_value < next_value:			# \/
				return "top", "center", 0, 13
			elif current_value == next_value:		# \-
				return "bottom", "center", 0, -10
			elif current_value > next_value:		# \\
				return "top", "right", 0, 10
		return "bottom", "center"
		
	def _plot_subplot_with_annotations(
		self:int, 
		subplot_position:int, 
		vertical_spans:str, 
		ylabel:str, 
		data_column:str, 
		plot_label:str, 
		plot_color:str, 
		hline_color:str, 
		hline_label:str, 
		annotation_color:str=None, 
		percentage_data_column:str=None
		):
		"""
		Plot a subplot with annotations and optional percentage data.

		Args:
			subplot_position (int): The position of the subplot in the grid.
			vertical_spans (int): How many vertical spaces the subplot occupies in the grid.
			ylabel (str): The label for the y-axis of the plot.
			data_column (str): The name of the column to be plotted.
			plot_label (str): The label for the main plot in the legend.
			plot_color (str): The color of the main plot.
			hline_color (str): The color of the horizontal line in the plot.
			hline_label (str): The label for the horizontal line in the legend.
			annotation_color (str, optional): The color of the annotations. Defaults to the plot_color.
			percentage_data_column (str, optional): The name of the column for percentage data. Defaults to None.
		"""
		annotation_color = plot_color if annotation_color is None else annotation_color
		
		plt.subplot2grid((9, 1), (subplot_position, 0), rowspan=vertical_spans, colspan=1)
		plt.plot(self.last_week_data["day_date"], self.last_week_data[data_column], label=plot_label, color=plot_color)
		plt.axhline(y=self.last_week_data[data_column].mean(), color=hline_color, linestyle='--', label=hline_label)
		plt.ylabel(ylabel)
		
		if subplot_position == 8:
			plt.xlabel('Day Date')
			
		plt.legend()
		
		if percentage_data_column:
			for i, (date, value, percentage) in enumerate(zip(self.last_week_data['day_date'], self.last_week_data[data_column], self.last_week_data[percentage_data_column])):
				previous_value = self.last_week_data[data_column][i-1] if i > 0 else self.last_week_data['ttl_weight'][i]
				next_value = self.last_week_data[data_column][i+1] if i < len(self.last_week_data)-1 else self.last_week_data['ttl_weight'][i]
				va, ha, x_diff, y_diff = self._decide_annotation_position(previous_value, value, next_value)

				# Concatenating the percentage data to the annotation text
				annotate_text_large = f'{value:.2f}'
				annotate_text_small = f'({(percentage*100):.2f}%)'

				# Adding annotations
				plt.annotate(annotate_text_large, (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color=annotation_color, fontweight='bold', path_effects=self.path_effect)
				plt.annotate(annotate_text_small, (date, value), textcoords="offset points", xytext=(x_diff, y_diff), ha=ha, va=va, fontsize=8, color="black", path_effects=self.path_effect)
		else:
			for i, (date, value) in enumerate(zip(self.last_week_data['day_date'], self.last_week_data[data_column])):
				previous_value = self.last_week_data[data_column][i-1] if i > 0 else self.last_week_data['ttl_weight'][i]
				next_value = self.last_week_data[data_column][i+1] if i < len(self.last_week_data)-1 else self.last_week_data['ttl_weight'][i]
				va, ha, x_diff, y_diff = self._decide_annotation_position(previous_value, value, next_value)
				plt.annotate(f'{value:.2f}', (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color=annotation_color, fontweight='bold', path_effects=self.path_effect)

	def _run(self):
		plt.figure(figsize=(12, 19))
		
		subplots_config = [
			{"subplot_position": 0, "ylabel": 'Total Weight (kg)',				"vertical_spans": 2, "data_column": 'ttl_weight',	"plot_label": 'Total Weight',					"hline_label": "Mean",				"plot_color": "blue",	"hline_color": "lightblue"},
			{"subplot_position": 2, "ylabel": 'Total Weight Difference (kg)',	"vertical_spans": 1, "data_column": 'ttl_diff',		"plot_label": 'Total Weight Daily Difference',	"hline_label": 'Total Weekly SD',	"plot_color": 'blue',	"hline_color": "lightblue"},
			{"subplot_position": 3, "ylabel": 'Muscle Weight (kg)',				"vertical_spans": 2, "data_column": 'mus_weight',	"plot_label": 'Muscle Weight',					"hline_label": "Mean",				"plot_color": "green",	"hline_color": "lightgreen",	"percentage_data_column": "mus_percentage"},
			{"subplot_position": 5, "ylabel": 'Muscle Difference (kg)',			"vertical_spans": 1, "data_column": 'mus_diff',		"plot_label": 'Muscle Daily Difference',		"hline_label": 'Total Weekly SD',	"plot_color": 'green',	"hline_color": "lightgreen"},
			{"subplot_position": 6, "ylabel": 'Body Fat Weight (kg)',			"vertical_spans": 2, "data_column": 'fat_weight',	"plot_label": 'Body Fat Weight',				"hline_label": "Mean",				"plot_color": 'red',	"hline_color": 'lightcoral',	"percentage_data_column": 'fat_percentage',	"annotation_color": 'darkred'},
			{"subplot_position": 8, "ylabel": 'Body Fat Difference (kg)',		"vertical_spans": 1, "data_column": 'fat_diff',		"plot_label": 'Body Fat Daily Difference',		"hline_label": 'Total Weekly SD',	"plot_color": 'red',	"hline_color": "lightcoral",	"annotation_color": "darkred"}
		]

		for config in subplots_config:
			self._plot_subplot_with_annotations(**config)
		
		plt.tight_layout()
		plt.savefig(self.plot_path)
