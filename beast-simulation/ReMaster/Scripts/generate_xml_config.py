import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml

# Load the YAML configuration file
with open('/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-gendata/ReMaster/Scripts/xml_config.yaml', 'r') as file:
    config = yaml.safe_load(file)



# Create the root element
root = ET.Element("beast", version=config['beast']['version'], namespace=config['beast']['namespace'])

# Add a run element with sub-elements
run = ET.SubElement(root, "run", spec=config['run']["spec"], nSims= config['run']['nSims'])

simulate = ET.SubElement(run, "simulate", spec=config['run']["simulate"]["spec"], id=config['run']["simulate"]["id"])
trajectory = ET.SubElement(simulate, "trajectory", spec="StochasticTrajectory", id="traj")

# Add population elements
ET.SubElement(trajectory, "population", spec="RealParameter", id="S", value=config['run']["simulate"]["trajectory"]["population"]["spec_S"])
ET.SubElement(trajectory, "population", spec="RealParameter", id="E", value=config['run']["simulate"]["trajectory"]["population"]["spec_E"])
ET.SubElement(trajectory, "population", spec="RealParameter", id="I", value=config['run']["simulate"]["trajectory"]["population"]["spec_I"])

# Add samplePopulation elements
ET.SubElement(trajectory, "samplePopulation", spec="RealParameter", id="R", value= config['run']["simulate"]["trajectory"]["samplePopulation"]["spec_R"])  
ET.SubElement(trajectory, "samplePopulation", spec="RealParameter", id="sample", value= config['run']["simulate"]["trajectory"]["samplePopulation"]["spec_sample"])

# Add reaction elements
ET.SubElement(trajectory, "reaction", spec="Reaction", rate=config['run']["simulate"]["trajectory"]["reaction"]["spec_I_E_rate"]).text = "I + S -> I + E"
ET.SubElement(trajectory, "reaction", spec="Reaction", rate=config['run']["simulate"]["trajectory"]["reaction"]["spec_E_I_rate"]).text = "E -> I"
ET.SubElement(trajectory, "reaction", spec="Reaction", rate=config['run']["simulate"]["trajectory"]["reaction"]["spec_R_rate"]).text = "I -> R"
ET.SubElement(trajectory, "reaction", spec="Reaction", rate=config['run']["simulate"]["trajectory"]["reaction"]["spec_sampling_rate"]).text = "I -> R + sample"

# Add logger elements
logger1 = ET.SubElement(run, "logger", spec="Logger", fileName="$(filebase).traj")
ET.SubElement(logger1, "log", idref="traj")

logger2 = ET.SubElement(run, "logger", spec="Logger", mode="tree", fileName="$(filebase).full.trees")
log2 = ET.SubElement(logger2, "log", spec="TypedTreeLogger")
ET.SubElement(log2, "tree", spec="PrunedTree", samplePops="R", simulatedTree="@tree")

logger3 = ET.SubElement(run, "logger", spec="Logger", mode="tree", fileName="$(filebase).sampled.trees")
log3 = ET.SubElement(logger3, "log", spec="TypedTreeLogger")
ET.SubElement(log3, "tree", spec="PrunedTree", samplePops="sample", simulatedTree="@tree")


# Create the ElementTree object
tree = ET.ElementTree(root)

# Write to XML file
tree.write("/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-gendata/ReMaster/library.xml", encoding="utf-8", xml_declaration=True)


# Convert to string and pretty print
xml_str = ET.tostring(root, encoding='utf-8')
pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

# Print the XML tree to console
print(pretty_xml)
# Optionally, write the XML to a file