from owlready2 import *
from typing import List, Dict, Optional, Any
from datetime import time as Time
import os

def _get_value(prop, default=None) -> Any:
    """Safely get a property value, handling both list and scalar values."""
    if prop is None:
        return default
    if isinstance(prop, list):
        return prop[0] if prop else default
    return prop

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
            raise FileNotFoundError(f"Ontology file {owl_file} not found")
    
    
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

    def _get_patient_for_surgery(self, surgery) -> str:
        """Helper to find the patient undergoing a specific surgery"""
        for p in self.onto.Patient.instances():
            if surgery in p.undergoes_surgery:
                return p.name
        return 'N/A'
    
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
                    'patient': self._get_patient_for_surgery(surgery),
                    'start_time': _get_value(timeslot.start_time, 'N/A'),
                    'end_time': _get_value(timeslot.end_time, 'N/A'),
                    'theatre': _get_value(surgery.requires_theatre_type).name if surgery.requires_theatre_type else 'N/A'
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
                        'patient': self._get_patient_for_surgery(surgery),
                        'surgeon': _get_value(surgery.performs_operation).name if surgery.performs_operation else 'N/A',
                        'start_time': _get_value(timeslot.start_time, 'N/A'),
                        'end_time': _get_value(timeslot.end_time, 'N/A')
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
    
    def add_timeslot(self, name: str, start: str, end: str, duration: int, date: str = None) -> bool:
        """Add a new timeslot to the ontology"""
        try:
            with self.onto:
                timeslot = self.onto.TimeSlot(name)
                timeslot.start_time = [start]
                timeslot.end_time = [end]
                timeslot.duration = [duration]
                if date:
                    timeslot.date = [date]
            
            self.save()
            return True
        except Exception as e:
            print(f"Error adding timeslot: {e}")
            return False
    
    def get_timeslots_by_date(self, date: str) -> List:
        """Get all timeslots for a specific date (format: YYYY-MM-DD)"""
        try:
            all_timeslots = self.get_all_timeslots()
            return [ts for ts in all_timeslots if ts.date and ts.date[0] == date]
        except Exception as e:
            print(f"Error getting timeslots by date: {e}")
            return []
    
    def get_surgeries_by_date(self, date: str) -> List[Dict]:
        """Get all surgeries scheduled for a specific date"""
        try:
            timeslots = self.get_timeslots_by_date(date)
            surgeries = []
            
            for ts in timeslots:
                # Find surgeries in this timeslot
                for surgery in self.onto.Surgery.instances():
                    if surgery.has_timeslot and surgery.has_timeslot[0] == ts:
                        surgeries.append({
                            'surgery': surgery.name,
                            'patient': self._get_patient_for_surgery(surgery),
                            'surgeon': _get_value(surgery.performs_operation).name if surgery.performs_operation else 'N/A',
                            'theatre': _get_value(surgery.requires_theatre_type).name if surgery.requires_theatre_type else 'N/A',
                            'start_time': _get_value(ts.start_time, 'N/A'),
                            'end_time': _get_value(ts.end_time, 'N/A'),
                            'date': date,
                            'is_emergency': _get_value(surgery.is_emergency, False)
                        })
            
            return surgeries
        except Exception as e:
            print(f"Error getting surgeries by date: {e}")
            return []
    
    def get_theatre_schedule_by_date(self, theatre_name: str, date: str) -> List[Dict]:
        """Get surgeries scheduled in a specific theatre on a specific date"""
        try:
            all_surgeries = self.get_surgeries_by_date(date)
            return [s for s in all_surgeries if s['theatre'] == theatre_name]
        except Exception as e:
            print(f"Error getting theatre schedule by date: {e}")
            return []
    
    # ========== DELETE METHODS ==========
    
    def delete_surgery(self, surgery_name: str) -> bool:
        """Delete a surgery and its associated patient from the ontology"""
        try:
            # Find the surgery
            surgery = self.onto.search_one(iri=f"*{surgery_name}")
            if not surgery:
                print(f"❌ Surgery '{surgery_name}' not found")
                return False
            
            # Find and delete associated patient
            patients = [p for p in self.onto.Patient.instances() 
                       if surgery in p.undergoes_surgery]
            
            for patient in patients:
                print(f"🗑️ Deleting associated patient: {patient.name}")
                destroy_entity(patient)
            
            # Delete the surgery
            print(f"🗑️ Deleting surgery: {surgery_name}")
            destroy_entity(surgery)
            
            self.save()
            print(f"✅ Successfully deleted surgery '{surgery_name}' and associated data")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting surgery: {e}")
            return False
    
    def delete_patient(self, patient_name: str) -> bool:
        """Delete a patient from the ontology"""
        try:
            patient = self.onto.search_one(iri=f"*{patient_name}")
            if not patient:
                print(f"❌ Patient '{patient_name}' not found")
                return False
            
            print(f"🗑️ Deleting patient: {patient_name}")
            destroy_entity(patient)
            
            self.save()
            print(f"✅ Successfully deleted patient '{patient_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting patient: {e}")
            return False
    
    def delete_schedule_by_surgeon(self, surgeon_name: str) -> bool:
        """Delete all surgeries performed by a specific surgeon"""
        try:
            surgeon = self.get_surgeon_by_name(surgeon_name)
            if not surgeon:
                print(f"❌ Surgeon '{surgeon_name}' not found")
                return False
            
            surgeries = list(surgeon.performs_operation)
            if not surgeries:
                print(f"ℹ️ No surgeries found for surgeon '{surgeon_name}'")
                return True
            
            deleted_count = 0
            for surgery in surgeries:
                # Find and delete associated patients
                patients = [p for p in self.onto.Patient.instances() 
                           if surgery in p.undergoes_surgery]
                
                for patient in patients:
                    print(f"🗑️ Deleting patient: {patient.name}")
                    destroy_entity(patient)
                
                print(f"🗑️ Deleting surgery: {surgery.name}")
                destroy_entity(surgery)
                deleted_count += 1
            
            self.save()
            print(f"✅ Deleted {deleted_count} surgery(ies) for surgeon '{surgeon_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting schedules: {e}")
            return False
    
    def delete_schedule_by_timeslot(self, timeslot_name: str) -> bool:
        """Delete all surgeries in a specific timeslot"""
        try:
            timeslot = self.onto.search_one(iri=f"*{timeslot_name}")
            if not timeslot:
                print(f"❌ Timeslot '{timeslot_name}' not found")
                return False
            
            # Find surgeries in this timeslot
            surgeries = [s for s in self.onto.Surgery.instances() 
                        if s.has_timeslot and s.has_timeslot[0] == timeslot]
            
            if not surgeries:
                print(f"ℹ️ No surgeries found in timeslot '{timeslot_name}'")
                return True
            
            deleted_count = 0
            for surgery in surgeries:
                # Find and delete associated patients
                patients = [p for p in self.onto.Patient.instances() 
                           if surgery in p.undergoes_surgery]
                
                for patient in patients:
                    print(f"🗑️ Deleting patient: {patient.name}")
                    destroy_entity(patient)
                
                print(f"🗑️ Deleting surgery: {surgery.name}")
                destroy_entity(surgery)
                deleted_count += 1
            
            self.save()
            print(f"✅ Deleted {deleted_count} surgery(ies) from timeslot '{timeslot_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting schedules: {e}")
            return False
    
    def delete_all_schedules(self) -> bool:
        """Delete ALL surgeries and patients (WARNING: This clears all schedule data!)"""
        try:
            # Get all surgeries and patients
            surgeries = list(self.onto.Surgery.instances())
            patients = list(self.onto.Patient.instances())
            
            if not surgeries and not patients:
                print("ℹ️ No schedules to delete")
                return True
            
            # Delete all patients
            for patient in patients:
                print(f"🗑️ Deleting patient: {patient.name}")
                destroy_entity(patient)
            
            # Delete all surgeries
            for surgery in surgeries:
                print(f"🗑️ Deleting surgery: {surgery.name}")
                destroy_entity(surgery)
            
            self.save()
            print(f"✅ Deleted {len(surgeries)} surgery(ies) and {len(patients)} patient(s)")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting all schedules: {e}")
            return False
    
    def get_schedule_info(self, surgery_name: str) -> Optional[Dict]:
        """Get detailed information about a specific surgery schedule"""
        try:
            surgery = self.onto.search_one(iri=f"*{surgery_name}")
            if not surgery:
                return None
            
            # Get associated patient
            patient = None
            for p in self.onto.Patient.instances():
                if surgery in p.undergoes_surgery:
                    patient = p
                    break
            
            timeslot = _get_value(surgery.has_timeslot)
            info = {
                'surgery_name': surgery.name,
                'surgeon': _get_value(surgery.performs_operation).name if surgery.performs_operation else 'N/A',
                'theatre': _get_value(surgery.requires_theatre_type).name if surgery.requires_theatre_type else 'N/A',
                'timeslot': timeslot.name if timeslot else 'N/A',
                'start_time': _get_value(timeslot.start_time, 'N/A') if timeslot else 'N/A',
                'end_time': _get_value(timeslot.end_time, 'N/A') if timeslot else 'N/A',
                'duration': _get_value(surgery.estimated_duration, 'N/A'),
                'is_emergency': _get_value(surgery.is_emergency, False),
                'patient_name': patient.name if patient else 'N/A',
                'patient_ward': _get_value(patient.admitted_to).name if patient and patient.admitted_to else 'N/A',
                'recovery_room': _get_value(patient.assigned_to_recovery).name if patient and patient.assigned_to_recovery else 'N/A'
            }
            
            return info
            
        except Exception as e:
            print(f"❌ Error getting schedule info: {e}")
            return None
    
    def get_patient_info(self, patient_name: str) -> Optional[Dict]:
        """Get detailed information about a specific patient"""
        try:
            patient = self.onto.search_one(iri=f"*{patient_name}")
            if not patient:
                return None
            
            # Get surgery information
            surgery_info = 'No surgery scheduled'
            surgery_name = 'N/A'
            surgeon_name = 'N/A'
            timeslot_info = 'N/A'
            
            if patient.undergoes_surgery:
                surgery = patient.undergoes_surgery[0]
                surgery_name = surgery.name
                
                if surgery.performs_operation:
                    surgeon_name = surgery.performs_operation[0].name
                
                if surgery.has_timeslot:
                    ts = _get_value(surgery.has_timeslot)
                    start = _get_value(ts.start_time, 'N/A') if ts else 'N/A'
                    end = _get_value(ts.end_time, 'N/A') if ts else 'N/A'
                    timeslot_info = f"{start} to {end}"
                    surgery_info = f"{surgery_name} scheduled from {start} to {end}"
            
            severity_obj = _get_value(patient.has_severity)
            admission_ts = _get_value(patient.admitted_at_time)
            
            info = {
                'patient_name': patient.name,
                'surgery': surgery_name,
                'surgery_details': surgery_info,
                'surgeon': surgeon_name,
                'timeslot': timeslot_info,
                'ward': _get_value(patient.admitted_to).name if patient.admitted_to else 'N/A',
                'recovery_room': _get_value(patient.assigned_to_recovery).name if patient.assigned_to_recovery else 'N/A',
                'severity': _get_value(severity_obj.severity_level, 'N/A') if severity_obj and hasattr(severity_obj, 'severity_level') else 'N/A',
                'admission_time': _get_value(admission_ts.start_time, 'N/A') if admission_ts and hasattr(admission_ts, 'start_time') else 'N/A'
            }
            
            return info
            
        except Exception as e:
            print(f"❌ Error getting patient info: {e}")
            return None
    
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