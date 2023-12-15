import yaml
import random
import sys
import os
import json

print("Fumo's are being randomized... Please wait warmly!")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Get the directory of the current script file
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_directory = current_dir

def load_yaml(file_name):
    file_path = os.path.join(yaml_directory, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


def save_fumos_yaml(data, file_path):
    with open(file_path, 'w') as file:
        for entry in data:
            file.write(f"- id: {entry['id']}\n")
            if entry['en'].startswith('{:color'):
                file.write(f"  en: '{entry['en']}'\n")
            else:
                # Ensure proper YAML multi-line string formatting
                formatted_description = entry['en'].replace('\n', '\n    ')
                file.write(f"  en: >-\n    {formatted_description}\n")

def load_preferences(file_name):
    file_path = os.path.join(yaml_directory, file_name)
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_preferences(preferences):
    guaranteed_count = sum(1 for key, value in preferences.items() if value == 1)
    available_count = sum(1 for key, value in preferences.items() if value != 2)

    if guaranteed_count > 9:
        print("Too many guaranteed fumos! Please reduce the number of guaranteed fumos in fumo_preferences.json.")
    if available_count < 9:
        print("Not enough fumos available for randomization. Please adjust your preferences in fumo_preferences.json.")

def extract_plain_name(fumo_entry):
    # Extract the plain name from the fumo entry
    try:
        # Extract the name part after the color tag
        name_with_tag = fumo_entry['name']
        return name_with_tag.split('}')[-1].strip()
    except IndexError:
        return fumo_entry['name']  # Fallback to the full name if splitting fails


def shuffle_fumos(fumo_reference_file, fumos_file_path, preferences):
    # Load the Fumo reference data
    fumo_reference = load_yaml(fumo_reference_file)

    # Create a dictionary for quick lookup of fumo details by plain name
    fumo_details = {}
    for fumo in fumo_reference:
        plain_name = fumo['name'].split('}')[1].split(' Fumo')[0].strip()
        fumo_details[plain_name] = fumo

    # Initialize the final Fumos list with None
    final_fumos = [None] * 9

    # Process preferences and categorize Fumos
    for index, (fumo_name, pref) in enumerate(preferences.items()):
        if fumo_name in fumo_details:
            if pref == 3:
                final_fumos[index] = fumo_details[fumo_name]

    # List for guaranteed and available Fumos
    guaranteed_fumos = [fumo_details[name] for name, pref in preferences.items() if pref == 1 and name in fumo_details]
    available_fumos = [fumo_details[name] for name, pref in preferences.items() if pref == 0 and name in fumo_details]

    # Remove guaranteed fumos from available fumos to avoid duplicates
    available_fumos = [fumo for fumo in available_fumos if fumo not in guaranteed_fumos]

    # Randomly select Fumos to fill up remaining slots
    remaining_slots = final_fumos.count(None) - len(guaranteed_fumos)
    selected_fumos = random.sample(available_fumos, min(len(available_fumos), remaining_slots))

    # Merge guaranteed and selected Fumos
    randomized_fumos = guaranteed_fumos + selected_fumos

    # Shuffle the combined list to randomize guaranteed Fumos
    random.shuffle(randomized_fumos)

    # Fill the None slots in final_fumos with randomized Fumos
    randomized_index = 0
    for i in range(9):
        if final_fumos[i] is None:
            final_fumos[i] = randomized_fumos[randomized_index]
            randomized_index += 1

    # Ensure that the final list has exactly 9 Fumos
    if len(final_fumos) != 9:
        raise ValueError(f"Final Fumos list does not have 9 elements. It has {len(final_fumos)} elements.")

    # Explicitly define the IDs for each Fumo
    fumo_ids = [
        "0x3B0B", "0x3B0C", "0x3B0D", "0x3B0E", "0x4C55", "0x4C56",
        "0x3B15", "0x3B16", "0x3B1B", "0x3B1C", "0x3B1D", "0x3B1E",
        "0x3B1F", "0x3B20", "0x3B21", "0x3B22", "0x3B11", "0x3B12"
    ]

    # Pair each ID with a unique name and description
    new_fumos_content = []
    for i in range(9):
        name_id = fumo_ids[i * 2]
        description_id = fumo_ids[i * 2 + 1]
        name_entry = final_fumos[i]['name']
        description_entry = final_fumos[i]['description']
        new_fumos_content.append({'id': name_id, 'en': name_entry})
        new_fumos_content.append({'id': description_id, 'en': description_entry})

    # Save the new fumo's.yml
    save_fumos_yaml(new_fumos_content, fumos_file_path)


current_dir = os.path.dirname(os.path.abspath(__file__))
fumo_reference_file = os.path.join(current_dir, "fumo_reference.yml")
fumos_file_path = os.path.join(current_dir, "msg", "fumo's.yml")
mod_file_path = resource_path("mod.yml")

def extract_plain_name(fumo_entry):
    # Extract the plain name from the fumo entry
    try:
        # Extract the name part after the color tag
        name_with_tag = fumo_entry['name']
        return name_with_tag.split('}')[-1].strip()
    except IndexError:
        return fumo_entry['name']  # Fallback to the full name if splitting fails

def shuffle_mod(fumos_file_path, mod_file_path, fumo_line_numbers):
    # Load the shuffled fumo's.yml
    shuffled_fumos_data = load_yaml(fumos_file_path)

    # Extract the shuffled character names from fumo's.yml
    shuffled_character_names = [entry['en'].split('}')[1].split(' Fumo')[0].strip() for entry in shuffled_fumos_data if 'Fumo' in entry['en']]

    # Load the original mod.yml content
    with open(mod_file_path, 'r', encoding="utf-8") as file:
        content = file.readlines()

    # Update the specific lines in mod.yml with the new character-based names
    for i, line_num in enumerate(fumo_line_numbers):
        if i < len(shuffled_character_names):
            new_character_name = shuffled_character_names[i]
            content[line_num] = f"  - name: remastered/Fumo's/{new_character_name}.dds\n"
        else:
            break  # Break the loop if there are no more character names to assign

    # Save the updated content back to the output file
    with open(mod_file_path, 'w', encoding="utf-8") as file:
        file.writelines(content)

def main():
    try:
        # Determine the directory where the executable is located
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        # Set the paths for fumo_reference.yml, fumo's.yml, mod.yml, and preferences JSON
        fumo_reference_file = os.path.join(application_path, "fumo_reference.yml")
        fumos_file_path = os.path.join(application_path, "msg", "fumo's.yml")
        mod_file_path = os.path.join(application_path, "mod.yml")
        preferences_file = os.path.join(application_path, "fumo_preferences.json")

       # Load preferences from JSON file
        with open(preferences_file, 'r') as file:
            preferences = json.load(file)

        # Debugging: Print loaded preferences
        print("Loaded preferences:", preferences)

        # Validate preferences
        validate_preferences(preferences)
        if sum(value == 1 for value in preferences.values()) > 9:
            raise ValueError("Too many guaranteed fumos! Please reduce the amount of guaranteed fumos in fumo_preferences.json!")

        # Define the line numbers where the Fumo entries are located in mod.yml
        fumo_line_numbers = [539, 545, 551, 557, 563, 569, 575, 581, 587]

        # Call the shuffle functions with preferences
        shuffle_fumos(fumo_reference_file, fumos_file_path, preferences)
        shuffle_mod(fumos_file_path, mod_file_path, fumo_line_numbers)

        # ASCII Art
        print(r"""
                /@@&%###%%%%%###&&@&,                           ,%@&&###%%%%%%##%&@@(               
               %%%%%%%%%%%%%%%%%%%%%%%%%#&&.             .&@%%%%%%%%%%%%%%%%%%%%%%%%%%              
               &%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#&&     &@#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&              
               @%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#&              
               /#%%%%%%%%%%%%%%%%%%#%%%#%@#*. ...........,#@&#%%%%%%%%%%%%%%%%%%%%%%#/              
                @#%%%%%%%%%%%%%%%%@,. ........................ ...@%%%%%%%%%%%%%%%##@               
                 %%#%%%%%%%#%&(.................................... ../&#%%%%%%%%%#&                
                  ,&%%%%%%&...............................................&#%%%%%&*                 
                  ,%%%%%&...................................................&#%%%%*                 
                  &##&@.......................................................@&##&                 
                 @%##,..................&(............... &&.................. ,%#%@.               
             &&#%%%%....,........... .%  &...............(   @...........&.......%%%%#&&            
         /&##%%%%%#.......... ......%     (............../     (..........@.......%%%%%%##@(        
      @%%#%%%%%%%%(... % ..... .. ##@%*   *.............@     *%@%* ... ...&....../#%%%%%%%##%&.    
   @&##%%%%%%%%%%&....%..........%         #............,        (..........,......&%%%%%%%%%%##%@  
       %@%%%%%%%%%....&........./           (. ........@          ( ........@......##%%%%%%#@&      
           &%%%%#,... (........ @.*(#%%&&&&&&((....... %&@&&&&%%#((/# . ....%......,##%%%@          
              @## ....%........###%(((((((((&  % .....& &  #((((/((((.......%.......##&             
                @ ....@........@&(((((((((((@    //...& @(((((((((/(%.......&...... @               
                @ .... (.......@*//((((((((#.       .&   %((((((/((/(/.....,(...... @               
                @ ....@./......&  &((((((/@               @/((((((%. &.... #..(.... @               
                & .../.. @ ....@                                     &...,*....&  . &               
                &..&.......@...&                                     #. @.......*@..%               
                /&@..........*% ,%           %.       ,,           @,.&........../%&#               
                 @ ....... ......../&                           @,.........  .....*%                
                &.......&*@.....&.......%@*               (@#...  .#*.... &%&. .....@               
               @@@@@%.     &(...&  %#...@(@&/%   .&    @(@@*&. .&( .*. .&(     *&@@@@@              
                              &@&.    &      %#(@((#%@#@      (    #&&#                             
                           (@@@#,.,&%(# /   &#@((&(%((&%&   &*/(%&( ,#&@@&                          
                         &,          .& #(  @(((@&%@&((%@  &*,(.           @.                       
                       @            .#&@#  &%@(&&#%%@%(%%@  &@#@             @                      
                         &/       .&    %#%%((((%%%#@(((##%%,.   @      . ,@                        
                           /&@&#%*    .%%&&#(((&#%%%##(((#&%%@     #%%@@&%                          
                         &%#%%*     .%#%%%%%%#%##%%%%%&#%%%%%%#@      %#%#&@                        
                      &#%%%%#&    &#%%%%%%%%%#%%%%%%%%%%%%%%%%%%#%#    %%%%%#%@                     
                 ,&@*          %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#@          #@#.                
                 (@.  .@       (#%%%%%%%%&,&%%%%%%%%%%%%%&.@%%%%%%%%%       .@   /@,                
                     @%  .&     @%#%@.       &#%%%%%%%%%       ,@#%#%    ,&   @&                    
                        ,@@#,  ./%#. .(@( %,    &###@    (( &@*...&#*.  ,%@&.                       
                               @ %....&*.@(/ &(   .   %% &,&.%(  .,(/%                              
                              (*.......  /& *@&*     (@&. &..........&                              
                               @........,&                 @........ @                              
                                .@&*.*@&                     @&,./&@
    """)

        print("Fumo randomization complete! Press any key to exit...")
        input()

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()