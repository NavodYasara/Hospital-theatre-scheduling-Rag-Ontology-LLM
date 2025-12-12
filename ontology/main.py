from owlready2 import *
from datetime import datetime, time
from owlready2 import Imp

# Create or load ontology
onto = get_ontology("ontology/hospital.owl")
onto.load()

onto = get_ontology("http://test.org/simple.owl")



with onto:
    # Base class
    class Person(Thing):pass # The superclass for all human actors.
    class Location(Thing):pass
    class ClinicalProcess(Thing):pass
    class Resource(Thing):pass
    class TimeConstraint(Thing): pass


    # Conflict Detection Class
    class SchedulingConflict(Thing):pass
    class EquipmentConflict(SchedulingConflict): pass
    class TheatreConflict(SchedulingConflict): pass
    class SpecializationMismatch(SchedulingConflict): pass
    class hasRecoverySchedule(Thing): pass  # For recovery rule
    
    # Subclasses
    class Staff(Person):pass
    class Surgeon(Staff):pass
    class Nurse(Staff):pass
    class Anesthetist(Staff):pass
    class Patient(Person):pass

    class Theatre(Location):pass
    class Ward(Location):pass
    class RecoveryRoom(Location):pass

    class MedicalProcedure(ClinicalProcess):pass
    class TimeSlot(ClinicalProcess):pass

    class SurgicalEquipment(Resource):pass
    class Surgery(MedicalProcedure):pass

    
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

    class hasSpecialty(ObjectProperty): 
        domain = [Surgeon]; 
        range = [str]  # "Neuro", "Cardio"
    class hasUrgency(DataProperty): 
        domain = [Patient]; 
        range = [str]  # "High", "Low"
    class supportsProcedure(ObjectProperty): 
        domain = [Theatre]; 
        range = [str]
    
    class isAvailable(ObjectProperty): 
        domain = [TimeSlot]; range = [Thing]  # Inferred
        range = [Thing]  # Inferred
        
    class compatibleWith(ObjectProperty): 
        domain = [Surgeon]
        range = [Surgery]  # Inferred

    class overlapsWith(ObjectProperty): 
        domain = [TimeSlot]; 
        range = [TimeSlot]; 
        symmetric = True
        
    # Additional Object Properties
       
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
           
    class hasQualification(ObjectProperty):
        domain = [Staff]    
        range = [str]
    
    class requiresQualification(ObjectProperty):
        domain = [Surgery]
        range = [str]

        
    # Data Properties

    class has_license_number(DataProperty):
        domain = [Surgeon]
        range = [str]
    
    class estimated_duration(DataProperty):
        domain = [Surgery]
        range = [int]  # duration in minutes

    class is_emergency(DataProperty):
        domain = [Surgery]
        range = [bool]
    
    class start_time(DataProperty):
        domain = [TimeSlot]
        range = [time]
    
    class end_time(DataProperty):
        domain = [TimeSlot]
        range = [time]
    
    class duration(DataProperty):
        domain = [TimeSlot]
        range = [int]  # duration in minutes
        
    class MinimumRecoveryTime(DataProperty):
        domain = [Surgery]
        range = [int]
        
    class hasPriority(DataProperty):
        domain = [Surgery]
        range = [int]
    
    
    
    
    # Create Instances (Individuals)
    
    # Phase 1: Create TimeSlot instances
    TS1 = onto.TimeSlot("TimeSlot_08_00")
    TS1.start_time = [time(8, 0)]
    TS1.end_time = [time(10, 30)]
    TS1.duration = [150]
    
    TS2 = onto.TimeSlot("TimeSlot_10_45")
    TS2.start_time = [time(10, 45)]
    TS2.end_time = [time(13, 15)]
    TS2.duration = [150]
    
    TS3 = onto.TimeSlot("TimeSlot_14_00")
    TS3.start_time = [time(14, 0)]
    TS3.end_time = [time(16, 30)]
    TS3.duration = [150]
    
    TS4 = onto.TimeSlot("TimeSlot_16_45")
    TS4.start_time = [time(16, 45)]
    TS4.end_time = [time(19, 15)]
    TS4.duration = [150]
    
    # Establish temporal overlaps (morning and afternoon slots don't overlap)
    TS1.has_temporal_overlap = [TS2]
    TS2.has_temporal_overlap = [TS1]
    TS3.has_temporal_overlap = [TS4]
    TS4.has_temporal_overlap = [TS3]
    
    # Phase 2: Define Theatres
    NeuroTheatre = onto.Theatre("Neuro_Theatre")
    OrthoTheatre = onto.Theatre("Ortho_Theatre")
    CardioTheatre = onto.Theatre("Cardio_Theatre")
    GeneralTheatre = onto.Theatre("General_Theatre")
    
    # Phase 3: Define Surgeons with specializations
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
    
    # Phase 4: Define Nurses
    Nurse1 = onto.Nurse("Nurse_Sarah")
    Nurse1.works_in_theatre = [NeuroTheatre]
    
    Nurse2 = onto.Nurse("Nurse_James")
    Nurse2.works_in_theatre = [OrthoTheatre]
    
    Nurse3 = onto.Nurse("Nurse_Emily")
    Nurse3.works_in_theatre = [CardioTheatre]
    
    # Phase 5: Define Anesthetists
    Anesthetist1 = onto.Anesthetist("Anesthetist_Michael")
    Anesthetist1.works_in_theatre = [NeuroTheatre]
    
    Anesthetist2 = onto.Anesthetist("Anesthetist_David")
    Anesthetist2.works_in_theatre = [OrthoTheatre]
    
    # Phase 6: Define Surgeries
    
    # Brain Surgery
    BrainSurgery = onto.Surgery("Brain_Surgery")
    BrainSurgery.estimated_duration = [180]
    BrainSurgery.is_emergency = [True]
    BrainSurgery.requires_theatre_type = [NeuroTheatre]
    BrainSurgery.requires_equipment = [onto.SurgicalEquipment("Neuro_Scope")]
    BrainSurgery.has_timeslot = [TS1]
    BrainSurgery.performs_operation = [NeuroSurgeon]
    BrainSurgery.has_assigned_staff = [Nurse1, Anesthetist1]
    
    # Cardiac Surgery
    CardiacSurgery = onto.Surgery("Cardiac_Bypass_Surgery")
    CardiacSurgery.estimated_duration = [240]
    CardiacSurgery.is_emergency = [False]
    CardiacSurgery.requires_theatre_type = [CardioTheatre]
    CardiacSurgery.requires_equipment = [onto.SurgicalEquipment("Cardiac_Monitor"), onto.SurgicalEquipment("Bypass_Machine")]
    CardiacSurgery.has_timeslot = [TS2]
    CardiacSurgery.performs_operation = [CardiothoracicSurgeon]
    CardiacSurgery.has_assigned_staff = [Nurse3, Anesthetist2]
    
    # Orthopedic Surgery
    OrthopedicSurgery = onto.Surgery("Hip_Replacement_Surgery")
    OrthopedicSurgery.estimated_duration = [120]
    OrthopedicSurgery.is_emergency = [False]
    OrthopedicSurgery.requires_theatre_type = [OrthoTheatre]
    OrthopedicSurgery.requires_equipment = [onto.SurgicalEquipment("Hip_Prosthesis"), onto.SurgicalEquipment("Surgical_Drill")]
    OrthopedicSurgery.has_timeslot = [TS3]
    OrthopedicSurgery.performs_operation = [OrthopedicSurgeon]
    OrthopedicSurgery.has_assigned_staff = [Nurse2, Anesthetist2]
    
    # General Surgery
    GeneralSurgery = onto.Surgery("Appendectomy")
    GeneralSurgery.estimated_duration = [90]
    GeneralSurgery.is_emergency = [True]
    GeneralSurgery.requires_theatre_type = [GeneralTheatre]
    GeneralSurgery.requires_equipment = [onto.SurgicalEquipment("Laparoscope")]
    GeneralSurgery.has_timeslot = [TS4]
    GeneralSurgery.performs_operation = [GeneralSurgeon]
    GeneralSurgery.has_assigned_staff = [Nurse1]
    
    # Phase 7: Define Wards
    NeuroWard = onto.Ward("Neurology_Ward")
    CardioWard = onto.Ward("Cardiology_Ward")
    OrthoWard = onto.Ward("Orthopedic_Ward")
    GeneralWard = onto.Ward("General_Ward")
    
    # Phase 8: Define Recovery Rooms
    RecoveryRoom1 = onto.RecoveryRoom("Recovery_Room_A")
    RecoveryRoom2 = onto.RecoveryRoom("Recovery_Room_B")
    RecoveryRoom3 = onto.RecoveryRoom("Recovery_Room_C")
    
    # Phase 9: Define Patients and assign to surgeries
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
    
    # Phase 10: Add SWRL Rules for Constraint Checking
        
    # SWRL Rule: Detect scheduling conflicts when surgeon has overlapping surgeries
    rule_conflict = Imp()
    rule_conflict.set_as_rule("""
        Surgeon(?s) ^ performs_operation(?s,?op1) ^ performs_operation(?s,?op2) ^ has_timeslot(?op1,?t1) ^ 
        has_timeslot(?op2,?t2) ^ has_temporal_overlap(?t1,?t2) ^ differentFrom(?op1,?op2) -> SchedulingConflict(?s)
    """)
    onto.add_rule(rule_conflict)

    # SWRL Rule: Equipment Availability Conflict
    rule_equipment_conflict = Imp()
    rule_equipment_conflict.set_as_rule("""
        requires_equipment(?s1, ?e) ^ requires_equipment(?s2, ?e) ^ has_timeslot(?s1, ?t1) ^ has_timeslot(?s2, ?t2) ^ 
        has_temporal_overlap(?t1, ?t2) ^ differentFrom(?s1, ?s2) -> EquipmentConflict(?e)
    """)
    onto.add_rule(rule_equipment_conflict)
    
    # SWRL Rule: Theatre Availability Conflict
    rule_theatre_availability_conflict = Imp()
    rule_theatre_availability_conflict.set_as_rule("""
        requires_theatre_type(?s1, ?th) ^ requires_theatre_type(?s2, ?th) ^ has_timeslot(?s1, ?t1) ^ has_timeslot(?s2, ?t2) ^ 
        has_temporal_overlap(?t1, ?t2) ^ differentFrom(?s1, ?s2) -> TheatreConflict(?th)
    """)
    onto.add_rule(rule_theatre_availability_conflict)

        
    # SWRL Rule: Patient Recovery Room Transition
    rule_recovery_conflict = Imp()
    rule_recovery_conflict.set_as_rule("""
        Patient(?p) ^ is_assigned_to(?p, ?t) ^ assigned_to_recovery(?p, ?r) ^ start_time(?t, ?st) ^ end_time(?t, ?et) -> hasRecoverySchedule(?p)
    """)
    onto.add_rule(rule_recovery_conflict)
    

    # SWRL Rule: Surgeon Specialization Mismatch
    rule_specialization_mismatch = Imp()
    rule_specialization_mismatch.set_as_rule("""
        Surgeon(?s) ^ performs_operation(?s, ?op) ^ requires_theatre_type(?op, ?th) ^ works_in_theatre(?s, ?wt) ^ differentFrom(?th, ?wt) -> SpecializationMismatch(?s)
    """)
    onto.add_rule(rule_specialization_mismatch)

    # SWRL Rule: Define overlapsWith based on time intervals
    rule_time_overlap = Imp()
    rule_time_overlap.set_as_rule("""
    TimeSlot(?t1) ^ start_time(?t1, ?s1) ^ end_time(?t1, ?e1) ^ TimeSlot(?t2) ^ start_time(?t2, ?s2) ^ end_time(?t2, ?e2) ^
    swrlb:lessThan(?s1, ?e2) ^ swrlb:lessThan(?s2, ?e1) -> overlapsWith(?t1, ?t2)
    """)
    onto.add_rule(rule_time_overlap)



# Save ontology
onto.save(file="ontology/hospital.owl", format="rdfxml")
print("Ontology saved successfully.")

sync_reasoner_pellet()  # infers conflicts

print("✅ Reasoner works!")
print(list(onto.SchedulingConflict.instances()))  # Should detect issues

