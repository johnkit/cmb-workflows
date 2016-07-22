<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">

  <!-- Category & Analysis specifications -->

  <!-- Attribute definitions -->
  <Includes>
    <!-- Note: order is important, e.g., put expressions first -->
    <File>templates/grid-2d.sbt</File>
  </Includes>

  <!-- View specifications -->
  <Views>
    <View Type="Group" Title="SimBuilder" TopLevel="true">
      <Views>
        <View Title="Grid"/>
      </Views>
    </View>

    <View Type="Instanced" Title="Grid">
      <InstancedAttributes>
        <Att Name="Geometry" Type="geometry" />
        <Att Name="Grid" Type="grid" />
      </InstancedAttributes>
    </View>
  </Views>
</SMTK_AttributeSystem>
