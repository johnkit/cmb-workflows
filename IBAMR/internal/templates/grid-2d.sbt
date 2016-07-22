<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="geometry" Label="Geometry" BaseType="" Version="0">
      <ItemDefinitions>
        <Double Name="origin" Label="Lower Left Corner" Version="0" NumberOfRequiredValues="2">
          <BriefDescription>physical location of the lower left corner</BriefDescription>
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <Double Name="length" Label="Physical Length" Version="0" NumberOfRequiredValues="2">
          <BriefDescription>physical size of the geometry domain</BriefDescription>
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DefaultValue>1.0</DefaultValue>
          <Range>
            <Min Inclusive="false">0.0</Min>
          </Range>
        </Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="grid" Label="Grid" BaseType="" Version="0">
      <ItemDefinitions>
        <Int Name="base-grid-size" Label="Base Grid Size" Version="0" NumberOfRequiredValues="2">
          <BriefDescription>number of grid cells at the base/coarsest refinement level</BriefDescription>
          <ComponentLabels>
            <Label>x:</Label>
            <Label>y:</Label>
          </ComponentLabels>
          <DefaultValue>64</DefaultValue>
          <Range>
            <Min Inclusive="true">1</Min>
          </Range>
        </Int>
        <Int Name="max-levels" Label="Maximum Levels" Version="0">
          <DefaultValue>1</DefaultValue>
          <Range>
            <Min Inclusive="true">1</Min>
          </Range>
        </Int>
        <Int Name="refinement-ratio" Label="Refinement Ratio">
          <ChildrenDefinitions>
            <Int Name="fixed-refinement-ratio" Label="Fixed Refinement Ratio">
              <DefaultValue>2</DefaultValue>
              <Range>
                <Min Inclusive="true">1</Min>
              </Range>
            </Int>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value Enum="Fixed">fixed</Value>
              <Items>
                <Item>fixed-refinement-ratio</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </Int>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>