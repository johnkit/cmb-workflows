<?xml version="1.0"?>
<SMTK_AttributeSystem Version="2">
  <Definitions>
    <AttDef Type="ExportSpec" Label="Settings" BaseType="" Version="0">
      <ItemDefinitions>
        <String Name="AnalysisTypes" Label="Analysis Types" Version="0" AdvanceLevel="99" NumberOfRequiredValues="1" Extensible="true" />
        <File Name="OutputFile" Label="Output File (*.o3p, *.omega3p)" Version="0"
              NumberOfRequiredValues="1" ShouldExist="false"
              FileFilters="Omega3P files (*.o3p *.omega3p);;All files (*.*)" />
        <File Name="PythonScript" Label="Python script" Version="0" AdvanceLevel="0" NumberOfRequiredValues="1" ShouldExist="true" FileFilters="Python files (*.py);;All files (*.*)" />

        <Group Name="NERSCSimulation" Label="Submit job to NERSC"
               Optional="true" IsEnabledByDefault="false"
               Version="0" NumberOfRequiredGroups="1">
          <ItemDefinitions>
            <String Name="JobName" Label="Job name" Version="0">
              <BriefDescription>Label you can use to track your job</BriefDescription>
              <DefaultValue>Omega3P</DefaultValue>
            </String>
            <String Name="CumulusHost" Label="Cumulus host" Version="0">
              <DefaultValue>http://localhost:8080</DefaultValue>
            </String>
            <String Name="NERSCRepository" Label="Project repository" Version="0" />
            <String Name="NERSCAccountName" Label="NERSC account name" Version="0" />
            <String Name="NERSCAccountPassword" Label="NERSC account password"
                    Secure="true" Version="0" />
            <String Name="Machine" Label="NERSC Machine" Version="0">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="Cori (Cray XC40)">cori</Value>
                <Value Enum="Edison (Cray XC30)">edison</Value>
              </DiscreteInfo>
            </String>
            <String Name="JobDirectory" Label="Job directory" Version="0"
                    Optional="true" IsEnabledByDefault="false">
              <BriefDescription>Typically this should be set to the absolute path
to the Scratch directory. ModelBuilder will create a separate
subdirectory for each job.
              </BriefDescription>
            </String>
            <String Name="Queue" Label="Queue" Version="0">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="debug">debug</Value>
                <Value Enum="regular">normal</Value>
                <Value Enum="premium">premium</Value>
                <Value Enum="low priority">low</Value>
                <Value Enum="scavenger">scavenger</Value>
              </DiscreteInfo>
            </String>
            <Int Name="NumberOfNodes" Label="Number of nodes" Version="0">
              <DefaultValue>1</DefaultValue>
              <RangeInfo><Min Inclusive="true">1</Min></RangeInfo>
            </Int>
            <!--  Note that SLAC calls this number of "cores" -->
            <Int Name="NumberOfTasks" Label="Number of cores" Version="0">
              <DefaultValue>1</DefaultValue>
              <RangeInfo><Min Inclusive="true">1</Min></RangeInfo>
            </Int>
            <Int Name="Timeout" Label="Time limit" Units="min" Version="0">
              <DefaultValue>5</DefaultValue>
              <RangeInfo><Min Inclusive="true">1</Min></RangeInfo>
            </Int>
            <String Name="TailFile" Label="Tail Filename" Version="0" AdvanceLevel="1">
              <DefaultValue>omega3p_results/omega3p.log</DefaultValue>
            </String>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
     </AttDef>
   </Definitions>
  <Views>
    <View Type="Group" Title="Export" TopLevel="true"
          Style="Tiled" FilterByCategory="false">
      <Views>
        <View Title="Export Settings" />
      </Views>
    </View>
    <View Type="Instanced" Title="Export Settings">
      <InstancedAttributes>
        <Att Name="Options" Type="ExportSpec" />
      </InstancedAttributes>
    </View>
  </Views>
</SMTK_AttributeSystem>
