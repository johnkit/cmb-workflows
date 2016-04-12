<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Category and Analysis Information-->
  <Categories Default="Overland Flow"></Categories>
  <Analyses>
    <Analysis Type="Overland Flow">
      <Cat>Overland Flow</Cat>
    </Analysis>
  </Analyses>

  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="computation" Unique="true">
      <ItemDefinitions>
        <Group Name="computation-group" Label="Computation parameters">
          <ItemDefinitions>
            <Int Name="output-units" Label="Output units" Version="0" Optional="true" IsEnabledByDefault="false">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="Metric">METRIC</Value>
                <Value Enum="English">ENGLISH</Value>
              </DiscreteInfo>
            </Int>
            <Int Name="total-time" Label="Total time (min)" Version="0">
              <DefaultValue>500</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0</Min>
              </RangeInfo>
            </Int>

            <Int Name="time-step" Label="Time step (sec)" Version="0">
              <DefaultValue>10</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0</Min>
              </RangeInfo>
            </Int>
            <Double Name="event-min-flow" Label="Min flow end of event" Version="0">
              <DefaultValue>0.0</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">0.0</Min>
              </RangeInfo>
            </Double>
            <Group Name="end-time" Label="End Time" Version="0" Optional="true" IsEnabledByDefault="false">
              <ItemDefinitions>
                <Int Name="year" Label="Year" Version="0">
                  <DefaultValue>2050</DefaultValue>
                </Int>
                <Int Name="month" Label="Month">
                  <DiscreteInfo DefaultIndex="0">
                    <Value Enum="Jan">1</Value>
                    <Value Enum="Feb">2</Value>
                    <Value Enum="Mar">3</Value>
                    <Value Enum="Apr">4</Value>
                    <Value Enum="May">5</Value>
                    <Value Enum="Jun">6</Value>
                    <Value Enum="Jul">7</Value>
                    <Value Enum="Aug">8</Value>
                    <Value Enum="Sep">9</Value>
                    <Value Enum="Oct">10</Value>
                    <Value Enum="Nov">11</Value>
                    <Value Enum="Dec">12</Value>
                  </DiscreteInfo>
                </Int>
                <Int Name="day" Label="Day" Version="0">
                  <DefaultValue>1</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">1</Min>
                    <Max Inclusive="true">31</Max>
                  </RangeInfo>
                </Int>
                <Int Name="hour" Label="Hour" Version="0">
                  <DefaultValue>0</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">0</Min>
                    <Max Inclusive="true">23</Max>
                  </RangeInfo>
                </Int>
                <Int Name="minute" Label="Minute" Version="0">
                  <DefaultValue>0</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">0</Min>
                    <Max Inclusive="true">59</Max>
                  </RangeInfo>
                </Int>
              </ItemDefinitions>
            </Group>
            <Int Name="number-of-threads" Label="Number of Threads" Version="0" AdvanceLevel="1" Optional="true" IsEnabledByDefault="false">
              <DefaultValue>1</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0</Min>
              </RangeInfo>
            </Int>
          </ItemDefinitions>
        </Group>
        <Group Name="output-frequencies" Label="Output frequencies">
          <ItemDefinitions>
            <Int Name="map-frequency" Label="Map Frequency" Units="min" Version="0">
              <DefaultValue>5</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0</Min>
              </RangeInfo>
            </Int>
            <Int Name="hyd-frequency" Label="Hydrograph Frequency" Units="min" Version="0">
              <DefaultValue>5</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0</Min>
              </RangeInfo>
            </Int>
            <Int Name="map-type" Label="Output format">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="ASCII grid sequence">0</Value>
                <Value Enum="WMS gridded dataset">1</Value>
              </DiscreteInfo>
            </Int>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="overland-flow" Unique="true">
      <ItemDefinitions>
        <Group Name="overland-flow" Label="Overland flow">
          <Categories>
            <Cat>Overland Flow</Cat>
          </Categories>
          <ItemDefinitions>
            <String Name="computation-method" Label="Computation method">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="Explicit">EXPLICIT</Value>
                <Value Enum="ADE">ADE</Value>
                <Value Enum="ADE-PC">ADE-PC</Value>
              </DiscreteInfo>
            </String>
            <File Name="elevation-file" Label="Elevation File" Version="0" NumberOfRequiredValues="1" FileFilters="Elevation files (*.ele);;All files (*.*)" ShouldExist="true"></File>
            <Void Name="overbank flow" Label="Enable overbank flow" Version="0" Optional="true" IsEnabledByDefault="false"></Void>
            <Double Name="max-courant-number" Label="Max Courant Number" Optional="true" IsEnabledByDefault="false">
              <DefaultValue>0.06</DefaultValue>
            </Double>
            <File Name="initial-depth" Label="Initial depth file" Version="0" NumberOfRequiredValues="1" ShouldExist="true" FileFilters="Input hot start files (*.idp);;All files (*.*)" Optional="true" IsEnabledByDefault="false"></File>
            <File Name="read-ov-hotstart" Label="Input hot start file" Version="0" NumberOfRequiredValues="1" ShouldExist="true" FileFilters="Input hot start files (*.idp);;All files (*.*)" Optional="true" IsEnabledByDefault="false"></File>
            <Void Name="write-ov-hotstart" Label="Write final overland depths" Version="0" Optional="true" IsEnabledByDefault="false"></Void>
            <String Name="roughness" Label="Roughness model" Version="0" Optional="true" IsEnabledByDefault="false">
              <ChildrenDefinitions>
                <File Name="roughness-file" Label="Roughness File" Version="0" NumberOfRequiredValues="1" FileFilters="Roughness files (*.ovn);;All files (*.*)" ShouldExist="true"></File>
                <Double Name="mannings-n" Label="Manning's n" Version="0">
                  <DefaultValue>0.1</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">0.0</Min>
                    <Max Inclusive="true">1.0</Max>
                  </RangeInfo>
                </Double>
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="0">
                <Structure>
                  <Value Enum="File">ROUGHNESS</Value>
                  <Items>
                    <Item>roughness-file</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value Enum="Uniform">MANNING_N</Value>
                  <Items>
                    <Item>mannings-n</Item>
                  </Items>
                </Structure>
              </DiscreteInfo>
            </String>
            <Void Name="ov-boundary" Label="Apply overland boundaries" Version="0" Optional="true" IsEnabledByDefault="false">
              <BriefDescription>Do overland boundaries according to the OVERLAND_BOUNDARY table</BriefDescription>
            </Void>
            <File Name="embankment" Label="Embankment file" Version="0" NumberOfRequiredValues="1" ShouldExist="true" FileFilters="Embankment files (*.dik);;All files (*.*)" Optional="true" IsEnabledByDefault="false">
              <BriefDescription>Set up no-flow embankments between overland grid cells</BriefDescription>
            </File>
            <File Name="lowspot" Label="Lowspot file" Version="0" NumberOfRequiredValues="1" ShouldExist="true" FileFilters="Lowspot files (*.lsp);;All files (*.*)" Optional="true" IsEnabledByDefault="false">
              <BriefDescription>Set up low spots for overtopping on the embankments</BriefDescription>
            </File>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="grid" Unique="true">
      <ItemDefinitions>
        <Group Name="grid" Label="Grid">
          <ItemDefinitions>
            <Double Name="gridsize" Label="Grid size (m)">
              <DefaultValue>100.0</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0.0</Min>
              </RangeInfo>
            </Double>
            <Int Name="rows" Label="Rows">
              <DefaultValue>10
                <RangeInfo>
                  <Min Inclusive="true">1</Min>
                </RangeInfo>
              </DefaultValue>
            </Int>
            <Int Name="columns" Label="Colums">
              <DefaultValue>10
                <RangeInfo>
                  <Min Inclusive="true">1</Min>
                </RangeInfo>
              </DefaultValue>
            </Int>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="precipitation" Unique="true">
      <ItemDefinitions>
        <Group Name="precipitation" Label="Rainfall event(s)">
          <ItemDefinitions>
            <String Name="rainfall-events" Label="Format">
              <ChildrenDefinitions>
                <Double Name="intensity" Label="Intensity (mm/hr)">
                  <DefaultValue>10.0</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">0.0</Min>
                  </RangeInfo>
                </Double>
                <Int Name="duration" Label="Duration (min)">
                  <DefaultValue>60</DefaultValue>
                  <RangeInfo>
                    <Min Inclusive="true">0</Min>
                  </RangeInfo>
                </Int>
                <Group Name="start" Label="Start date/time">
                  <ItemDefinitions>
                    <Int Name="year" Label="Year">
                      <DefaultValue>2015</DefaultValue>
                      <RangeInfo>
                        <Min Inclusive="true">1900</Min>
                      </RangeInfo>
                    </Int>
                    <Int Name="month" Label="Month">
                      <DiscreteInfo DefaultIndex="0">
                        <Value Enum="Jan">1</Value>
                        <Value Enum="Feb">2</Value>
                        <Value Enum="Mar">3</Value>
                        <Value Enum="Apr">4</Value>
                        <Value Enum="May">5</Value>
                        <Value Enum="Jun">6</Value>
                        <Value Enum="Jul">7</Value>
                        <Value Enum="Aug">8</Value>
                        <Value Enum="Sep">9</Value>
                        <Value Enum="Oct">10</Value>
                        <Value Enum="Nov">11</Value>
                        <Value Enum="Dec">12</Value>
                      </DiscreteInfo>
                    </Int>
                    <Int Name="day" Label="Day">
                      <DefaultValue>1</DefaultValue>
                      <RangeInfo>
                        <Min Inclusive="true">1</Min>
                        <Max Inclusive="true">31</Max>
                      </RangeInfo>
                    </Int>
                    <Int Name="hour" Label="Hour">
                      <DefaultValue>12</DefaultValue>
                      <RangeInfo>
                        <Min Inclusive="true">0</Min>
                        <Max Inclusive="true">23</Max>
                      </RangeInfo>
                    </Int>
                    <Int Name="minute" Label="Minute">
                      <DefaultValue>0</DefaultValue>
                      <RangeInfo>
                        <Min Inclusive="true">0</Min>
                        <Max Inclusive="true">59</Max>
                      </RangeInfo>
                    </Int>
                  </ItemDefinitions>
                </Group>
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="0">
                <Structure>
                  <Value Enum="Uniform">uniform</Value>
                  <Items>
                    <Item>intensity</Item>
                    <Item>duration</Item>
                    <Item>start</Item>
                  </Items>
                </Structure>
              </DiscreteInfo>
            </String>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
  </Definitions>

  <!-- Workflow views-->
  <Views>
    <View Type="Group" Title="SimBuilder" TopLevel="true">
      <Views>
        <View Title="Job Control"></View>
        <View Title="Overland Flow"></View>
        <View Title="Grid"></View>
        <View Title="Precipitation"></View>
      </Views>
    </View>
    <View Type="Instanced" Title="Job Control">    
      <InstancedAttributes>
        <Att Name="Computation" Type="computation"></Att>
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Overland Flow">
      <InstancedAttributes>
        <Att Name="OverlandFlow" Type="overland-flow"></Att>
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Grid">
      <InstancedAttributes>
        <Att Name="Grid" Type="grid"></Att>
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Precipitation">
      <InstancedAttributes>
        <Att Name="Precipitation" Type="precipitation"></Att>
      </InstancedAttributes>
    </View>
  </Views>
</SMTK_AttributeSystem>