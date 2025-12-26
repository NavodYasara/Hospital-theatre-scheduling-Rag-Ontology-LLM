"""
============================================================================
FILE: create_ontology.py - ONTOLOGY CREATION SCRIPT
============================================================================

Usage:
    python create_ontology.py
    
This will create/overwrite ontology/hospital.owl with a fresh ontology
including all classes, properties, sample data, and SWRL rules.
============================================================================
"""

from owlready2 import *
import os

def create_hospital_ontology():
    """
    Create a complete hospital theatre scheduling ontology from scratch.
    This includes classes, properties, instances, and SWRL rules.
    """
    
    print("=" * 80)
    print("🏥 HOSPITAL THEATRE SCHEDULING ONTOLOGY CREATOR")
    print("=" * 80)
    print()
    
    # Get the ontology file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    owl_file = os.path.join(current_dir, "ontology", "hospital.owl")
    
    # Check if file exists
    if os.path.exists(owl_file):
        response = input(f"⚠️  File '{owl_file}' already exists. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Cancelled. Ontology creation aborted.")
            return
        else:
            os.remove(owl_file)
            print(f"🗑️  Deleted existing file: {owl_file}")
    
    print("📝 Creating new ontology...")
    print()
    
    # Create ontology
    onto = get_ontology("http://test.org/hospital.owl")
    
    with onto:
        # ====================================================================
        # STEP 1: Define Top-Level Classes
        # ====================================================================
        print("Step 1/7: Creating top-level classes...")
        
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
        
        # ====================================================================
        # STEP 2: Define Subclasses
        # ====================================================================
        print("Step 2/7: Creating specialized subclasses...")
        
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
        
        # Theatre Types
        class NeuroTheatre(Theatre):
            """Neurosurgery theatre"""
            pass
        
        class OrthoTheatre(Theatre):
            """Orthopedic surgery theatre"""
            pass
        
        class CardioTheatre(Theatre):
            """Cardiac surgery theatre"""
            pass
        
        class GeneralTheatre(Theatre):
            """General surgery theatre"""
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
        
        # Conflict Types
        class TheatreConflict(SchedulingConflict):
            """Theatre double-booking conflicts"""
            pass
        
        class SpecializationMismatch(SchedulingConflict):
            """Surgeon-theatre specialization mismatches"""
            pass
        
        class hasRecoverySchedule(Thing):
            """Marker class for patients with recovery schedules"""
            pass
        
        # ====================================================================
        # STEP 3: Define Object Properties (Relationships)
        # ====================================================================
        print("Step 3/7: Creating object properties (relationships)...")
        
        class performs_operation(ObjectProperty):
            """Surgeon performs a surgery"""
            domain = [Surgeon]
            range = [Surgery]
        
        class has_timeslot(ObjectProperty):
            """Surgery has a scheduled timeslot"""
            domain = [Surgery]
            range = [TimeSlot]
        
        class requires_theatre_type(ObjectProperty):
            """Surgery requires a specific theatre type"""
            domain = [Surgery]
            range = [Theatre]
        
        class works_in_theatre(ObjectProperty):
            """Staff member works in a theatre"""
            domain = [Staff]
            range = [Theatre]
        
        class has_assigned_staff(ObjectProperty):
            """Surgery has assigned staff members"""
            domain = [Surgery]
            range = [Staff]
        
        class undergoes_surgery(ObjectProperty):
            """Patient undergoes a surgery"""
            domain = [Patient]
            range = [Surgery]
        
        class scheduled_for(ObjectProperty):
            """Patient is scheduled for a surgery"""
            domain = [Patient]
            range = [Surgery]
        
        class has_severity(ObjectProperty):
            """Patient has a severity level"""
            domain = [Patient]
            range = [Severity]
        
        class admitted_to(ObjectProperty):
            """Patient admitted to a ward"""
            domain = [Patient]
            range = [Ward]
        
        class admitted_at_time(ObjectProperty):
            """Patient admitted at a specific time"""
            domain = [Patient]
            range = [TimeSlot]
        
        class assigned_to_recovery(ObjectProperty):
            """Patient assigned to a recovery room"""
            domain = [Patient]
            range = [RecoveryRoom]
        
        class discharged_from(ObjectProperty):
            """Patient discharged from a ward"""
            domain = [Patient]
            range = [Ward]
        
        class occurs_in(ObjectProperty):
            """Clinical process occurs in a location"""
            domain = [ClinicalProcess]
            range = [Location]
        
        class requires_postop_care_in(ObjectProperty):
            """Surgery requires post-op care in a location"""
            domain = [Surgery]
            range = [Location]
        
        class has_temporal_overlap(ObjectProperty):
            """Timeslots have temporal overlap"""
            domain = [TimeSlot]
            range = [TimeSlot]
        
        class available_during(ObjectProperty):
            """Staff available during a timeslot"""
            domain = [Staff]
            range = [TimeSlot]
        
        class assigned_to_surgery(ObjectProperty):
            """Staff assigned to a surgery"""
            domain = [Staff]
            range = [Surgery]
        
        class on_duty_in(ObjectProperty):
            """Staff on duty in a ward"""
            domain = [Staff]
            range = [Ward]
        
        # ====================================================================
        # STEP 4: Define Data Properties (Attributes)
        # ====================================================================
        print("Step 4/7: Creating data properties (attributes)...")
        
        class has_license_number(DataProperty, FunctionalProperty):
            """Surgeon's license number"""
            domain = [Surgeon]
            range = [int]
        
        class start_time(DataProperty, FunctionalProperty):
            """Start time of a timeslot"""
            domain = [TimeSlot]
            range = [str]
        
        class end_time(DataProperty, FunctionalProperty):
            """End time of a timeslot"""
            domain = [TimeSlot]
            range = [str]
        
        class date(DataProperty, FunctionalProperty):
            """Date of a timeslot"""
            domain = [TimeSlot]
            range = [str]
        
        class duration(DataProperty, FunctionalProperty):
            """Duration in minutes"""
            domain = [TimeSlot]
            range = [int]
        
        class estimated_duration(DataProperty, FunctionalProperty):
            """Estimated duration of surgery in minutes"""
            domain = [Surgery]
            range = [int]
        
        class is_emergency(DataProperty, FunctionalProperty):
            """Whether surgery is emergency"""
            domain = [Surgery]
            range = [bool]
        
        class surgery_status(DataProperty, FunctionalProperty):
            """Status of surgery"""
            domain = [Surgery]
            range = [str]
        
        class actual_start_time(DataProperty):
            """Actual start time of surgery"""
            domain = [Surgery]
            range = [str]
        
        class actual_end_time(DataProperty):
            """Actual end time of surgery"""
            domain = [Surgery]
            range = [str]
        
        class availability_status(DataProperty):
            """Staff availability status"""
            domain = [Staff]
            range = [bool]
        
        class severity_level(DataProperty, FunctionalProperty):
            """Severity level description"""
            domain = [Severity]
            range = [str]
        
        # ====================================================================
        # STEP 5: Create Instances - Reference Data
        # ====================================================================
        print("Step 5/7: Creating reference data instances...")
        
        # Severity Levels
        severe = Severe(severity_level="Severe")
        moderate = Moderate(severity_level="Moderate")
        mild = Mild(severity_level="Mild")
        minor = Minor(severity_level="Minor")
        
        # Theatres
        neuro_theatre = Neuro_Theatre()
        ortho_theatre = Ortho_Theatre()
        cardio_theatre = Cardio_Theatre()
        general_theatre = General_Theatre()
        
        # Wards
        neurology_ward = Neurology_Ward()
        cardiology_ward = Cardiology_Ward()
        orthopedic_ward = Orthopedic_Ward()
        general_ward = General_Ward()
        
        # Recovery Rooms
        recovery_a = Recovery_Room_A()
        recovery_b = Recovery_Room_B()
        recovery_c = Recovery_Room_C()
        
        # Timeslots
        ts_08_00 = TimeSlot_08_00(
            start_time="08:00",
            end_time="10:30",
            duration=150,
            date="2025-12-26"
        )
        
        ts_10_45 = TimeSlot_10_45(
            start_time="10:45",
            end_time="13:15",
            duration=150,
            date="2025-12-27"
        )
        
        ts_14_00 = TimeSlot_14_00(
            start_time="14:00",
            end_time="16:30",
            duration=150,
            date="2025-12-28"
        )
        
        ts_16_45 = TimeSlot_16_45(
            start_time="16:45",
            end_time="19:15",
            duration=150,
            date="2025-12-26"
        )
        
        ts_19_30 = TimeSlot_19_30(
            start_time="19:30",
            end_time="22:00",
            duration=150,
            date="2025-12-27"
        )
        
        ts_22_45 = TimeSlot_22_45(
            start_time="22:45",
            end_time="01:15",
            duration=150,
            date="2025-12-28"
        )
        
        # Set temporal overlaps (for SWRL rules)
        ts_08_00.has_temporal_overlap = [ts_10_45]
        ts_10_45.has_temporal_overlap = [ts_08_00]
        ts_14_00.has_temporal_overlap = [ts_16_45]
        ts_16_45.has_temporal_overlap = [ts_14_00]
        ts_19_30.has_temporal_overlap = [ts_22_45]
        ts_22_45.has_temporal_overlap = [ts_19_30]
        
        # ====================================================================
        # STEP 6: Create Instances - Staff and Surgeries
        # ====================================================================
        print("Step 6/7: Creating staff, surgeries, and patients...")
        
        # Anaesthetists
        anaesthetist_michael = Anaesthetist_Michael()
        anaesthetist_michael.works_in_theatre = [neuro_theatre]
        
        anaesthetist_david = Anaesthetist_David()
        anaesthetist_david.works_in_theatre = [ortho_theatre]
        
        anaesthetist_elijah = Anaesthetist_Elijah()
        anaesthetist_elijah.works_in_theatre = [cardio_theatre]
        
        anaesthetist_frank = Anaesthetist_Frank()
        anaesthetist_frank.works_in_theatre = [general_theatre]
        
        # Surgeons and Their Surgeries
        
        # Dr. Smith - Neurosurgeon
        dr_smith = Dr_Smith(has_license_number=12345)
        dr_smith.works_in_theatre = [neuro_theatre]
        
        brain_surgery = Brain_Surgery(
            estimated_duration=240,
            is_emergency=False
        )
        brain_surgery.requires_theatre_type = [neuro_theatre]
        brain_surgery.has_timeslot = [ts_08_00]
        brain_surgery.has_assigned_staff = [dr_smith, anaesthetist_michael]
        brain_surgery.performs_operation = [dr_smith]
        dr_smith.performs_operation = [brain_surgery]
        
        # Dr. Johnson - Orthopedic Surgeon
        dr_johnson = Dr_Johnson(has_license_number=67890)
        dr_johnson.works_in_theatre = [ortho_theatre]
        
        hip_surgery = Hip_Replacement_Surgery(
            estimated_duration=120,
            is_emergency=False
        )
        hip_surgery.requires_theatre_type = [ortho_theatre]
        hip_surgery.has_timeslot = [ts_14_00]
        hip_surgery.has_assigned_staff = [dr_johnson, anaesthetist_david]
        dr_johnson.performs_operation = [hip_surgery]
        
        # Dr. Williams - General Surgeon (working in Cardio - CONFLICT!)
        dr_williams = Dr_Williams(has_license_number=78901)
        dr_williams.works_in_theatre = [cardio_theatre]
        
        cardiac_surgery = Cardiac_Bypass_Surgery(
            estimated_duration=180,
            is_emergency=True
        )
        cardiac_surgery.requires_theatre_type = [neuro_theatre]  # Mismatch!
        cardiac_surgery.has_timeslot = [ts_08_00]  # Same as brain surgery - conflict!
        cardiac_surgery.has_assigned_staff = [dr_williams, anaesthetist_elijah]
        cardiac_surgery.performs_operation = [dr_smith]  # Dr. Smith double-booked!
        dr_williams.performs_operation = [cardiac_surgery]
        
        # Dr. Brown - General Surgeon
        dr_brown = Dr_Brown(has_license_number=34567)
        dr_brown.works_in_theatre = [general_theatre]
        
        appendectomy = Appendectomy(
            estimated_duration=90,
            is_emergency=True
        )
        appendectomy.requires_theatre_type = [general_theatre]
        appendectomy.has_timeslot = [ts_16_45]
        appendectomy.has_assigned_staff = [dr_brown, anaesthetist_frank]
        dr_brown.performs_operation = [appendectomy]
        
        # Patients
        patient_john = Patient_John_Doe()
        patient_john.scheduled_for = [brain_surgery]
        patient_john.admitted_at_time = [ts_08_00]
        patient_john.has_severity = [severe]
        patient_john.admitted_to = [neurology_ward]
        patient_john.assigned_to_recovery = [recovery_a]
        patient_john.undergoes_surgery = [brain_surgery]
        
        patient_mary = Patient_Mary_Smith()
        patient_mary.scheduled_for = [cardiac_surgery]
        patient_mary.admitted_at_time = [ts_10_45]
        patient_mary.has_severity = [moderate]
        patient_mary.admitted_to = [cardiology_ward]
        patient_mary.assigned_to_recovery = [recovery_b]
        patient_mary.undergoes_surgery = [cardiac_surgery]
        
        patient_robert = Patient_Robert_Johnson()
        patient_robert.scheduled_for = [hip_surgery]
        patient_robert.admitted_at_time = [ts_14_00]
        patient_robert.has_severity = [minor]
        patient_robert.admitted_to = [orthopedic_ward]
        patient_robert.assigned_to_recovery = [recovery_c]
        patient_robert.undergoes_surgery = [hip_surgery]
        
        patient_linda = Patient_Linda_Williams()
        patient_linda.scheduled_for = [appendectomy]
        patient_linda.admitted_at_time = [ts_16_45]
        patient_linda.has_severity = [severe]
        patient_linda.admitted_to = [general_ward]
        patient_linda.assigned_to_recovery = [recovery_a]
        patient_linda.undergoes_surgery = [appendectomy]
        
        # Additional patients without surgeries
        patient_john_w = Patient_John_Williams()
        patient_john_w.admitted_at_time = [ts_19_30]
        patient_john_w.has_severity = [moderate]
        patient_john_w.admitted_to = [general_ward]
        patient_john_w.assigned_to_recovery = [recovery_a]
        
        patient_sarah = Patient_Sarah_Brown()
        patient_sarah.admitted_at_time = [ts_22_45]
        patient_sarah.has_severity = [mild]
        patient_sarah.admitted_to = [general_ward]
        patient_sarah.assigned_to_recovery = [recovery_a]
        
        # Special test patient
        padma = Padma_Wickramage()
        padma.has_severity = [mild]
        padma.admitted_to = [neurology_ward]
        padma.assigned_to_recovery = [recovery_a]
        padma.undergoes_surgery = [brain_surgery]
        
        patient_emergency = Patient_Emergency_Case()
        patient_emergency.has_severity = [severe]
        patient_emergency.admitted_to = [cardiology_ward]
        patient_emergency.assigned_to_recovery = [recovery_b]
        patient_emergency.undergoes_surgery = [cardiac_surgery]
        
        # ====================================================================
        # STEP 7: Add SWRL Rules for Reasoning
        # ====================================================================
        print("Step 7/7: Adding SWRL rules for automated reasoning...")
        
        # Rule 1: Recovery Schedule Detection
        # If a patient is admitted at a time AND assigned to recovery, mark as having recovery schedule
        rule1 = Imp()
        rule1.set_as_rule("""
            Patient(?p), 
            admitted_at_time(?p, ?t), 
            assigned_to_recovery(?p, ?r) 
            -> hasRecoverySchedule(?p)
        """)
        
        # Rule 2: Specialization Mismatch Detection
        # If a surgeon performs operation in a theatre different from their specialty
        rule2 = Imp()
        rule2.set_as_rule("""
            Surgeon(?s), 
            performs_operation(?s, ?op), 
            requires_theatre_type(?op, ?th), 
            works_in_theatre(?s, ?wt), 
            differentFrom(?th, ?wt) 
            -> SpecializationMismatch(?s)
        """)
        
        # Rule 3: Theatre Conflict Detection
        # If two different surgeries require same theatre at overlapping times
        rule3 = Imp()
        rule3.set_as_rule("""
            requires_theatre_type(?s1, ?th), 
            requires_theatre_type(?s2, ?th), 
            has_timeslot(?s1, ?t1), 
            has_timeslot(?s2, ?t2), 
            has_temporal_overlap(?t1, ?t2), 
            differentFrom(?s1, ?s2) 
            -> TheatreConflict(?th)
        """)
        
        # Rule 4: Surgeon Double-Booking Detection
        # If same surgeon performs two operations at overlapping times
        rule4 = Imp()
        rule4.set_as_rule("""
            Surgeon(?s), 
            performs_operation(?s, ?op1), 
            performs_operation(?s, ?op2), 
            has_timeslot(?op1, ?t1), 
            has_timeslot(?op2, ?t2), 
            has_temporal_overlap(?t1, ?t2), 
            differentFrom(?op1, ?op2) 
            -> SchedulingConflict(?s)
        """)
    
    # ====================================================================
    # SAVE THE ONTOLOGY
    # ====================================================================
    print()
    print("💾 Saving ontology...")
    onto.save(file=owl_file, format="rdfxml")
    
    print()
    print("=" * 80)
    print("✅ ONTOLOGY CREATED SUCCESSFULLY!")
    print("=" * 80)
    print(f"📁 File: {owl_file}")
    print(f"📊 Size: {os.path.getsize(owl_file)} bytes")
    print()
    
    # Print summary statistics
    print("📈 ONTOLOGY SUMMARY:")
    print(f"   • Classes: {len(list(onto.classes()))}")
    print(f"   • Object Properties: {len(list(onto.object_properties()))}")
    print(f"   • Data Properties: {len(list(onto.data_properties()))}")
    print(f"   • Individuals: {len(list(onto.individuals()))}")
    print(f"   • SWRL Rules: 4")
    print()
    
    print("👥 SAMPLE DATA CREATED:")
    print(f"   • Surgeons: 4 (Dr_Smith, Dr_Johnson, Dr_Williams, Dr_Brown)")
    print(f"   • Theatres: 4 (Neuro, Ortho, Cardio, General)")
    print(f"   • Timeslots: 6")
    print(f"   • Surgeries: 4")
    print(f"   • Patients: 8")
    print(f"   • Severity Levels: 4 (Severe, Moderate, Mild, Minor)")
    print()
    
    print("⚠️  INTENTIONAL CONFLICTS INCLUDED FOR TESTING:")
    print(f"   • Surgeon Double-Booking: Dr_Smith (Brain_Surgery + Cardiac_Bypass)")
    print(f"   • Theatre Conflict: Neuro_Theatre (same timeslot)")
    print(f"   • Specialization Mismatch: Dr_Williams (works in Cardio, operates in Neuro)")
    print()
    
    print("🎯 NEXT STEPS:")
    print("   1. Run the Streamlit app: streamlit run app.py")
    print("   2. Go to 'Conflict Detection' tab to see conflicts")
    print("   3. Use 'Add Schedule' to add new surgeries")
    print("   4. Chat with the assistant to query the ontology")
    print()
    print("=" * 80)

if __name__ == "__main__":
    create_hospital_ontology()
