<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="controls" Label="Controls" BaseType="" Version="0">
      <ItemDefinitions>
        <String Name="tagging-method" Label="Tagging Method">
          <DiscreteInfo DefaultIndex="0">
            <Value>GRADIENT_DETECTOR</Value>
            <Value>REFINE_BOXES</Value>
          </DiscreteInfo>
        </String>
        <Group Name="load-balancer" Label="Load Balancer">
          <ItemDefinitions>
            <String Name="bin-pack-method" Label="Bin Pack Method">
              <DiscreteInfo DefaultIndex="0">
                <Value>SPATIAL</Value>
              </DiscreteInfo>
            </String>
            <Int Name="max-workload-factor" Label="Max Workload Factor">
              <DefaultValue>1</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
                <Max Inclusive="true">1</Max>
              </RangeInfo>
            </Int>
          </ItemDefinitions>
        </Group>
        <Group Name="timer-manager" Label="Timer Manager">
          <ItemDefinitions>
            <Void Name="print-exclusive" Label="Print Exclusive" Optional="true" IsEnabledByDefault="false"></Void>
            <Void Name="print-total" Label="Print Total" Optional="true" IsEnabledByDefault="true"></Void>
            <Double Name="print-threshold" Label="Print Threshold">
              <DefaultValue>0.1</DefaultValue>
            </Double>
            <String Name="timer-list" Label="Timer List" Extensible="true" NumberOfRequiredValues="1">
              <DefaultValue>*::*::*</DefaultValue>
            </String>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>
