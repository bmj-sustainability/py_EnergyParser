"""When operating on IDF objects, it is sometimes useful to delete everything EXCEPT for the following classes 
Expressed as a dict containing sets of class names
"""


#from ProjectScripts.generate_variants import *

keptClassesDict =  {
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
