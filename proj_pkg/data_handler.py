from pymatgen.core.composition import Composition
import pandas as pd
import re

def convert_percentage(match):
    number = float(match.group(1))
    return str(number / 100)

def split_chemicals(formula):
    if '+' in formula or '-' in formula:
        # Split based on + or -. Note that + or - are just separators, not operators
        chemicals = re.split(r'\s*[\+\-]\s*', formula)
    else:
        # Return the whole formula as one piece
        chemicals = [formula]
    return chemicals

def process_formula_to_composition(formula):
    component_dict = {}

    # Split based on + or - first. Note - is a hyphen sign, not minus
    chemicals = split_chemicals(formula)

    for chem in chemicals:
        # Check if wt% is in the item
        if 'wt%' in chem:
            # Extract wt% value and the formula
            wt_match = re.search(r'(\d*\.?\d+)\s*wt%', chem)
            formula_match = re.search(r'[A-Z][a-z]?\d*\.?\d*(\([\w\d]+\))?[A-Za-z\d]*', chem)

            if wt_match and formula_match:
                wt_percent = float(wt_match.group(1))

                # Extract the chemical formula
                formula_str = formula_match.group(0)
                comp = Composition(formula_str)
                molar_mass = comp.weight
                mol_fraction = wt_percent / molar_mass

                for element, amount in comp.as_dict().items():
                    component_dict[element] = component_dict.get(element, 0) + amount * mol_fraction 
        else:
            # take this whole part as 100g or 100wt% of compound 
            wt_percent =  100

            comp = Composition(chem)
            molar_mass = comp.weight

            mol_fraction = wt_percent / molar_mass

            for element, amount in comp.as_dict().items():
                component_dict[element] = component_dict.get(element, 0) + amount * mol_fraction
    
    
    final_comp = Composition(component_dict)

    return final_comp


def convert_to_composition(formula: pd.Series, formula_type: pd.Series, output_name: str = "pymatgen Composition") -> pd.Series:
    """
    Converts a given series of chemical formulas into pymatgen Composition objects based on their type.

    Parameters:
    - formula (pd.Series): Series containing the chemical formulas.
    - formula_type (pd.Series): Series indicating whether the formula is "Stoichiometric Formula", "Mass Formula", or "Mixed Formula".
    - output_name (str): Name of the output series. Default is "pymatgen Composition".

    Returns:
    - pd.Series: A new series with pymatgen Composition objects.
    """
    # Check if both series are of the same size
    if len(formula) != len(formula_type):
        raise ValueError("The input series must be of the same length.")

    # Initialize an empty list to store the results
    compositions = []
    iter = 0
    # Iterate through each formula and type
    for formula, ftype in zip(formula, formula_type):
        try:
            if ftype == "Stoichiometric Formula":
                # Direct conversion for stoichiometric formulas
                try:
                    # converts the percentage to a fraction, if any
                    formula = re.sub(r'(\d+\.?\d*)%', convert_percentage, formula)

                    comp = Composition(formula)
                    compositions.append(comp)
                except Exception as e:
                    compositions.append(None)
                    print(f"Error converting stoichiometric formula '{formula}', entry {iter} to Composition: {e}")

            elif ftype == "Mixed Formula":
                if 'wt%' in formula:
                    try:
                        comp = process_formula_to_composition(formula)
                        compositions.append(comp)
                    except Exception as e:
                        compositions.append(None)
                        print(f"Error converting mixed formula '{formula}', entry {iter} to Composition: {e}")

                else: 
                    raise ValueError("The formula is not in the expected format for mixed formula. It should contain wt%")

            else:
                raise ValueError(f"Formula type '{ftype}' is not recognized.")
            
        except ValueError as ve:
            # Log the error and append None to keep the series length consistent
            compositions.append(None)
            print(f"ValueError encountered at entry {iter}: {ve}")
        iter += 1

    # Convert the list to a pandas series with the desired output name
    return pd.Series(compositions, name=output_name)


def check_threshold(threshold):
    # Ensure the threshold is valid (either percentage or fraction)
    if isinstance(threshold, str) and threshold.endswith('%'):
        # Convert percentage string to a fraction
        updated_threshold = float(threshold.strip('%')) / 100
    elif isinstance(threshold, (int, float)) and 0 < threshold <= 1:
        # Accept fractions as is
        updated_threshold = threshold
    else:
        raise ValueError("Threshold must be a percentage string (e.g., '5%') or a fraction (e.g., 0.05)")
    
    return updated_threshold


# Function to classify dopant and host
def classify_host_dopant(composition, threshold):

    # Check and update the threshold
    threshold = check_threshold(threshold)

    # Get the total amount of all elements in the composition
    total_amount = sum(composition.get_el_amt_dict().values())

    dopants = []
    hosts = []

    # Classify each element
    for element, amount in composition.get_el_amt_dict().items():
        fraction = amount / total_amount
        element_amt = f"{element}{amount}"

        if fraction <= threshold:
            dopants.append(element_amt)
        else:
            hosts.append(element_amt)

    # Ensure there is at least one host
    if not hosts:
        raise ValueError("No host element found in the composition. The threshold may be too high.")

    # Return None for dopants if empty
    return hosts, dopants if dopants else None

# Function to apply classify_dopant_host to a series of compositions
def classify_host_dopant_bulk(composition_series, threshold):
    threshold = check_threshold(threshold)

    host_percent = (1 - threshold) * 100
    dopant_percent = threshold * 100

    # Lists to store results
    hosts_list = []
    dopants_list = []

    # Apply the classify_dopant_host function to each composition in the series
    for comp in composition_series:
        hosts, dopants = classify_host_dopant(comp, threshold)
        hosts_list.append(', '.join(hosts))  # Convert to string for the DataFrame
        dopants_list.append(', '.join(dopants) if dopants else None)

    # Create a DataFrame with Hosts and Dopants columns
    result_df = pd.DataFrame({
        f'Host({host_percent}%)': hosts_list,
        f'Dopant({dopant_percent}%)': dopants_list
    })

    return result_df


