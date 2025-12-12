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
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat Assistant", 
        "🔍 Conflict Detection", 
        "📊 Schedule View",
        "➕ Add Schedule"
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
            - What equipment is needed for cardiac bypass surgery?
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
        - ⚙️ **Equipment Conflicts**: Same equipment needed by multiple surgeries at the same time
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
                    if conflicts['surgeon_conflicts']:
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
                    
                    if conflicts['equipment_conflicts']:
                        st.subheader("⚙️ Equipment Conflicts")
                        for conflict in conflicts['equipment_conflicts']:
                            with st.expander(f"⚠️ {conflict['equipment']} - {conflict['severity']} SEVERITY"):
                                st.write(f"**Description:** {conflict['description']}")
                                st.write(f"**Conflicting Surgeries:**")
                                st.write(f"- {conflict['surgery1']}")
                                st.write(f"- {conflict['surgery2']}")
                                
                                st.markdown("**💡 Suggested Resolution:**")
                                st.info("Reschedule one surgery or arrange for backup equipment.")
                    
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
            
            surgery_name = st.text_input("Surgery Name", placeholder="e.g., Knee_Arthroscopy")
            
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
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Add Surgery", type="primary"):
                if not surgery_name:
                    st.error("Please enter a surgery name")
                elif not selected_surgeon:
                    st.error("Please select a surgeon")
                elif not selected_theatre:
                    st.error("Please select a theatre")
                elif not selected_timeslot:
                    st.error("Please select a timeslot")
                else:
                    # Check for conflicts before adding
                    with st.spinner("Checking for conflicts..."):
                        # This is a simplified check - you can enhance it
                        conflicts = conflict_detector.detect_all_conflicts()
                        
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
                            st.success(f"✅ Surgery '{surgery_name}' added successfully!")
                            st.info("💡 Tip: Go to 'Conflict Detection' tab to verify no conflicts exist")
                            
                            # Clear cache to reload data
                            st.cache_resource.clear()
                        else:
                            st.error("❌ Failed to add surgery. Check logs for details.")
        
        with col2:
            if st.button("🔍 Preview Conflicts"):
                if selected_surgeon and selected_timeslot:
                    st.info("This would check for potential conflicts with this scheduling")
                    # You can implement preview logic here
                else:
                    st.warning("Fill in surgeon and timeslot first")
        
        with col3:
            if st.button("🔄 Reset Form"):
                st.rerun()

if __name__ == "__main__":
    main()