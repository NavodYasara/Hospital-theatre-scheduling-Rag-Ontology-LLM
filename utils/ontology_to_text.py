from typing import List, Dict, Any

def _get_value(prop, default=None) -> Any:
    """Safely get a property value, handling both list and scalar values."""
    if prop is None:
        return default
    if isinstance(prop, list):
        return prop[0] if prop else default
    return prop

class OntologyToText:
    """
    Converts ontology entities into natural language text chunks
    for vector database storage
    """
    
    def __init__(self, ontology_manager):
        self.onto_mgr = ontology_manager
        self.onto = ontology_manager.onto
    
    def surgeon_to_text(self, surgeon) -> str:
        """Convert surgeon entity to natural language"""
        license = _get_value(surgeon.has_license_number, 'N/A')
        
        # Get specialization
        specialization = 'N/A'
        if surgeon.works_in_theatre:
            theatre = _get_value(surgeon.works_in_theatre)
            specialization = theatre.name.replace('_Theatre', '').replace('_', ' ')
        
        # Get current surgeries
        surgeries = []
        for surgery in surgeon.performs_operation:
            if surgery.has_timeslot:
                ts = _get_value(surgery.has_timeslot)
                start = _get_value(ts.start_time, 'N/A') if ts else 'N/A'
                end = _get_value(ts.end_time, 'N/A') if ts else 'N/A'
                surgeries.append(f"{surgery.name} ({start} - {end})")
        
        surgeries_text = ", ".join(surgeries) if surgeries else "No surgeries scheduled"
        
        text = f"""Surgeon: {surgeon.name}
        License Number: {license}
        Specialization: {specialization}
        Works In: {_get_value(surgeon.works_in_theatre).name if surgeon.works_in_theatre else 'N/A'}
        Current Surgeries: {surgeries_text}
        This surgeon is qualified to perform surgeries requiring {specialization} expertise."""
        
        return text.strip()
    
    def theatre_to_text(self, theatre) -> str:
        """Convert theatre entity to natural language"""
        # Get surgeries scheduled in this theatre
        surgeries = []
        for surgery in self.onto.Surgery.instances():
            if surgery.requires_theatre_type and _get_value(surgery.requires_theatre_type) == theatre:
                if surgery.has_timeslot:
                    ts = _get_value(surgery.has_timeslot)
                    start = _get_value(ts.start_time, 'N/A') if ts else 'N/A'
                    surgeon = _get_value(surgery.performs_operation).name if surgery.performs_operation else 'N/A'
                    surgeries.append(f"{surgery.name} at {start} with {surgeon}")
        
        surgeries_text = ", ".join(surgeries) if surgeries else "No surgeries scheduled"
        theatre_type = theatre.name.replace('_Theatre', '').replace('_', ' ')
        
        text = f"""Theatre: {theatre.name}
        Type: {theatre_type}
        Specialization: {theatre_type} surgeries
        Current Schedule: {surgeries_text}
        This theatre is equipped for {theatre_type} surgical procedures."""
        
        return text.strip()
    
    def surgery_to_text(self, surgery) -> str:
        """Convert surgery entity to natural language"""
        surgeon = _get_value(surgery.performs_operation).name if surgery.performs_operation else 'N/A'
        theatre = _get_value(surgery.requires_theatre_type).name if surgery.requires_theatre_type else 'N/A'
        duration = _get_value(surgery.estimated_duration, 'N/A')
        emergency = _get_value(surgery.is_emergency, False)
        
        timeslot = 'Not scheduled'
        date = 'N/A'
        if surgery.has_timeslot:
            ts = _get_value(surgery.has_timeslot)
            start = _get_value(ts.start_time, 'N/A') if ts else 'N/A'
            end = _get_value(ts.end_time, 'N/A') if ts else 'N/A'
            date = _get_value(ts.date, 'N/A') if ts else 'N/A'
            timeslot = f"{start} to {end} on {date}"
        
        
        emergency_text = "This is an EMERGENCY surgery requiring immediate attention." if emergency else ""
        
        text = f"""Surgery: {surgery.name}
        Surgeon: {surgeon}
        Theatre: {theatre}
        Scheduled Date: {date}
        Scheduled Time: {timeslot}
        Duration: {duration} minutes
        Emergency Status: {'EMERGENCY' if emergency else 'Routine'}
        {emergency_text}"""
        
        return text.strip()
    
    def patient_to_text(self, patient) -> str:
        """Convert patient entity to natural language"""
        # Get surgery information
        surgery_info = 'No surgery scheduled'
        if patient.undergoes_surgery:
            surgery = _get_value(patient.undergoes_surgery)
            if surgery and surgery.has_timeslot:
                ts = _get_value(surgery.has_timeslot)
                start = _get_value(ts.start_time, 'N/A') if ts else 'N/A'
                end = _get_value(ts.end_time, 'N/A') if ts else 'N/A'
                surgery_info = f"{surgery.name} scheduled from {start} to {end}"
        
        # Get admission time
        admission_time = 'Not assigned'
        if patient.admitted_at_time:
            ts = _get_value(patient.admitted_at_time)
            start = _get_value(ts.start_time, 'N/A') if ts else 'N/A'
            admission_time = f"{start}"
        
        ward = _get_value(patient.admitted_to).name if patient.admitted_to else 'N/A'
        recovery = _get_value(patient.assigned_to_recovery).name if patient.assigned_to_recovery else 'N/A'
        severity_obj = _get_value(patient.has_severity)
        severity = _get_value(severity_obj.severity_level, 'N/A') if severity_obj and hasattr(severity_obj, 'severity_level') else 'N/A'
        
        text = f"""Patient: {patient.name}
        Surgery: {surgery_info}
        Admission Time: {admission_time}
        Admitted to Ward: {ward}
        Recovery Room: {recovery}
        Severity: {severity}
        This patient has a scheduled surgery and post-operative recovery plan."""
        
        return text.strip()
    
    def timeslot_to_text(self, timeslot) -> str:
        """Convert timeslot to natural language"""
        start = _get_value(timeslot.start_time, 'N/A')
        end = _get_value(timeslot.end_time, 'N/A')
        duration = _get_value(timeslot.duration, 'N/A')
        date = _get_value(timeslot.date, 'N/A')
        
        # Find surgeries in this timeslot
        surgeries = []
        for surgery in self.onto.Surgery.instances():
            if surgery.has_timeslot and _get_value(surgery.has_timeslot) == timeslot:
                surgeon = _get_value(surgery.performs_operation).name if surgery.performs_operation else 'Unknown'
                surgeries.append(f"{surgery.name} (Surgeon: {surgeon})")
        
        surgeries_text = ", ".join(surgeries) if surgeries else "Available - no surgeries scheduled"
        
        text = f"""Timeslot: {timeslot.name}
        Date: {date}
        Start Time: {start}
        End Time: {end}
        Duration: {duration} minutes
        Scheduled Surgeries: {surgeries_text}"""
        
        return text.strip()
    
    def convert_all(self) -> List[Dict]:
        """Convert entire ontology to text documents"""
        documents = []
        
        # Convert all surgeons
        for surgeon in self.onto.Surgeon.instances():
            documents.append({
                'text': self.surgeon_to_text(surgeon),
                'type': 'surgeon',
                'entity_id': surgeon.name
            })
        
        # Convert all theatres
        for theatre in self.onto.Theatre.instances():
            documents.append({
                'text': self.theatre_to_text(theatre),
                'type': 'theatre',
                'entity_id': theatre.name
            })
        
        # Convert all surgeries
        for surgery in self.onto.Surgery.instances():
            documents.append({
                'text': self.surgery_to_text(surgery),
                'type': 'surgery',
                'entity_id': surgery.name
            })
        
        # Convert all patients
        for patient in self.onto.Patient.instances():
            documents.append({
                'text': self.patient_to_text(patient),
                'type': 'patient',
                'entity_id': patient.name
            })
        
        # Convert all timeslots
        for timeslot in self.onto.TimeSlot.instances():
            documents.append({
                'text': self.timeslot_to_text(timeslot),
                'type': 'timeslot',
                'entity_id': timeslot.name
            })
        
        # Add general knowledge
        documents.append({
            'text': """Hospital Scheduling Rules:
                1. Each surgeon can only perform one surgery at a time
                2. Each theatre can only host one surgery at a time
                3. Surgeons should operate in their specialization theatre
                4. Emergency surgeries have higher priority than routine surgeries
                5. Minimum rest time between surgeries should be respected
                6. Post-operative recovery rooms must be available""",
            'type': 'rules',
            'entity_id': 'scheduling_rules'
        })
        
        return documents