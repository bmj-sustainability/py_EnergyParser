"""When operating on IDF objects, it is sometimes useful to delete everything EXCEPT for the following classes 
Expressed as a dict containing sets of class names
"""

#from ProjectScripts.generate_variants import *





kept_classes_dict =  {

                      
        'geometryAndHVAC_LIDL_Baseline': set([
                          # Control ##################
                          'Version',
                          'SimulationControl',
                          'Building',
                          'ShadowCalculation',
                          'Site:Location',
                          'SizingPeriod:DesignDay',
                          'RunPeriod',
                          'RunPeriodControl:DaylightSavingTime',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:Deep',
                          'Site:GroundTemperature:Shallow',
                          'Site:GroundReflectance',
                          'Site:GroundReflectance:SnowModifier',                          
                          
                          # Schedules #################
                          'ScheduleTypeLimits',
                          'Schedule:Day:Hourly',
                          'Schedule:Week:Daily',
                          'Schedule:Compact',
               
                           # Surface Construction Elements ##################
                          'Material',
                          'Material:NoMass',
                          'Material:InfraredTransparent',
                          'Material:AirGap',
                          'WindowMaterial:Glazing',
                          'WindowMaterial:Gas', 
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Shade',
                          'MaterialProperty:GlazingSpectralData',
                          'Construction',
                          
                          # Surfaces
                          'Zone',
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'WindowProperty:ShadingControl',
                          'WindowProperty:FrameAndDivider',
                          'Shading:Building:Detailed',
                          
                          # Advanced Surfaces
                          'SurfaceProperty:OtherSideCoefficients',
                          
                          # Loads ######################
                          'People',
                          'Lights',
                          'ElectricEquipment',          
                          'ZoneInfiltration:DesignFlowRate',
                        
                          # Daylighting
                          'Daylighting:Controls',
                          'OutputControl:IlluminanceMap:Style',
                          
                          # Zone Airflow
                          #'ZoneInfiltration:DesignFlowRate',
                          
                          # HVAC Design Objects
                          'DesignSpecification:OutdoorAir',
                          'DesignSpecification:ZoneAirDistribution',
                          'Sizing:Parameters',
                          'Sizing:Zone',
                          'Sizing:System',
                          'Sizing:Plant',
                          
                          # Zone HVAC Controls and Thermostats
                          #'ZoneControl:Humidistat',
                          'ZoneControl:Thermostat',
                          #'ZoneControl:Thermostat:OperativeTemperature',
                          'ThermostatSetpoint:DualSetpoint',
                          
                          # Zone HVAC Air Loop Terminal Units

                          # Zone HVAC Forced Air Units
                          'ZoneHVAC:PackagedTerminalHeatPump',
                          
                          # HVAC
                          'ZoneHVAC:EquipmentConnections',
                          
                          # Zone HVAC Air Loop Terminal Units
                          'AirTerminal:SingleDuct:Uncontrolled',

                          
                          # Zone HVAC Equipment Connections
                          'ZoneHVAC:EquipmentConnections',
                          'ZoneHVAC:EquipmentList',
                          
                          # Fans
                          'Fan:OnOff',
                          
                          # Coils
                          'Coil:Cooling:DX:SingleSpeed',
                          'Coil:Heating:DX:SingleSpeed',
                          'Coil:Heating:Electric',
                          
                          # Heat Recovery
                          'HeatExchanger:AirToAir:SensibleAndLatent',
                          
                          # Unitary Equipment
                          'AirLoopHVAC:UnitaryHeatPump:AirToAir',
                          
                          # Controllers
                          'Controller:OutdoorAir',
                          'AirLoopHVAC:ControllerList',

                          
                          # Air Distribution
                          'AirLoopHVAC',
                          'AirLoopHVAC:OutdoorAirSystem:EquipmentList',
                          'AirLoopHVAC:OutdoorAirSystem',
                          'OutdoorAir:Mixer',
                          'AirLoopHVAC:ZoneSplitter',
                          'AirLoopHVAC:SupplyPath',
                          'AirLoopHVAC:ZoneMixer',
                          'AirLoopHVAC:ReturnPath',
                          
                          
                          # Node-Branch Management
                          'Branch',   
                          'BranchList',                          
                          'NodeList',
                          'OutdoorAir:Nodelist',
                          
                          # System Availability Managers
                          'AvailabilityManager:Scheduled',
                          'AvailabilityManagerAssignmentList',
                          
                          # Setpoint Managers
                          'SetpointManager:Scheduled',    
                          
                          # Performance Curves
                          'Curve:Quadratic',
                          'Curve:Cubic',
                          'Curve:Exponent',
                          'Curve:Biquadratic',
                          
                          ]),      
                      


                    
        'TRNSYS' :  set([
                         'Building'
                         'Zone',
                         'BuildingSurface:Detailed',                            
                         'FenestrationSurface:Detailed',
                         'SurfaceProperty:OtherSideCoefficients',
                         'GlobalGeometryRules',
                         'Construction',
                         'WindowProperty:ShadingControl'
                         ]),
        
        'MoreClassesTEMP' : set([
                          # Geometry ##################
                          'Zone',                          
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'Shading:Building:Detailed',

                          # Loads ######################
                          'People',
                          'ElectricEquipment',          
                          'Lights',
                          'Schedule:Compact',
                          'ZoneInfiltration:DesignFlowRate',
                          'ScheduleTypeLimits',
                                          
                           # Materials ##################
                          'Material:AirGap',
                          'Material:InfraredTransparent',
                          'WindowMaterial:Gas', 
                          'Material:NoMass',
                          'Material',
                          'Construction',
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Glazing',
                          ]),
                          
        'onlyGeometry' : set([
                          # Geometry ##################
                          'Zone',                          
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'Shading:Building:Detailed',
                          ]),      
        'noHVAC': set([   
                          # Control ##################
                          'Version',
                          'SimulationControl',
                          'Building',
                          'ShadowCalculation',
                          'Site:Location',
                          'SizingPeriod:DesignDay',
                          'RunPeriod',
                          'RunPeriodControl:DaylightSavingTime',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:Deep',
                          'Site:GroundTemperature:Shallow',
                          'Site:GroundReflectance',
                          'Site:GroundReflectance:SnowModifier',                          
                          
                          # Schedules #################
                          'ScheduleTypeLimits',
                          'Schedule:Day:Hourly',
                          'Schedule:Week:Daily',
                          'Schedule:Compact',
               
                           # Surface Construction Elements ##################
                          'Material',
                          'Material:NoMass',
                          'Material:InfraredTransparent',
                          'Material:AirGap',
                          'WindowMaterial:Glazing',
                          'WindowMaterial:Gas', 
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Shade',
                          'MaterialProperty:GlazingSpectralData',
                          'Construction',
                          
                          # Surfaces
                          'Zone',
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'WindowProperty:ShadingControl',
                          'WindowProperty:FrameAndDivider',
                          'Shading:Building:Detailed',
                          
                          # Advaced Surfaces
                          'SurfaceProperty:OtherSideCoefficients',
                          
                          # Loads ######################
                          'People',
                          'Lights',
                          'ElectricEquipment',          
                          'ZoneInfiltration:DesignFlowRate',
                        
                          # Daylighting
                          'Daylighting:Controls',
                          'OutputControl:IlluminanceMap:Style'
                          
                          # Zone Airflow
                          #'ZoneInfiltration:DesignFlowRate',
                          
                          # HVAC Design Objects
                          #'DesignSpecification:OutdoorAir',
                          #'DesignSpecification:ZoneAirDistribution',
                          #'Sizing:Zone',
                          'Sizing:System',
                          'Sizing:Plant',
                          
                          # Zone HVAC Controls and Thermostats
                          #'ZoneControl:Humidistat',
                          #'ZoneControl:Thermostat',
                          #'ZoneControl:Thermostat:OperativeTemperature',
                          #'ThermostatSetpoint:DualSetpoint',
                          
                          
                          # HVAC
                          #'ZoneHVAC:EquipmentConnections',
                          
                          ]),  

        'noHVAC_LIDL_Baseline': set([   
                          # Control ##################
                          'Version',
                          'SimulationControl',
                          'Building',
                          'ShadowCalculation',
                          'Site:Location',
                          'SizingPeriod:DesignDay',
                          'RunPeriod',
                          'RunPeriodControl:DaylightSavingTime',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:Deep',
                          'Site:GroundTemperature:Shallow',
                          'Site:GroundReflectance',
                          'Site:GroundReflectance:SnowModifier',                          
                          
                          # Schedules #################
                          'ScheduleTypeLimits',
                          'Schedule:Day:Hourly',
                          'Schedule:Week:Daily',
                          'Schedule:Compact',
               
                           # Surface Construction Elements ##################
                          'Material',
                          'Material:NoMass',
                          'Material:InfraredTransparent',
                          'Material:AirGap',
                          'WindowMaterial:Glazing',
                          'WindowMaterial:Gas', 
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Shade',
                          'MaterialProperty:GlazingSpectralData',
                          'Construction',
                          
                          # Surfaces
                          'Zone',
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'WindowProperty:ShadingControl',
                          'WindowProperty:FrameAndDivider',
                          'Shading:Building:Detailed',
                          
                          # Advaced Surfaces
                          'SurfaceProperty:OtherSideCoefficients',
                          
                          # Loads ######################
                          'People',
                          'Lights',
                          'ElectricEquipment',          
                          'ZoneInfiltration:DesignFlowRate',
                        
                          # Daylighting
                          'Daylighting:Controls',
                          'OutputControl:IlluminanceMap:Style'
                          
                          # Zone Airflow
                          #'ZoneInfiltration:DesignFlowRate',
                          
                          # HVAC Design Objects
                          #'DesignSpecification:OutdoorAir',
                          #'DesignSpecification:ZoneAirDistribution',
                          #'Sizing:Zone',
                          'Sizing:System',
                          'Sizing:Plant',
                          
                          # Zone HVAC Controls and Thermostats
                          #'ZoneControl:Humidistat',
                          #'ZoneControl:Thermostat',
                          #'ZoneControl:Thermostat:OperativeTemperature',
                          #'ThermostatSetpoint:DualSetpoint',
                          
                          
                          # HVAC
                          #'ZoneHVAC:EquipmentConnections',
                          
                          ]),  
                      
                      
        'geometryAndHVAC_LIDL_Proposed': set([
                          # Control ##################
                          'Version',
                          'SimulationControl',
                          'Building',
                          'ShadowCalculation',
                          'Site:Location',
                          'SizingPeriod:DesignDay',
                          'RunPeriod',
                          'RunPeriodControl:DaylightSavingTime',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:BuildingSurface',
                          'Site:GroundTemperature:Deep',
                          'Site:GroundTemperature:Shallow',
                          'Site:GroundReflectance',
                          'Site:GroundReflectance:SnowModifier',                          
                          
                          # Schedules #################
                          'ScheduleTypeLimits',
                          'Schedule:Day:Hourly',
                          'Schedule:Week:Daily',
                          'Schedule:Compact',
               
                           # Surface Construction Elements ##################
                          'Material',
                          'Material:NoMass',
                          'Material:InfraredTransparent',
                          'Material:AirGap',
                          'WindowMaterial:Glazing',
                          'WindowMaterial:Gas', 
                          'WindowMaterial:SimpleGlazingSystem',
                          'WindowMaterial:Shade',
                          'MaterialProperty:GlazingSpectralData',
                          'Construction',
                          
                          # Surfaces
                          'Zone',
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'GlobalGeometryRules',
                          'WindowProperty:ShadingControl',
                          'WindowProperty:FrameAndDivider',
                          'Shading:Building:Detailed',
                          
                          # Advanced Surfaces
                          'SurfaceProperty:OtherSideCoefficients',
                          
                          # Loads ######################
                          'People',
                          'Lights',
                          'ElectricEquipment',          
                          'ZoneInfiltration:DesignFlowRate',
                        
                          # Daylighting
                          'Daylighting:Controls',
                          'OutputControl:IlluminanceMap:Style',
                          
                          # Zone Airflow
                          #'ZoneInfiltration:DesignFlowRate',
                          
                          # HVAC Design Objects
                          'DesignSpecification:OutdoorAir',
                          'DesignSpecification:ZoneAirDistribution',
                          'Sizing:Parameters',
                          'Sizing:Zone',
                          'Sizing:System',
                          'Sizing:Plant',
                          
                          # Zone HVAC Forced Air Units
                          'ZoneHVAC:PackagedTerminalHeatPump',
                          
                          # Zone HVAC Controls and Thermostats
                          #'ZoneControl:Humidistat',
                          'ZoneControl:Thermostat',
                          #'ZoneControl:Thermostat:OperativeTemperature',
                          'ThermostatSetpoint:DualSetpoint',
                          # Zone HVAC Air Loop Terminal Units
                          
                          # HVAC
                          'ZoneHVAC:EquipmentConnections',
                          
                          # Zone HVAC Air Loop Terminal Units
                          'AirTerminal:SingleDuct:Uncontrolled',

                          
                          # Zone HVAC Equipment Connections
                          'ZoneHVAC:EquipmentConnections',
                          'ZoneHVAC:EquipmentList',
                          
                          # Fans
                          'Fan:ConstantVolume',
                          
                          # Coils
                          'Coil:Cooling:DX:SingleSpeed',
                          'Coil:Cooling:DX:TwoStageWithHumidityControlMode',
                          'CoilPerformance:DX:Cooling',

                          'Coil:Heating:DX:SingleSpeed',
                          'Coil:Heating:Electric',
                          
                          'CoilSystem:Cooling:DX',
                          
                          # Heat Recovery
                          'HeatExchanger:AirToAir:SensibleAndLatent',
                          
                          # Unitary Equipment
                          'AirLoopHVAC:UnitaryHeatPump:AirToAir',
                          
                          # Controllers
                          'Controller:OutdoorAir',
                          'AirLoopHVAC:ControllerList',

                          
                          # Air Distribution
                          'AirLoopHVAC',
                          'AirLoopHVAC:OutdoorAirSystem:EquipmentList',
                          'AirLoopHVAC:OutdoorAirSystem',
                          'OutdoorAir:Mixer',
                          'AirLoopHVAC:ZoneSplitter',
                          'AirLoopHVAC:SupplyPath',
                          'AirLoopHVAC:ZoneMixer',
                          'AirLoopHVAC:ReturnPath',
                          
                          
                          # Node-Branch Management
                          'Branch',   
                          'BranchList',                          
                          'NodeList',
                          'OutdoorAir:Nodelist',
                          
                          # System Availability Managers
                          'AvailabilityManager:Scheduled',
                          'AvailabilityManagerAssignmentList',
                          
                          # Setpoint Managers
                          'SetpointManager:Scheduled',
                          'SetpointManager:MixedAir',
                          
                          # Performance Curves
                          'Curve:Quadratic',
                          'Curve:Cubic',
                          'Curve:Exponent',
                          'Curve:Biquadratic,',

                          ]),      
                      
                                        
        'geometryAndSpaceLoads' : set([
                          # Geometry ##################
                          'Zone',                          
                          'BuildingSurface:Detailed',                            
                          'FenestrationSurface:Detailed',
                          'Shading:Building:Detailed',
                          'ZoneInfiltration:DesignFlowRate',
                          'ElectricEquipment',
                          'Lights',
                          'People',
                          'ZoneList',
                          'ScheduleTypeLimits',
                          'Schedule:Day:Interval',
                          'Schedule:Week:Daily',
                          'Schedule:Year',
                          ]),                          


}
