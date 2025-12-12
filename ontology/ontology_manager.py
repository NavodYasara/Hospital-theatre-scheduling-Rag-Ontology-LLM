from owlready2 import *
from typing import List, Dict, Optional
from datetime import time as Time
import os

class OntologyManager:
    """
    Main interface for hospital ontology operations
    Handles all CRUD operations on the knowledge base
    """
    
    def __init__(self, owl_file: str = "ontology/hospital.owl"):
        """Initialize ontology manager"""
        self.owl_file = owl_file
        
        # Load or create ontology
        if os.path.exists(owl_file):
            self.onto = get_ontology(owl_file).load()
            print(f"✅ Loaded existing ontology from {owl_file}")
        else:
            self.onto = self._create_new_ontology()
            print(f"✅ Created new ontology")
    
    def _create_new_ontology(self):
        """Create a new ontology with schema"""
        onto = get_ontology("http://test.org/hospital.owl")
        
        with onto:
            # Base Classes
            class Person(Thing): pass
            class Location(Thing): pass
            class ClinicalProcess(Thing): pass
            class Resource(Thing): pass
            
            # Conflict Classes
            class SchedulingConflict(Thing): pass
            class EquipmentConflict(SchedulingConflict): pass
            class TheatreConflict(SchedulingConflict): pass
            class SpecializationMismatch(SchedulingConflict): pass
            class hasRecoverySchedule(Thing): pass
            
            # Person Subclasses
            class Staff(Person): pass
            class Surgeon(Staff): pass
            class Nurse(Staff): pass
            class Anesthetist(Staff): pass
            class Patient(Person): pass
            
            # Location Subclasses
            class Theatre(Location): pass
            class Ward(Location): pass
            class RecoveryRoom(Location): pass
            
            # Clinical Process Subclasses
            class MedicalProcedure(ClinicalProcess): pass
            class Surgery(MedicalProcedure): pass
            class TimeSlot(ClinicalProcess): pass
            
            # Resource Subclasses
            class SurgicalEquipment(Resource): pass
            
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
                range = [str]
            
            class end_time(DataProperty):
                domain = [TimeSlot]
                range = [str]
            
            class duration(DataProperty):
                domain = [TimeSlot]
                range = [int]
        
        onto.save(file=self.owl_file, format="rdfxml")
        return onto
    
    # ========== QUERY METHODS ==========
    
    def get_all_surgeons(self) -> List:
        """Return all surgeon instances"""
        return list(self.onto.Surgeon.instances())
    
    def get_surgeon_by_name(self, name: str):
        """Find surgeon by name"""
        return self.onto.search_one(iri=f"*{name}")
    
    def get_all_theatres(self) -> List:
        """Return all theatre instances"""
        return list(self.onto.Theatre.instances())
    
    def get_all_surgeries(self) -> List:
        """Return all surgery instances"""
        return list(self.onto.Surgery.instances())
    
    def get_all_patients(self) -> List:
        """Return all patient instances"""
        return list(self.onto.Patient.instances())
    
    def get_all_timeslots(self) -> List:
        """Return all timeslot instances"""
        return list(self.onto.TimeSlot.instances())
    
    def get_surgeon_schedule(self, surgeon_name: str) -> List[Dict]:
        """Get all surgeries for a specific surgeon"""
        surgeon = self.get_surgeon_by_name(surgeon_name)
        if not surgeon:
            return []
        
        schedule = []
        for surgery in surgeon.performs_operation:
            if surgery.has_timeslot:
                timeslot = surgery.has_timeslot[0]
                schedule.append({
                    'surgery': surgery.name,
                    'start_time': timeslot.start_time[0] if timeslot.start_time else 'N/A',
                    'end_time': timeslot.end_time[0] if timeslot.end_time else 'N/A',
                    'theatre': surgery.requires_theatre_type[0].name if surgery.requires_theatre_type else 'N/A'
                })
        return schedule
    
    def get_theatre_schedule(self, theatre_name: str) -> List[Dict]:
        """Get all surgeries scheduled in a specific theatre"""
        theatre = self.onto.search_one(iri=f"*{theatre_name}")
        if not theatre:
            return []
        
        schedule = []
        for surgery in self.onto.Surgery.instances():
            if surgery.requires_theatre_type and surgery.requires_theatre_type[0] == theatre:
                if surgery.has_timeslot:
                    timeslot = surgery.has_timeslot[0]
                    schedule.append({
                        'surgery': surgery.name,
                        'surgeon': surgery.performs_operation[0].name if surgery.performs_operation else 'N/A',
                        'start_time': timeslot.start_time[0] if timeslot.start_time else 'N/A',
                        'end_time': timeslot.end_time[0] if timeslot.end_time else 'N/A'
                    })
        return schedule
    
    # ========== CREATE METHODS ==========
    
    def add_surgeon(self, name: str, license_number: str, theatre_name: str) -> bool:
        """Add a new surgeon to the ontology"""
        try:
            with self.onto:
                surgeon = self.onto.Surgeon(name)
                surgeon.has_license_number = [license_number]
                
                # Find or create theatre
                theatre = self.onto.search_one(iri=f"*{theatre_name}")
                if theatre:
                    surgeon.works_in_theatre = [theatre]
                
            self.save()
            return True
        except Exception as e:
            print(f"Error adding surgeon: {e}")
            return False
    
    def add_surgery(self, name: str, surgeon_name: str, theatre_name: str, 
                   timeslot_name: str, duration: int, is_emergency: bool = False) -> bool:
        """Add a new surgery to the ontology"""
        try:
            with self.onto:
                surgery = self.onto.Surgery(name)
                surgery.estimated_duration = [duration]
                surgery.is_emergency = [is_emergency]
                
                # Link surgeon
                surgeon = self.get_surgeon_by_name(surgeon_name)
                if surgeon:
                    surgery.performs_operation = [surgeon]
                
                # Link theatre
                theatre = self.onto.search_one(iri=f"*{theatre_name}")
                if theatre:
                    surgery.requires_theatre_type = [theatre]
                
                # Link timeslot
                timeslot = self.onto.search_one(iri=f"*{timeslot_name}")
                if timeslot:
                    surgery.has_timeslot = [timeslot]
            
            self.save()
            return True
        except Exception as e:
            print(f"Error adding surgery: {e}")
            return False
    
    def add_timeslot(self, name: str, start: str, end: str, duration: int) -> bool:
        """Add a new timeslot to the ontology"""
        try:
            with self.onto:
                timeslot = self.onto.TimeSlot(name)
                timeslot.start_time = [start]
                timeslot.end_time = [end]
                timeslot.duration = [duration]
            
            self.save()
            return True
        except Exception as e:
            print(f"Error adding timeslot: {e}")
            return False
    
    # ========== UTILITY METHODS ==========
    
    def count_entities(self) -> int:
        """Count total entities in ontology"""
        return len(list(self.onto.individuals()))
    
    def save(self):
        """Save ontology changes"""
        self.onto.save(file=self.owl_file, format="rdfxml")
        print("💾 Ontology saved")
    
    def get_ontology_summary(self) -> Dict:
        """Get summary statistics"""
        return {
            'total_entities': self.count_entities(),
            'surgeons': len(list(self.onto.Surgeon.instances())),
            'theatres': len(list(self.onto.Theatre.instances())),
            'surgeries': len(list(self.onto.Surgery.instances())),
            'patients': len(list(self.onto.Patient.instances())),
            'timeslots': len(list(self.onto.TimeSlot.instances()))
        }