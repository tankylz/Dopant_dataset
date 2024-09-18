
<div style="font-family: Charter, sans; font-size: 18px;">

# To-Do List

## Goals

- Ensure the accuracy of the dataset

- Format the data to be human and machine readable

- Generate informative visualizations

- Checkpoint: Publish Data In Data In Brief

- Long-term: To use dataset for machine learning, relating composition to properties

## Low-hanging fruits

- [x] Make the DOIs all consistent links

- [x] Remove rows containing missing DOIs
  - 840 total (573 mrl, 19 personal, 250 blanks)
  - 8548 datapoints remaining

- [ ] Download all papers and put them in the repo  
  - [ ] Use legit sources, not scihub. So need to login with credentials.

## Missing Data Still

- [ ] Synthesis data need to consolidate / separate mixing parameters, synthesis method and preparative route

- [ ] Source 1 (data collected by Layla and Leng Ze)
  - [ ] Bulk or Thin Film
  - [ ] Calcination and Mixing Parameters - Maybe do it after consolidating the synthesis data

## Columns to consider deleting

- Space group, ICSD stuff

- Thermal Diffusivity, Weighted Mobility, Measurement Atmosphere, Carrier Concentration, Carrier Mobility

## Functions for Column Conversion

- [ ] Function to convert Mass and Mixed Formula to Stoichiometric compositions
  - Eg. Some formula are now in weight ratios ((W18O40)0.3(ZnO)0.7) and some are in a mixture of stoichiometric ratios and weight ratios (0.9Cu2Se-0.1(Bi0.88Pb0.06Ca0.06CuSeO)-0.01 wt% Graphene)
  - **WORST CASE**: Delete these entries (count how many of them are there first)
  - 302 total (all mixed formula, i.e. some parts are stoichiometrically represented, typically the compound itself, while other parts are mass represented)
  - [x] Done initial function
  - [ ] Need to check if the conversion is correct 

- [ ] Host-Dopant Based on a Function
  - [ ] Function to take in a threshold % (like 1%) to separate dopant from host
  - [ ] Potential issues: It cannot parse dopants that are compounds
    - E.g. (AgCl)0.001PbTe(0.999) is supposed to be (PbTe)0.999 as host and (AgCl)0.001 as dopant. But we might get Ag0.001, Cl0.001.
    - E.g. (AgCl)0.001PbTe(0.999)Cu0.001 is supposed to be (PbTe)0.999 as host and (AgCl)0.001 and Cu0.001 as dopant. But we might get Ag0.001, Cl0.001 and Cu0.001

- [ ] Might want to remove base and alloy formulas
  - [ ] If we don't remove it, need to verify base + alloy = pretty formula

- [ ] Generation of electronic and lattice thermal conductivity from total thermal conductivity
  - Need to have at least two of those properties
    - [ ] If 2 properties, take a simple difference or sum will get you the other
    - [ ] If 3 properties, need to verify if that electronic + lattice = total

- [ ] Need to rebase the temperature of some of Sparks' Thermoelectric Data as per comments - some may be 1000K but taken from another temperature.

## Data Verification

- [ ] Resolve all comments in Excel

- [ ] Verification of TE numerical values
  - [ ] Outlier analysis &rarr; Then manually check through said outliers

- [ ] Verification of textual data (synthesis, comments)
  - [ ] Use LLM
  - [ ] For pretty formula, ask if the formula is present in the paper?

## Data Visualization

- [ ] Thermoelectric values (e.g. zT) over the years
  - Line plot
  - Either take average (with std dev?) or maximum

- [ ] doped vs undoped
  - single bar plot
  - might want to isolate DOIs containing both doped and undoped data for fairer comparison?

- [ ] properties by family - scatterplot with different colours + size of scatterplot giving a third property
  - [ ] Check the material family first - some are ambiguous
  - Alternatively, just show common material family (maybe at least 2 different DOIs of the same family after removing those unsure)

- [ ] Best performing thermoelectric material by temperatures
