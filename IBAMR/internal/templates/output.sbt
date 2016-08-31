<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="output" Label="Output" BaseType="" Version="0">
      <ItemDefinitions>
        <Void Name="enable-logging" Label="Enable Logging" Optional="true" IsEnabledByDefault="true"></Void>
        <Group Name="output-fields" Label="Output Fields">
          <ItemDefinitions>
            <Void Name="velocity" Label="Velocity" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="pressure" Label="Pressure" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="body-force" Label="Body Force" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="vorticity" Label="Vorticity (omega)" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="divergence" Label="Divergence of Velocity" Optional="true" IsEnabledByDefault="true"></Void>
          </ItemDefinitions>
        </Group>
        <Group Name="log" Label="Log Output">
          <ItemDefinitions>
            <File Name="log-file" Label="Log File" NumberOfRequiredValues="1">
              <DefaultValue>IB2d.log</DefaultValue>
            </File>
            <Void Name="log-all-nodes" Label="Log All Nodes" Optional="true" IsEnabledByDefault="false"></Void>
          </ItemDefinitions>
        </Group>
        <Group Name="visualization" Label="Visualization Output">
          <ItemDefinitions>
            <Group Name="visit" Label="VisIt" Optional="true" IsEnabledByDefault="true">
              <ItemDefinitions>
                <Int Name="number-procs-per-file" Label="Number of Process per File">
                  <DefaultValue>1</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">1</Min>
                  </RangeInfo>
                </Int>
              </ItemDefinitions>
            </Group>
            <Void Name="exodus" Label="ExodusII" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="silo" Label="Silo" Optional="true" IsEnabledByDefault="false"></Void>
            <Int Name="interval" Label="Output Interval">
              <DefaultValue>250</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Directory Name="directory" Label="Directory" NumberOfRequiredValues="1">
              <DefaultValue>viz_IB2d</DefaultValue>
            </Directory>
          </ItemDefinitions>
        </Group>
        <Group Name="restart" Label="Restart Output" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <Int Name="interval" Label="Restart Dump Interval">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Directory Name="directory" Label="Directory" NumberOfRequiredValues="1">
              <DefaultValue>restart_IB2d</DefaultValue>
            </Directory>
          </ItemDefinitions>
        </Group>
        <Group Name="hierarchy" Label="Hierarchy Data Output" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <Int Name="interval" Label="Hierarchy Data Dump Interval">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Directory Name="directory" Label="Directory" NumberOfRequiredValues="1">
              <DefaultValue>hier_data_IB2d</DefaultValue>
            </Directory>
          </ItemDefinitions>
        </Group>
        <Group Name="timer" Label="Timer Output" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <Int Name="interval" Label="Timer Parameters Dump Interval">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>
