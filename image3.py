# image3.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Use Courier font globally
plt.rcParams['font.family'] = 'monospace'

# Colors
blue = "#0056a9"

# Download the Excel file from the Texas DSHS website
url = "https://www.dshs.texas.gov/sites/default/files/LIDS-Immunizations/xls/2023-2024_School_Vaccination_Coverage_Levels_Seventh_Grade.xlsx"
df_schools = pd.read_excel(url, sheet_name="Coverage by District", skiprows=2)

# Rename columns
df_schools.columns = [
    "Facility Number", "School Type", "Facility Name", "Facility Address", "County",
    "Tdap/Td", "Meningococcal", "HepA", "HepB", "MMR", "Polio", "Varicella"
]

# Target counties
target_counties = [
    "Cochran", "Dallam", "Dawson", "Gaines", "Garza",
    "Lynn", "Lamar", "Lubbock", "Terry", "Yoakum"
]

# Filter and clean data
df_target = df_schools[df_schools["County"].isin(target_counties)]
df_target = df_target[["Facility Name", "County", "MMR"]].dropna()
df_target["Facility Name"] = df_target["Facility Name"].str.upper()

# Select the 10 schools with the lowest MMR
df_lowest = df_target.sort_values("MMR").head(10)

# Build labels: SCHOOL NAME (COUNTY)
labels = [f"{row['Facility Name']} ({row['County'].upper()})" for _, row in df_lowest.iterrows()]

# Plot
plt.figure(figsize=(10, 6))
bars = plt.barh(labels, df_lowest["MMR"], color=blue)

# Style
plt.xlabel("PERCENTAGE OF SEVENTH GRADERS IN THE DISTRICT WITH THE MMR VACCINE", fontsize=12, color=blue)
plt.xticks(color=blue, fontsize=10)
plt.yticks(color=blue, fontsize=10)
plt.xlim(0, 1)

# Remove grid and title
plt.grid(False)
plt.title("")  # no title

# Color spines
for spine in plt.gca().spines.values():
    spine.set_edgecolor(blue)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='both', colors=blue)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x * 100:.0f}%"))

# Save to SVG
plt.tight_layout()
plt.savefig("3.svg", format="svg")
print("SVG file generated: 3.svg")
