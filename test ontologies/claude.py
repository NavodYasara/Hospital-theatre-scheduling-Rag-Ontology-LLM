from owlready2 import *
from datetime import datetime, time

# Create ontology
onto = get_ontology("http://test.org/hospital.owl")

with onto:
    # Base Classes
    class Person(Thing):
        """Superclass for all human actors"""
        pass
    
    class Location(Thing):
        """Superclass for all physical locations"""
        pass
    
    class ClinicalProcess(Thing):
        """Superclass for clinical processes"""
        pass
    
    class Resource(Thing):
        """Superclass for hospital resources"""
        pass
    
    # Conflict Detection Classes
    class SchedulingConflict(Thing):
        """Base class for scheduling conflicts"""
        pass
    
    class EquipmentConflict(SchedulingConflict):
        """Equipment double-booking conflict"""
        pass
    
    class TheatreConflict(SchedulingConflict):
        """Theatre double-booking conflict"""
        pass
    
    class SpecializationMismatch(SchedulingConflict):
        """Surgeon working in wrong theatre type"""
        pass
    
    class hasRecoverySchedule(Thing):
        """Marker class for recovery scheduling"""
        pass
    
    # Person Subclasses
    class Staff(Person):
        pass
    
    class Surgeon(Staff):
        pass
    
    class Anesthetist(Staff):
        pass
    
    class Patient(Person):
        pass
    
    # Location Subclasses
    class Theatre(Location):
        pass
    
    class Ward(Location):
        pass
    
    class RecoveryRoom(Location):
        pass
    
    # Clinical Process Subclasses
    class MedicalProcedure(ClinicalProcess):
        pass
    
    class Surgery(MedicalProcedure):
        pass
    
    class TimeSlot(ClinicalProcess):
        pass
    
    # Resource Subclasses
    class SurgicalEquipment(Resource):
        pass
    
    # Object Properties
    class performs_operation(ObjectProperty):
        domain = [Surgeon]
        range = [Surgery]
    
    class requires_theatre_type(ObjectProperty):
        domain = [Surgery]
        range = [Theatre]
    
    class requires_equipment(ObjectProperty):
        domain = [Surgery]
        range = [SurgicalEquipment]
    
    class is_assigned_to(ObjectProperty):
        domain = [Patient]
        range = [TimeSlot]
    
    class has_timeslot(ObjectProperty):
        domain = [Surgery]
        range = [TimeSlot]
    
    class has_temporal_overlap(ObjectProperty):
        domain = [TimeSlot]
        range = [TimeSlot]
        symmetric = True
    
    class has_assigned_staff(ObjectProperty):
        domain = [Surgery]
        range = [Staff]
    
    class admitted_to(ObjectProperty):
        domain = [Patient]
        range = [Ward]
    
    class assigned_to_recovery(ObjectProperty):
        domain = [Patient]
        range = [RecoveryRoom]
    
    class works_in_theatre(ObjectProperty):
        domain = [Staff]
        range = [Theatre]
    
    # Data Properties
    class has_license_number(DataProperty):
        domain = [Surgeon]
        range = [str]
    
    class estimated_duration(DataProperty):
        domain = [Surgery]
        range = [int]
    
    class is_emergency(DataProperty):
        domain = [Surgery]
        range = [bool]
    
    class start_time(DataProperty):
        domain = [TimeSlot]
        range = [str]  # Changed from time to str for OWL compatibility
    
    class end_time(DataProperty):
        domain = [TimeSlot]
        range = [str]  # Changed from time to str for OWL compatibility
    
    class duration(DataProperty):
        domain = [TimeSlot]
        range = [int]

# Create Instances

# Phase 1: TimeSlots
TS1 = onto.TimeSlot("TimeSlot_08_00")
TS1.start_time = ["08:00"]
TS1.end_time = ["10:30"]
TS1.duration = [150]

TS2 = onto.TimeSlot("TimeSlot_10_45")
TS2.start_time = ["10:45"]
TS2.end_time = ["13:15"]
TS2.duration = [150]

TS3 = onto.TimeSlot("TimeSlot_14_00")
TS3.start_time = ["14:00"]
TS3.end_time = ["16:30"]
TS3.duration = [150]

TS4 = onto.TimeSlot("TimeSlot_16_45")
TS4.start_time = ["16:45"]
TS4.end_time = ["19:15"]
TS4.duration = [150]

# Establish temporal overlaps
TS1.has_temporal_overlap = [TS2]
TS2.has_temporal_overlap = [TS1]
TS3.has_temporal_overlap = [TS4]
TS4.has_temporal_overlap = [TS3]

# Phase 2: Theatres
NeuroTheatre = onto.Theatre("Neuro_Theatre")
OrthoTheatre = onto.Theatre("Ortho_Theatre")
CardioTheatre = onto.Theatre("Cardio_Theatre")
GeneralTheatre = onto.Theatre("General_Theatre")

# Phase 3: Surgeons
NeuroSurgeon = onto.Surgeon("Dr_Smith")
NeuroSurgeon.has_license_number = ["NS12345"]
NeuroSurgeon.works_in_theatre = [NeuroTheatre]

OrthopedicSurgeon = onto.Surgeon("Dr_Johnson")
OrthopedicSurgeon.has_license_number = ["OS67890"]
OrthopedicSurgeon.works_in_theatre = [OrthoTheatre]

CardiothoracicSurgeon = onto.Surgeon("Dr_Williams")
CardiothoracicSurgeon.has_license_number = ["CS78901"]
CardiothoracicSurgeon.works_in_theatre = [CardioTheatre]

GeneralSurgeon = onto.Surgeon("Dr_Brown")
GeneralSurgeon.has_license_number = ["GS34567"]
GeneralSurgeon.works_in_theatre = [GeneralTheatre]


# Phase 5: Anesthetists
Anesthetist1 = onto.Anesthetist("Anesthetist_Michael")
Anesthetist1.works_in_theatre = [NeuroTheatre]

Anesthetist2 = onto.Anesthetist("Anesthetist_David")
Anesthetist2.works_in_theatre = [OrthoTheatre]

# Phase 6: Equipment
NeuroScope = onto.SurgicalEquipment("Neuro_Scope")
CardiacMonitor = onto.SurgicalEquipment("Cardiac_Monitor")
BypassMachine = onto.SurgicalEquipment("Bypass_Machine")
HipProsthesis = onto.SurgicalEquipment("Hip_Prosthesis")
SurgicalDrill = onto.SurgicalEquipment("Surgical_Drill")
Laparoscope = onto.SurgicalEquipment("Laparoscope")

# Phase 7: Surgeries
BrainSurgery = onto.Surgery("Brain_Surgery")
BrainSurgery.estimated_duration = [180]
BrainSurgery.is_emergency = [True]
BrainSurgery.requires_theatre_type = [NeuroTheatre]
BrainSurgery.requires_equipment = [NeuroScope]
BrainSurgery.has_timeslot = [TS1]
BrainSurgery.performs_operation = [NeuroSurgeon]


CardiacSurgery = onto.Surgery("Cardiac_Bypass_Surgery")
CardiacSurgery.estimated_duration = [240]
CardiacSurgery.is_emergency = [False]
CardiacSurgery.requires_theatre_type = [CardioTheatre]
CardiacSurgery.requires_equipment = [CardiacMonitor, BypassMachine]
CardiacSurgery.has_timeslot = [TS2]
CardiacSurgery.performs_operation = [CardiothoracicSurgeon]

OrthopedicSurgery = onto.Surgery("Hip_Replacement_Surgery")
OrthopedicSurgery.estimated_duration = [120]
OrthopedicSurgery.is_emergency = [False]
OrthopedicSurgery.requires_theatre_type = [OrthoTheatre]
OrthopedicSurgery.requires_equipment = [HipProsthesis, SurgicalDrill]
OrthopedicSurgery.has_timeslot = [TS3]
OrthopedicSurgery.performs_operation = [OrthopedicSurgeon]

GeneralSurgery = onto.Surgery("Appendectomy")
GeneralSurgery.estimated_duration = [90]
GeneralSurgery.is_emergency = [True]
GeneralSurgery.requires_theatre_type = [GeneralTheatre]
GeneralSurgery.requires_equipment = [Laparoscope]
GeneralSurgery.has_timeslot = [TS4]
GeneralSurgery.performs_operation = [GeneralSurgeon]

# Phase 8: Wards
NeuroWard = onto.Ward("Neurology_Ward")
CardioWard = onto.Ward("Cardiology_Ward")
OrthoWard = onto.Ward("Orthopedic_Ward")
GeneralWard = onto.Ward("General_Ward")

# Phase 9: Recovery Rooms
RecoveryRoom1 = onto.RecoveryRoom("Recovery_Room_A")
RecoveryRoom2 = onto.RecoveryRoom("Recovery_Room_B")
RecoveryRoom3 = onto.RecoveryRoom("Recovery_Room_C")

# Phase 10: Patients
Patient1 = onto.Patient("Patient_John_Doe")
Patient1.is_assigned_to = [TS1]
Patient1.admitted_to = [NeuroWard]
Patient1.assigned_to_recovery = [RecoveryRoom1]

Patient2 = onto.Patient("Patient_Mary_Smith")
Patient2.is_assigned_to = [TS2]
Patient2.admitted_to = [CardioWard]
Patient2.assigned_to_recovery = [RecoveryRoom2]

Patient3 = onto.Patient("Patient_Robert_Johnson")
Patient3.is_assigned_to = [TS3]
Patient3.admitted_to = [OrthoWard]
Patient3.assigned_to_recovery = [RecoveryRoom3]

Patient4 = onto.Patient("Patient_Linda_Williams")
Patient4.is_assigned_to = [TS4]
Patient4.admitted_to = [GeneralWard]
Patient4.assigned_to_recovery = [RecoveryRoom1]

# Phase 11: SWRL Rules for Conflict Detection
with onto:
    # Rule 1: Detect scheduling conflicts (surgeon has overlapping surgeries)
    rule1 = Imp()
    rule1.set_as_rule("""
        Surgeon(?s), performs_operation(?s, ?op1), performs_operation(?s, ?op2),
        has_timeslot(?op1, ?t1), has_timeslot(?op2, ?t2),
        has_temporal_overlap(?t1, ?t2), differentFrom(?op1, ?op2)
        -> SchedulingConflict(?s)
    """)
    
    # Rule 2: Equipment conflict detection
    rule2 = Imp()
    rule2.set_as_rule("""
        requires_equipment(?s1, ?e), requires_equipment(?s2, ?e),
        has_timeslot(?s1, ?t1), has_timeslot(?s2, ?t2),
        has_temporal_overlap(?t1, ?t2), differentFrom(?s1, ?s2)
        -> EquipmentConflict(?e)
    """)
    
    # Rule 3: Theatre conflict detection
    rule3 = Imp()
    rule3.set_as_rule("""
        requires_theatre_type(?s1, ?th), requires_theatre_type(?s2, ?th),
        has_timeslot(?s1, ?t1), has_timeslot(?s2, ?t2),
        has_temporal_overlap(?t1, ?t2), differentFrom(?s1, ?s2)
        -> TheatreConflict(?th)
    """)
    
    # Rule 4: Specialization mismatch detection
    rule4 = Imp()
    rule4.set_as_rule("""
        Surgeon(?s), performs_operation(?s, ?op),
        requires_theatre_type(?op, ?th), works_in_theatre(?s, ?wt),
        differentFrom(?th, ?wt)
        -> SpecializationMismatch(?s)
    """)
    
    # Rule 5: Recovery schedule tracking
    rule5 = Imp()
    rule5.set_as_rule("""
        Patient(?p), is_assigned_to(?p, ?t), assigned_to_recovery(?p, ?r)
        -> hasRecoverySchedule(?p)
    """)

# Save ontology
onto.save(file="ontology/hospital.owl", format="rdfxml")
print("✅ Ontology saved successfully to ontology/hospital.owl")

# Run reasoner
try:
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    print("✅ Reasoner executed successfully!")
    
    # Check for conflicts
    print("\n=== CONFLICT DETECTION RESULTS ===")
    
    scheduling_conflicts = list(onto.SchedulingConflict.instances())
    print(f"\n📋 Scheduling Conflicts: {len(scheduling_conflicts)}")
    for conflict in scheduling_conflicts:
        print(f"  - {conflict.name}")
    
    equipment_conflicts = list(onto.EquipmentConflict.instances())
    print(f"\n⚙️  Equipment Conflicts: {len(equipment_conflicts)}")
    for conflict in equipment_conflicts:
        print(f"  - {conflict.name}")
    
    theatre_conflicts = list(onto.TheatreConflict.instances())
    print(f"\n🏥 Theatre Conflicts: {len(theatre_conflicts)}")
    for conflict in theatre_conflicts:
        print(f"  - {conflict.name}")
    
    specialization_mismatches = list(onto.SpecializationMismatch.instances())
    print(f"\n🔍 Specialization Mismatches: {len(specialization_mismatches)}")
    for mismatch in specialization_mismatches:
        print(f"  - {mismatch.name}")
    
    recovery_schedules = list(onto.hasRecoverySchedule.instances())
    print(f"\n🛏️  Recovery Schedules: {len(recovery_schedules)}")
    for schedule in recovery_schedules:
        print(f"  - {schedule.name}")
    
except Exception as e:
    print(f"❌ Reasoner error: {e}")
    print("Note: Pellet reasoner may have issues with complex SWRL rules")