from owlready2 import *
from datetime import datetime, time

# Create ontology
onto = get_ontology("http://test.org/hospital.owl")


with onto:
    # Base Classes
    class Person(Thing):pass #Superclass for all human actors
    class Location(Thing):pass #Superclass for all physical locations
    class ClinicalProcess(Thing):pass #Superclass for clinical processes
    class Resource(Thing):pass #Superclass for hospital resources
    class SchedulingConflict(Thing):pass # Conflict Detection Classes
    class hasRecoverySchedule(Thing):pass #Marker class for recovery scheduling
    class Severity(Thing):pass #Severity classification

    class TheatreConflict(SchedulingConflict):pass #Theatre double-booking conflict
    class SpecializationMismatch(SchedulingConflict):pass #Surgeon working in wrong theatre type
    
    # Person Subclasses
    class Staff(Person):pass #Superclass for all staff
    class Surgeon(Staff):pass #Surgeon
    class Anesthetist(Staff):pass #Anesthetist
    class Patient(Person):pass #Patient
    
    # Location Subclasses
    class Theatre(Location):pass #Theatre
    class Ward(Location):pass #Ward
    class RecoveryRoom(Location):pass #Recovery Room
    
    # Clinical Process Subclasses
    class MedicalProcedure(ClinicalProcess):pass #Medical Procedure
    class Surgery(MedicalProcedure):pass #Surgery
    class TimeSlot(ClinicalProcess):pass #TimeSlot
    
    
    # Object Properties
    class performs_operation(ObjectProperty):
        domain = [Surgeon];range = [Surgery] #Surgeon performs surgery
    class has_severity(ObjectProperty):
        domain = [Patient];range = [Severity] #Patient has severity
    class requires_theatre_type(ObjectProperty):
        domain = [Surgery];range = [Theatre] #Surgery requires theatre type
    class is_assigned_to(ObjectProperty):
        domain = [Patient];range = [TimeSlot] #Patient is assigned to timeslot
    class has_timeslot(ObjectProperty):
        domain = [Surgery];range = [TimeSlot] #Surgery has timeslot
    class has_temporal_overlap(ObjectProperty):
        domain = [TimeSlot];range = [TimeSlot];symmetric = True #Timeslots have temporal overlap
    class has_assigned_staff(ObjectProperty):
        domain = [Surgery];range = [Staff] #Surgery has assigned staff
    class admitted_to(ObjectProperty):
        domain = [Patient];range = [Ward] #Patient is admitted to ward
    class assigned_to_recovery(ObjectProperty):
        domain = [Patient];range = [RecoveryRoom] #Patient is assigned to recovery room
    class works_in_theatre(ObjectProperty):
        domain = [Staff];range = [Theatre]
    class undergoes_surgery(ObjectProperty): 
        domain = [Patient];range = [Surgery]
    
    # Data Properties
    class has_license_number(DataProperty):
        domain = [Surgeon];range = [str] #Surgeon has license number
    class severity_level(DataProperty):  # RENAMED from 'severity' to avoid confusion
        domain = [Severity];range = [str] #Severity level description
    class estimated_duration(DataProperty):
        domain = [Surgery];range = [int] #Surgery has estimated duration
    class is_emergency(DataProperty):
        domain = [Surgery];range = [bool] #Surgery is emergency (FIXED: was incorrectly used on Patient)
    class start_time(DataProperty):
        domain = [TimeSlot];range = [str] #TimeSlot start time
    class end_time(DataProperty):
        domain = [TimeSlot];range = [str] #TimeSlot end time
    class duration(DataProperty):
        domain = [TimeSlot];range = [int] #TimeSlot duration

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

TS5 = onto.TimeSlot("TimeSlot_19_30")
TS5.start_time = ["19:30"]
TS5.end_time = ["22:00"]
TS5.duration = [150]

TS6 = onto.TimeSlot("TimeSlot_22_45")
TS6.start_time = ["22:45"]
TS6.end_time = ["01:15"]  # FIXED: was "25:15" which is invalid
TS6.duration = [150]

# Severity Levels (FIXED: Now independent class with values)
Sev1 = onto.Severity("Severe")
Sev1.severity_level = ["Severe"]

Sev2 = onto.Severity("Moderate")
Sev2.severity_level = ["Moderate"]

Sev3 = onto.Severity("Mild")
Sev3.severity_level = ["Mild"]

Sev4 = onto.Severity("Minor")
Sev4.severity_level = ["Minor"]

# Establish temporal overlaps
TS1.has_temporal_overlap = [TS2]
TS2.has_temporal_overlap = [TS1]
TS3.has_temporal_overlap = [TS4]
TS4.has_temporal_overlap = [TS3]
TS5.has_temporal_overlap = [TS6] 
TS6.has_temporal_overlap = [TS5] 

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


# Phase 4: Anesthetists
Anesthetist1 = onto.Anesthetist("Anesthetist_Michael")
Anesthetist1.works_in_theatre = [NeuroTheatre]

Anesthetist2 = onto.Anesthetist("Anesthetist_David")
Anesthetist2.works_in_theatre = [OrthoTheatre]

Anesthetist3 = onto.Anesthetist("Anesthetist_Elijah")
Anesthetist3.works_in_theatre = [CardioTheatre]

Anesthetist4 = onto.Anesthetist("Anesthetist_Frank")
Anesthetist4.works_in_theatre = [GeneralTheatre]


# Phase 6: Surgeries 
BrainSurgery = onto.Surgery("Brain_Surgery")
BrainSurgery.estimated_duration = [180]
BrainSurgery.is_emergency = [True] 
BrainSurgery.requires_theatre_type = [NeuroTheatre]
BrainSurgery.has_timeslot = [TS1]
BrainSurgery.has_assigned_staff = [NeuroSurgeon, Anesthetist1]  
NeuroSurgeon.performs_operation = [BrainSurgery]

CardiacSurgery = onto.Surgery("Cardiac_Bypass_Surgery")
CardiacSurgery.estimated_duration = [240]
CardiacSurgery.is_emergency = [False] 
CardiacSurgery.requires_theatre_type = [CardioTheatre]
CardiacSurgery.has_timeslot = [TS2]
CardiacSurgery.has_assigned_staff = [CardiothoracicSurgeon, Anesthetist3] 
CardiothoracicSurgeon.performs_operation = [CardiacSurgery] 

OrthopedicSurgery = onto.Surgery("Hip_Replacement_Surgery")
OrthopedicSurgery.estimated_duration = [120]
OrthopedicSurgery.is_emergency = [False] 
OrthopedicSurgery.requires_theatre_type = [OrthoTheatre]
OrthopedicSurgery.has_timeslot = [TS3]
OrthopedicSurgery.has_assigned_staff = [OrthopedicSurgeon, Anesthetist2]  
OrthopedicSurgeon.performs_operation = [OrthopedicSurgery] 

GeneralSurgery = onto.Surgery("Appendectomy")
GeneralSurgery.estimated_duration = [90]
GeneralSurgery.is_emergency = [True] 
GeneralSurgery.requires_theatre_type = [GeneralTheatre]
GeneralSurgery.has_timeslot = [TS4]
GeneralSurgery.has_assigned_staff = [GeneralSurgeon, Anesthetist4]  
GeneralSurgeon.performs_operation = [GeneralSurgery] 

# Phase 7: Wards
NeuroWard = onto.Ward("Neurology_Ward")
CardioWard = onto.Ward("Cardiology_Ward")
OrthoWard = onto.Ward("Orthopedic_Ward")
GeneralWard = onto.Ward("General_Ward")

# Phase 8: Recovery Rooms
RecoveryRoom1 = onto.RecoveryRoom("Recovery_Room_A")
RecoveryRoom2 = onto.RecoveryRoom("Recovery_Room_B")
RecoveryRoom3 = onto.RecoveryRoom("Recovery_Room_C")

# Phase 9: Patients 
Patient1 = onto.Patient("Patient_John_Doe")
Patient1.is_assigned_to = [TS1]
Patient1.has_severity = [Sev1]
Patient1.admitted_to = [NeuroWard]
Patient1.assigned_to_recovery = [RecoveryRoom1]
Patient1.undergoes_surgery = [BrainSurgery] 

Patient2 = onto.Patient("Patient_Mary_Smith")
Patient2.is_assigned_to = [TS2]
Patient2.has_severity = [Sev2]
Patient2.admitted_to = [CardioWard]
Patient2.assigned_to_recovery = [RecoveryRoom2]
Patient2.undergoes_surgery = [CardiacSurgery] 

Patient3 = onto.Patient("Patient_Robert_Johnson")
Patient3.is_assigned_to = [TS3]
Patient3.has_severity = [Sev4]
Patient3.admitted_to = [OrthoWard]
Patient3.assigned_to_recovery = [RecoveryRoom3]
Patient3.undergoes_surgery = [OrthopedicSurgery] 

Patient4 = onto.Patient("Patient_Linda_Williams")
Patient4.is_assigned_to = [TS4]
Patient4.has_severity = [Sev1]
Patient4.admitted_to = [GeneralWard]
Patient4.assigned_to_recovery = [RecoveryRoom1]
Patient4.undergoes_surgery = [GeneralSurgery]  

Patient5 = onto.Patient("Patient_John_Williams")
Patient5.is_assigned_to = [TS5]
Patient5.has_severity = [Sev2]
Patient5.admitted_to = [GeneralWard]
Patient5.assigned_to_recovery = [RecoveryRoom1]
# No surgery assigned (waiting list)

Patient6 = onto.Patient("Patient_Sarah_Brown") 
Patient6.is_assigned_to = [TS6]
Patient6.has_severity = [Sev3]
Patient6.admitted_to = [GeneralWard]
Patient6.assigned_to_recovery = [RecoveryRoom1]
# No surgery assigned (waiting list)

# Phase 10: SWRL Rules for Conflict Detection
with onto:
    # Rule 1: Detect scheduling conflicts (surgeon has overlapping surgeries)
    rule1 = Imp()
    rule1.set_as_rule("""
        Surgeon(?s), performs_operation(?s, ?op1), performs_operation(?s, ?op2),
        has_timeslot(?op1, ?t1), has_timeslot(?op2, ?t2),
        has_temporal_overlap(?t1, ?t2), differentFrom(?op1, ?op2)
        -> SchedulingConflict(?s)
    """)
    
    # Rule 2: Theatre conflict detection
    rule2 = Imp()
    rule2.set_as_rule("""
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
print("\n📝 FIXES APPLIED:")
print("  ✅ Corrected performs_operation direction")
print("  ✅ Moved is_emergency from Patient to Surgery")

# Run reasoner
try:
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    print("\n✅ Reasoner executed successfully!")
    
    # Check for conflicts
    print("\n=== CONFLICT DETECTION RESULTS ===")
    
    scheduling_conflicts = list(onto.SchedulingConflict.instances())
    print(f"\n📋 Scheduling Conflicts: {len(scheduling_conflicts)}")
    for conflict in scheduling_conflicts:
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
    
    # Print statistics
    print("\n=== ONTOLOGY STATISTICS ===")
    print(f"Total Individuals: {len(list(onto.individuals()))}")
    print(f"Surgeons: {len(list(onto.Surgeon.instances()))}")
    print(f"Anesthetists: {len(list(onto.Anesthetist.instances()))}")
    print(f"Patients: {len(list(onto.Patient.instances()))}")
    print(f"Surgeries: {len(list(onto.Surgery.instances()))}")
    print(f"Theatres: {len(list(onto.Theatre.instances()))}")
    print(f"TimeSlots: {len(list(onto.TimeSlot.instances()))}")
    print(f"Wards: {len(list(onto.Ward.instances()))}")
    print(f"Recovery Rooms: {len(list(onto.RecoveryRoom.instances()))}")
    
except Exception as e:
    print(f"❌ Reasoner error: {e}")
    print("Note: Pellet reasoner may have issues with complex SWRL rules")
