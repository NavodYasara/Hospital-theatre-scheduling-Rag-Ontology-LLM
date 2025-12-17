# """
# Initialize the hospital ontology with sample data
# This script populates the ontology with surgeons, theatres, timeslots, and sample surgeries
# """
# from ontology.ontology_manager import OntologyManager
# from datetime import time

# def initialize_hospital_data():
#     """Add initial data to the hospital ontology"""
    
#     # Initialize ontology manager
#     onto_mgr = OntologyManager("ontology/hospital.owl")
    
#     print("🏥 Initializing Hospital Ontology Data...")
#     print("=" * 60)
    
#     # Add Theatres
#     print("\n📍 Adding Theatres...")
#     theatres = [
#         "Neuro_Theatre",
#         "Ortho_Theatre", 
#         "Cardio_Theatre",
#         "General_Theatre"
#     ]
    
#     with onto_mgr.onto:
#         for theatre_name in theatres:
#             # Check if theatre already exists
#             existing = onto_mgr.onto.search_one(iri=f"*{theatre_name}")
#             if not existing:
#                 onto_mgr.onto.Theatre(theatre_name)
#                 print(f"  ✅ Added {theatre_name}")
#             else:
#                 print(f"  ⏭️  {theatre_name} already exists")
    
#     onto_mgr.save()
    
#     # Add Surgeons
#     print("\n👨‍⚕️ Adding Surgeons...")
#     surgeons = [
#         ("Dr_Smith", "NS12345", "Neuro_Theatre"),
#         ("Dr_Johnson", "OS67890", "Ortho_Theatre"),
#         ("Dr_Williams", "CS78901", "Cardio_Theatre"),
#         ("Dr_Brown", "GS34567", "General_Theatre"),
#     ]
    
#     for name, license, theatre in surgeons:
#         success = onto_mgr.add_surgeon(name, license, theatre)
#         if success:
#             print(f"  ✅ Added {name} (License: {license}, Theatre: {theatre})")
#         else:
#             print(f"  ⚠️  Failed to add {name} (may already exist)")
    
#     # Add Timeslots
#     print("\n⏰ Adding Timeslots...")
#     timeslots = [
#         ("TimeSlot_08_00", "08:00", "10:30", 150),
#         ("TimeSlot_10_45", "10:45", "13:15", 150),
#         ("TimeSlot_14_00", "14:00", "16:30", 150),
#         ("TimeSlot_16_45", "16:45", "19:15", 150),
#     ]
    
#     for name, start, end, duration in timeslots:
#         success = onto_mgr.add_timeslot(name, start, end, duration)
#         if success:
#             print(f"  ✅ Added {name} ({start} - {end})")
#         else:
#             print(f"  ⚠️  Failed to add {name} (may already exist)")
    
#     # Add Sample Surgeries
#     print("\n🏥 Adding Sample Surgeries...")
#     surgeries = [
#         ("Brain_Surgery", "Dr_Smith", "Neuro_Theatre", "TimeSlot_08_00", 180, True),
#         ("Cardiac_Bypass_Surgery", "Dr_Williams", "Cardio_Theatre", "TimeSlot_10_45", 240, False),
#         ("Hip_Replacement_Surgery", "Dr_Johnson", "Ortho_Theatre", "TimeSlot_14_00", 120, False),
#         ("Appendectomy", "Dr_Brown", "General_Theatre", "TimeSlot_16_45", 90, True),
#     ]
    
#     for name, surgeon, theatre, timeslot, duration, is_emergency in surgeries:
#         success = onto_mgr.add_surgery(name, surgeon, theatre, timeslot, duration, is_emergency)
#         if success:
#             emergency_tag = "🚨 EMERGENCY" if is_emergency else ""
#             print(f"  ✅ Added {name} {emergency_tag}")
#         else:
#             print(f"  ⚠️  Failed to add {name} (may already exist)")
    
#     # Print summary
#     print("\n" + "=" * 60)
#     print("📊 Ontology Summary:")
#     summary = onto_mgr.get_ontology_summary()
#     print(f"  • Surgeons: {summary['surgeons']}")
#     print(f"  • Theatres: {summary['theatres']}")
#     print(f"  • Timeslots: {summary['timeslots']}")
#     print(f"  • Surgeries: {summary['surgeries']}")
#     print(f"  • Patients: {summary['patients']}")
#     print(f"  • Total Entities: {summary['total_entities']}")
#     print("=" * 60)
#     print("✅ Initialization Complete!")
#     print("\n💡 Tip: Restart your Streamlit app to see the changes")

# if __name__ == "__main__":
#     initialize_hospital_data()
