<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="output" Label="Output" BaseType="" Version="0">
      <ItemDefinitions>
        <Group Name="log" Label="Log Output">
          <ItemDefinitions>
            <File Name="log-file" Label="Log File" NumberOfRequiredValues="1">
              <DefaultValue>"IB2d.log"</DefaultValue>
            </File>
            <Void Name="log-all-nodes" Label="Log All Nodes" Optional="true" IsEnabledByDefault="false"></Void>
          </ItemDefinitions>
        </Group>
        <Group Name="visualization" Label="Visualization Output" Optional="true" IsEnabledByDefault="true">
          <ItemDefinitions>
            <Group Name="visit" Label="VisIt" Optional="true" IsEnabledByDefault="true">
              <ItemDefinitions>
                <Int Name="number-procs-per-file" Label="Number of Process per File">
                  <DefaultValue>1</DefaultValue>
                  <RangeInfo>
                    <Minimum Inclusive="true">1</Minimum>
                  </RangeInfo>
                </Int>
              </ItemDefinitions>
            </Group>
            <Void Name="exodus" Label="ExodusII" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="silo" Label="Silo" Optional="false" IsEnabledByDefault="true"></Void>
            <Directory Name="directory" Label="Directory" NumberOfRequiredValues="1">
              <DefaultValue>"viz_IB2d"</DefaultValue>
            </Directory>
          </ItemDefinitions>
        </Group>
        <Group Name="restart" Label="Restart Output" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <Int Name="interval" Label="Restart Dump Interval">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Minimum Inclusive="true">1</Minimum>
              </RangeInfo>
            </Int>
            <Directory Name="directory" Label="Directory" NumberOfRequiredValues="1">
              <DefaultValue>"restart_IB2d"</DefaultValue>
            </Directory>
          </ItemDefinitions>
        </Group>
        <Group Name="hierarchy" Label="Hierarchy Data Output" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <Int Name="interval" Label="Hierarchy Data Dump Interval">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Minimum Inclusive="true">1</Minimum>
              </RangeInfo>
            </Int>
            <Directory Name="directory" Label="Directory" NumberOfRequiredValues="1">
              <DefaultValue>"hier_data_IB2d"</DefaultValue>
            </Directory>
          </ItemDefinitions>
        </Group>
        <Group Name="timer" Label="Timer Output" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <Int Name="interval" Label="Timer Parameters Dump Interval">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Minimum Inclusive="true">1</Minimum>
              </RangeInfo>
            </Int>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>