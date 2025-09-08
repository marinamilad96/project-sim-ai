import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml
import pandas as pd
import numpy as np

# Load the YAML configuration file
with open('/Users/MiladM-Dev/Documents/1PhD/project-1-N450/project-1.1-gendata/ReMaster/Scripts/xml_config.yaml', 'r') as file:
    config = yaml.safe_load(file)
class generate_xml_files:
    def __init__(self, config):
        self.config = config

    def read_csv(self):
        self.df = pd.read_csv(self.config["FilePath"]["CSVFilePath"])
        #self.df.columns = self.df.iloc[0] # Remove the first row
        #self.df.drop(self.df.index[0], inplace=True)
        #self.df.reset_index(drop=True, inplace=True)
        return self.df


    def create_xml(self):
        # convert DataFrame to numpy array
        arr = self.df.to_numpy()
        for i, self.row in enumerate(arr):
            self.paramters, self.InfectionRate, self.IncubationRate, self.RecoveryRate, self.SamplingRate, self.S, self.E, self.I, self.R, self.Sample, self.logEvery = self.row
            
            print(f"Run {i+1}: paramters={self.paramters}, InfectionRate={self.InfectionRate}, "
                  f"IncubationRate={self.IncubationRate}, RecoveryRate={self.RecoveryRate}, "
                  f"SamplingRate={self.SamplingRate}, S={self.S}, E={self.E}, I={self.I}, R={self.R}, Sample={self.Sample}")
            
            # Create the root element
            root = ET.Element("beast", version=self.config['beast']['version'], namespace=self.config['beast']['namespace'])

            # Add a run element with sub-elements
            run = ET.SubElement(root, "run", spec=self.config['run']["spec"], nSims= self.config['run']['nSims'])

            simulate = ET.SubElement(run, "simulate", spec=self.config['run']["simulate"]["spec"], id=self.config['run']["simulate"]["id"], tEnd="365.0")
            trajectory = ET.SubElement(simulate, "trajectory", spec="StochasticTrajectory", id="traj")

            # Add population elements
            ET.SubElement(trajectory, "population", spec="RealParameter", id="S", value=str(self.S))
            ET.SubElement(trajectory, "population", spec="RealParameter", id="E", value=str(self.E))
            ET.SubElement(trajectory, "population", spec="RealParameter", id="I", value=str(self.I))

            # Add samplePopulation elements
            ET.SubElement(trajectory, "samplePopulation", spec="RealParameter", id="R", value= str(self.R))
            ET.SubElement(trajectory, "samplePopulation", spec="RealParameter", id="sample", value= str(self.Sample))

            # Add reaction elements
            ET.SubElement(trajectory, "reaction", spec="Reaction", rate=str(self.InfectionRate)).text = "I + S -> I + E"
            ET.SubElement(trajectory, "reaction", spec="Reaction", rate=str(self.IncubationRate)).text = "E -> I"
            ET.SubElement(trajectory, "reaction", spec="Reaction", rate=str(self.RecoveryRate)).text = "I -> R"
            ET.SubElement(trajectory, "reaction", spec="Reaction", rate=str(self.SamplingRate)).text = "I -> R + sample"

            # Add logger elements
            logger1 = ET.SubElement(run, "logger", spec="Logger", fileName="$(filebase).traj", logEvery=str(self.logEvery))
            ET.SubElement(logger1, "log", idref="traj")

            logger2 = ET.SubElement(run, "logger", spec="Logger", mode="tree", fileName="$(filebase).full.trees", logEvery=str(self.logEvery))
            log2 = ET.SubElement(logger2, "log", spec="TypedTreeLogger")
            ET.SubElement(log2, "tree", spec="PrunedTree", samplePops="R", simulatedTree="@tree")

            logger3 = ET.SubElement(run, "logger", spec="Logger", mode="tree", fileName="$(filebase).sampled.trees", logEvery=str(self.logEvery))
            log3 = ET.SubElement(logger3, "log", spec="TypedTreeLogger")
            ET.SubElement(log3, "tree", spec="PrunedTree", samplePops="sample", simulatedTree="@tree")

            
            # Create the ElementTree object
            tree = ET.ElementTree(root)

            # Write to XML file
            tree.write(self.config["FilePath"]["outputFilePath"]+f"{self.paramters}_{i+1}.xml", encoding="utf-8", xml_declaration=True)

            #xml_str = ET.tostring(root, encoding='utf-8')
            #pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
            #print(pretty_xml)
            

    def excute(self):
        self.read_csv()

        self.create_xml()

xml_files = generate_xml_files(config)
xml_files.excute()

print(f"""XML files generated successfully.

You can find them in {config["FilePath"]["outputFilePath"]}

""")
      
      
