# ============================================================================
# FILE: app.py - MAIN STREAMLIT APPLICATION
# ============================================================================
import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ontology.ontology_manager import OntologyManager
from ontology.reasoner import ConflictDetector
from rag.retriever import RAGRetriever
from llm.ollama_client import OllamaClient
from llm.prompt_templates import SYSTEM_PROMPT, CHECK_AVAILABILITY_PROMPT, DETECT_CONFLICTS_PROMPT

# Page configuration
st.set_page_config(
    page_title="🏥 Hospital Theatre Scheduling",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.chat_history = []

# Initialize system components
@st.cache_resource
def initialize_system():
    """Initialize all system components"""
    try:
        # Initialize ontology manager
        onto_mgr = OntologyManager("ontology/hospital.owl")
        
        # Initialize conflict detector
        conflict_detector = ConflictDetector(onto_mgr)
        
        # Initialize RAG retriever
        rag_retriever = RAGRetriever(onto_mgr)
        rag_retriever.initialize()
        
        # Initialize LLM client
        llm_client = OllamaClient(model="llama3.1:8b")  # Change model as needed
        
        return onto_mgr, conflict_detector, rag_retriever, llm_client, None
    except Exception as e:
        return None, None, None, None, str(e)

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.title("🏥 Hospital System")
        st.markdown("---")
        
        # Initialize system
        onto_mgr, conflict_detector, rag_retriever, llm_client, error = initialize_system()
        
        if error:
            st.error(f"❌ Initialization Error: {error}")
            st.stop()
        
        # System status
        st.subheader("📊 System Status")
        summary = onto_mgr.get_ontology_summary()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Surgeons", summary['surgeons'])
            st.metric("Theatres", summary['theatres'])
            st.metric("Patients", summary['patients'])
        with col2:
            st.metric("Surgeries", summary['surgeries'])
            st.metric("Timeslots", summary['timeslots'])
            st.metric("Total Entities", summary['total_entities'])
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Refresh Data"):
            st.cache_resource.clear()
            st.rerun()
        
        if st.button("🔍 Run Conflict Scan"):
            st.session_state.run_conflict_scan = True
        
        st.markdown("---")
        
        # LLM Model Selection
        st.subheader("🤖 LLM Settings")
        available_models = ["llama3.1:8b", "mistral", "phi3:mini", "llama2", "qwen:1.8b"]
        selected_model = st.selectbox("Model:", available_models, index=0)
        
        if selected_model != llm_client.model:
            llm_client.model = selected_model
            st.info(f"Switched to {selected_model}")
    
    # Main content
    st.title("🏥 Intelligent Hospital Theatre Scheduling Assistant")
    st.caption("Powered by Ontology + RAG + Ollama LLM")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Chat Assistant", 
        "🔍 Conflict Detection", 
        "📊 Schedule View",
        "➕ Add Schedule",
        "🗑️ Delete Schedule"
    ])
    
    # TAB 1: Chat Assistant
    with tab1:
        st.header("Chat with Scheduling Assistant")
        
        # Example queries
        with st.expander("💡 Example Questions"):
            st.markdown("""
            - Is Dr. Smith available tomorrow at 9 AM?
            - Which surgeons specialize in cardiology?
            - Show me all surgeries scheduled for today
            - Are there any conflicts in the current schedule?
            - Suggest a time slot for an emergency brain surgery
            """)
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message['role']):
                st.write(message['content'])
                
                if 'sources' in message and message['sources']:
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(message['sources'][:3], 1):
                            st.caption(f"{i}. {source[:200]}...")
        
        # Chat input
        user_query = st.chat_input("Ask about schedules, availability, conflicts...")
        
        if user_query:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_query
            })
            
            with st.chat_message('user'):
                st.write(user_query)
            
            # Generate response
            with st.chat_message('assistant'):
                with st.spinner('🤔 Thinking...'):
                    # Retrieve context
                    context = rag_retriever.retrieve_context(user_query, top_k=5)
                    context_str = rag_retriever.get_formatted_context(context)
                    
                    # Generate LLM response
                    response = llm_client.generate(
                        prompt=user_query,
                        context=context_str,
                        system_prompt=SYSTEM_PROMPT
                    )
                    
                    st.write(response)
                    
                    # Add to history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response,
                        'sources': context['sources']
                    })
            
            # Rerun to update chat display
            st.rerun()
    
    # TAB 2: Conflict Detection
    with tab2:
        st.header("Conflict Detection & Analysis")
        
        st.markdown("""
        This system automatically detects:
        - 👨‍⚕️ **Surgeon Double-Bookings**: Same surgeon scheduled for multiple surgeries at overlapping times
        - 🏥 **Theatre Conflicts**: Same theatre booked for multiple surgeries simultaneously
        - 🔍 **Specialization Mismatches**: Surgeons operating in theatres outside their specialization
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            if st.button("🔍 Scan for Conflicts", type="primary"):
                st.session_state.run_conflict_scan = True
        
        if st.session_state.get('run_conflict_scan', False):
            with st.spinner("🔄 Analyzing schedules..."):
                conflicts = conflict_detector.detect_all_conflicts()
                
                total_conflicts = sum(len(v) for v in conflicts.values())
                
                if total_conflicts == 0:
                    st.success("✅ No conflicts detected! All schedules are valid.")
                else:
                    st.error(f"⚠️ Found {total_conflicts} conflict(s)")
                    
                    # Display conflicts by type
                    if conflicts.get('patient_conflicts'):
                        st.subheader("👤 Patient Double-Bookings (CRITICAL)")
                        for conflict in conflicts['patient_conflicts']:
                            with st.expander(f"🚫 {conflict['patient']} - {conflict['severity']} SEVERITY", expanded=True):
                                st.error(f"**Description:** {conflict['description']}")
                                st.write(f"**Conflicting Surgeries:**")
                                st.write(f"- {conflict['surgery1']}")
                                st.write(f"- {conflict['surgery2']}")
                                
                                st.markdown("**💡 Suggested Resolution:**")
                                st.info("IMMEDIATELY reschedule one surgery. A patient cannot be in two places at once.")

                    if conflicts.get('surgeon_conflicts'):
                        st.subheader("👨‍⚕️ Surgeon Double-Bookings")
                        for conflict in conflicts['surgeon_conflicts']:
                            with st.expander(f"⚠️ {conflict['surgeon']} - {conflict['severity']} SEVERITY"):
                                st.write(f"**Description:** {conflict['description']}")
                                st.write(f"**Conflicting Surgeries:**")
                                st.write(f"- {conflict['surgery1']}")
                                st.write(f"- {conflict['surgery2']}")
                                
                                st.markdown("**💡 Suggested Resolution:**")
                                st.info("Reschedule one surgery to a non-overlapping time slot or assign a different qualified surgeon.")
                    
                    if conflicts['theatre_conflicts']:
                        st.subheader("🏥 Theatre Double-Bookings")
                        for conflict in conflicts['theatre_conflicts']:
                            with st.expander(f"⚠️ {conflict['theatre']} - {conflict['severity']} SEVERITY"):
                                st.write(f"**Description:** {conflict['description']}")
                                st.write(f"**Conflicting Surgeries:**")
                                st.write(f"- {conflict['surgery1']}")
                                st.write(f"- {conflict['surgery2']}")
                                
                                st.markdown("**💡 Suggested Resolution:**")
                                st.info("Move one surgery to an available alternative theatre or adjust the time slots.")
                    
                    if conflicts['specialization_mismatches']:
                        st.subheader("🔍 Specialization Mismatches")
                        for conflict in conflicts['specialization_mismatches']:
                            with st.expander(f"⚠️ {conflict['surgeon']} - {conflict['severity']} SEVERITY"):
                                st.write(f"**Description:** {conflict['description']}")
                                st.write(f"**Surgeon's Theatre:** {conflict['surgeon_theatre']}")
                                st.write(f"**Required Theatre:** {conflict['required_theatre']}")
                                
                                st.markdown("**💡 Suggested Resolution:**")
                                st.info("Assign a surgeon who specializes in this theatre type or relocate the surgery to the surgeon's specialized theatre.")
            
            st.session_state.run_conflict_scan = False
    
    # TAB 3: Schedule View
    with tab3:
        st.header("Current Schedules")
        
        view_type = st.selectbox("View by:", ["Surgeon", "Theatre", "All Timeslots"])
        
        if view_type == "Surgeon":
            surgeons = onto_mgr.get_all_surgeons()
            surgeon_names = [s.name for s in surgeons]
            
            if surgeon_names:
                selected = st.selectbox("Select Surgeon:", surgeon_names)
                
                if selected:
                    st.subheader(f"📅 Schedule for {selected}")
                    schedule = onto_mgr.get_surgeon_schedule(selected)
                    
                    if schedule:
                        for item in schedule:
                            with st.container():
                                col1, col2, col3 = st.columns(3)
                                col1.write(f"**{item['surgery']}**")
                                col2.write(f"🕐 {item['start_time']} - {item['end_time']}")
                                col3.write(f"🏥 {item['theatre']}")
                                st.markdown("---")
                    else:
                        st.info("No surgeries scheduled for this surgeon")
            else:
                st.warning("No surgeons found in the ontology")
        
        elif view_type == "Theatre":
            theatres = onto_mgr.get_all_theatres()
            theatre_names = [t.name for t in theatres]
            
            if theatre_names:
                selected = st.selectbox("Select Theatre:", theatre_names)
                
                if selected:
                    st.subheader(f"📅 Schedule for {selected}")
                    schedule = onto_mgr.get_theatre_schedule(selected)
                    
                    if schedule:
                        for item in schedule:
                            with st.container():
                                col1, col2, col3 = st.columns(3)
                                col1.write(f"**{item['surgery']}**")
                                col2.write(f"👨‍⚕️ {item['surgeon']}")
                                col3.write(f"🕐 {item['start_time']} - {item['end_time']}")
                                st.markdown("---")
                    else:
                        st.info("No surgeries scheduled in this theatre")
            else:
                st.warning("No theatres found in the ontology")
        
        elif view_type == "All Timeslots":
            st.subheader("📅 All Scheduled Timeslots")
            timeslots = onto_mgr.get_all_timeslots()
            
            if timeslots:
                for ts in timeslots:
                    with st.expander(f"⏰ {ts.name} ({ts.start_time[0] if ts.start_time else 'N/A'} - {ts.end_time[0] if ts.end_time else 'N/A'})"):
                        # Find surgeries in this timeslot
                        surgeries = [s for s in onto_mgr.get_all_surgeries() 
                                   if s.has_timeslot and s.has_timeslot[0] == ts]
                        
                        if surgeries:
                            for surgery in surgeries:
                                col1, col2, col3 = st.columns(3)
                                col1.write(f"**Surgery:** {surgery.name}")
                                
                                surgeon = surgery.performs_operation[0].name if surgery.performs_operation else 'N/A'
                                col2.write(f"**Surgeon:** {surgeon}")
                                
                                theatre = surgery.requires_theatre_type[0].name if surgery.requires_theatre_type else 'N/A'
                                col3.write(f"**Theatre:** {theatre}")
                                
                                st.markdown("---")
                        else:
                            st.info("No surgeries scheduled in this timeslot")
            else:
                st.warning("No timeslots found in the ontology")
    
    # TAB 4: Add Schedule
    with tab4:
        st.header("➕ Add New Surgery Schedule")
        
        st.markdown("Fill in the details below to schedule a new surgery:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Surgery Details")
            
            # Surgery Type Dropdown (instead of text input)
            surgery_types = [
                "Brain_Surgery",
                "Cardiac_Bypass_Surgery",
                "Hip_Replacement_Surgery",
                "Knee_Arthroscopy",
                "Appendectomy",
                "Spinal_Surgery",
                "Cataract_Surgery",
                "Hernia_Repair",
                "Gallbladder_Removal",
                "Thyroid_Surgery",
                "Custom (Type Below)"
            ]
            
            selected_surgery_type = st.selectbox(
                "Surgery Type",
                surgery_types,
                help="Select a surgery type from the list or choose 'Custom' to enter your own"
            )
            
            # Show text input only if "Custom" is selected
            if selected_surgery_type == "Custom (Type Below)":
                surgery_name = st.text_input(
                    "Custom Surgery Name",
                    placeholder="e.g., Knee_Arthroscopy",
                    help="Enter a custom surgery name using underscores instead of spaces"
                )
            else:
                surgery_name = selected_surgery_type
                st.info(f"Selected: **{surgery_name}**")
            
            # Get available surgeons
            surgeons = onto_mgr.get_all_surgeons()
            surgeon_names = [s.name for s in surgeons]
            
            if surgeon_names:
                selected_surgeon = st.selectbox("Select Surgeon", surgeon_names)
            else:
                st.warning("No surgeons available")
                selected_surgeon = None
            
            duration = st.number_input("Estimated Duration (minutes)", min_value=30, max_value=600, value=120, step=15)
            
            is_emergency = st.checkbox("Emergency Surgery", value=False)
        
        with col2:
            st.subheader("Theatre & Time")
            
            # Get available theatres
            theatres = onto_mgr.get_all_theatres()
            theatre_names = [t.name for t in theatres]
            
            if theatre_names:
                selected_theatre = st.selectbox("Select Theatre", theatre_names)
            else:
                st.warning("No theatres available")
                selected_theatre = None
            
            # Get available timeslots
            timeslots = onto_mgr.get_all_timeslots()
            timeslot_names = [f"{ts.name} ({ts.start_time[0] if ts.start_time else 'N/A'} - {ts.end_time[0] if ts.end_time else 'N/A'})" 
                             for ts in timeslots]
            
            if timeslot_names:
                selected_timeslot_display = st.selectbox("Select Timeslot", timeslot_names)
                selected_timeslot = timeslots[timeslot_names.index(selected_timeslot_display)].name
            else:
                st.warning("No timeslots available")
                selected_timeslot = None
        
        # Patient Information Section (NEW)
        st.markdown("---")
        st.subheader("👤 Patient Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            patient_name = st.text_input(
                "Patient Name",
                placeholder="e.g., Patient_John_Doe",
                help="Enter patient name using underscores instead of spaces"
            )
        
        with col4:
            # Severity Level Dropdown (NEW)
            severity_levels = ["Severe", "Moderate", "Mild", "Minor"]
            selected_severity = st.selectbox(
                "Patient Severity Level",
                severity_levels,
                index=1,  # Default to "Moderate"
                help="Select the severity level for this patient"
            )
        
        # Additional patient details
        col5, col6 = st.columns(2)
        
        with col5:
            # Get available wards
            wards = list(onto_mgr.onto.Ward.instances())
            ward_names = [w.name for w in wards] if wards else ["General_Ward"]
            
            selected_ward = st.selectbox(
                "Admission Ward",
                ward_names,
                help="Select the ward where patient will be admitted"
            )
        
        with col6:
            # Get available recovery rooms
            recovery_rooms = list(onto_mgr.onto.RecoveryRoom.instances())
            recovery_room_names = [r.name for r in recovery_rooms] if recovery_rooms else ["Recovery_Room_A"]
            
            selected_recovery = st.selectbox(
                "Recovery Room",
                recovery_room_names,
                help="Select the recovery room for post-operative care"
            )
        
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Add Surgery Schedule", type="primary"):
                # Validation
                if not surgery_name:
                    st.error("Please select or enter a surgery name")
                elif not selected_surgeon:
                    st.error("Please select a surgeon")
                elif not selected_theatre:
                    st.error("Please select a theatre")
                elif not selected_timeslot:
                    st.error("Please select a timeslot")
                elif not patient_name:
                    st.error("Please enter a patient name")
                else:
                    # Check for conflicts before adding
                    with st.spinner("Creating surgery schedule..."):
                        try:
                            # Add the surgery
                            success = onto_mgr.add_surgery(
                                name=surgery_name,
                                surgeon_name=selected_surgeon,
                                theatre_name=selected_theatre,
                                timeslot_name=selected_timeslot,
                                duration=duration,
                                is_emergency=is_emergency
                            )
                            
                            if success:
                                # Add patient with all details
                                with onto_mgr.onto:
                                    # Create patient
                                    patient = onto_mgr.onto.Patient(patient_name)
                                    
                                    # Find severity instance
                                    severity_instance = onto_mgr.onto.search_one(iri=f"*{selected_severity}")
                                    if severity_instance:
                                        patient.has_severity = [severity_instance]
                                    
                                    # Find timeslot
                                    timeslot_instance = onto_mgr.onto.search_one(iri=f"*{selected_timeslot}")
                                    if timeslot_instance:
                                        patient.is_assigned_to = [timeslot_instance]
                                    
                                    # Find ward
                                    ward_instance = onto_mgr.onto.search_one(iri=f"*{selected_ward}")
                                    if ward_instance:
                                        patient.admitted_to = [ward_instance]
                                    
                                    # Find recovery room
                                    recovery_instance = onto_mgr.onto.search_one(iri=f"*{selected_recovery}")
                                    if recovery_instance:
                                        patient.assigned_to_recovery = [recovery_instance]
                                    
                                    # Link patient to surgery
                                    surgery_instance = onto_mgr.onto.search_one(iri=f"*{surgery_name}")
                                    if surgery_instance:
                                        patient.undergoes_surgery = [surgery_instance]
                                
                                # Save changes
                                onto_mgr.save()
                                
                                st.success(f"✅ Surgery schedule created successfully!")
                                st.success(f"   • Surgery: **{surgery_name}**")
                                st.success(f"   • Patient: **{patient_name}** (Severity: {selected_severity})")
                                st.success(f"   • Surgeon: **{selected_surgeon}**")
                                st.success(f"   • Theatre: **{selected_theatre}**")
                                st.success(f"   • Time: **{selected_timeslot}**")
                                
                                st.info("💡 Tip: Go to 'Conflict Detection' tab to verify no conflicts exist")
                                
                                # Clear cache to reload data
                                st.cache_resource.clear()
                            else:
                                st.error("❌ Failed to add surgery. Check logs for details.")
                        
                        except Exception as e:
                            st.error(f"❌ Error creating schedule: {str(e)}")
                            st.exception(e)
        
        with col2:
            if st.button("🔍 Preview Conflicts"):
                if selected_surgeon and selected_timeslot:
                    with st.spinner("Checking for potential conflicts..."):
                        conflicts = conflict_detector.detect_all_conflicts()
                        
                        total_conflicts = sum(len(v) for v in conflicts.values())
                        
                        if total_conflicts == 0:
                            st.success("✅ No conflicts detected with current schedules!")
                        else:
                            st.warning(f"⚠️ Found {total_conflicts} potential conflict(s)")
                            
                            if conflicts['surgeon_conflicts']:
                                st.error(f"👨‍⚕️ Surgeon conflicts: {len(conflicts['surgeon_conflicts'])}")
                            if conflicts['theatre_conflicts']:
                                st.error(f"🏥 Theatre conflicts: {len(conflicts['theatre_conflicts'])}")
                else:
                    st.warning("Fill in surgeon and timeslot first")
        
        with col3:
            if st.button("🔄 Reset Form"):
                st.rerun()
    
    # TAB 5: Delete Schedule
    with tab5:
        st.header("🗑️ Delete Surgery Schedules")
        
        st.warning("⚠️ **Warning:** Deleting a schedule will permanently remove the surgery and associated patient data from the ontology.")
        
        # Delete options
        delete_option = st.radio(
            "Select deletion method:",
            ["Delete Specific Surgery", "Delete by Surgeon", "Delete by Timeslot", "Delete All Schedules"],
            horizontal=False
        )
        
        st.markdown("---")
        
        if delete_option == "Delete Specific Surgery":
            st.subheader("🔍 Delete a Specific Surgery")
            
            # Get all surgeries
            surgeries = onto_mgr.get_all_surgeries()
            surgery_names = [s.name for s in surgeries]
            
            if surgery_names:
                selected_surgery = st.selectbox("Select Surgery to Delete:", surgery_names)
                
                # Show surgery details
                if selected_surgery:
                    st.markdown("### 📋 Surgery Details")
                    info = onto_mgr.get_schedule_info(selected_surgery)
                    
                    if info:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Surgery:** {info['surgery_name']}")
                            st.write(f"**Surgeon:** {info['surgeon']}")
                            st.write(f"**Theatre:** {info['theatre']}")
                            st.write(f"**Time:** {info['start_time']} - {info['end_time']}")
                        with col2:
                            st.write(f"**Patient:** {info['patient_name']}")
                            st.write(f"**Ward:** {info['patient_ward']}")
                            st.write(f"**Recovery Room:** {info['recovery_room']}")
                            st.write(f"**Emergency:** {'Yes' if info['is_emergency'] else 'No'}")
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button("🗑️ Delete Surgery", type="primary", key="delete_single"):
                            with st.spinner("Deleting surgery..."):
                                success = onto_mgr.delete_surgery(selected_surgery)
                                if success:
                                    st.success(f"✅ Successfully deleted surgery '{selected_surgery}'")
                                    st.info("💡 Refreshing data...")
                                    st.cache_resource.clear()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete surgery")
            else:
                st.info("No surgeries found in the system")
        
        elif delete_option == "Delete by Surgeon":
            st.subheader("👨‍⚕️ Delete All Surgeries by Surgeon")
            
            surgeons = onto_mgr.get_all_surgeons()
            surgeon_names = [s.name for s in surgeons]
            
            if surgeon_names:
                selected_surgeon = st.selectbox("Select Surgeon:", surgeon_names)
                
                # Show surgeon's schedule
                if selected_surgeon:
                    st.markdown("### 📅 Surgeon's Current Schedule")
                    schedule = onto_mgr.get_surgeon_schedule(selected_surgeon)
                    
                    if schedule:
                        for item in schedule:
                            with st.container():
                                col1, col2, col3 = st.columns(3)
                                col1.write(f"**{item['surgery']}**")
                                col2.write(f"🕐 {item['start_time']} - {item['end_time']}")
                                col3.write(f"🏥 {item['theatre']}")
                                st.markdown("---")
                        
                        st.warning(f"⚠️ This will delete **{len(schedule)} surgery(ies)** and associated patient data")
                        
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if st.button("🗑️ Delete All", type="primary", key="delete_surgeon"):
                                with st.spinner(f"Deleting schedules for {selected_surgeon}..."):
                                    success = onto_mgr.delete_schedule_by_surgeon(selected_surgeon)
                                    if success:
                                        st.success(f"✅ Successfully deleted all schedules for '{selected_surgeon}'")
                                        st.cache_resource.clear()
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to delete schedules")
                    else:
                        st.info(f"No surgeries scheduled for {selected_surgeon}")
            else:
                st.info("No surgeons found in the system")
        
        elif delete_option == "Delete by Timeslot":
            st.subheader("⏰ Delete All Surgeries in a Timeslot")
            
            timeslots = onto_mgr.get_all_timeslots()
            timeslot_names = [f"{ts.name} ({ts.start_time[0] if ts.start_time else 'N/A'} - {ts.end_time[0] if ts.end_time else 'N/A'})" 
                             for ts in timeslots]
            
            if timeslot_names:
                selected_timeslot_display = st.selectbox("Select Timeslot:", timeslot_names)
                selected_timeslot = timeslots[timeslot_names.index(selected_timeslot_display)].name
                
                # Show surgeries in this timeslot
                if selected_timeslot:
                    st.markdown("### 📋 Surgeries in This Timeslot")
                    surgeries_in_slot = [s for s in onto_mgr.get_all_surgeries() 
                                        if s.has_timeslot and s.has_timeslot[0].name == selected_timeslot]
                    
                    if surgeries_in_slot:
                        for surgery in surgeries_in_slot:
                            with st.container():
                                col1, col2, col3 = st.columns(3)
                                col1.write(f"**{surgery.name}**")
                                surgeon = surgery.performs_operation[0].name if surgery.performs_operation else 'N/A'
                                col2.write(f"👨‍⚕️ {surgeon}")
                                theatre = surgery.requires_theatre_type[0].name if surgery.requires_theatre_type else 'N/A'
                                col3.write(f"🏥 {theatre}")
                                st.markdown("---")
                        
                        st.warning(f"⚠️ This will delete **{len(surgeries_in_slot)} surgery(ies)** and associated patient data")
                        
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if st.button("🗑️ Delete All", type="primary", key="delete_timeslot"):
                                with st.spinner(f"Deleting schedules in timeslot..."):
                                    success = onto_mgr.delete_schedule_by_timeslot(selected_timeslot)
                                    if success:
                                        st.success(f"✅ Successfully deleted all schedules in timeslot")
                                        st.cache_resource.clear()
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to delete schedules")
                    else:
                        st.info(f"No surgeries scheduled in this timeslot")
            else:
                st.info("No timeslots found in the system")
        
        elif delete_option == "Delete All Schedules":
            st.subheader("⚠️ Delete ALL Schedules")
            
            st.error("🚨 **DANGER ZONE** 🚨")
            st.warning("This will permanently delete ALL surgeries and patients from the system!")
            
            # Show current statistics
            summary = onto_mgr.get_ontology_summary()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Surgeries", summary['surgeries'])
            with col2:
                st.metric("Total Patients", summary['patients'])
            
            st.markdown("---")
            
            # Confirmation checkbox
            confirm = st.checkbox("I understand this action cannot be undone")
            
            if confirm:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("🗑️ DELETE ALL", type="primary", key="delete_all"):
                        with st.spinner("Deleting all schedules..."):
                            success = onto_mgr.delete_all_schedules()
                            if success:
                                st.success("✅ Successfully deleted all schedules")
                                st.cache_resource.clear()
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete schedules")
            else:
                st.info("👆 Check the box above to enable deletion")

if __name__ == "__main__":
    main()