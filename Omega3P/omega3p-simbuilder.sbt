<?xml version="1.0"?>
<!--Created by XmlV2StringWriter-->
<SMTK_AttributeSystem Version="2">
  <!--**********  Category and Analysis Information ***********-->
  <Categories Default="Omega3P"/>
  <Analyses>
    <Analysis Type="Omega 3P Analysis">
      <Cat>Omega3P</Cat>
    </Analysis>
  </Analyses>
  <!--**********  Attribute Definitions ***********-->
  <Definitions>
   <AttDef Type="Tolerant" Label="Tolerant" Version="0">
    <ItemDefinitions>
      <Void Name="Tolerant" Label="Tolerant" Version="0"
            Optional="true" IsEnabledByDefault="false" />
    </ItemDefinitions>
   </AttDef>

    <AttDef Type="SurfaceProperty"
            Label="Surface Boundary Condition"
            BaseType="" Version="0" Unique="true">
      <AssociationsDef Name="SurfacePropertyAssociations"
                       Version="0"
                       NumberOfRequiredValues="0" Extensible="true">
        <MembershipMask>face</MembershipMask>
      </AssociationsDef>
      <ItemDefinitions>
        <String Name="Type" Version="0">
          <BriefDescription>Indicates the type of surface boundary condition</BriefDescription>
          <ChildrenDefinitions>
            <Double Name="Sigma" Label="Conductivity" Version="0"
                    AdvanceLevel="0" NumberOfRequiredValues="1" Units="s/m">
              <BriefDescription>Impedance Surface Conductivity.</BriefDescription>
              <DefaultValue>5.8e7</DefaultValue>
            </Double>
            <Double Name="Theta" Label="Theta (Relative Phase Angle)" Version="0"
                    AdvanceLevel="0" NumberOfRequiredValues="1">
              <BriefDescription>Relative Phase Between Master and Slave Surfaces</BriefDescription>
              <DefaultValue>0.0</DefaultValue>
            </Double>
            <Int Name="NumModes" Label="Number of Modes" Version="0" Optional="true"
                    AdvanceLevel="0" NumberOfRequiredValues="1">
              <BriefDescription>Number of Modes Loaded on Port</BriefDescription>
            </Int>
            <ModelEntity Name="SlaveSurface" Label="Slave Surface" Version="0"
                    AdvanceLevel="0" NumberOfRequiredValues="1">
              <MembershipMask>face</MembershipMask>
            </ModelEntity>
          </ChildrenDefinitions>
          <DiscreteInfo>
            <Value Enum="Electric">Electric</Value>
            <Value Enum="Magnetic">Magnetic</Value>
            <Structure>
              <Value Enum="Exterior">Exterior</Value>
                <Items><Item>Sigma</Item></Items>
            </Structure>
            <Structure>
              <Value Enum="Impedance">Impedance</Value>
              <Items>
                <Item>Sigma</Item>
              </Items>
            </Structure>
             <Value Enum="Absorbing">Absorbing</Value>
            <Structure>
              <Value Enum="Waveguide">Waveguide</Value>
              <Items>
                <Item>NumModes</Item>
              </Items>
            </Structure>
            <Structure>
              <Value Enum="Periodic">Periodic</Value>
              <Items>
                <Item>Theta</Item>
                <Item>SlaveSurface</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
   </AttDef>

   <AttDef Type="HFormulation" Label="HFormulation" Version="0">
    <ItemDefinitions>
      <Void Name="HFormulation" Label="HFormulation" Version="0"
            Optional="true" IsEnabledByDefault="false" />
    </ItemDefinitions>
   </AttDef>

   <AttDef Type="Port" Label="Port" BaseType="" Version="0" Unique="true">
      <AssociationsDef Name="PortAssociations" Version="0" NumberOfRequiredValues="0" Extensible="true">
        <MembershipMask>face</MembershipMask>
      </AssociationsDef>
      <ItemDefinitions>
        <Int Name="NumberOfModes" Label="Number of modes" Version="0">
          <RangeInfo><Min Inclusive="true">0</Min></RangeInfo>
          <DefaultValue>1</DefaultValue>
        </Int>
      </ItemDefinitions>
   </AttDef>

   <AttDef Type="FEInfo" BaseType="" Version="0">
      <ItemDefinitions>
        <Int Name="Order" Label="Global Order" Version="0" >
          <RangeInfo>
            <Min Inclusive="false">0</Min>
          </RangeInfo>
          <DefaultValue>2</DefaultValue>
        </Int>
       <Void Name="EnableCurvedSurfaces" Label="Enable Curved Surfaces" Version="0" Optional="true" IsEnabledByDefault="true"/>
      </ItemDefinitions>
   </AttDef>
    <AttDef Type="RegionHighOrder" BaseType="" Version="0" Unique="true">
      <AssociationsDef Name="MaterialAssociations" Version="0" NumberOfRequiredValues="0" Extensible="true">
        <MembershipMask>volume</MembershipMask>
      </AssociationsDef>
      <ItemDefinitions>
        <Int Name="RegionHighOrder" Label="Region High Order" Version="0" >
           <RangeInfo>
            <Min Inclusive="false">0</Min>
          </RangeInfo>
          <DefaultValue>2</DefaultValue>
        </Int>
      </ItemDefinitions>
    </AttDef>

   <AttDef Type="EigenSolver" Label="EigenSolver" BaseType="" Version="0">
      <ItemDefinitions>
        <Int Name="NumEigenvalues" Label="Number of eigenmodes searched" Version="0" >
          <RangeInfo>
            <Min Inclusive="false">0</Min>
          </RangeInfo>
          <DefaultValue>1</DefaultValue>
        </Int>
        <Double Name="FrequencyShift" Label="Frequency Shift" Version="0" Units="Hz">
          <RangeInfo>
            <Min Inclusive="true">0.0</Min>
          </RangeInfo>
          <DefaultValue>1.0e9</DefaultValue>
        </Double>
      </ItemDefinitions>
   </AttDef>

    <AttDef Type="PostProcess" Label="Post Process" BaseType="" Version="0">
      <ItemDefinitions>
        <Void Name="ModeFiles" Label="Write *.mod files"
           Version="0" Optional="true" IsEnabledByDefault="true" />
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="Material" BaseType="" Version="0" Unique="true">
      <AssociationsDef Name="MaterialAssociations" Version="0" NumberOfRequiredValues="0" Extensible="true">
        <MembershipMask>volume</MembershipMask>
      </AssociationsDef>
      <ItemDefinitions>
        <Double Name="Epsilon" Label="Relative Permittivity" Version="0" >
          <BriefDescription>Real Component of Relative Permittivity</BriefDescription>
          <DefaultValue>1.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="false">0</Min>
          </RangeInfo>
        </Double>
        <Double Name="ImgEpsilon" Label="Imaginary Relative Permittivity" Version="0" Optional="true" >
          <BriefDescription>Imaginary Component of Relative Permittivity associated with material loss</BriefDescription>
          <DefaultValue>0.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0</Min>
          </RangeInfo>
        </Double>
        <Double Name="Mu" Label="Relative Permeability" Version="0" >
          <BriefDescription>Real Component of Relative Permeability</BriefDescription>
          <DefaultValue>1.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="false">0</Min>
          </RangeInfo>
        </Double>
        <Double Name="ImgMu" Label="Imaginary Relative Permeability" Version="0" Optional="true" >
          <BriefDescription>Imaginary Component of Relative Permeability associated with material loss</BriefDescription>
          <DefaultValue>0.0</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">0</Min>
          </RangeInfo>
        </Double>
       </ItemDefinitions>
   </AttDef>
  </Definitions>

  <!--********** Workflow Views ***********-->
  <Views>
    <View Type="Group" Title="SimBuilder" TopLevel="true" TabPosition="North">
      <DefaultColor>1., 1., 0.5, 1.</DefaultColor>
      <InvalidColor>1, 0.5, 0.5, 1</InvalidColor>
      <AdvancedFontEffects />
      <Views>
        <View Title="Boundary Conditions" />
        <View Title="Ports" />
        <View Title="Materials" />
        <View Title="Analysis" />
      </Views>
    </View>

    <View Type="Group" Title="Boundary Conditions" Style="Tiled">
      <Views>
        <View Title="HFormulation" />
        <View Title="Surface Properties" />
      </Views>
    </View>
    <View Type="Instanced" Title="HFormulation">
      <InstancedAttributes>
        <Att Name="HForumulation" Type="HFormulation" />
      </InstancedAttributes>
    </View>
    <View Type="Attribute" Title="Surface Properties" ModelEntityFilter="f">
      <AttributeTypes>
        <Att Type="SurfaceProperty" />
      </AttributeTypes>
    </View>

    <View Type="Attribute" Title="Ports" ModelEntityFilter="f">
      <AttributeTypes>
        <Att Type="Port" />
      </AttributeTypes>
    </View>
    <View Type="Attribute" Title="Materials" ModelEntityFilter="r">
      <AttributeTypes>
        <Att Type="Material" />
      </AttributeTypes>
    </View>
    <View Type="Group" Title="Analysis" Style="Tiled">
      <Views>
        <View Title="Tolerant" />
        <View Title="FiniteElement" />
        <View Title="EigenSolver" />
        <View Title="Post Process" />
        <View Title="High Order Regions" />
      </Views>
    </View>
    <View Type="Instanced" Title="Tolerant">
      <InstancedAttributes>
        <Att Name="Tolerant" Type="Tolerant" />
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="FiniteElement">
      <InstancedAttributes>
        <Att Name="Finite Element Info" Type="FEInfo" />
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="EigenSolver">
      <InstancedAttributes>
        <Att Name="EigenSolver" Type="EigenSolver" />
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Post Process">
      <InstancedAttributes>
        <Att Name="PostProcess" Type="PostProcess" />
      </InstancedAttributes>
    </View>
    <View Type="Attribute" Title="High Order Regions" ModelEntityFilter="r">
      <AttributeTypes>
        <Att Type="RegionHighOrder" />
      </AttributeTypes>
    </View>
  </Views>
</SMTK_AttributeSystem>
