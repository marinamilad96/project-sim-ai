import xml.etree.ElementTree as ET
import yaml
import pandas as pd
import os


# Load the YAML configuration file
with open('/home/miladm/scratch/project-sim-ai/config-files/sconfig.yaml', 'r') as file:
    config = yaml.safe_load(file)


class generate_xml_files:
    def __init__(self, config):
        self.config = config

    def read_csv(self):
        self.df = pd.read_csv(os.path.expandvars(self.config["FilePath"]["CSVFilePath"]))
        return self.df

    def create_xml(self):
        # convert DataFrame to numpy array
        arr = self.df.to_numpy()
        for i, self.row in enumerate(arr):
            self.paramters, self.InfectionRate, self.IncubationRate, self.DiagnosisRate, self.SamplingRate, self.S, self.E, self.I, self.D, self.Sample, self.InfectionRate_M, self.IncubationRate_M, self.DiagnosisRate_M, self.MigrationRate_0to1, self.MigrationRate_1to0 = self.row

            print(f"Run {i+1}: paramters={self.paramters}, InfectionRate={self.InfectionRate}, "
                  f"IncubationRate={self.IncubationRate}, DiagnosisRate={self.DiagnosisRate}, "
                  f"SamplingRate={self.SamplingRate}, S={self.S}, E={self.E}, I={self.I}, D={self.D}, Sample={self.Sample}, "
                  f"InfectionRate_M={self.InfectionRate_M}, IncubationRate_M={self.IncubationRate_M}, "
                  f"DiagnosisRate_M={self.DiagnosisRate_M}, MigrationRate_1to0={self.MigrationRate_1to0}")

            # Create the root element
            root = ET.Element(
                "beast", version= "2.0", namespace="beast.base.inference.parameter:beast.base.inference:remaster")

            # Add a run element with sub-elements
            run = ET.SubElement(
                root, "run", spec="Simulator", nSims="1")

            simulate = ET.SubElement(
                run, "simulate", spec="SimulatedTree", id="tree")
            trajectory = ET.SubElement(
                simulate, "trajectory", spec="StochasticTrajectory", id="traj", maxTime="1100.0")

            # Add population elements
            ET.SubElement(trajectory, "population",
                          spec="RealParameter", id="S", value=str(self.S), dimension="2")
            ET.SubElement(trajectory, "population",
                          spec="RealParameter", id="E", value=str(self.E), dimension="2")
            ET.SubElement(trajectory, "population",
                          spec="RealParameter", id="I", value=str(self.I), dimension="2")

            # Add samplePopulation elements
            ET.SubElement(trajectory, "samplePopulation",
                          spec="RealParameter", id="D", value=str(self.D), dimension="2")
            ET.SubElement(trajectory, "samplePopulation",
                          spec="RealParameter", id="sample", value=str(self.Sample))

            # SEIR reactions  Germany=0, outside=1
            plate = ET.SubElement(trajectory, "plate", var="i", range="0:1")
            reaction1 = ET.SubElement(
                plate, "reaction", spec="Reaction", rate=str(self.IncubationRate))
            reaction1.text = "E[$(i)]:1 -> I[$(i)]:1"

            # Germany reactions

            reaction2 = ET.SubElement(
                trajectory, "reaction", spec="Reaction", rate=str(self.DiagnosisRate))
            reaction2.text = "I[0] -> D[0]"

            reaction3 = ET.SubElement(
                trajectory, "reaction", spec="Reaction", rate=str(self.InfectionRate))
            reaction3.text = "S[0] + I[0]:1 -> I[0]:1 + E[0]:1"

            reaction4 = ET.SubElement(
                trajectory, "reaction", spec="Reaction", rate=str(self.SamplingRate))
            reaction4.text = "I[0]:1 -> D[0] + sample[0]:1"

            # Outside reactions

            reaction6 = ET.SubElement(
                trajectory, "reaction", spec="Reaction", rate=str(self.InfectionRate_M))
            reaction6.text = "S[1] + I[1]:1 -> I[1]:1 + E[1]:1"

            reaction7 = ET.SubElement(
                trajectory, "reaction", spec="Reaction", rate=str(self.DiagnosisRate_M))
            reaction7.text = "I[1] -> D[1]"

            # Migration from outside to Germany
            reaction8 = ET.SubElement(
                trajectory, "reaction", spec="Reaction", rate=str(self.MigrationRate_1to0))
            reaction8.text = "I[1]:1 -> I[0]:1"

            # Migration from Germany to outside
            # reaction7 = ET.SubElement(trajectory, "reaction", spec="Reaction", rate=str(self.MigrationRate_0to1))
            # reaction7.text = "I[0] -> I[1]"

            # Add logger elements
            logger1 = ET.SubElement(
                run, "logger", spec="Logger", fileName="$(filebase)-$(seed).traj")
            ET.SubElement(logger1, "log", idref="traj")

            logger2 = ET.SubElement(run, "logger", spec="Logger", mode="tree",
                                    fileName="$(filebase)-$(seed).full.trees")
            log2 = ET.SubElement(logger2, "log", spec="TypedTreeLogger")
            ET.SubElement(log2, "tree", spec="PrunedTree",
                          samplePops="D", simulatedTree="@tree")

            logger3 = ET.SubElement(run, "logger", spec="Logger", mode="tree",
                                    fileName="$(filebase)-$(seed).sampled.trees")
            log3 = ET.SubElement(logger3, "log", spec="TypedTreeLogger")
            ET.SubElement(log3, "tree", spec="PrunedTree",
                          samplePops="sample", simulatedTree="@tree")

            # Add a Space or "/n" without using minidom package

            def indent(elem, level=0):
                i = "\n" + level * "  "
                if len(elem):
                    if not elem.text or not elem.text.strip():
                        elem.text = i + "  "
                    for child in elem:
                        indent(child, level + 1)
                    if not elem.tail or not elem.tail.strip():
                        elem.tail = i
                else:
                    if level and (not elem.tail or not elem.tail.strip()):
                        elem.tail = i
            indent(root)

            # Create the ElementTree object
            tree = ET.ElementTree(root)

            # Write to XML file
            #tree.write(os.path.expandvars(self.config["FilePath"]["outputFilePath"]) + f"{self.paramters}_{i+1}.xml", encoding="utf-8", xml_declaration=True)

            output_path = os.path.join(
                os.path.expandvars(self.config["FilePath"]["outputFilePath"]),
                f"{self.paramters}_{i+1}.xml"
            )

            # make sure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # now write the XML
            tree.write(output_path, encoding="utf-8", xml_declaration=True)

            print("Saving XML to:", output_path)


    def excute(self):
        self.read_csv()
        self.create_xml()


xml_files = generate_xml_files(config)
xml_files.excute()

print(f"""XML files generated successfully.

You can find them in {os.path.expandvars(self.config["FilePath"]["outputFilePath"])}

""")
