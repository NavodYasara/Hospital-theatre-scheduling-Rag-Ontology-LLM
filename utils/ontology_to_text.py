from typing import List, Dict

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
        license = surgeon.has_license_number[0] if surgeon.has_license_number else 'N/A'
        
        # Get specialization
        specialization = 'N/A'
        if surgeon.works_in_theatre:
            theatre = surgeon.works_in_theatre[0]
            specialization = theatre.name.replace('_Theatre', '').replace('_', ' ')
        
        # Get current surgeries
        surgeries = []
        for surgery in surgeon.performs_operation:
            if surgery.has_timeslot:
                ts = surgery.has_timeslot[0]
                start = ts.start_time[0] if ts.start_time else 'N/A'
                end = ts.end_time[0] if ts.end_time else 'N/A'
                surgeries.append(f"{surgery.name} ({start} - {end})")
        
        surgeries_text = ", ".join(surgeries) if surgeries else "No surgeries scheduled"
        
        text = f"""Surgeon: {surgeon.name}
        License Number: {license}
        Specialization: {specialization}
        Works In: {surgeon.works_in_theatre[0].name if surgeon.works_in_theatre else 'N/A'}
        Current Surgeries: {surgeries_text}
        This surgeon is qualified to perform surgeries requiring {specialization} expertise."""
        
        return text.strip()
    
    def theatre_to_text(self, theatre) -> str:
        """Convert theatre entity to natural language"""
        # Get surgeries scheduled in this theatre
        surgeries = []
        for surgery in self.onto.Surgery.instances():
            if surgery.requires_theatre_type and surgery.requires_theatre_type[0] == theatre:
                if surgery.has_timeslot:
                    ts = surgery.has_timeslot[0]
                    start = ts.start_time[0] if ts.start_time else 'N/A'
                    surgeon = surgery.performs_operation[0].name if surgery.performs_operation else 'N/A'
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
        surgeon = surgery.performs_operation[0].name if surgery.performs_operation else 'N/A'
        theatre = surgery.requires_theatre_type[0].name if surgery.requires_theatre_type else 'N/A'
        duration = surgery.estimated_duration[0] if surgery.estimated_duration else 'N/A'
        emergency = surgery.is_emergency[0] if surgery.is_emergency else False
        
        timeslot = 'Not scheduled'
        if surgery.has_timeslot:
            ts = surgery.has_timeslot[0]
            start = ts.start_time[0] if ts.start_time else 'N/A'
            end = ts.end_time[0] if ts.end_time else 'N/A'
            timeslot = f"{start} to {end}"
        
        
        emergency_text = "This is an EMERGENCY surgery requiring immediate attention." if emergency else ""
        
        text = f"""Surgery: {surgery.name}
        Surgeon: {surgeon}
        Theatre: {theatre}
        Scheduled Time: {timeslot}
        Duration: {duration} minutes
        Emergency Status: {'EMERGENCY' if emergency else 'Routine'}
        {emergency_text}"""
        
        return text.strip()
    
    def patient_to_text(self, patient) -> str:
        """Convert patient entity to natural language"""
        timeslot = 'Not assigned'
        if patient.is_assigned_to:
            ts = patient.is_assigned_to[0]
            start = ts.start_time[0] if ts.start_time else 'N/A'
            end = ts.end_time[0] if ts.end_time else 'N/A'
            timeslot = f"{start} to {end}"
        
        ward = patient.admitted_to[0].name if patient.admitted_to else 'N/A'
        recovery = patient.assigned_to_recovery[0].name if patient.assigned_to_recovery else 'N/A'
        
        text = f"""Patient: {patient.name}
        Surgery Timeslot: {timeslot}
        Admitted to Ward: {ward}
        Recovery Room: {recovery}
        This patient has a scheduled surgery and post-operative recovery plan."""
        
        return text.strip()
    
    def timeslot_to_text(self, timeslot) -> str:
        """Convert timeslot to natural language"""
        start = timeslot.start_time[0] if timeslot.start_time else 'N/A'
        end = timeslot.end_time[0] if timeslot.end_time else 'N/A'
        duration = timeslot.duration[0] if timeslot.duration else 'N/A'
        
        # Find surgeries in this timeslot
        surgeries = []
        for surgery in self.onto.Surgery.instances():
            if surgery.has_timeslot and surgery.has_timeslot[0] == timeslot:
                surgeon = surgery.performs_operation[0].name if surgery.performs_operation else 'Unknown'
                surgeries.append(f"{surgery.name} (Surgeon: {surgeon})")
        
        surgeries_text = ", ".join(surgeries) if surgeries else "Available - no surgeries scheduled"
        
        text = f"""Timeslot: {timeslot.name}
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