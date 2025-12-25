from owlready2 import sync_reasoner_pellet, Imp
from typing import List, Dict, Tuple
from datetime import datetime

class ConflictDetector:
    """
    Detects scheduling conflicts using ontology reasoning
    and programmatic validation
    """
    
    def __init__(self, ontology_manager):
        self.onto_mgr = ontology_manager
        self.onto = ontology_manager.onto
    
    def run_pellet_reasoner(self):
        """Execute Pellet reasoner to infer conflicts"""
        try:
            print("🔄 Running Pellet reasoner...")
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            print("✅ Reasoner completed")
            return True
        except Exception as e:
            print(f"❌ Reasoner error: {e}")
            return False
    
    def add_swrl_rules(self):
        """Add SWRL rules for conflict detection"""
        with self.onto:
            # Rule 1: Scheduling Conflict - surgeon has overlapping surgeries
            rule1 = Imp()
            rule1.set_as_rule("""
                Surgeon(?s), performs_operation(?s, ?op1), performs_operation(?s, ?op2),
                has_timeslot(?op1, ?t1), has_timeslot(?op2, ?t2),
                has_temporal_overlap(?t1, ?t2), differentFrom(?op1, ?op2)
                -> SchedulingConflict(?s)
            """)
            
            # Rule 2: Theatre Conflict
            rule2 = Imp()
            rule2.set_as_rule("""
                requires_theatre_type(?s1, ?th), requires_theatre_type(?s2, ?th),
                has_timeslot(?s1, ?t1), has_timeslot(?s2, ?t2),
                has_temporal_overlap(?t1, ?t2), differentFrom(?s1, ?s2)
                -> TheatreConflict(?th)
            """)
            
            # Rule 3: Specialization Mismatch
            rule3 = Imp()
            rule3.set_as_rule("""
                Surgeon(?s), performs_operation(?s, ?op),
                requires_theatre_type(?op, ?th), works_in_theatre(?s, ?wt),
                differentFrom(?th, ?wt)
                -> SpecializationMismatch(?s)
            """)
            
            # Rule 4: Recovery Schedule
            rule4 = Imp()
            rule4.set_as_rule("""
                Patient(?p), is_assigned_to(?p, ?t), assigned_to_recovery(?p, ?r)
                -> hasRecoverySchedule(?p)
            """)
        
        self.onto_mgr.save()
        print("✅ SWRL rules added")
    
    # ========== PROGRAMMATIC CONFLICT DETECTION ==========
    
    def check_surgeon_conflicts(self, surgeon_name: str = None) -> List[Dict]:
        """Check if surgeon has overlapping surgeries"""
        conflicts = []
        
        surgeons = [self.onto_mgr.get_surgeon_by_name(surgeon_name)] if surgeon_name else self.onto_mgr.get_all_surgeons()
        
        for surgeon in surgeons:
            if not surgeon:
                continue
            
            surgeries = list(surgeon.performs_operation)
            
            # Compare all pairs of surgeries
            for i in range(len(surgeries)):
                for j in range(i + 1, len(surgeries)):
                    surgery1 = surgeries[i]
                    surgery2 = surgeries[j]
                    
                    if self._surgeries_overlap(surgery1, surgery2):
                        conflicts.append({
                            'type': 'Surgeon Double-Booking',
                            'surgeon': surgeon.name,
                            'surgery1': surgery1.name,
                            'surgery2': surgery2.name,
                            'severity': 'HIGH',
                            'description': f"{surgeon.name} is scheduled for two surgeries at overlapping times"
                        })
        
        return conflicts
    
    def check_theatre_conflicts(self, theatre_name: str = None) -> List[Dict]:
        """Check if theatre has overlapping bookings"""
        conflicts = []
        
        theatres = [self.onto.search_one(iri=f"*{theatre_name}")] if theatre_name else self.onto_mgr.get_all_theatres()
        
        for theatre in theatres:
            if not theatre:
                continue
            
            # Get all surgeries in this theatre
            surgeries = [s for s in self.onto.Surgery.instances() 
                        if s.requires_theatre_type and s.requires_theatre_type[0] == theatre]
            
            # Compare all pairs
            for i in range(len(surgeries)):
                for j in range(i + 1, len(surgeries)):
                    if self._surgeries_overlap(surgeries[i], surgeries[j]):
                        conflicts.append({
                            'type': 'Theatre Double-Booking',
                            'theatre': theatre.name,
                            'surgery1': surgeries[i].name,
                            'surgery2': surgeries[j].name,
                            'severity': 'HIGH',
                            'description': f"{theatre.name} is double-booked"
                        })
        
        return conflicts
    

    
    def check_specialization_mismatches(self) -> List[Dict]:
        """Check if surgeons are working in wrong theatre types"""
        mismatches = []
        
        for surgery in self.onto.Surgery.instances():
            if not surgery.performs_operation or not surgery.requires_theatre_type:
                continue
            
            surgeon = surgery.performs_operation[0]
            required_theatre = surgery.requires_theatre_type[0]
            
            if surgeon.works_in_theatre:
                surgeon_theatres = surgeon.works_in_theatre
                
                if required_theatre not in surgeon_theatres:
                    # Create readable list of allowed theatres
                    allowed_names = ", ".join([t.name for t in surgeon_theatres])
                    mismatches.append({
                        'type': 'Specialization Mismatch',
                        'surgeon': surgeon.name,
                        'surgery': surgery.name,
                        'surgeon_theatre': allowed_names,  # Keep key for compatibility, but content is list
                        'required_theatre': required_theatre.name,
                        'severity': 'MEDIUM',
                        'description': f"{surgeon.name} is authorized for [{allowed_names}] but surgery requires {required_theatre.name}"
                    })
        
        return mismatches
    
    def check_patient_conflicts(self, patient_name: str = None) -> List[Dict]:
        """Check if patient has overlapping surgeries"""
        conflicts = []
        
        patients = [self.onto.search_one(iri=f"*{patient_name}")] if patient_name else self.onto_mgr.get_all_patients()
        
        for patient in patients:
            if not patient:
                continue
            
            # Get all surgeries for this patient
            surgeries = patient.undergoes_surgery
            
            # Compare all pairs
            for i in range(len(surgeries)):
                for j in range(i + 1, len(surgeries)):
                    if self._surgeries_overlap(surgeries[i], surgeries[j]):
                        conflicts.append({
                            'type': 'Patient Double-Booking',
                            'patient': patient.name,
                            'surgery1': surgeries[i].name,
                            'surgery2': surgeries[j].name,
                            'severity': 'CRITICAL',
                            'description': f"Patient {patient.name} is scheduled for two surgeries at overlapping times"
                        })
        return conflicts

    def detect_all_conflicts(self) -> Dict[str, List[Dict]]:
        """Run all conflict detection checks"""
        return {
            'surgeon_conflicts': self.check_surgeon_conflicts(),
            'theatre_conflicts': self.check_theatre_conflicts(),
            'patient_conflicts': self.check_patient_conflicts(),
            'specialization_mismatches': self.check_specialization_mismatches()
        }
    
    # ========== HELPER METHODS ==========
    
    def _surgeries_overlap(self, surgery1, surgery2) -> bool:
        """Check if two surgeries have overlapping timeslots"""
        if not surgery1.has_timeslot or not surgery2.has_timeslot:
            return False
        
        ts1 = surgery1.has_timeslot[0]
        ts2 = surgery2.has_timeslot[0]
        
        # Check if timeslots have temporal overlap property
        if hasattr(ts1, 'has_temporal_overlap') and ts2 in ts1.has_temporal_overlap:
            return True
        
        # Check time strings using robust parsing
        if ts1.start_time and ts1.end_time and ts2.start_time and ts2.end_time:
            return self._times_overlap(
                ts1.start_time[0], ts1.end_time[0],
                ts2.start_time[0], ts2.end_time[0]
            )
        
        return False
    
    def _times_overlap(self, start1: str, end1: str, start2: str, end2: str) -> bool:
        """Check if two time ranges overlap using datetime objects"""
        try:
            # Helper to parse time string
            def parse_time(t_str):
                # Try multiple formats
                for fmt in ["%H:%M", "%H:%M:%S", "%I:%M %p"]:
                    try:
                        return datetime.strptime(t_str.strip(), fmt).time()
                    except ValueError:
                        continue
                return None

            s1 = parse_time(start1)
            e1 = parse_time(end1)
            s2 = parse_time(start2)
            e2 = parse_time(end2)

            if not all([s1, e1, s2, e2]):
                return False
            
            # Check overlap: start1 < end2 AND start2 < end1
            return s1 < e2 and s2 < e1
        except Exception as e:
            print(f"Time comparison error: {e}")
            return False