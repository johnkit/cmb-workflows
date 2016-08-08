<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeSystem Version="2">
  <!-- Attribute Definitions-->
  <Definitions>
    <AttDef Type="solver" Label="Solver" BaseType="" Version="0">
      <ItemDefinitions>
        <Group Name="time" Label="Time">
          <ItemDefinitions>
            <Double Name="start-time" Label="Start Time">
              <DefaultValue>0.0</DefaultValue>
            </Double>
            <Double Name="end-time" Label="End Time">
              <DefaultValue>10.0</DefaultValue>
            </Double>
            <Double Name="grow-dt" Label="Timestep Growth Factor">
              <DefaultValue>2.0</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1.0</Min>
              </RangeInfo>
            </Double>
            <Double Name="dt-max" Label="Maximum Timestep Size">
              <DefaultValue>0.000488</DefaultValue>
              <RangeInfo>
                <Min Inclusive="false">0.0</Min>
              </RangeInfo>
            </Double>
            <Void Name="error-on-dt-change" Label="Error on DT Change" Optional="true" IsEnabledByDefault="true">
              <BriefDescription>Emit error message if the time step size changes</BriefDescription>
            </Void>
          </ItemDefinitions>
        </Group>
        <Group Name="hierarchy-integrator" Label="IBHierarchyIntegrator">
          <ItemDefinitions>
            <Int Name="num-cycles" Label="Number of Cycles (fixed-point iteration)">
              <DefaultValue>1</DefaultValue>
              <RangeInfo>
                <Min Inclusive="true">1</Min>
              </RangeInfo>
            </Int>
            <Double Name="regrid-cfl-interval" Label="Regrid CFL Interval">
              <DefaultValue>0.5</DefaultValue>
              <RangeInfo>
                <Minimum Inclusive="true">0.0</Minimum>
              </RangeInfo>
            </Double>
          </ItemDefinitions>
        </Group>
        <Group Name="fe-method" Label="IBFEMethod">
          <ItemDefinitions>
            <String Name="ib-delta-function" Label="IB Delta Function">
              <BriefDescription>type of smoothed delta function to use for Lagrangian-Eulerian interaction</BriefDescription>
              <DiscreteInfo DefaultIndex="1">
                <Value>IB_3</Value>
                <Value>IB_4</Value>
                <Value>IB_6</Value>
                <Value>PIECEWISE_LINEAR</Value>
                <Value>PIECEWISE_CUBIC</Value>
                <Value>BSPLINE_3</Value>
                <Value>BSPLINE_4</Value>
                <Value>BSPLINE_5</Value>
                <Value>BSPLINE_6</Value>
              </DiscreteInfo>
            </String>
            <Void Name="split-forces" Label="Split Forces" Optional="true" IsEnabledByDefault="false"></Void>
            <Void Name="use-jump-conditions" Label="Use Jump Conditions" Optional="true" IsEnabledByDefault="false"></Void>
            <Void Name="use-consistent-mass-matrix" Label="Use Consistent Mass Matrix" Optional="true" IsEnabledByDefault="true"></Void>
            <Double Name="ib-point-density" Label="IB Point Density">
              <DefaultValue>3.0</DefaultValue>
              <RangeInfo>
                <Minimum Inclusive="false">0.0</Minimum>
              </RangeInfo>
            </Double>
          </ItemDefinitions>
        </Group>
        <Group Name="solver" Label="Solver">
          <ItemDefinitions>
            <String Name="solver-type" Label="Solver Type">
              <ChildrenDefinitions>
                <Void Name="second-order-pressure-update" Label="Second Order Pressure Update" Optional="true" IsEnabledByDefault="true"></Void>
                <String Name="projection-method" Label="Projection Method">
                  <DiscreteInfo DefaultIndex="1">
                    <Value>PRESSURE_INCREMENT</Value>
                    <Value>PRESSURE_UPDATE</Value>
                  </DiscreteInfo>
                </String>
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="1">
                <Structure>
                  <Value>COLLOCATED</Value>
                  <Items>
                    <Item>projection-method</Item>
                    <Item>second-order-pressure-update</Item>
                  </Items>
                </Structure>
                <Value>STAGGERED</Value>
              </DiscreteInfo>
            </String>
            <String Name="convective-ts-type" Label="Convective Timestep Type">
              <DiscreteInfo DefaultIndex="0">
                <Value>ADAMS_BASHFORTH</Value>
                <Value>FOWARD_EULER</Value>
                <Value>MIDPOINT_RULE</Value>
                <Value>TRAPEZOIDAL_RULE</Value>
              </DiscreteInfo>
            </String>
            <String Name="convective-op-type" Label="Convective Discretization Type">
              <DiscreteInfo DefaultIndex="1">
                <Value>CENTERED</Value>
                <Value>PPM</Value>
              </DiscreteInfo>
            </String>
            <String Name="convective-diff-form" Label="Convective Difference Form">
              <DiscreteInfo DefaultIndex="0">
                <Value>ADVECTIVE</Value>
                <Value>CONSERVATIVE</Value>
                <Value>SKEW_SYMMETRIC</Value>
              </DiscreteInfo>
            </String>
            <Void Name="normalize-pressure" Label="Normalize Pressure" Optional="true" IsEnabledByDefault="false"></Void>
            <Double Name="cfl-max" Label="Maximum CFL Number">
              <BriefDescription>recommended &lt;= 0.5</BriefDescription>
              <DefaultValue>0.25</DefaultValue>
              <RangeInfo>
                <Minimum Inclusive="false">0.0</Minimum>
              </RangeInfo>
            </Double>
            <Group Name="vorticity-tagging" Label="Vorticity Tagging" Optional="true" IsEnabledByDefault="true">
              <ItemDefinitions>
                <Double Name="vorticity-rel-thresh" Label="Vorticity Relative Threshold(s)" Extensible="true" NumberOfRequiredValues="1">
                  <DefaultValue>0.01</DefaultValue>
                </Double>
                <Int Name="tag-buffer" Label="Tag Buffer(s)" Extensible="true" NumberOfRequiredValues="1">
                  <DefaultValue>1</DefaultValue>
                </Int>
              </ItemDefinitions>
            </Group>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeSystem>