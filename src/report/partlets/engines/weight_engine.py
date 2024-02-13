from src.env.helpers import Paths
#from datetime import date
import polars as pl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

path = Paths()

weight_path = path.get_file_path("refined", "WM_WeightMeasurements.parquet")
df_w = pl.read_parquet(weight_path)

path_effect = [path_effects.withStroke(linewidth=2, foreground='white')]

# Função decide_annotation_position
def decide_annotation_position(previous_value, current_value, next_value):
    if previous_value < current_value:
        if current_value < next_value:  # //
            return "bottom", "center", 0, -7
        elif current_value == next_value:  # /-
            return "bottom", "center", 0, 13
        elif current_value > next_value:  # /\
            return "bottom", "center", 0, -10
    elif previous_value == current_value:
        if current_value < next_value:  # -/
            return "top", "center", 0, -13
        elif current_value == next_value:  # --
            return "bottom", "center", 0, 0
        elif current_value > next_value:  # -\
            return "bottom", "center", 0, 15
    elif previous_value > current_value:
        if current_value < next_value:  # \/
            return "top", "center", 0, 13
        elif current_value == next_value:  # \-
            return "bottom", "center", 0, 0
        elif current_value > next_value:  # \\
            return "top", "right", 0, 10
    return "bottom", "center"



# Ajustando as datas para exibir apenas a última semana
last_week_start = df_w['day_date'].max() - pl.duration(weeks=1)
last_week_data = df_w.filter(df_w['day_date'] >= last_week_start)

# Plotando os gráficos individuais
plt.figure(figsize=(12, 19))

# Plot 1: Total Weight
plt.subplot2grid((9, 1), (0, 0), rowspan=2, colspan=1)
#plt.subplot(611)
plt.plot(last_week_data['day_date'], last_week_data['ttl_weight'], label='Total Weight', color='blue')
plt.axhline(y=last_week_data['ttl_weight'].mean(), color='lightblue', linestyle='--', label='Mean')
#plt.xlabel('Day Date')
plt.ylabel('Total Weight (kg)')
plt.legend()
for i, (date, value) in enumerate(zip(last_week_data['day_date'], last_week_data['ttl_weight'])):
    previous_value = last_week_data['ttl_weight'][i-1] if i > 0 else last_week_data['ttl_weight'][i]
    next_value = last_week_data['ttl_weight'][i+1] if i < len(last_week_data)-1 else last_week_data['ttl_weight'][i]
    va, ha, x_diff, y_diff = decide_annotation_position(previous_value, value, next_value)
    plt.annotate(f'{value:.2f}', (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color='blue', fontweight='bold', path_effects=path_effect)

# Plot 2: Total Weight (Diff)
plt.subplot2grid((9, 1), (2, 0), rowspan=1, colspan=1)
#plt.subplot(612)
plt.plot(last_week_data['day_date'], last_week_data['ttl_diff'], label='Total Weight Daily Difference', color='blue')
plt.axhline(y=last_week_data['ttl_weight'].std(), color='lightblue', linestyle='--', label='Total Weekly SD')
#plt.xlabel('Day Date')
plt.ylabel('Total Weight Difference (kg)')
plt.legend()
for i, (date, value) in enumerate(zip(last_week_data['day_date'], last_week_data['ttl_diff'])):
    previous_value = last_week_data['ttl_diff'][i-1] if i > 0 else last_week_data['ttl_diff'][i]
    next_value = last_week_data['ttl_diff'][i+1] if i < len(last_week_data)-1 else last_week_data['ttl_diff'][i]
    va, ha, x_diff, y_diff = decide_annotation_position(previous_value, value, next_value)
    plt.annotate(f'{value:.2f}', (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color='blue', fontweight='bold', path_effects=path_effect)
    
# Plot 3: Muscle Weight
#plt.subplot(613)
plt.subplot2grid((9, 1), (3, 0), rowspan=2, colspan=1)
plt.plot(last_week_data['day_date'], last_week_data['mus_weight'], label='Muscle Weight', color='green')
plt.axhline(y=last_week_data['mus_weight'].mean(), color='lightgreen', linestyle='--', label='Mean')
plt.ylabel('Muscle Weight (kg)')
plt.legend()
for i, (date, value, percentage) in enumerate(zip(last_week_data['day_date'], last_week_data['mus_weight'], last_week_data['mus_percentage'])):
	previous_value = last_week_data['mus_weight'][i-1] if i > 0 else last_week_data['ttl_weight'][i]
	next_value = last_week_data['mus_weight'][i+1] if i < len(last_week_data)-1 else last_week_data['ttl_weight'][i]
	va, ha, x_diff, y_diff = decide_annotation_position(previous_value, value, next_value)
    
	# Concatenando o valor do campo mus_percentage ao texto do annotate
	annotate_text_large = f'{value:.2f}'
	annotate_text_small = f'({(percentage*100):.2f}%)'
    
	# Adicionando anotações
	plt.annotate(annotate_text_large, (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color='green', fontweight='bold', path_effects=path_effect)
	plt.annotate(annotate_text_small, (date, value), textcoords="offset points", xytext=(x_diff, y_diff), ha=ha, va=va, fontsize=8, color="black", path_effects=path_effect)


# Plot 4: Muscle Weight (Diff)
plt.subplot2grid((9, 1), (5, 0), rowspan=1, colspan=1)
#plt.subplot(614)
plt.plot(last_week_data['day_date'], last_week_data['mus_diff'], label='Muscle Daily Difference', color='green')
plt.axhline(y=last_week_data['mus_weight'].std(), color='lightgreen', linestyle='--', label='Muscle Weekly SD')
#plt.xlabel('Day Date')
plt.ylabel('Muscle Difference (kg)')
plt.legend()
for i, (date, value) in enumerate(zip(last_week_data['day_date'], last_week_data['mus_diff'])):
    previous_value = last_week_data['mus_diff'][i-1] if i > 0 else last_week_data['mus_diff'][i]
    next_value = last_week_data['mus_diff'][i+1] if i < len(last_week_data)-1 else last_week_data['mus_diff'][i]
    va, ha, x_diff, y_diff = decide_annotation_position(previous_value, value, next_value)
    plt.annotate(f'{value:.2f}', (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color='green', fontweight='bold', path_effects=path_effect)

# Plot 5: Fat Weight
plt.subplot2grid((9, 1), (6, 0), rowspan=2, colspan=1)
#plt.subplot(615)
plt.plot(last_week_data['day_date'], last_week_data['fat_weight'], label='Body Fat Weight', color='red')
plt.axhline(y=last_week_data['fat_weight'].mean(), color='lightcoral', linestyle='--', label='Mean')
#plt.xlabel('Day Date')
plt.ylabel('Body Fat Weight (kg)')
plt.legend()
for i, (date, value, percentage) in enumerate(zip(last_week_data['day_date'], last_week_data['fat_weight'], last_week_data['fat_percentage'])):
	previous_weight = last_week_data['fat_weight'][i-1] if i > 0 else last_week_data['ttl_weight'][i]
	next_weight = last_week_data['fat_weight'][i+1] if i < len(last_week_data)-1 else last_week_data['ttl_weight'][i]
	va, ha, x_diff, y_diff = decide_annotation_position(previous_value, value, next_value)

	# Concatenando o valor do campo mus_percentage ao texto do annotate
	annotate_text_large = f'{value:.2f}'
	annotate_text_small = f'({(percentage*100):.2f}%)'

	# Adicionando anotações
	plt.annotate(annotate_text_large, (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color='darkred', fontweight='bold', path_effects=path_effect)
	plt.annotate(annotate_text_small, (date, value), textcoords="offset points", xytext=(x_diff, y_diff), ha=ha, va=va, fontsize=8, color="black", path_effects=path_effect)


# Plot 6: Fat Weight (Diff)
plt.subplot2grid((9, 1), (8, 0), rowspan=1, colspan=1)
#plt.subplot(616)
plt.plot(last_week_data['day_date'], last_week_data['fat_diff'], label='Body Fat Daily Difference', color='red')
plt.axhline(y=last_week_data['fat_diff'].mean(), color='lightcoral', linestyle='--', label='Body Fat Weekly SD')
plt.xlabel('Day Date')
plt.ylabel('Body Fat Difference (kg)')
plt.legend()
for i, (date, value) in enumerate(zip(last_week_data['day_date'], last_week_data['fat_diff'])):
    previous_value = last_week_data['fat_diff'][i-1] if i > 0 else last_week_data['fat_diff'][i]
    next_value = last_week_data['fat_diff'][i+1] if i < len(last_week_data)-1 else last_week_data['fat_diff'][i]
    va, ha, x_diff, y_diff = decide_annotation_position(previous_value, value, next_value)
    plt.annotate(f'{value:.2f}', (date, value), textcoords="offset points", xytext=(0, 0), ha=ha, va=va, fontsize=13, color="darkred", fontweight='bold', path_effects=path_effect)


# Ajustando o layout
plt.tight_layout()
plt.savefig(config.get_partitioned_file_path(f"WM_{config.dt.date}.png"))
#plt.show()