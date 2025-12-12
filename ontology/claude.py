from owlready2 import *
from datetime import datetime, time

# Create ontology
onto = get_ontology("http://test.org/hospital.owl")

with onto:
    # Base Classes
    class Person(Thing):pass
    class Location(Thing):pass
    class ClinicalProcess(Thing):pass
    class Resource(Thing):pass
    class SchedulingConflict(Thing):pass
    class hasRecoverySchedule(Thing):pass #Marker class for recovery scheduling
    
    # Person Subclasses
    class Staff(Person):pass
    
    class Surgeon(Staff):pass
    class Anesthetist(Staff):pass   
    class Patient(Person):pass
    # Location Subclasses
    class Theatre(Location):pass
    class RecoveryRoom(Location):pass
    # Clinical Process Subclasses
    class Surgery(ClinicalProcess):pass
    class TimeSlot(ClinicalProcess):pass
    # Resource Subclasses
    class SurgicalEquipment(Resource):pass  
    # Conflict Detection Classes
    class EquipmentConflict(SchedulingConflict):pass
    class TheatreConflict(SchedulingConflict):pass
    class SpecializationMismatch(SchedulingConflict):pass #Surgeon working in wrong theatre type
    
    # Object Properties
    class performs_operation(ObjectProperty):
        domain = [Surgeon];range = [Surgery]
    class requires_theatre_type(ObjectProperty):
        domain = [Surgery];range = [Theatre]
    class requires_equipment(ObjectProperty):
        domain = [Surgery];range = [SurgicalEquipment]
    class is_assigned_to(ObjectProperty):
        domain = [Patient];range = [TimeSlot]    
    class has_timeslot(ObjectProperty):
        domain = [Surgery];range = [TimeSlot]    
    class has_temporal_overlap(ObjectProperty):
        domain = [TimeSlot];range = [TimeSlot]
    class has_assigned_staff(ObjectProperty):
        domain = [Surgery];range = [Staff]
    class assigned_to_recovery(ObjectProperty):
        domain = [Patient];range = [RecoveryRoom]
    class works_in_theatre(ObjectProperty):
        domain = [Staff];range = [Theatre]
    
    # Data Properties
    class has_license_number(DataProperty):
        domain = [Surgeon];range = [str]
    class estimated_duration(DataProperty):
        domain = [Surgery];range = [int]
    class is_emergency(DataProperty):
        domain = [Surgery];range = [bool]
    class start_time(DataProperty):
        domain = [TimeSlot];range = [str]
    class end_time(DataProperty):
        domain = [TimeSlot];range = [str]
    class duration(DataProperty):
        domain = [TimeSlot];range = [int]

# Create Individuals

    
    
# Save ontology
onto.save(file="ontology/hospital.owl", format="rdfxml")
print("✅ Ontology saved successfully to ontology/hospital.owl")