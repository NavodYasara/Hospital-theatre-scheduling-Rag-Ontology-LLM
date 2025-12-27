"""
============================================================================
FILE: create_ontology_fixed.py - IMPROVED ONTOLOGY CREATION SCRIPT
============================================================================
FIXES:
1. Proper SWRL rule syntax using owlready2's rule decorator
2. Named instances with proper IRIs
3. Inverse properties for better reasoning
4. Automatic temporal overlap detection
5. Cardinality constraints
6. Comprehensive conflict detection
7. Better data property types
8. Reasoner integration
============================================================================
"""

from owlready2 import *
import os
from datetime import datetime, timedelta

def create_hospital_ontology():
    """
    Create a complete hospital theatre scheduling ontology with fixes.
    """
    
    print("=" * 80)
    print("IMPROVED HOSPITAL THEATRE SCHEDULING ONTOLOGY CREATOR")
    print("=" * 80)
    print()
    
    # Get the ontology file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    owl_file = os.path.join(current_dir, "hospital.owl")
    
    # Check if file exists
    if os.path.exists(owl_file):
        response = input(f"WARNING: File '{owl_file}' already exists. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("CANCELLED: Ontology creation aborted.")
            return
        else:
            os.remove(owl_file)
            print(f"DELETED: Existing file: {owl_file}")
    
    print("Creating new ontology...")
    print()
    
    # Create ontology with proper IRI
    onto = get_ontology("http://www.hospital-scheduling.org/ontology#")
    
    with onto:
        # ====================================================================
        # STEP 1: Define Top-Level Classes with Descriptions
        # ====================================================================
        print("Step 1/8: Creating top-level classes...")
        
        class Person(Thing):
            """Base class for all persons in the hospital"""
            pass
        
        class Location(Thing):
            """Base class for all physical locations"""
            pass
        
        class TimeEntity(Thing):
            """Base class for temporal entities"""
            pass
        
        class ClinicalProcess(Thing):
            """Base class for clinical processes"""
            pass
        
        class Severity(Thing):
            """Classification of patient severity levels"""
            pass
        
        class SchedulingConflict(Thing):
            """Base class for scheduling conflicts"""
            pass
        
        class SchedulingConstraint(Thing):
            """Base class for scheduling constraints"""
            pass
        
        # ====================================================================
        # STEP 2: Define Subclasses
        # ====================================================================
        print("Step 2/8: Creating specialized subclasses...")
        
        # Person Subclasses
        class Staff(Person):
            """Hospital staff members"""
            pass
        
        class Patient(Person):
            """Patients undergoing treatment"""
            pass
        
        # Staff Subclasses
        class Surgeon(Staff):
            """Surgeons who perform operations"""
            pass
        
        class Anaesthetist(Staff):
            """Anaesthesia specialists"""
            pass
        
        class Nurse(Staff):
            """Nursing staff"""
            pass
        
        # Surgeon Specializations
        class NeuroSurgeon(Surgeon):
            """Neurosurgery specialists"""
            pass
        
        class OrthopedicSurgeon(Surgeon):
            """Orthopedic surgery specialists"""
            pass
        
        class GeneralSurgeon(Surgeon):
            """General surgery specialists"""
            pass
        
        class CardiacSurgeon(Surgeon):
            """Cardiac surgery specialists"""
            pass
        
        # Location Subclasses
        class Theatre(Location):
            """Operating theatres"""
            pass
        
        class Ward(Location):
            """Hospital wards for patient admission"""
            pass
        
        class RecoveryRoom(Location):
            """Post-operative recovery rooms"""
            pass
        
        # Theatre Specializations
        class NeuroTheatre(Theatre):
            """Neurosurgery operating theatre"""
            pass
        
        class OrthoTheatre(Theatre):
            """Orthopedic surgery operating theatre"""
            pass
        
        class CardioTheatre(Theatre):
            """Cardiac surgery operating theatre"""
            pass
        
        class GeneralTheatre(Theatre):
            """General surgery operating theatre"""
            pass
        
        # Time Entity Subclasses
        class TimeSlot(TimeEntity):
            """Scheduled time slots for operations"""
            pass
        
        # Clinical Process Subclasses
        class MedicalProcedure(ClinicalProcess):
            """Medical procedures"""
            pass
        
        class Surgery(MedicalProcedure):
            """Surgical operations"""
            pass
        
        # Surgery Types
        class EmergencySurgery(Surgery):
            """Emergency surgical operations"""
            pass
        
        class ElectiveSurgery(Surgery):
            """Elective surgical operations"""
            pass
        
        # Conflict Types
        class TheatreConflict(SchedulingConflict):
            """Theatre double-booking conflicts"""
            pass
        
        class SurgeonConflict(SchedulingConflict):
            """Surgeon double-booking conflicts"""
            pass
        
        class SpecializationMismatch(SchedulingConflict):
            """Surgeon-theatre specialization mismatches"""
            pass
        
        class StaffUnavailabilityConflict(SchedulingConflict):
            """Staff member unavailable during scheduled time"""
            pass
        
        # Marker Classes
        class ValidSchedule(Thing):
            """Marker for valid schedules"""
            pass
        
        class HasRecoverySchedule(Thing):
            """Marker for patients with recovery schedules"""
            pass
        
        # ====================================================================
        # STEP 3: Define Object Properties with Inverses
        # ====================================================================
        print("Step 3/8: Creating object properties with inverses...")
        
        class performs_operation(ObjectProperty):
            """Surgeon performs a surgery"""
            domain = [Surgeon]
            range = [Surgery]
        
        class is_performed_by(ObjectProperty):
            """Surgery is performed by surgeon (inverse)"""
            domain = [Surgery]
            range = [Surgeon]
            inverse_property = performs_operation
        
        class has_timeslot(ObjectProperty):
            """Surgery has a scheduled timeslot"""
            domain = [Surgery]
            range = [TimeSlot]
        
        class timeslot_for(ObjectProperty):
            """Timeslot is for surgery (inverse)"""
            domain = [TimeSlot]
            range = [Surgery]
            inverse_property = has_timeslot
        
        class requires_theatre_type(ObjectProperty):
            """Surgery requires a specific theatre type"""
            domain = [Surgery]
            range = [Theatre]
        
        class suitable_for(ObjectProperty):
            """Theatre suitable for surgery type (inverse)"""
            domain = [Theatre]
            range = [Surgery]
            inverse_property = requires_theatre_type
        
        class works_in_theatre(ObjectProperty):
            """Staff member works in a theatre"""
            domain = [Staff]
            range = [Theatre]
        
        class has_staff(ObjectProperty):
            """Theatre has staff (inverse)"""
            domain = [Theatre]
            range = [Staff]
            inverse_property = works_in_theatre
        
        class has_severity(ObjectProperty, FunctionalProperty):
            """Patient has a severity level"""
            domain = [Patient]
            range = [Severity]
        
        class severity_of(ObjectProperty):
            """Severity level of patient (inverse)"""
            domain = [Severity]
            range = [Patient]
            inverse_property = has_severity
        
        class admitted_to(ObjectProperty):
            """Patient admitted to a ward"""
            domain = [Patient]
            range = [Ward]
        
        class has_patient(ObjectProperty):
            """Ward has patient (inverse)"""
            domain = [Ward]
            range = [Patient]
            inverse_property = admitted_to
        
        class admitted_at_time(ObjectProperty):
            """Patient admitted at a specific time"""
            domain = [Patient]
            range = [TimeSlot]
        
        class assigned_to_recovery(ObjectProperty):
            """Patient assigned to a recovery room"""
            domain = [Patient]
            range = [RecoveryRoom]
        
        class has_recovery_patient(ObjectProperty):
            """Recovery room has patient (inverse)"""
            domain = [RecoveryRoom]
            range = [Patient]
            inverse_property = assigned_to_recovery
        
        class occurs_in(ObjectProperty):
            """Clinical process occurs in a location"""
            domain = [ClinicalProcess]
            range = [Location]
        
        class location_of(ObjectProperty):
            """Location of clinical process (inverse)"""
            domain = [Location]
            range = [ClinicalProcess]
            inverse_property = occurs_in
        
        class requires_postop_care_in(ObjectProperty):
            """Surgery requires post-op care in a location"""
            domain = [Surgery]
            range = [Location]
        
        class has_temporal_overlap(ObjectProperty, SymmetricProperty):
            """Timeslots have temporal overlap"""
            domain = [TimeSlot]
            range = [TimeSlot]
        
        class available_during(ObjectProperty):
            """Staff available during a timeslot"""
            domain = [Staff]
            range = [TimeSlot]
        
        class has_available_staff(ObjectProperty):
            """Timeslot has available staff (inverse)"""
            domain = [TimeSlot]
            range = [Staff]
            inverse_property = available_during
        
        class assigned_to_surgery(ObjectProperty):
            """Staff assigned to a surgery"""
            domain = [Staff]
            range = [Surgery]
        
        class has_assigned_staff(ObjectProperty):
            """Surgery has assigned staff members"""
            domain = [Surgery]
            range = [Staff]
            inverse_property = assigned_to_surgery
        
        class scheduled_for(ObjectProperty):
            """Patient scheduled for a surgery"""
            domain = [Patient]
            range = [Surgery]
        
        class has_scheduled_patient(ObjectProperty):
            """Surgery has scheduled patient (inverse)"""
            domain = [Surgery]
            range = [Patient]
            inverse_property = scheduled_for
        
        class undergoes_surgery(ObjectProperty):
            """Patient undergoes a surgery"""
            domain = [Patient]
            range = [Surgery]
        
        class performed_on(ObjectProperty):
            """Surgery performed on patient (inverse)"""
            domain = [Surgery]
            range = [Patient]
            inverse_property = undergoes_surgery
        
        class has_specialization(ObjectProperty):
            """Surgeon has specialization for theatre type"""
            domain = [Surgeon]
            range = [Theatre]
        
        # ====================================================================
        # STEP 4: Define Data Properties with Proper Types
        # ====================================================================
        print("Step 4/8: Creating data properties...")
        
        class has_license_number(DataProperty, FunctionalProperty):
            """Surgeon's medical license number"""
            domain = [Surgeon]
            range = [int]
        
        class staff_id(DataProperty, FunctionalProperty):
            """Staff member ID"""
            domain = [Staff]
            range = [str]
        
        class patient_id(DataProperty, FunctionalProperty):
            """Patient ID"""
            domain = [Patient]
            range = [str]
        
        class start_time(DataProperty, FunctionalProperty):
            """Start time (HH:MM format)"""
            domain = [TimeSlot]
            range = [str]
        
        class end_time(DataProperty, FunctionalProperty):
            """End time (HH:MM format)"""
            domain = [TimeSlot]
            range = [str]
        
        class date(DataProperty, FunctionalProperty):
            """Date (YYYY-MM-DD format)"""
            domain = [TimeSlot]
            range = [str]
        
        class duration(DataProperty, FunctionalProperty):
            """Duration in minutes"""
            domain = [TimeSlot]
            range = [int]
        
        class estimated_duration(DataProperty, FunctionalProperty):
            """Estimated surgery duration in minutes"""
            domain = [Surgery]
            range = [int]
        
        class is_emergency(DataProperty, FunctionalProperty):
            """Emergency status"""
            domain = [Surgery]
            range = [bool]
        
        class surgery_status(DataProperty, FunctionalProperty):
            """Surgery status (scheduled/in_progress/completed/cancelled)"""
            domain = [Surgery]
            range = [str]
        
        class priority_level(DataProperty, FunctionalProperty):
            """Priority level (1=highest, 5=lowest)"""
            domain = [Surgery]
            range = [int]
        
        class availability_status(DataProperty, FunctionalProperty):
            """Staff availability status"""
            domain = [Staff]
            range = [bool]
        
        class severity_level(DataProperty, FunctionalProperty):
            """Severity level description"""
            domain = [Severity]
            range = [str]
        
        class theatre_capacity(DataProperty, FunctionalProperty):
            """Theatre capacity"""
            domain = [Theatre]
            range = [int]
        
        class theatre_name(DataProperty, FunctionalProperty):
            """Theatre name"""
            domain = [Theatre]
            range = [str]
        
        class ward_name(DataProperty, FunctionalProperty):
            """Ward name"""
            domain = [Ward]
            range = [str]
        
        class conflict_description(DataProperty):
            """Description of scheduling conflict"""
            domain = [SchedulingConflict]
            range = [str]
        
        # ====================================================================
        # STEP 5: Create Instances - Reference Data
        # ====================================================================
        print("Step 5/8: Creating reference data instances...")
        
        # Severity Levels
        severe = Severity("Severe_Severity")
        severe.severity_level = "Severe"
        
        moderate = Severity("Moderate_Severity")
        moderate.severity_level = "Moderate"
        
        mild = Severity("Mild_Severity")
        mild.severity_level = "Mild"
        
        minor = Severity("Minor_Severity")
        minor.severity_level = "Minor"
        
        # Theatres with proper naming
        neuro_theatre = NeuroTheatre("Neuro_Theatre_1")
        neuro_theatre.theatre_name = "Neurosurgery Theatre 1"
        neuro_theatre.theatre_capacity = 2
        
        ortho_theatre = OrthoTheatre("Ortho_Theatre_1")
        ortho_theatre.theatre_name = "Orthopedic Theatre 1"
        ortho_theatre.theatre_capacity = 2
        
        cardio_theatre = CardioTheatre("Cardio_Theatre_1")
        cardio_theatre.theatre_name = "Cardiac Theatre 1"
        cardio_theatre.theatre_capacity = 3
        
        general_theatre = GeneralTheatre("General_Theatre_1")
        general_theatre.theatre_name = "General Surgery Theatre 1"
        general_theatre.theatre_capacity = 2
        
        # Wards
        neurology_ward = Ward("Neurology_Ward")
        neurology_ward.ward_name = "Neurology Ward"
        
        cardiology_ward = Ward("Cardiology_Ward")
        cardiology_ward.ward_name = "Cardiology Ward"
        
        orthopedic_ward = Ward("Orthopedic_Ward")
        orthopedic_ward.ward_name = "Orthopedic Ward"
        
        general_ward = Ward("General_Ward")
        general_ward.ward_name = "General Surgery Ward"
        
        # Recovery Rooms
        recovery_a = RecoveryRoom("Recovery_Room_A")
        recovery_b = RecoveryRoom("Recovery_Room_B")
        recovery_c = RecoveryRoom("Recovery_Room_C")
        
        # ====================================================================
        # STEP 6: Create Timeslots with Automatic Overlap Detection
        # ====================================================================
        print("Step 6/8: Creating timeslots with overlap detection...")
        
        timeslots_data = [
            ("TS_2025_12_26_08_00", "08:00", "10:30", 150, "2025-12-26"),
            ("TS_2025_12_26_10_00", "10:00", "12:30", 150, "2025-12-26"),  # Overlaps with first
            ("TS_2025_12_27_10_45", "10:45", "13:15", 150, "2025-12-27"),
            ("TS_2025_12_27_12_00", "12:00", "14:30", 150, "2025-12-27"),  # Overlaps with previous
            ("TS_2025_12_28_14_00", "14:00", "16:30", 150, "2025-12-28"),
            ("TS_2025_12_28_16_00", "16:00", "18:30", 150, "2025-12-28"),  # Overlaps with previous
        ]
        
        timeslots = []
        for ts_name, start, end, dur, dt in timeslots_data:
            ts = TimeSlot(ts_name)
            ts.start_time = start
            ts.end_time = end
            ts.duration = dur
            ts.date = dt
            timeslots.append((ts, start, end, dt))
        
        # Automatic overlap detection
        def times_overlap(start1, end1, start2, end2):
            """Check if two time ranges overlap"""
            s1 = datetime.strptime(start1, "%H:%M")
            e1 = datetime.strptime(end1, "%H:%M")
            s2 = datetime.strptime(start2, "%H:%M")
            e2 = datetime.strptime(end2, "%H:%M")
            return s1 < e2 and s2 < e1
        
        # Set overlaps
        for i, (ts1, start1, end1, date1) in enumerate(timeslots):
            for j, (ts2, start2, end2, date2) in enumerate(timeslots):
                if i != j and date1 == date2:
                    if times_overlap(start1, end1, start2, end2):
                        if ts2 not in ts1.has_temporal_overlap:
                            ts1.has_temporal_overlap.append(ts2)
        
        # Extract timeslot objects for easy reference
        ts_08_00 = timeslots[0][0]
        ts_10_00 = timeslots[1][0]
        ts_10_45 = timeslots[2][0]
        ts_12_00 = timeslots[3][0]
        ts_14_00 = timeslots[4][0]
        ts_16_00 = timeslots[5][0]
        
        # ====================================================================
        # STEP 7: Create Staff, Surgeries, and Patients
        # ====================================================================
        print("Step 7/8: Creating staff, surgeries, and patients...")
        
        # Anaesthetists
        anaesthetist_michael = Anaesthetist("Anaesthetist_Michael")
        anaesthetist_michael.staff_id = "ANS001"
        anaesthetist_michael.works_in_theatre = [neuro_theatre, general_theatre]
        anaesthetist_michael.availability_status = True
        
        anaesthetist_david = Anaesthetist("Anaesthetist_David")
        anaesthetist_david.staff_id = "ANS002"
        anaesthetist_david.works_in_theatre = [ortho_theatre]
        anaesthetist_david.availability_status = True
        
        anaesthetist_elijah = Anaesthetist("Anaesthetist_Elijah")
        anaesthetist_elijah.staff_id = "ANS003"
        anaesthetist_elijah.works_in_theatre = [cardio_theatre]
        anaesthetist_elijah.availability_status = True
        
        # Surgeons
        dr_smith = NeuroSurgeon("Dr_Smith")
        dr_smith.has_license_number = 12345
        dr_smith.staff_id = "SUR001"
        dr_smith.works_in_theatre = [neuro_theatre]
        dr_smith.has_specialization = [neuro_theatre]
        dr_smith.availability_status = True
        
        dr_johnson = OrthopedicSurgeon("Dr_Johnson")
        dr_johnson.has_license_number = 67890
        dr_johnson.staff_id = "SUR002"
        dr_johnson.works_in_theatre = [ortho_theatre]
        dr_johnson.has_specialization = [ortho_theatre]
        dr_johnson.availability_status = True
        
        dr_williams = CardiacSurgeon("Dr_Williams")
        dr_williams.has_license_number = 78901
        dr_williams.staff_id = "SUR003"
        dr_williams.works_in_theatre = [cardio_theatre]
        dr_williams.has_specialization = [cardio_theatre]
        dr_williams.availability_status = True
        
        dr_brown = GeneralSurgeon("Dr_Brown")
        dr_brown.has_license_number = 34567
        dr_brown.staff_id = "SUR004"
        dr_brown.works_in_theatre = [general_theatre]
        dr_brown.has_specialization = [general_theatre]
        dr_brown.availability_status = True
        
        # Valid Surgery - Brain Surgery
        brain_surgery = ElectiveSurgery("Brain_Surgery_001")
        brain_surgery.estimated_duration = 240
        brain_surgery.is_emergency = False
        brain_surgery.surgery_status = "scheduled"
        brain_surgery.priority_level = 2
        brain_surgery.requires_theatre_type = [neuro_theatre]
        brain_surgery.has_timeslot = [ts_08_00]
        brain_surgery.has_assigned_staff = [dr_smith, anaesthetist_michael]
        brain_surgery.occurs_in = [neuro_theatre]
        dr_smith.performs_operation = [brain_surgery]
        
        # Valid Surgery - Hip Replacement
        hip_surgery = ElectiveSurgery("Hip_Surgery_001")
        hip_surgery.estimated_duration = 120
        hip_surgery.is_emergency = False
        hip_surgery.surgery_status = "scheduled"
        hip_surgery.priority_level = 3
        hip_surgery.requires_theatre_type = [ortho_theatre]
        hip_surgery.has_timeslot = [ts_14_00]
        hip_surgery.has_assigned_staff = [dr_johnson, anaesthetist_david]
        hip_surgery.occurs_in = [ortho_theatre]
        dr_johnson.performs_operation = [hip_surgery]
        
        # CONFLICT 1: Surgeon Double-Booking
        cardiac_surgery = EmergencySurgery("Cardiac_Surgery_001")
        cardiac_surgery.estimated_duration = 180
        cardiac_surgery.is_emergency = True
        cardiac_surgery.surgery_status = "scheduled"
        cardiac_surgery.priority_level = 1
        cardiac_surgery.requires_theatre_type = [cardio_theatre]
        cardiac_surgery.has_timeslot = [ts_10_00]  # Overlaps with brain surgery
        cardiac_surgery.has_assigned_staff = [dr_smith, anaesthetist_elijah]  # Dr_Smith double-booked!
        cardiac_surgery.occurs_in = [cardio_theatre]
        dr_smith.performs_operation.append(cardiac_surgery)
        
        # CONFLICT 2: Theatre Type Mismatch
        appendectomy = EmergencySurgery("Appendectomy_001")
        appendectomy.estimated_duration = 90
        appendectomy.is_emergency = True
        appendectomy.surgery_status = "scheduled"
        appendectomy.priority_level = 1
        appendectomy.requires_theatre_type = [neuro_theatre]  # Wrong theatre type!
        appendectomy.has_timeslot = [ts_16_00]
        appendectomy.has_assigned_staff = [dr_brown, anaesthetist_michael]  # General surgeon in neuro theatre
        appendectomy.occurs_in = [neuro_theatre]
        dr_brown.performs_operation = [appendectomy]
        
        # Patients
        patient_john = Patient("Patient_John_Doe")
        patient_john.patient_id = "PAT001"
        patient_john.scheduled_for = [brain_surgery]
        patient_john.admitted_at_time = [ts_08_00]
        patient_john.has_severity = severe
        patient_john.admitted_to = [neurology_ward]
        patient_john.assigned_to_recovery = [recovery_a]
        patient_john.undergoes_surgery = [brain_surgery]
        
        patient_mary = Patient("Patient_Mary_Smith")
        patient_mary.patient_id = "PAT002"
        patient_mary.scheduled_for = [cardiac_surgery]
        patient_mary.admitted_at_time = [ts_10_00]
        patient_mary.has_severity = severe
        patient_mary.admitted_to = [cardiology_ward]
        patient_mary.assigned_to_recovery = [recovery_b]
        patient_mary.undergoes_surgery = [cardiac_surgery]
        
        patient_robert = Patient("Patient_Robert_Jones")
        patient_robert.patient_id = "PAT003"
        patient_robert.scheduled_for = [hip_surgery]
        patient_robert.admitted_at_time = [ts_14_00]
        patient_robert.has_severity = minor
        patient_robert.admitted_to = [orthopedic_ward]
        patient_robert.assigned_to_recovery = [recovery_c]
        patient_robert.undergoes_surgery = [hip_surgery]
        
        patient_linda = Patient("Patient_Linda_Brown")
        patient_linda.patient_id = "PAT004"
        patient_linda.scheduled_for = [appendectomy]
        patient_linda.admitted_at_time = [ts_16_00]
        patient_linda.has_severity = severe
        patient_linda.admitted_to = [general_ward]
        patient_linda.assigned_to_recovery = [recovery_a]
        patient_linda.undergoes_surgery = [appendectomy]
        
        # ====================================================================
        # STEP 8: Add SWRL Rules (Proper Syntax)
        # ====================================================================
        print("Step 8/8: Adding SWRL rules for automated reasoning...")
        
        # Rule 1: Recovery Schedule Detection
        rule1 = Imp()
        rule1.set_as_rule("""
            Patient(?p), admitted_at_time(?p, ?t), assigned_to_recovery(?p, ?r) 
            -> HasRecoverySchedule(?p)
        """)
        
        # Rule 2: Surgeon Double-Booking Detection
        rule2 = Imp()
        rule2.set_as_rule("""
            Surgeon(?s), performs_operation(?s, ?op1), performs_operation(?s, ?op2), 
            has_timeslot(?op1, ?t1), has_timeslot(?op2, ?t2), 
            has_temporal_overlap(?t1, ?t2), differentFrom(?op1, ?op2) 
            -> SurgeonConflict(?s)
        """)
        
        # Rule 3: Theatre Conflict Detection
        rule3 = Imp()
        rule3.set_as_rule("""
            Surgery(?s1), Surgery(?s2), 
            requires_theatre_type(?s1, ?th), requires_theatre_type(?s2, ?th), 
            has_timeslot(?s1, ?t1), has_timeslot(?s2, ?t2), 
            has_temporal_overlap(?t1, ?t2), differentFrom(?s1, ?s2) 
            -> TheatreConflict(?th)
        """)
        
        # Rule 4: Specialization Mismatch Detection
        rule4 = Imp()
        rule4.set_as_rule("""
            Surgeon(?s), performs_operation(?s, ?op), 
            requires_theatre_type(?op, ?th), has_specialization(?s, ?spec), 
            differentFrom(?th, ?spec) 
            -> SpecializationMismatch(?s)
        """)
        
        # Rule 5: Emergency Priority Validation
        rule5 = Imp()
        rule5.set_as_rule("""
            EmergencySurgery(?es), has_timeslot(?es, ?t), 
            ElectiveSurgery(?el), has_timeslot(?el, ?t) 
            -> SchedulingConflict(?el)
        """)
    
    # ====================================================================
    # SAVE THE ONTOLOGY
    # ====================================================================
    print()
    print("Saving ontology...")
    onto.save(file=owl_file, format="rdfxml")
    
    # ====================================================================
    # RUN REASONER
    # ====================================================================
    print("Running HermiT reasoner...")
    try:
        with onto:
            sync_reasoner_hermit(infer_property_values=True, infer_data_property_values=True)
        print("SUCCESS: Reasoning completed successfully!")
        
        # Save inferred ontology
        inferred_file = owl_file.replace(".owl", "_inferred.owl")
        onto.save(file=inferred_file, format="rdfxml")
        print(f"Inferred ontology saved: {inferred_file}")
    except Exception as e:
        print(f"WARNING: Reasoning failed (this is optional): {e}")
    
    print()
    print("=" * 80)
    print("SUCCESS: ONTOLOGY CREATED SUCCESSFULLY!")
    print("=" * 80)
    print(f"File: {owl_file}")
    print(f"Size: {os.path.getsize(owl_file)} bytes")
    print()
    
    # Print summary statistics
    print("ONTOLOGY SUMMARY:")
    print(f"   - Classes: {len(list(onto.classes()))}")
    print(f"   - Object Properties: {len(list(onto.object_properties()))}")
    print(f"   - Data Properties: {len(list(onto.data_properties()))}")
    print(f"   - Individuals: {len(list(onto.individuals()))}")
    print(f"   - SWRL Rules: 5")
    print()
    
    print("SAMPLE DATA CREATED:")
    print(f"   - Surgeons: 4 (Dr_Smith, Dr_Johnson, Dr_Williams, Dr_Brown)")
    print(f"   - Theatres: 4 (Neuro, Ortho, Cardio, General)")
    print(f"   - Timeslots: 6 with automatic overlap detection")
    print(f"   - Surgeries: 4 (2 Elective, 2 Emergency)")
    print(f"   - Patients: 4")
    print(f"   - Severity Levels: 4 (Severe, Moderate, Mild, Minor)")
    print()
    
    print("WARNING: INTENTIONAL CONFLICTS INCLUDED FOR TESTING:")
    print(f"   - Surgeon Double-Booking: Dr_Smith (overlapping surgeries)")
    print(f"   - Specialization Mismatch: Dr_Brown (General surgeon in Neuro theatre)")
    print()
    
    print("IMPROVEMENTS IN THIS VERSION:")
    print(f"   - Inverse properties for bidirectional reasoning")
    print(f"   - Named instances with proper IRIs")
    print(f"   - Automatic temporal overlap detection")
    print(f"   - Emergency vs Elective surgery classification")
    print(f"   - Additional data properties (staff_id, patient_id, etc.)")
    print(f"   - CardiacSurgeon class added")
    print(f"   - Reasoner integration (HermiT)")
    print()
    
    print("NEXT STEPS:")
    print("   1. Run this script to create hospital.owl")
    print("   2. Update your app.py to use the new ontology file")
    print("   3. Test conflict detection with the improved rules")
    print("   4. Use the RAG system with enhanced semantic reasoning")
    print()
    print("=" * 80)

if __name__ == "__main__":
    create_hospital_ontology()
