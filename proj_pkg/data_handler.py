from pymatgen.core.composition import Composition
import pandas as pd
import re

def convert_percentage(match):
    number = float(match.group(1))
    return str(number / 100)

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
        if ftype == "Stoichiometric Formula":
            # Direct conversion for stoichiometric formulas
            try:
                # converts the percentage to a fraction, if any
                formula = re.sub(r'(\d+\.?\d*)%', convert_percentage, formula)

                comp = Composition(formula)
                compositions.append(comp)
            except Exception as e:
                compositions.append(None)
                print(f"Error converting '{formula}', entry {iter} to Composition: {e}")

        elif ftype == "Mixed Formula":
            try:
                # Extract components and their stoichiometric or mass ratios
                pattern = re.findall(r'(\(?[A-Za-z0-9\.\(\)]+(?:\d*\.\d+|\d+)?\)?)([0-9\.]*\s*wt%?)?', formula)

                component_dict = {}
                total_moles = 0


                if 'wt%' in pattern:
                    wt_percent = True # Set flag for wt% handling and denotes that other ratio are mole fractions
                else:
                    wt_percent = False # Set flag for handling ratio as mass fractions


                for compound, ratio in pattern:
                    # Clean and convert compound
                    compound = compound.replace("(", "").replace(")", "").strip()


                    if wt_percent:
                        # Handle wt% ratios distinctly
                        # e.g. 0.9Cu2Se-0.1(Bi0.88Pb0.06Ca0.06CuSeO)-0.02 wt% C the 0.02 is wt% but 0.9 and 0.1 are mole fractions
                        if 'wt%' in ratio:
                            # Convert wt% to a fraction of total mass
                            
                            ratio = float(ratio.replace("wt%", "").strip()) / 100.0
                            # Convert to pymatgen Composition to calculate molar mass
                            comp = Composition(compound)
                            molar_mass = comp.weight
                            # Calculate moles based on mass ratio and molar mass
                            moles = ratio / molar_mass
                            # Add moles of the additive without altering primary components
                            for element, amount in comp.as_dict().items():
                                component_dict[element] = component_dict.get(element, 0) + amount * moles 
                        else:
                            # Treat stoichiometric ratio directly as a mole fraction
                            ratio = float(ratio.strip()) if ratio.strip() else 1.0 # Handle empty ratios as 1.0 or 100%
                            comp = Composition(compound)
                            # Scale composition by stoichiometric ratio
                            for element, amount in comp.as_dict().items():
                                component_dict[element] = component_dict.get(element, 0) + amount * ratio
                    else: 
                        # Case to handle the ratios as mass fractions
                        # e.g. (W18O49)0.25(ZnO)0.75. The 0.25 and 0.75 are mass fractions
                        ratio = float(ratio.strip()) if ratio.strip() else 1.0 # Handle empty ratios as 1.0 or 100%
                        comp = Composition(compound)
                        molar_mass = comp.weight
                        # Calculate moles based on mass ratio and molar mass
                        moles = ratio / molar_mass
                        # Add moles of the additive without altering primary components
                        for element, amount in comp.as_dict().items():
                            component_dict[element] = component_dict.get(element, 0) + amount * moles 


                # Create the final composition without normalizing primary to additive ratios
                final_comp = Composition(component_dict)
                compositions.append(final_comp)
            except Exception as e:
                compositions.append(None)
                print(f"Error converting mixed formula '{formula}', entry {iter} to Composition: {e}")

        else:
            # Placeholder for handling mass formulas or any other types
            compositions.append(None)
        iter += 1

    # Convert the list to a pandas series with the desired output name
    return pd.Series(compositions, name=output_name)
