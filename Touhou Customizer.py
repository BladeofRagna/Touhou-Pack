import sys
import os
import json
import random
import yaml
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QCheckBox, QMessageBox, QLabel, QTabWidget, QScrollArea, QVBoxLayout, QComboBox
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QContextMenuEvent, QIcon
from ruamel.yaml import YAML

def load_config():
    config_path = resource_path("config.yaml")
    yaml = YAML()
    yaml.preserve_quotes = True  # Preserve any quotes
    try:
        with open(config_path, 'r') as file:
            return yaml.load(file) or {}
    except FileNotFoundError:
        return {}

def save_config(config):
    config_path = resource_path("config.yaml")
    yaml = YAML()
    yaml.default_flow_style = False  # Use block-style YAML for readability
    yaml.indent(mapping=2, sequence=4, offset=2)  # Adjust indentation to match your preferences
    with open(config_path, 'w') as file:
        yaml.dump(config, file)


# Define application_path for both dev and executable environments
if getattr(sys, 'frozen', False):
    # If bundled with PyInstaller, get executable location
    application_path = os.path.dirname(sys.executable)
else:
    # If running as a normal script, get script directory
    application_path = os.path.dirname(os.path.abspath(__file__))

# Helper function to load YAML data
def load_yaml(file_name):
    with open(file_name, 'r') as file:
        return yaml.safe_load(file)

# Helper function to resolve resource paths for both development and PyInstaller
def resource_path(relative_path):
    return os.path.join(application_path, relative_path)

# Helper function to save the randomized fumos into fumo's.yml in proper YAML format
def save_fumos_yaml(data, file_path):
    try:
        with open(file_path, 'w') as file:
            for entry in data:
                file.write(f"- id: {entry['id']}\n")
                if '\n' in entry['en']:
                    formatted_description = entry['en'].replace('\n', '\n    ')
                    file.write(f"  en: >-\n    {formatted_description}\n")
                else:
                    file.write(f"  en: '{entry['en']}'\n")
        print(f"fumo's.yml saved successfully to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving fumo's.yml: {str(e)}")

# Function to update specific lines in mod.yml with new Fumo names
def update_mod_yml(mod_file_path, fumo_names, fumo_line_numbers):
    try:
        with open(mod_file_path, 'r', encoding='utf-8') as file:
            mod_lines = file.readlines()
        for i, line_num in enumerate(fumo_line_numbers):
            if i < len(fumo_names):
                new_line = f"  - name: remastered/Fumo's/{fumo_names[i]}.dds\n"
                mod_lines[line_num] = new_line
        with open(mod_file_path, 'w', encoding='utf-8') as file:
            file.writelines(mod_lines)
        print(f"mod.yml updated successfully at lines: {fumo_line_numbers}")
    except Exception as e:
        print(f"An error occurred while updating mod.yml: {str(e)}")

# Function to extract the plain name from the fumo entry (removes color codes and 'Fumo')
def extract_plain_name(fumo_entry):
    try:
        name_with_tag = fumo_entry['name']
        plain_name = name_with_tag.split('}')[1].replace(' Fumo', '').strip()
        return plain_name
    except IndexError:
        return fumo_entry['name']

# Mapping each fumo to its slot group
fumo_groups = {
    "Reimu": 1, "Reisen": 1, "Rumia": 1, "Tewi": 1, "Rin": 1,
    "Alice": 2, "Murasa": 2, "Renko": 2, "Eirin": 2, "Parsee": 2,
    "Remilia": 3, "Satori": 3, "Maribel": 3, "Kaguya": 3, "Kogasa": 3,
    "Sanae": 4, "Aya": 4, "Yukari": 4, "Suwako": 4, "Nue": 4,
    "Cirno": 5, "Sakuya": 5, "Ran": 5, "Kasen": 5, "Sagume": 5,
    "Utsuho": 6, "Seija": 6, "Chen": 6, "Tiny Remilia": 6, "Junko": 6,
    "Marisa": 7, "Patchouli": 7, "Nitori": 7, "Hunter Flandre": 7, "Joon": 7,
    "Yuyuko": 8, "Youmu": 8, "Flandre": 8, "Retro Reimu": 8, "Shion": 8,
    "Koishi": 9, "Momiji": 9, "Suika": 9, "Retro Marisa": 9, "Tenshi": 9
}

# Create slot groups for each fumo slot
fumo_slot_groups = {
    1: ["Reimu", "Reisen", "Rumia", "Tewi", "Rin"],
    2: ["Alice", "Murasa", "Renko", "Eirin", "Parsee"],
    3: ["Remilia", "Satori", "Maribel", "Kaguya", "Kogasa"],
    4: ["Sanae", "Aya", "Yukari", "Suwako", "Nue"],
    5: ["Cirno", "Sakuya", "Ran", "Kasen", "Sagume"],
    6: ["Utsuho", "Seija", "Chen", "Tiny Remilia", "Junko"],
    7: ["Marisa", "Patchouli", "Nitori", "Hunter Flandre", "Joon"],
    8: ["Yuyuko", "Youmu", "Flandre", "Retro Reimu", "Shion"],
    9: ["Koishi", "Momiji", "Suika", "Retro Marisa", "Tenshi"]
}

# CustomCheckBox class to handle right-click (highlight) behavior
class CustomCheckBox(QCheckBox):
    def __init__(self, label, main_window):
        super().__init__(label)
        self.is_background_filled = False
        self.main_window = main_window  # Store reference to MainWindow

    def contextMenuEvent(self, event):
        # Use the stored reference to MainWindow
        fumo_name = self.text()

        # Get the fumo group mapping
        fumo_groups = self.main_window.fumo_groups

        fumo_group = fumo_groups.get(fumo_name, None)
        if fumo_group is None:
            return  # Fumo not in the group mapping

        # If the fumo is highlighted, unhighlight it and reset it
        if self.is_background_filled:
            self.setStyleSheet("")
            self.is_background_filled = False
            self.main_window.set_checkbox_state(self, 0)
            self.main_window.states[fumo_name] = 0
            self.main_window.preferences[fumo_name] = 0
        else:
            # Unhighlight any other fumos in the same slot group
            for checkbox in self.main_window.checkboxes.values():
                other_fumo_name = checkbox.text()
                other_fumo_group = fumo_groups.get(other_fumo_name, None)

                # Unhighlight if it's in the same slot group
                if checkbox.is_background_filled and other_fumo_group == fumo_group:
                    checkbox.setStyleSheet("")
                    checkbox.is_background_filled = False
                    self.main_window.set_checkbox_state(checkbox, 0)
                    self.main_window.states[checkbox.text()] = 0
                    self.main_window.preferences[checkbox.text()] = 0

            # Highlight the selected fumo
            self.setStyleSheet("background-color: gray")
            self.is_background_filled = True
            self.main_window.set_checkbox_state(self, 3)
            self.main_window.states[fumo_name] = 3
            self.main_window.preferences[fumo_name] = 3

class MainWindow(QMainWindow):
    def check_first_run(self):
        # Check if this is the first run from the configuration
        if self.config.get("first_run", True):  # Default to True if the key doesn't exist
            # Create a detailed first-run message
            message = (
                "Thank you for downloading the Touhou Pack mod! This is your first time "
                "running the Touhou Pack Customizer, so this message will briefly explain how this works!\n\n"
                "There are a few tabs you can check out; the first is the 'Fumos' tab. "
                "Here you can change what Fumos will be randomized to appear in-game! Clicking once will do partial fill "
                "and will ban that Fumo from being randomized. Clicking a second time will guarantee that Fumo will ALWAYS be randomized. "
                "You can also right click a Fumo to ensure that they'll appear no matter what; however only one Fumo within a row may be selected!\n\n"
                "Within the Textures + Text tab you can disable most textures and text in the mod! Beware though, only enabling text edits "
                "tends to have a few loading inconsistencies and may cause some text edits to not appear correctly.\n\n"
                "The Misc. tab has a few additional features as well! (As of Version 1.0.0, none of these except the loading icon are available! Sorry!)\n\n"
                "That's all! Thank you again for downloading the mod and using the customizer program!"
            )

            # Show the message in a message box
            QMessageBox.information(
                self,
                "Welcome to the Touhou Pack Customizer!",
                message
            )

            # Update the configuration to set first_run to False
            self.config["first_run"] = False
            save_config(self.config)


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Touhou Pack Customizer")

        # Set the window icon
        icon_path = resource_path("fumo_icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Initialize attributes
        self.preferences = {}
        self.checkboxes = {}
        self.states = {}
        self.background_states = {}
        self.config = load_config()  # Load configuration

        # Define fumo groups
        self.fumo_groups = {
            "Reimu": 1, "Reisen": 1, "Rumia": 1, "Tewi": 1, "Rin": 1,
            "Alice": 2, "Murasa": 2, "Renko": 2, "Eirin": 2, "Parsee": 2,
            "Remilia": 3, "Satori": 3, "Maribel": 3, "Kaguya": 3, "Kogasa": 3,
            "Sanae": 4, "Aya": 4, "Yukari": 4, "Suwako": 4, "Nue": 4,
            "Cirno": 5, "Sakuya": 5, "Ran": 5, "Kasen": 5, "Sagume": 5,
            "Utsuho": 6, "Seija": 6, "Chen": 6, "Tiny Remilia": 6, "Junko": 6,
            "Marisa": 7, "Patchouli": 7, "Nitori": 7, "Hunter Flandre": 7, "Joon": 7,
            "Yuyuko": 8, "Youmu": 8, "Flandre": 8, "Retro Reimu": 8, "Shion": 8,
            "Koishi": 9, "Momiji": 9, "Suika": 9, "Retro Marisa": 9, "Tenshi": 9
        }

        # Initialize tabs and layouts
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.setup_fumos_tab()
        self.setup_textures_tab()
        self.setup_misc_tab()
        self.setup_credits_tab()

        # Check for first run
        self.check_first_run()


    def setup_fumos_tab(self):
        # Move your existing Fumos code here
        self.preferences = {}
        self.checkboxes = {}
        self.states = {}
        self.background_states = {}

        # Create layout for the Fumos tab
        fumos_layout = QGridLayout()

        # Load preferences and populate the layout
        self.load_preferences(fumos_layout)

        self.button_randomize = QPushButton("Save Preferences and Randomize")
        self.button_randomize.clicked.connect(self.on_button_click)

        self.button_save = QPushButton("Save Preferences")
        self.button_save.clicked.connect(self.on_save_button_click)

        self.button_reset = QPushButton("Reset All")
        self.button_reset.clicked.connect(self.on_reset_button_click)

        fumos_layout.addWidget(self.button_randomize, 10, 0, 1, 2)
        fumos_layout.addWidget(self.button_save, 10, 3, 1, 1)
        fumos_layout.addWidget(self.button_reset, 10, 2, 1, 1)

        # Add Fumos layout to its tab
        fumos_tab = QWidget()
        fumos_tab.setLayout(fumos_layout)
        self.tabs.addTab(fumos_tab, "Fumos")

    def setup_textures_tab(self):
        # Create the "Textures" tab and main layout
        self.textures_tab = QWidget()
        textures_layout = QVBoxLayout()

        # Create a scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(245)  # Limit the scrollable area height

        # Create a widget to hold the checkboxes and its layout
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        # Load configuration
        self.config = load_config()
        self.config.setdefault('textures', {})  # Ensure the 'textures' key exists

        # Define the options and their associated lines in mod.yml
        self.texture_options = {
            "Disable Explosion/Magnet Burst Textures": [(667, 696)],
            "Disable Phantom Form/Valor Form Textures": [(697, 716), (722, 726)],
            "Disable Fairy Form/Wisdom Form Textures": [(114, 128), (314, 318)],
            "Disable Scarlet Form/Limit Form Textures": [(129, 198), (309, 313)],
            "Disable Faith Form/Master Form Textures": [(627, 666), (717, 721)],
            "Disable Resurrection Form/Final Form Textures": [(827, 936)],
            "Disable Sora-Rin/Lion Sora Textures": [(199, 208)],
            "Disable HP, MP, Faith/Drive HUD Textures": [(209, 298), (508, 529)],
            "Disable Puzzle Textures (Includes Puzzle items in field)": [(319, 462), (980, 984)],
            "Disable Prize Drops Textures": [(99, 113)],
            "Disable Final Xemnas Arena Textures": [(937, 984)],
            "Disable Drive/High-Drive Recovery Item Textures": [(299, 308)],
            "Disable Room Fadeout Texture": [(727, 821)],
            "Disable Save Image Textures": [(617, 621)],
            "Disable Spell Text (Includes Elements)": [(20, 33)],
            "Disable Puzzle Piece Text": [(62, 89)],
            "Disable Form and Ability Text": [(6, 19)],
            "Disable Fumo Text": [(48, 61)],
            "Disable Etc. Text Changes & Font": [(34, 47), (822, 826)],
        }

        # Add checkboxes to the scrollable layout
        self.texture_checkboxes = {}
        for label, line_range in self.texture_options.items():
            config_key = label if label != "Disable Puzzle Textures (Includes Puzzle items in field)" else "Disable Puzzle Textures"
            checkbox = QCheckBox(label)
            checkbox.setChecked(self.config['textures'].get(config_key, 0) == 1)
            self.texture_checkboxes[label] = checkbox
            scroll_layout.addWidget(checkbox)

        # Apply the scrollable layout to the scroll content widget
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Add the scrollable area to the main layout
        textures_layout.addWidget(scroll_area)

        # Add the "Apply Changes" button below the scroll area
        apply_button = QPushButton("Apply Changes")
        apply_button.clicked.connect(self.apply_texture_changes)
        textures_layout.addWidget(apply_button)

        # Apply the main layout to the tab
        self.textures_tab.setLayout(textures_layout)
        self.tabs.addTab(self.textures_tab, "Textures + Text")

    def apply_texture_changes(self):
        # Path to the mod.yml file
        mod_file_path = resource_path("mod.yml")

        try:
            # Read the file contents
            with open(mod_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Modify lines based on checkbox states
            for label, line_ranges in self.texture_options.items():
                # Skip options without defined line ranges
                if line_ranges is None:
                    continue

                config_key = label if label != "Disable Puzzle Textures (Includes Puzzle items in field)" else "Disable Puzzle Textures"
                checkbox = self.texture_checkboxes[label]

                # Process each line range for the current option
                for start_line, end_line in line_ranges:
                    if checkbox.isChecked():
                        # Comment out lines (add # at the start if not already commented)
                        for i in range(start_line - 1, end_line):  # Adjust for 0-based index
                            if not lines[i].strip().startswith("#"):
                                lines[i] = f"#{lines[i]}"
                        self.config['textures'][config_key] = 1  # Update config
                    else:
                        # Uncomment lines (remove # at the start if present)
                        for i in range(start_line - 1, end_line):
                            if lines[i].strip().startswith("#"):
                                lines[i] = lines[i][1:]
                        self.config['textures'][config_key] = 0  # Update config

            # Write the modified content back to the file
            with open(mod_file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)

            # Save updated configuration
            save_config(self.config)
            self.show_success_message("Settings have been successfully saved!")
        except Exception as e:
            self.show_error_message(f"An error occurred while updating mod.yml: {str(e)}")
    
    def setup_misc_tab(self):
        self.misc_tab = QWidget()
        misc_layout = QGridLayout()  # Use GridLayout for better control

        # Load configuration
        self.config = load_config()
        self.config.setdefault('misc', {})  # Ensure the 'misc' section exists

        # Create a checkbox for "Enable Alternate Forms"
        self.enable_alternate_forms_checkbox = QCheckBox("Enable Alternate Forms")
        self.enable_alternate_forms_checkbox.setChecked(self.config['misc'].get("Enable Alternate Forms", 0) == 1)
        self.enable_alternate_forms_checkbox.setEnabled(False)  # This disables the checkbox (grays it out)
        self.enable_alternate_forms_checkbox.setToolTip("Enables alternate form textures and text. (Feature under development)")
        misc_layout.addWidget(self.enable_alternate_forms_checkbox, 0, 0, 1, 2)  # Row 0, spanning 2 columns

        # **Create a disabled checkbox for "Enable Reimu Mod Compatibility"**
        self.enable_reimu_mod_checkbox = QCheckBox("Enable Reimu Mod Compatibility")
        self.enable_reimu_mod_checkbox.setChecked(self.config['misc'].get("Enable Reimu Mod", 0) == 1)
        self.enable_reimu_mod_checkbox.setEnabled(False)  # This disables the checkbox (grays it out)
        self.enable_reimu_mod_checkbox.setToolTip("Enables compatibility for the Reimu Model Mod, allowing her to take on the various forms!\nThis is a 'joke' feature, there's a massive chance this will never happen.")
        misc_layout.addWidget(self.enable_reimu_mod_checkbox, 1, 0, 1, 2)  # Row 1, spanning 2 columns

        # **Create a disabled checkbox for "Enable Reimu Mod Compatibility"**
        self.enable_gohei_checkbox = QCheckBox("Enable Gohei (Replaces Kingdom Key)")
        self.enable_gohei_checkbox.setChecked(self.config['misc'].get("Enable Gohei", 0) == 1)
        self.enable_gohei_checkbox.setEnabled(False)  # This disables the checkbox (grays it out)
        self.enable_gohei_checkbox.setToolTip("When enabled, this will have Reimu's Gohei replace the Kingdom Key!\nThis is currently a 'joke' feature. There's some development on it, but currently it does not work!\nIE: It causes the game to crash... A LOT!")
        misc_layout.addWidget(self.enable_gohei_checkbox, 2, 0, 1, 2)  # Row 2, spanning 2 columns

        # **Create a disabled checkbox for "Enable Reimu Mod Compatibility"**
        self.enable_soundpack_checkbox = QCheckBox("Enable Touhou Soundpack")
        self.enable_soundpack_checkbox.setChecked(self.config['misc'].get("Enable Touhou Soundpack", 0) == 1)
        self.enable_soundpack_checkbox.setEnabled(False)  # This disables the checkbox (grays it out)
        self.enable_soundpack_checkbox.setToolTip("When enabled, various sound effects will be replaced, such as\nsystem sounds (selections, cancels, etc.), certain attacks and other things!\n\nCurrently in development! Will eventually have new sounds compared to\nthe OG soundpack, which will be obsolete afterwards!")
        misc_layout.addWidget(self.enable_soundpack_checkbox, 3, 0, 1, 2)  # Row 3, spanning 2 columns

        # Create a drop-down menu (QComboBox) for selecting a Loading Icon
        self.loading_icon_label = QLabel("Select Loading Icon:")
        self.loading_icon_dropdown = QComboBox()

        # Define available options (Update names later if needed)
        self.loading_icon_dropdown.setToolTip("You can change the loading icon that appears in place of the spinning heart icon.")
        self.loading_icons = [
            "Reimu", 
            "Sanae", 
            "Murasa", 
            "Dormey", 
            "Suwako",
            "KH2 (Default)",
            "Random"
        ]
        self.loading_icon_dropdown.addItems(self.loading_icons)

        # Load saved selection from config.yaml
        saved_icon = self.config['misc'].get("Loading Icon", "Default")
        if saved_icon in self.loading_icons:
            self.loading_icon_dropdown.setCurrentText(saved_icon)

        # Place label and dropdown side by side
        misc_layout.addWidget(self.loading_icon_label, 4, 0)  # Row 3, Column 0
        misc_layout.addWidget(self.loading_icon_dropdown, 4, 1)  # Row 3, Column 1

        # Create a "Confirm Changes" button
        self.apply_misc_button = QPushButton("Apply Changes")
        self.apply_misc_button.clicked.connect(self.apply_misc_changes)
        misc_layout.addWidget(self.apply_misc_button, 5, 0, 1, 2)  # Row 4, spanning 2 columns

        # Apply the layout to the Misc tab
        self.misc_tab.setLayout(misc_layout)
        self.tabs.addTab(self.misc_tab, "Misc.")
    
    def save_misc_settings(self):
        self.config['misc']["Enable Alternate Forms"] = 1 if self.enable_alternate_forms_checkbox.isChecked() else 0
        self.config['misc']["Loading Icon"] = self.loading_icon_dropdown.currentText()
        save_config(self.config)

    def apply_misc_changes(self):
        # Save the selected settings
        self.config['misc']["Enable Alternate Forms"] = 1 if self.enable_alternate_forms_checkbox.isChecked() else 0
        self.config['misc']["Enable Reimu Mod"] = 1 if self.enable_reimu_mod_checkbox.isChecked() else 0
        self.config['misc']["Enable Gohei"] = 1 if self.enable_gohei_checkbox.isChecked() else 0
        self.config['misc']["Enable Touhou Soundpack"] = 1 if self.enable_soundpack_checkbox.isChecked() else 0
        selected_icon = self.loading_icon_dropdown.currentText()

        # If "Random" is selected, pick a random icon from the list (excluding "Random")
        if selected_icon == "Random":
            available_icons = [icon for icon in self.loading_icons if icon != "Random"]
            selected_icon = random.choice(available_icons)

        # Save the chosen icon to config.yaml
        self.config['misc']["Loading Icon"] = selected_icon
        save_config(self.config)

        # Modify mod.yml
        mod_file_path = resource_path("mod.yml")

        try:
            with open(mod_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Modify line 532 to change the loading icon
            line_index = 531  # Line 532 in a 0-based index
            if line_index < len(lines):
                lines[line_index] = f'  - name: Loading Icons/{selected_icon}.dds\n'

            with open(mod_file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)

            self.show_success_message(f"Changes have been successfully applied!")
        except Exception as e:
            self.show_error_message(f"An error occurred while updating mod.yml: {str(e)}")

    def setup_credits_tab(self):
        self.credits_tab = QWidget()

        # Create a centered container
        credits_container = QWidget()
        credits_layout = QVBoxLayout()
        credits_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("<h3>Touhou Pack + Customizer - Credits</h3>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Contributors
        contributors_label = QLabel(
            "<b>Mod Creator:</b> BladeofRagna/Ragna/ragna58<br>"
            "<b>Puzzle Art:</b><br>"
            "'Fairy' by Bero @beruwk0<br>"
            "'Youkai' by harapan-kun<br>"
            "'Sisters' by moosu @moosu193<br>"
            "'Teamwork' by Tiv @tiv_<br>"
            "'Abilities' by zounose<br>"
            "'Lunatic' by parasite oyatsu<br>"
            "<b>Special Thanks:</b><br>"
            "roromaniac8 for pushing me on for this project! (Thanks a ton man!)<br>"
            "Python branch of ChatGPT for making this even remotely possible!<br>"
            "And 'The Crew' for supporting me and this mod!<br>"
        )
        contributors_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Version
        mod_version_label = QLabel("<i>Mod Version: <b>3.0.0</b></i>")
        version_label = QLabel("<i>Customizer Version <b>1.0.0</b></i>")
        mod_version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        changelog_label = QLabel('<a href="https://github.com/BladeofRagna/Touhou-Pack/blob/main/mod.yml">Changelog</a>')
        changelog_label.setOpenExternalLinks(True)  # ✅ Opens the link in the user's default browser
        changelog_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set fixed width for better alignment
        title_label.setMaximumWidth(400)
        contributors_label.setMaximumWidth(400)
        mod_version_label.setMaximumWidth(400)
        version_label.setMaximumWidth(400)

        # Add labels to layout
        credits_layout.addWidget(title_label)
        credits_layout.addWidget(contributors_label)
        credits_layout.addWidget(mod_version_label)
        credits_layout.addWidget(version_label)
        credits_layout.addWidget(changelog_label)

        # Apply layout to the container
        credits_container.setLayout(credits_layout)

        # Create a main layout to center the content
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(credits_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(1)

        # Apply layout to the tab
        self.credits_tab.setLayout(main_layout)
        self.tabs.addTab(self.credits_tab, "Credits")

    def on_save_button_click(self):
        try:
            # Save preferences to the preferences file
            preferences_file = resource_path("fumo_preferences.json")
            with open(preferences_file, 'w') as file:
                json.dump(self.preferences, file, indent=4)
            print(f"Preferences saved to {preferences_file}")
            self.show_success_message("Preferences saved successfully!")
        except Exception as e:
            self.show_error_message(f"An error occurred while saving preferences: {str(e)}")

    def load_preferences(self, layout):
        preferences_file = resource_path("fumo_preferences.json")
        try:
            with open(preferences_file, 'r') as file:
                self.preferences = json.load(file)

            row, col = 0, 0
            for index, (fumo_name, pref_value) in enumerate(self.preferences.items()):
                # Pass the MainWindow reference to CustomCheckBox
                checkbox = CustomCheckBox(fumo_name, self)
                checkbox.setTristate(True)
                checkbox.stateChanged.connect(self.on_checkbox_state_change)

                self.set_checkbox_state(checkbox, pref_value)
                self.states[fumo_name] = pref_value
                self.background_states[fumo_name] = False

                self.checkboxes[fumo_name] = checkbox
                layout.addWidget(checkbox, row, col)

                row += 1
                if row == 9:  # Start a new column every 9 rows
                    row = 0
                    col += 1

        except FileNotFoundError:
            self.show_error_message(f"Preferences file not found: {preferences_file}")

    def set_checkbox_state(self, checkbox, state):
        if state == 0:
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            checkbox.setStyleSheet("")
        elif state == 1:
            checkbox.setCheckState(Qt.CheckState.Checked)
        elif state == 2:
            checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
        elif state == 3:
            checkbox.setCheckState(Qt.CheckState.Checked)
            checkbox.setStyleSheet("background-color: gray")

    def on_checkbox_state_change(self, state):
        checkbox = self.sender()
        fumo_name = checkbox.text()

        if not checkbox.is_background_filled:
            if checkbox.checkState() == Qt.CheckState.Unchecked:
                new_state = 0
            elif checkbox.checkState() == Qt.CheckState.Checked:
                new_state = 1
            elif checkbox.checkState() == Qt.CheckState.PartiallyChecked:
                new_state = 2

            self.states[fumo_name] = new_state
            self.preferences[fumo_name] = new_state

    def validate_preferences(self, preferences):
        guaranteed_count = sum(1 for pref in preferences.values() if pref == 1)
        highlighted_count = sum(1 for pref in preferences.values() if pref == 3)
        excluded_count = sum(1 for pref in preferences.values() if pref == 2)

        total_used_fumos = guaranteed_count + highlighted_count

        if total_used_fumos > 9:
            raise ValueError(f"A maximum of 9 fumos can be used!\nPlease ensure that a total of 9 fumos are being used!\nThe total number includes guaranteed and highlighted fumos!")
        if excluded_count > 36:
            raise ValueError("A minimum of 9 fumos are needed! Please allow for more fumos to be used!")

    def on_button_click(self):
        try:
            # Validate preferences before randomization
            self.validate_preferences(self.preferences)

            preferences_file = resource_path("fumo_preferences.json")
            with open(preferences_file, 'w') as file:
                json.dump(self.preferences, file, indent=4)
            print(f"Preferences saved to {preferences_file}")

            fumo_reference_file = resource_path("fumo_reference.yml")
            fumos_file_path = resource_path("msg/fumo's.yml")
            mod_file_path = resource_path("mod.yml")
            fumo_line_numbers = [568, 574, 580, 586, 592, 598, 604, 610, 616]

            self.shuffle_fumos(fumo_reference_file, fumos_file_path, self.preferences, mod_file_path, fumo_line_numbers)

            self.show_success_message("Your fumo's have been randomized and preferences saved! Enjoy!")

        except Exception as e:
            self.show_error_message(f"An error occurred: {str(e)}")

    def shuffle_fumos(self, fumo_reference_file, fumos_file_path, preferences, mod_file_path, fumo_line_numbers):
        fumo_reference = load_yaml(fumo_reference_file)

        fumo_details = {}
        for fumo in fumo_reference:
            plain_name = fumo['name'].split('}')[1].split(' Fumo')[0].strip()
            fumo_details[plain_name] = fumo

        final_fumos = [None] * 9

        # Step 1: Place the right-clicked (default) fumos first
        for fumo_name, pref in preferences.items():
            fumo_group = fumo_groups.get(fumo_name, None)
            if fumo_group and fumo_name in fumo_details and pref == 3:
                final_fumos[fumo_group - 1] = fumo_details[fumo_name]

        # Step 2: Gather guaranteed fumos and shuffle them into random positions
        guaranteed_fumos = [fumo_details[fumo_name] for fumo_name, pref in preferences.items() if pref == 1 and fumo_name in fumo_details]
        random.shuffle(guaranteed_fumos)  # Shuffle guaranteed fumos

        available_slots = [i for i, fumo in enumerate(final_fumos) if fumo is None]
        random.shuffle(available_slots)  # Shuffle available slots to place guaranteed fumos

        for fumo in guaranteed_fumos:
            if available_slots:
                slot = available_slots.pop(0)  # Take a random slot
                final_fumos[slot] = fumo

        # Step 3: Randomly fill remaining slots with available fumos
        available_fumos = [fumo_details[fumo_name] for fumo_name, pref in preferences.items() if pref == 0 and fumo_name in fumo_details]
        remaining_slots = final_fumos.count(None)
        if remaining_slots > len(available_fumos):
            raise ValueError("Not enough available fumos for randomization.")
        
        selected_fumos = random.sample(available_fumos, remaining_slots)
        randomized_index = 0
        for i in range(9):
            if final_fumos[i] is None:
                final_fumos[i] = selected_fumos[randomized_index]
                randomized_index += 1

        # Ensure the final list has 9 fumos
        if len(final_fumos) != 9 or None in final_fumos:
            raise ValueError(f"Final Fumos list has missing elements or None values: {final_fumos}")

        # Define IDs and assign to each fumo
        fumo_ids = [
            "0x3B0B", "0x3B0C", "0x3B0D", "0x3B0E", "0x4C55", "0x4C56",
            "0x3B15", "0x3B16", "0x3B1B", "0x3B1C", "0x3B1D", "0x3B1E",
            "0x3B1F", "0x3B20", "0x3B21", "0x3B22", "0x3B11", "0x3B12"
        ]

        new_fumos_content = []
        for i in range(9):
            if final_fumos[i] is None:
                raise ValueError(f"Fumo at index {i} is None and was not assigned properly.")
            name_id = fumo_ids[i * 2]
            description_id = fumo_ids[i * 2 + 1]
            name_entry = final_fumos[i]['name']
            description_entry = final_fumos[i]['description']
            new_fumos_content.append({'id': name_id, 'en': name_entry})
            new_fumos_content.append({'id': description_id, 'en': description_entry})

        save_fumos_yaml(new_fumos_content, fumos_file_path)

        # Update mod.yml with the randomized fumo names
        fumo_clean_names = [extract_plain_name(fumo) for fumo in final_fumos]
        update_mod_yml(mod_file_path, fumo_clean_names, fumo_line_numbers)

    def on_reset_button_click(self):
        for fumo_name, checkbox in self.checkboxes.items():
            self.set_checkbox_state(checkbox, 0)
            self.preferences[fumo_name] = 0
            self.states[fumo_name] = 0
        print("All selections reset to default.")

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def show_success_message(self, message):
        # Play custom sound effect
        sound_path = resource_path("assets/success.wav")  # Path to your custom sound
        if os.path.exists(sound_path):  # Ensure file exists before playing
            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(sound_path))
            sound.setVolume(0.3)  # Max volume (adjust if needed)
            sound.play()

        # Show the message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.NoIcon)
        msg_box.setWindowTitle("Fumo Fumo!")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

# Main application loop
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
