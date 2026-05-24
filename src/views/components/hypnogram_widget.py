from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class HypnogramWidget(FigureCanvasQTAgg):
    def __init__(self, is_dark : bool = False, parent=None):
        # Use a style that respects our manual settings
        plt.style.use('seaborn-v0_8-dark-palette')

        # Create figure with explicit transparent background
        self.fig = Figure(facecolor='#1e1e1e')  # Match your app's dark background
        self.axes = self.fig.add_subplot(111)

        super().__init__(self.fig)
        self.setParent(parent)

        # Map your string labels to numeric values
        self.stage_map = {
            'WAKE': 2,
            'REM': 1,
            'NREM': 0,
        }

        # Consumer-style color palette
        self.stage_colors = {
            'WAKE': '#FF8C00',  # Orange
            'REM': '#9B59B6',  # Medium purple (transition color)
            'NREM': '#4B0082',  # Deep purple/indigo
        }

        self.is_dark = is_dark
        if self.is_dark:
            self._apply_dark_theme()
        else:
            self._apply_light_theme()

    def _apply_dark_theme(self):
        # Figure and axes backgrounds
        self.fig.patch.set_facecolor('#1e1e1e')
        self.axes.set_facecolor('#2d2d2d')

        # Text colors
        self.axes.tick_params(colors='#e0e0e0', labelsize=8)
        self.axes.xaxis.label.set_color('#e0e0e0')
        self.axes.yaxis.label.set_color('#e0e0e0')
        self.axes.title.set_color('#e0e0e0')

        # Spine colors
        for spine in self.axes.spines.values():
            spine.set_color('#444444')

        # Grid
        self.axes.grid(True, alpha=0.15, color='#e0e0e0')

        self.fig.tight_layout(pad=1.5)

    def _apply_light_theme(self):
        # Figure and axes backgrounds
        self.fig.patch.set_facecolor('#ffffff')
        self.axes.set_facecolor('#ffffff')

        # Text colors
        self.axes.tick_params(colors='#333333')
        self.axes.xaxis.label.set_color('#333333')
        self.axes.yaxis.label.set_color('#333333')
        self.axes.title.set_color('#333333')

        # Spine colors
        for spine in self.axes.spines.values():
            spine.set_color('#cccccc')

        # Grid
        self.axes.grid(True, alpha=0.3, color='#999999')

        self.fig.tight_layout(pad=1.5)

    def plot(self, stages_dict):
        # Convert to lists
        timestamps = list(stages_dict.keys())
        stage_labels = list(stages_dict.values())

        plot_timestamps = []
        plot_stages = []

        for ts, stage in zip(timestamps, stage_labels):
            ts = datetime.strptime(ts, '%H:%M:%S')
            if stage == 'START':
                pass
            elif stage == 'END':
                plot_timestamps.append(ts)
                plot_stages.append('WAKE')
            else:
                plot_timestamps.append(ts)
                plot_stages.append(stage)


        # 1. Clear and re-apply theme (clear() resets some settings)
        self.axes.clear()

        if self.is_dark:
            self._apply_dark_theme()
        else:
            self._apply_light_theme()

        # 2. Convert timestamps to numerical format
        numeric_timestamps = mdates.date2num(plot_timestamps)
        numeric_start = mdates.date2num(plot_timestamps[0])
        numeric_end = mdates.date2num(plot_timestamps[-1])

        # 3. Convert string stages to numbers for plotting
        numeric_stages = [self.stage_map[s] for s in plot_stages]

        # 4. Always plot the stepped line
        self.axes.step(numeric_timestamps, numeric_stages, where='post', color='#B07CC6', linewidth=2)

        # 5. Only add color fills if we have more than one segment
        if len(numeric_timestamps) > 1:
            for i in range(len(numeric_timestamps) - 1):
                t_start = numeric_timestamps[i]
                t_end = numeric_timestamps[i + 1]
                stage = plot_stages[i]
                color = self.stage_colors.get(stage, '#555555')

                self.axes.fill_between(
                    [t_start, t_end],
                   2.5,
                    numeric_stages[i],
                    step='post',
                    color=color,
                    alpha=0.4
                )

        # 6. Set axis limits
        if numeric_start is not None and numeric_end is not None:
            self.axes.set_xlim(numeric_start, numeric_end)
        self.axes.set_ylim(-0.5, 2.5)

        # 7. Y-axis labels
        self.axes.set_yticks([0, 1, 2])
        self.axes.set_yticklabels(['NREM', 'REM', 'WAKE'])

        # 8. X-axis formatting
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())

        # Grid
        self.axes.grid(True, alpha=0.15, axis='y')
        # Rotate time labels for readability
        self.fig.autofmt_xdate(rotation=30, ha='right')
        # Ensure the layout uses space efficiently
        self.fig.tight_layout(pad=1.5)

        # Redraw the canvas
        self.draw()