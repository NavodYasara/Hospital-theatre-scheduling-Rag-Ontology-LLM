
SYSTEM_PROMPT = """You are an intelligent hospital theatre scheduling assistant.

CRITICAL RULES:
1. ONLY use information from the Context section provided
2. If information is not in the context, say "I don't have that information in the knowledge base"
3. Always explain your reasoning step-by-step
4. Cite specific facts from the context
5. Be precise about conflicts and constraints
6. When detecting conflicts, clearly state the conflicting surgeries/resources/times

Your responses should be:
- Factual and grounded in the provided context
- Clear and concise
- Professional medical terminology
- Include reasoning for all recommendations"""

CHECK_AVAILABILITY_PROMPT = """Task: Check availability for scheduling

Query: {query}

Context from Hospital Knowledge Base:
{context}

Instructions:
1. Identify the surgeon, theatre, date, and time from the query
2. Check the context for existing schedules
3. Look for any conflicts (time overlaps, resource conflicts)
4. Provide a clear YES/NO answer with detailed reasoning

Format:
**Availability:** [Yes/No]
**Reasoning:** [Explain based on context]
**Conflicts Found:** [List any conflicts or "None"]
**Recommendation:** [Alternative suggestion if not available]"""

DETECT_CONFLICTS_PROMPT = """Task: Detect and explain scheduling conflicts

Current Schedule Information:
{context}

Instructions:
1. Analyze all surgeries, surgeons, theatres, and timeslots in the context
2. Identify any conflicts:
   - Surgeon double-bookings (same surgeon, overlapping times)
   - Theatre double-bookings (same theatre, overlapping times)
   - Specialization mismatches (surgeon in wrong theatre type)
3. For each conflict, explain why it's a problem
4. Suggest solutions

Format your response:
**Conflicts Detected:** [Number]

For each conflict:
**Conflict Type:** [Surgeon/Theatre/Specialization]
**Description:** [What's the conflict]
**Severity:** [High/Medium/Low]
**Solution:** [How to resolve]"""

SUGGEST_SCHEDULE_PROMPT = """Task: Suggest optimal scheduling

Requirements:
{requirements}

Available Resources:
{context}

Instructions:
1. Review available surgeons, theatres, and timeslots
2. Match surgeon specialization to surgery type
3. Ensure no time conflicts
4. Consider emergency priority if applicable
5. Provide top 2-3 scheduling options

Format:
**Option 1:**
- Surgeon: [Name]
- Theatre: [Name]
- Timeslot: [Start - End]
- Reasoning: [Why this is optimal]

**Option 2:**
[Same format]"""

EXPLAIN_CONFLICT_PROMPT = """Task: Explain conflict and suggest resolution

Conflict Details:
{conflict_info}

Context:
{context}

Instructions:
1. Explain why this conflict exists
2. Reference specific ontology rules or constraints violated
3. Assess the severity and impact
4. Suggest 2-3 concrete alternative solutions

Format:
**Conflict Explanation:**
[Detailed explanation]

**Rules Violated:**
[List ontology constraints]

**Impact:**
[Who/what is affected]

**Alternative Solutions:**
1. [First alternative]
2. [Second alternative]
3. [Third alternative]"""
