<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="parameters" Label="Physical Parameters" BaseType="" Version="0">
      <ItemDefinitions>
        <Double Name="viscosity" Label="Viscosity (mu)">
          <DefaultValue>0.01</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0.0</Min>
          </RangeInfo>
        </Double>
        <Double Name="density" Label="Density (rho)">
          <DefaultValue>1.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0.0</Min>
          </RangeInfo>
        </Double>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>
