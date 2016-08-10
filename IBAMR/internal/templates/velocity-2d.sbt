<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="velocity" Label="Velocity Boundary Condition" BaseType="" Version="0">
      <ItemDefinitions>
        <Group Name="enable" Label="Enable" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>a*u + b*du/dn = g</BriefDescription>
          <ItemDefinitions>
            <Double Name="a" Label="a Coefficients" NumberOfRequiredValues="4">
              <DefaultValue>1.0</DefaultValue>
            </Double>
            <Double Name="b" Label="b Coefficients" NumberOfRequiredValues="4">
              <DefaultValue>0.0</DefaultValue>
            </Double>
            <Double Name="g" Label="g Coefficients" NumberOfRequiredValues="4">
              <DefaultValue>0.0</DefaultValue>
            </Double>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>
