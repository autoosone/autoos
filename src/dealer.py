from crewai import Agent, Crew, Task
# from crewai_tools import SerperDevTool  # Temporarily disabled
from langchain_openai import ChatOpenAI


async def agent():
    # Dealer search and connection agent
    # search_tool = SerperDevTool()  # Temporarily disabled
    search_tool = []  # No tools for now
    
    dealer_finder = Agent(
        role="Dealer Relationship Manager",
        goal="Connect customers with the best local dealers",
        backstory="""You are a dealer relationship expert who helps customers find:
        - Reputable dealers in their area
        - Dealers with specific inventory
        - Best customer service ratings
        - Competitive pricing
        - Financing options
        - Test drive availability
        
        You maintain relationships with dealers across the country and know their
        strengths, specialties, and customer satisfaction records.""",
        tools=search_tool,  # Empty list for now
        llm=ChatOpenAI(model="gpt-4", temperature=0.7),
        verbose=True,
    )
    
    appointment_coordinator = Agent(
        role="Test Drive Coordinator",
        goal="Schedule test drives and dealer appointments",
        backstory="""You coordinate between customers and dealers to:
        - Schedule test drives
        - Arrange vehicle inspections
        - Set up financing meetings
        - Coordinate trade-in evaluations
        - Ensure smooth customer experience
        
        You understand dealer hours, availability, and can help customers
        prepare for their dealership visit.""",
        tools=search_tool,  # Empty list for now
        llm=ChatOpenAI(model="gpt-4", temperature=0.7),
        verbose=True,
    )
    
    # Define tasks
    dealer_search_task = Task(
        description="""Find dealers based on customer needs:
        {request}
        
        Search for:
        - Dealers within customer's location/radius
        - Dealers with specific vehicle inventory
        - Dealer ratings and reviews
        - Specialties (luxury, budget, specific brands)
        - Financing options available
        - Current promotions or incentives
        
        Provide top 3-5 dealers with:
        - Name and location
        - Distance from customer
        - Inventory highlights
        - Customer ratings
        - Contact information
        - Why recommended
        """,
        agent=dealer_finder,
        expected_output="List of recommended dealers with details and contact info",
    )
    
    appointment_task = Task(
        description="""Help schedule dealer appointments:
        
        Based on customer preferences:
        - Best times for test drives
        - Documents needed for visit
        - Questions to ask dealers
        - What to inspect in vehicles
        - Negotiation tips
        - Trade-in preparation (if applicable)
        
        Provide appointment scheduling guidance and dealer visit checklist.
        """,
        agent=appointment_coordinator,
        expected_output="Appointment scheduling advice and dealer visit preparation guide",
    )
    
    # Create and return crew
    crew = Crew(
        agents=[dealer_finder, appointment_coordinator],
        tasks=[dealer_search_task, appointment_task],
        verbose=True,
    )
    
    return crew
